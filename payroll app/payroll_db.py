import sqlite3
from datetime import datetime
import os

default_db_name = 'payroll_app.db'
DB_NAME = default_db_name # Global variable to hold the current DB name

def set_db_name(new_db_name):
    """Set the global database name."""
    global DB_NAME
    DB_NAME = new_db_name
    print(f"Database name set to: {DB_NAME}") # Debugging

def get_connection(db_name=None):
    """Get a database connection with proper error handling."""
    current_db = db_name or DB_NAME
    try:
        conn = sqlite3.connect(current_db)
        conn.execute("PRAGMA foreign_keys = ON") # Enforce foreign key constraints
        conn.execute("PRAGMA journal_mode = WAL") # Enable WAL mode for better performance
        conn.execute("PRAGMA synchronous = NORMAL") # Slightly faster than FULL
        conn.execute("PRAGMA cache_size = 10000") # Increase cache size
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error for {current_db}: {e}")
        return None

def save_all_data(db_name=None):
    """
    Ensures all pending database operations are committed.
    This function is called when the application is closing or during auto-save.
    """
    current_db = db_name or DB_NAME
    conn = None # Initialize conn to None
    try:
        conn = get_connection(current_db)
        if conn:
            conn.commit()
            print(f"All data committed successfully to {current_db}")
            return True
        else:
            print(f"No active connection to commit for {current_db}")
            return False
    except Exception as e:
        print(f"Error saving data to {current_db}: {e}")
        return False
    finally:
        if conn:
            conn.close() # Ensure connection is closed

def create_tables(db_name=None):
    """Create necessary tables if they don't exist."""
    conn = get_connection(db_name)
    if not conn:
        print("Failed to connect to database to create tables.")
        return False
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT,
                hourly_rate REAL NOT NULL,
                hire_date TEXT,
                dob TEXT,
                address TEXT,
                phone TEXT,
                email TEXT,
                emergency_contact TEXT,
                tax_id TEXT,
                bank_name TEXT,
                account_number TEXT,
                routing_number TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS payroll_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                run_date TEXT NOT NULL,
                frequency TEXT NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS payroll_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payroll_run_id INTEGER NOT NULL,
                employee_id INTEGER NOT NULL,
                hours_worked REAL NOT NULL,
                gross_pay REAL NOT NULL,
                federal_tax REAL DEFAULT 0.0,
                ss_tax REAL DEFAULT 0.0,
                medicare_tax REAL DEFAULT 0.0,
                ma_state_tax REAL DEFAULT 0.0,
                pfml_tax REAL DEFAULT 0.0,
                total_taxes REAL NOT NULL,
                net_pay REAL NOT NULL,
                bonus REAL DEFAULT 0.0,
                FOREIGN KEY (payroll_run_id) REFERENCES payroll_runs(id) ON DELETE CASCADE,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        print(f"Tables ensured in {db_name or DB_NAME}")
        return True
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        return False
    finally:
        if conn:
            conn.close()

# --- Employee Management Functions ---

def add_employee(name, position, hourly_rate, hire_date=None, dob=None, address=None, phone=None, email=None,
                 emergency_contact=None, tax_id=None, bank_name=None, account_number=None, routing_number=None, db_name=None):
    """Add a new employee to the database."""
    conn = get_connection(db_name)
    if not conn: return None
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO employees (name, position, hourly_rate, hire_date, dob, address, phone, email,
                                   emergency_contact, tax_id, bank_name, account_number, routing_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, position, hourly_rate, hire_date, dob, address, phone, email,
              emergency_contact, tax_id, bank_name, account_number, routing_number))
        conn.commit()
        return c.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding employee: {e}")
        return None
    finally:
        if conn: conn.close()

def get_all_employees(db_name=None):
    """Retrieve all employees."""
    conn = get_connection(db_name)
    if not conn: return []
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM employees ORDER BY name ASC')
        return c.fetchall()
    except sqlite3.Error as e:
        print(f"Error getting all employees: {e}")
        return []
    finally:
        if conn: conn.close()

def get_employee_by_id(employee_id, db_name=None):
    """Retrieve an employee by their ID."""
    conn = get_connection(db_name)
    if not conn: return None
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM employees WHERE id=?', (employee_id,))
        return c.fetchone()
    except sqlite3.Error as e:
        print(f"Error getting employee by ID: {e}")
        return None
    finally:
        if conn: conn.close()

def update_employee(employee_id, name, position, hourly_rate, hire_date=None, dob=None, address=None, phone=None, email=None,
                    emergency_contact=None, tax_id=None, bank_name=None, account_number=None, routing_number=None, db_name=None):
    """Update an existing employee's details."""
    conn = get_connection(db_name)
    if not conn: return False
    try:
        c = conn.cursor()
        c.execute('''
            UPDATE employees
            SET name=?, position=?, hourly_rate=?, hire_date=?, dob=?, address=?, phone=?, email=?,
                emergency_contact=?, tax_id=?, bank_name=?, account_number=?, routing_number=?
            WHERE id=?
        ''', (name, position, hourly_rate, hire_date, dob, address, phone, email,
              emergency_contact, tax_id, bank_name, account_number, routing_number, employee_id))
        conn.commit()
        return c.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error updating employee: {e}")
        return False
    finally:
        if conn: conn.close()

def delete_employee(employee_id, db_name=None):
    """Delete an employee and all associated payroll runs and details."""
    conn = get_connection(db_name)
    if not conn: return False
    try:
        c = conn.cursor()
        # Due to ON DELETE CASCADE, deleting from employees will automatically delete
        # associated payroll_runs and payroll_details.
        c.execute('DELETE FROM employees WHERE id=?', (employee_id,))
        conn.commit()
        return c.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting employee: {e}")
        return False
    finally:
        if conn: conn.close()

# --- Payroll Management Functions ---

def add_payroll_run(employee_id, run_date, frequency, hours_worked, gross_pay,
                    federal_tax, ss_tax, medicare_tax, ma_state_tax, pfml_tax,
                    total_taxes, net_pay, bonus, db_name=None):
    """Add a new payroll run and its details."""
    conn = get_connection(db_name)
    if not conn: return None
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO payroll_runs (employee_id, run_date, frequency)
            VALUES (?, ?, ?)
        ''', (employee_id, run_date, frequency))
        payroll_run_id = c.lastrowid

        c.execute('''
            INSERT INTO payroll_details (payroll_run_id, employee_id, hours_worked, gross_pay,
                                         federal_tax, ss_tax, medicare_tax, ma_state_tax, pfml_tax,
                                         total_taxes, net_pay, bonus)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (payroll_run_id, employee_id, hours_worked, gross_pay,
              federal_tax, ss_tax, medicare_tax, ma_state_tax, pfml_tax,
              total_taxes, net_pay, bonus))
        conn.commit()
        return payroll_run_id
    except sqlite3.Error as e:
        print(f"Error adding payroll run: {e}")
        return None
    finally:
        if conn: conn.close()

def get_all_payroll_runs_with_employee_names(db_name=None):
    """Retrieve all payroll runs with associated employee names."""
    conn = get_connection(db_name)
    if not conn: return []
    try:
        c = conn.cursor()
        c.execute('''
            SELECT
                pr.id, pr.employee_id, pr.run_date, pr.frequency,
                pd.hours_worked, pd.gross_pay, pd.federal_tax, pd.ss_tax,
                pd.medicare_tax, pd.ma_state_tax, pd.pfml_tax, pd.total_taxes,
                pd.net_pay, pd.bonus, e.name AS employee_name
            FROM payroll_runs pr
            JOIN payroll_details pd ON pr.id = pd.payroll_run_id
            JOIN employees e ON pr.employee_id = e.id
            ORDER BY pr.run_date DESC, e.name ASC
        ''')
        return c.fetchall()
    except sqlite3.Error as e:
        print(f"Error getting all payroll runs with employee names: {e}")
        return []
    finally:
        if conn: conn.close()


def get_payroll_run_details(run_id, db_name=None):
    """Retrieve full details for a specific payroll run."""
    conn = get_connection(db_name)
    if not conn: return None
    try:
        c = conn.cursor()
        c.execute('''
            SELECT
                pr.id, pr.employee_id, pr.run_date, pr.frequency,
                pd.hours_worked, pd.gross_pay, pd.federal_tax, pd.ss_tax,
                pd.medicare_tax, pd.ma_state_tax, pd.pfml_tax, pd.total_taxes,
                pd.net_pay, pd.bonus
            FROM payroll_runs pr
            JOIN payroll_details pd ON pr.id = pd.payroll_run_id
            WHERE pr.id = ?
        ''', (run_id,))
        return c.fetchone()
    except sqlite3.Error as e:
        print(f"Error getting payroll run details: {e}")
        return None
    finally:
        if conn: conn.close()

def get_employee_pay_history(employee_id, db_name=None):
    """Get the pay history for a specific employee."""
    conn = get_connection(db_name)
    if not conn: return []
    try:
        c = conn.cursor()
        c.execute('''
            SELECT pr.run_date, pr.frequency, pd.gross_pay, pd.federal_tax, pd.ss_tax, pd.medicare_tax, pd.ma_state_tax, pd.pfml_tax, pd.total_taxes, pd.net_pay, pd.bonus
            FROM payroll_details pd
            JOIN payroll_runs pr ON pd.payroll_run_id = pr.id
            WHERE pd.employee_id = ?
            ORDER BY pr.run_date DESC
        ''', (employee_id,))
        history = c.fetchall()
        return history
    except sqlite3.Error as e:
        print(f"Error getting employee pay history: {e}")
        return []
    finally:
        if conn: conn.close()


def delete_payroll_run(run_id, db_name=None):
    """Delete a payroll run and its details with proper error handling."""
    conn = get_connection(db_name)
    if not conn: return False
    try:
        c = conn.cursor()
        # Due to ON DELETE CASCADE, deleting from payroll_runs will automatically delete
        # associated payroll_details.
        c.execute('DELETE FROM payroll_runs WHERE id=?', (run_id,))
        conn.commit()
        return c.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting payroll run: {e}")
        return False
    finally:
        if conn: conn.close()

# Initial table creation when the module is imported, but only for the default DB.
# For user-selected profiles, create_tables is called explicitly in MainApp.
if __name__ == '__main__':
    # This block runs only when payroll_db.py is executed directly
    # It's good for initial setup or testing the DB functions independently.
    print(f"Initializing default database: {DB_NAME}")
    create_tables(DB_NAME)
    # Example usage (for testing)
    # add_employee("John Doe", "Software Engineer", 50.0)
    # emp = get_all_employees()
    # print(emp)
    # add_payroll_run(1, '2023-01-01', 'Bi-Weekly', 80, 4000, 600, 248, 58, 200, 27.2, 1133.2, 2866.8, 0)
    # print(get_all_payroll_runs_with_employee_names())
    print("Database initialization complete.")
