#!/usr/bin/env python3
"""
Check what data was imported into the database
"""

import sqlite3
import os

def check_import():
    """Check imported data"""
    print("=== Checking Imported Data ===")
    
    # Get app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    profile_dir = os.path.join(app_dir, 'profiles')
    db_path = os.path.join(profile_dir, "Default.db")
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check employees
        cursor.execute("SELECT COUNT(*) FROM employees")
        emp_count = cursor.fetchone()[0]
        print(f"Employees in database: {emp_count}")
        
        if emp_count > 0:
            cursor.execute("SELECT name, position, hourly_rate FROM employees LIMIT 10")
            employees = cursor.fetchall()
            print("\nSample employees:")
            for emp in employees:
                print(f"  - {emp[0]} ({emp[1] or 'No position'}) - ${emp[2]:.2f}/hr")
        
        # Check payroll records
        cursor.execute("SELECT COUNT(*) FROM payroll_runs")
        payroll_count = cursor.fetchone()[0]
        print(f"\nPayroll records in database: {payroll_count}")
        
        if payroll_count > 0:
            cursor.execute("SELECT employee_name, pay_date, gross_pay FROM payroll_runs LIMIT 10")
            payrolls = cursor.fetchall()
            print("\nSample payroll records:")
            for pay in payrolls:
                print(f"  - {pay[0]} ({pay[1]}) - ${pay[2]:.2f}")
        
        # Check table structure
        print("\n=== Table Structure ===")
        cursor.execute("PRAGMA table_info(employees)")
        emp_columns = cursor.fetchall()
        print("Employees table columns:")
        for col in emp_columns:
            print(f"  - {col[1]} ({col[2]})")
        
        cursor.execute("PRAGMA table_info(payroll_runs)")
        pay_columns = cursor.fetchall()
        print("\nPayroll_runs table columns:")
        for col in pay_columns:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking data: {e}")

if __name__ == "__main__":
    check_import()
