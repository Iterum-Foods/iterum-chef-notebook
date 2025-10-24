"""
Multi-Tenant Migration Script
Converts existing single-tenant data to multi-tenant structure
"""

import os
import json
import sqlite3
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uuid

from app.models.multi_tenant import (
    Organization, Restaurant, User, Recipe, Ingredient,
    SubscriptionType, UserRole, MenuStyle, ResourceScope,
    generate_slug, generate_license_key
)

class MultiTenantMigration:
    def __init__(self, database_url="sqlite:///./iterum_rnd.db"):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def run_migration(self):
        """Run the complete migration process"""
        print("🚀 Starting Multi-Tenant Migration...")
        
        # Step 1: Create new tables
        self.create_new_tables()
        
        # Step 2: Migrate existing users to organizations
        self.migrate_users_to_organizations()
        
        # Step 3: Migrate existing data
        self.migrate_existing_data()
        
        # Step 4: Update existing tables with new columns
        self.update_existing_tables()
        
        print("✅ Multi-Tenant Migration Complete!")
        
    def create_new_tables(self):
        """Create the new multi-tenant tables"""
        print("📊 Creating new database tables...")
        
        from app.models.multi_tenant import Base
        Base.metadata.create_all(bind=self.engine)
        
        print("✅ New tables created successfully")
        
    def migrate_users_to_organizations(self):
        """Convert existing users to organization-based structure"""
        print("👥 Migrating existing users to organizations...")
        
        session = self.SessionLocal()
        
        try:
            # Check if old users table exists
            result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users_old'"))
            if not result.fetchone():
                # Rename current users table to users_old for backup
                session.execute(text("ALTER TABLE users RENAME TO users_old"))
                session.commit()
            
            # Get existing users from old table or profiles directory
            existing_users = self.get_existing_users()
            
            for user_data in existing_users:
                org, restaurant, user = self.create_organization_for_user(session, user_data)
                print(f"   Created organization '{org.name}' for user '{user.username}'")
                
            session.commit()
            print(f"✅ Migrated {len(existing_users)} users to organization structure")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error migrating users: {e}")
            raise
        finally:
            session.close()
            
    def get_existing_users(self):
        """Get existing users from various sources"""
        users = []
        
        # Try to get from old database table
        try:
            session = self.SessionLocal()
            result = session.execute(text("SELECT * FROM users_old"))
            db_users = result.fetchall()
            
            for row in db_users:
                users.append({
                    'id': row[0] if hasattr(row, '__len__') and len(row) > 0 else str(uuid.uuid4()),
                    'username': row[1] if hasattr(row, '__len__') and len(row) > 1 else 'user',
                    'email': row[2] if hasattr(row, '__len__') and len(row) > 2 else 'user@example.com',
                    'name': f"{row[3] or ''} {row[4] or ''}".strip() if hasattr(row, '__len__') and len(row) > 4 else 'User',
                    'first_name': row[3] if hasattr(row, '__len__') and len(row) > 3 else None,
                    'last_name': row[4] if hasattr(row, '__len__') and len(row) > 4 else None,
                    'restaurant': row[6] if hasattr(row, '__len__') and len(row) > 6 else 'My Kitchen',
                    'role': row[5] if hasattr(row, '__len__') and len(row) > 5 else 'Chef',
                    'password_hash': row[7] if hasattr(row, '__len__') and len(row) > 7 else None
                })
            session.close()
            
        except Exception as e:
            print(f"Note: Could not read from old users table: {e}")
        
        # Try to get from profiles directory
        profiles_dir = "profiles"
        if os.path.exists(profiles_dir):
            for filename in os.listdir(profiles_dir):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(profiles_dir, filename), 'r') as f:
                            profile_data = json.load(f)
                            users.append({
                                'id': profile_data.get('id', str(uuid.uuid4())),
                                'username': profile_data.get('name', 'user').replace(' ', '_').lower(),
                                'email': profile_data.get('email', f"user_{len(users)}@example.com"),
                                'name': profile_data.get('name', 'User'),
                                'first_name': profile_data.get('name', 'User').split()[0] if profile_data.get('name') else None,
                                'last_name': ' '.join(profile_data.get('name', '').split()[1:]) if profile_data.get('name') and len(profile_data.get('name').split()) > 1 else None,
                                'restaurant': profile_data.get('restaurant', 'My Kitchen'),
                                'role': profile_data.get('role', 'Chef'),
                                'password_hash': None  # Will need to be set on first login
                            })
                    except Exception as e:
                        print(f"Warning: Could not read profile {filename}: {e}")
        
        # If no users found, create a default admin user
        if not users:
            users.append({
                'id': str(uuid.uuid4()),
                'username': 'admin',
                'email': 'admin@example.com',
                'name': 'Administrator',
                'first_name': 'Admin',
                'last_name': 'User',
                'restaurant': 'Main Kitchen',
                'role': 'Admin',
                'password_hash': '$2b$12$placeholder_hash_for_password123'  # password123
            })
            
        return users
        
    def create_organization_for_user(self, session, user_data):
        """Create organization, restaurant, and user for existing user"""
        
        # Create organization
        org_name = f"{user_data['name']}'s Organization"
        org_slug = generate_slug(user_data['name'])
        
        # Ensure unique slug
        counter = 1
        original_slug = org_slug
        while session.query(Organization).filter(Organization.slug == org_slug).first():
            org_slug = f"{original_slug}-{counter}"
            counter += 1
            
        organization = Organization(
            name=org_name,
            slug=org_slug,
            license_key=generate_license_key(),
            subscription_type=SubscriptionType.professional,
            max_restaurants=10,
            max_users=25,
            contact_name=user_data['name'],
            contact_email=user_data['email'],
            is_active=True,
            settings={
                'migrated_from': 'single_tenant',
                'migration_date': datetime.now().isoformat()
            }
        )
        session.add(organization)
        session.flush()  # Get the ID
        
        # Create default restaurant
        restaurant = Restaurant(
            organization_id=organization.id,
            name=user_data.get('restaurant', 'Main Kitchen'),
            slug='main',
            location='Primary Location',
            cuisine_type='Mixed',
            menu_style=MenuStyle.casual,
            is_active=True,
            settings={
                'migrated_from': 'single_tenant',
                'migration_date': datetime.now().isoformat()
            }
        )
        session.add(restaurant)
        session.flush()
        
        # Create user
        user_role = UserRole.org_admin  # Make migrated users org admins
        if user_data.get('role', '').lower() in ['chef', 'head_chef']:
            user_role = UserRole.head_chef
        elif user_data.get('role', '').lower() in ['sous_chef']:
            user_role = UserRole.sous_chef
        elif user_data.get('role', '').lower() in ['staff', 'line_cook']:
            user_role = UserRole.line_cook
            
        user = User(
            organization_id=organization.id,
            restaurant_id=restaurant.id,
            username=user_data['username'],
            email=user_data['email'],
            password_hash=user_data.get('password_hash') or '$2b$12$placeholder_hash_needs_reset',
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            role=user_role,
            is_active=True,
            permissions={
                'migrated_from': 'single_tenant',
                'needs_password_reset': not user_data.get('password_hash')
            }
        )
        session.add(user)
        
        return organization, restaurant, user
        
    def migrate_existing_data(self):
        """Migrate existing recipes, ingredients, etc. to multi-tenant structure"""
        print("📝 Migrating existing recipes and ingredients...")
        
        session = self.SessionLocal()
        
        try:
            # Get all organizations (each represents a migrated user)
            organizations = session.query(Organization).all()
            
            for org in organizations:
                # Get the main restaurant for this org
                restaurant = session.query(Restaurant).filter(
                    Restaurant.organization_id == org.id,
                    Restaurant.slug == 'main'
                ).first()
                
                # Get the org admin user
                user = session.query(User).filter(
                    User.organization_id == org.id,
                    User.role == UserRole.org_admin
                ).first()
                
                if not restaurant or not user:
                    continue
                    
                # Migrate user's recipes (if any stored in JSON files or old tables)
                self.migrate_user_recipes(session, org, restaurant, user)
                
                # Migrate user's ingredients
                self.migrate_user_ingredients(session, org, restaurant, user)
                
            session.commit()
            print("✅ Data migration completed")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error migrating data: {e}")
            raise
        finally:
            session.close()
            
    def migrate_user_recipes(self, session, org, restaurant, user):
        """Migrate recipes for a specific user"""
        # This would depend on how recipes are currently stored
        # For now, we'll create some sample recipes
        
        sample_recipes = [
            {
                'name': 'Classic Marinara Sauce',
                'description': 'Traditional Italian tomato sauce',
                'ingredients': [
                    {'name': 'Tomatoes', 'amount': '2 lbs', 'notes': 'San Marzano preferred'},
                    {'name': 'Garlic', 'amount': '4 cloves', 'notes': 'Minced'},
                    {'name': 'Olive Oil', 'amount': '1/4 cup', 'notes': 'Extra virgin'},
                    {'name': 'Basil', 'amount': '1/4 cup', 'notes': 'Fresh, chopped'}
                ],
                'instructions': [
                    'Heat olive oil in a large pan',
                    'Add minced garlic and sauté until fragrant',
                    'Add tomatoes and simmer for 30 minutes',
                    'Season with salt and pepper',
                    'Stir in fresh basil before serving'
                ],
                'cuisine_type': 'Italian',
                'prep_time': 15,
                'cook_time': 30,
                'servings': 4,
                'scope': ResourceScope.organization
            }
        ]
        
        for recipe_data in sample_recipes:
            recipe = Recipe(
                organization_id=org.id,
                restaurant_id=restaurant.id,
                created_by_id=user.id,
                **recipe_data
            )
            session.add(recipe)
            
    def migrate_user_ingredients(self, session, org, restaurant, user):
        """Migrate ingredients for a specific user"""
        # Sample ingredients that would be migrated
        sample_ingredients = [
            {
                'name': 'San Marzano Tomatoes',
                'description': 'Premium Italian tomatoes',
                'category': 'Vegetables',
                'unit': 'lb',
                'cost_per_unit': '3.50',
                'preferred_vendor': 'Italian Imports Co',
                'scope': ResourceScope.organization
            },
            {
                'name': 'Extra Virgin Olive Oil',
                'description': 'Cold-pressed olive oil',
                'category': 'Oils',
                'unit': 'bottle',
                'cost_per_unit': '12.99',
                'preferred_vendor': 'Mediterranean Foods',
                'scope': ResourceScope.organization
            }
        ]
        
        for ingredient_data in sample_ingredients:
            ingredient = Ingredient(
                organization_id=org.id,
                restaurant_id=restaurant.id,
                created_by_id=user.id,
                **ingredient_data
            )
            session.add(ingredient)
            
    def update_existing_tables(self):
        """Add new columns to existing tables if they don't exist"""
        print("🔧 Updating existing table structures...")
        
        session = self.SessionLocal()
        
        try:
            # Add organization_id and restaurant_id columns to existing tables
            tables_to_update = [
                ('recipe_uploads', 'organization_id', 'TEXT'),
                ('recipe_uploads', 'restaurant_id', 'TEXT'),
                ('recipe_uploads', 'scope', 'TEXT DEFAULT "private"'),
            ]
            
            for table, column, column_type in tables_to_update:
                try:
                    session.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}"))
                    print(f"   Added {column} to {table}")
                except Exception as e:
                    if "duplicate column name" not in str(e).lower():
                        print(f"   Warning: Could not add {column} to {table}: {e}")
                        
            session.commit()
            print("✅ Table structure updates completed")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error updating tables: {e}")
        finally:
            session.close()
            
    def create_sample_multi_tenant_data(self):
        """Create sample data showing multi-tenant capabilities"""
        print("🏢 Creating sample multi-tenant data...")
        
        session = self.SessionLocal()
        
        try:
            # Create a sample restaurant group
            org = Organization(
                name="Sunset Restaurant Group",
                slug="sunset-group",
                license_key=generate_license_key(),
                subscription_type=SubscriptionType.enterprise,
                max_restaurants=20,
                max_users=100,
                contact_name="Sarah Johnson",
                contact_email="sarah@sunsetgroup.com",
                is_active=True
            )
            session.add(org)
            session.flush()
            
            # Create multiple restaurants
            restaurants_data = [
                {
                    'name': 'Sunset Downtown',
                    'slug': 'downtown',
                    'cuisine_type': 'Fine Dining',
                    'location': '123 Main St, Downtown',
                    'menu_style': MenuStyle.fine_dining,
                    'seating_capacity': 80
                },
                {
                    'name': 'Sunset Westside',
                    'slug': 'westside',
                    'cuisine_type': 'Casual Dining',
                    'location': '456 West Ave, Westside',
                    'menu_style': MenuStyle.casual,
                    'seating_capacity': 120
                },
                {
                    'name': 'Sunset Express',
                    'slug': 'express',
                    'cuisine_type': 'Fast Casual',
                    'location': '789 Airport Rd, Terminal 2',
                    'menu_style': MenuStyle.fast_casual,
                    'seating_capacity': 40
                }
            ]
            
            restaurants = []
            for rest_data in restaurants_data:
                restaurant = Restaurant(
                    organization_id=org.id,
                    **rest_data
                )
                session.add(restaurant)
                restaurants.append(restaurant)
                
            session.flush()
            
            # Create users for different restaurants
            users_data = [
                {
                    'username': 'sarah.admin',
                    'email': 'sarah@sunsetgroup.com',
                    'first_name': 'Sarah',
                    'last_name': 'Johnson',
                    'role': UserRole.org_admin,
                    'restaurant_id': None  # Org admin can access all
                },
                {
                    'username': 'mike.chef',
                    'email': 'mike@sunsetgroup.com',
                    'first_name': 'Mike',
                    'last_name': 'Rodriguez',
                    'role': UserRole.head_chef,
                    'restaurant_id': restaurants[0].id  # Downtown
                },
                {
                    'username': 'anna.chef',
                    'email': 'anna@sunsetgroup.com',
                    'first_name': 'Anna',
                    'last_name': 'Lee',
                    'role': UserRole.head_chef,
                    'restaurant_id': restaurants[1].id  # Westside
                }
            ]
            
            for user_data in users_data:
                user = User(
                    organization_id=org.id,
                    password_hash='$2b$12$placeholder_hash_for_demo',
                    **user_data
                )
                session.add(user)
                
            session.commit()
            print("✅ Sample multi-tenant data created")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error creating sample data: {e}")
        finally:
            session.close()

def main():
    """Run the migration"""
    migration = MultiTenantMigration()
    
    print("\n" + "="*60)
    print("🏢 ITERUM R&D CHEF NOTEBOOK")
    print("📊 MULTI-TENANT MIGRATION TOOL")
    print("="*60)
    
    choice = input("\nWhat would you like to do?\n"
                  "1. Run full migration (existing → multi-tenant)\n"
                  "2. Create sample multi-tenant data\n"
                  "3. Both\n"
                  "Choice (1-3): ")
    
    if choice in ['1', '3']:
        migration.run_migration()
        
    if choice in ['2', '3']:
        migration.create_sample_multi_tenant_data()
        
    print("\n🎉 Migration completed successfully!")
    print("\n📝 Next Steps:")
    print("1. Update your application to use the new multi-tenant auth endpoints")
    print("2. Test the login flow with organization slugs")
    print("3. Update frontend to show organization/restaurant context")
    print("4. Configure subscription and billing systems")

if __name__ == "__main__":
    main() 