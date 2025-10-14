#!/usr/bin/env python3
"""
Check Waitlist Database Contents
Quick script to see what's in waitlist.db
"""

import sqlite3
import json
from datetime import datetime

def check_waitlist():
    try:
        # Connect to database
        conn = sqlite3.connect('waitlist.db')
        cursor = conn.cursor()
        
        print("=" * 60)
        print("📋 WAITLIST DATABASE CHECK")
        print("=" * 60)
        print()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM waitlist")
        total = cursor.fetchone()[0]
        print(f"✅ Total Entries: {total}")
        print()
        
        if total == 0:
            print("⚠️  Database is EMPTY - No waitlist signups yet")
            print()
            print("💡 This means:")
            print("   - No one has signed up yet")
            print("   - OR the backend hasn't been running")
            print("   - OR landing page hasn't been accessible")
            conn.close()
            return
        
        # Get status breakdown
        cursor.execute("SELECT status, COUNT(*) FROM waitlist GROUP BY status")
        status_counts = cursor.fetchall()
        print("📊 Status Breakdown:")
        for status, count in status_counts:
            print(f"   {status}: {count}")
        print()
        
        # Get source breakdown
        cursor.execute("SELECT source, COUNT(*) FROM waitlist GROUP BY source")
        source_counts = cursor.fetchall()
        print("📍 Source Breakdown:")
        for source, count in source_counts:
            print(f"   {source}: {count}")
        print()
        
        # Get recent entries
        cursor.execute("""
            SELECT email, name, company, role, source, created_at, status 
            FROM waitlist 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        recent = cursor.fetchall()
        
        print("🔥 Recent Entries (last 10):")
        print("-" * 60)
        for entry in recent:
            email, name, company, role, source, created_at, status = entry
            print(f"Email: {email}")
            if name:
                print(f"  Name: {name}")
            if company:
                print(f"  Company: {company}")
            if role:
                print(f"  Role: {role}")
            print(f"  Source: {source}")
            print(f"  Created: {created_at}")
            print(f"  Status: {status}")
            print()
        
        # Get oldest entry
        cursor.execute("SELECT created_at FROM waitlist ORDER BY created_at ASC LIMIT 1")
        oldest = cursor.fetchone()
        if oldest:
            print(f"📅 Oldest Entry: {oldest[0]}")
        
        # Get newest entry
        cursor.execute("SELECT created_at FROM waitlist ORDER BY created_at DESC LIMIT 1")
        newest = cursor.fetchone()
        if newest:
            print(f"📅 Newest Entry: {newest[0]}")
        
        print()
        print("=" * 60)
        print("✅ Database check complete!")
        print()
        print("💡 Next Steps:")
        print("   1. Export this data: python export_waitlist.py")
        print("   2. Migrate to Firestore for cloud storage")
        print("   3. Integrate with your CRM")
        print("=" * 60)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_waitlist()

