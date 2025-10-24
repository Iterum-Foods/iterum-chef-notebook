#!/usr/bin/env python3
"""
Import Master Payroll CSV data directly into the database
"""

import sqlite3
import csv
import os
import re
from datetime import datetime

def import_master_payroll():
    """Import Master Payroll CSV file"""
    print("=== Importing Master Payroll CSV ===")
    
    # Get app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    profile_dir = os.path.join(app_dir, 'profiles')
    db_path = os.path.join(profile_dir, "Default.db")
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("Database not found. Please run the app first to create the database.")
        return
    
    # Check if CSV file exists
    csv_file = "Master Payroll.csv"
    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Reading CSV file...")
        
        # Read and parse the CSV
        employees_data = {}
        payroll_data = []
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            current_date = None
            
            for row in reader:
                if len(row) > 0 and row[0].strip():
                    # Check if this is a date row (e.g., "01/12/25")
                    if re.match(r'\d{2}/\d{2}/\d{2}', row[0]):
                        current_date = row[0]
                        print(f"Processing pay period: {current_date}")
                    # Check if this is a header row
                    elif row[0] == "Employee":
                        continue
                    # Check if this is employee data
                    elif row[0].startswith('"') and len(row) >= 5:
                        # Extract employee name (remove quotes)
                        name = row[0].strip('"')
                        job_title = row[1] if len(row) > 1 else ""
                        regular_hours = float(row[2] or 0) if len(row) > 2 else 0
                        overtime_hours = float(row[3] or 0) if len(row) > 3 else 0
                        hourly_rate = float(row[4] or 0) if len(row) > 4 else 0
                        regular_pay = float(row[5] or 0) if len(row) > 5 else 0
                        overtime_pay = float(row[6] or 0) if len(row) > 6 else 0
                        total_pay = float(row[7] or 0) if len(row) > 7 else 0
                        net_sales = float(row[8] or 0) if len(row) > 8 else 0
                        total_gratuity = float(row[9] or 0) if len(row) > 9 else 0
                        employee_id = row[10] if len(row) > 10 else ""
                        job_code = row[11] if len(row) > 11 else ""
                        location = row[12] if len(row) > 12 else ""
                        
                        # Store employee data
                        if name not in employees_data:
                            employees_data[name] = {
                                'name': name,
                                'position': job_title,
                                'hourly_rate': hourly_rate,
                                'employee_id': employee_id,
                                'job_code': job_code,
                                'location': location
                            }
                        
                        # Store payroll data
                        if current_date and total_pay > 0:
                            payroll_data.append({
                                'employee_name': name,
                                'pay_date': current_date,
                                'regular_hours': regular_hours,
                                'overtime_hours': overtime_hours,
                                'hourly_rate': hourly_rate,
                                'regular_pay': regular_pay,
                                'overtime_pay': overtime_pay,
                                'total_pay': total_pay,
                                'net_sales': net_sales,
                                'total_gratuity': total_gratuity
                            })
        
        print(f"Found {len(employees_data)} employees and {len(payroll_data)} payroll records")
        
        # Import employees
        print("Importing employees...")
        imported_employees = 0
        for employee in employees_data.values():
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO employees (name, position, hourly_rate, employee_id, job_code, location)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (employee['name'], employee['position'], employee['hourly_rate'], 
                      employee['employee_id'], employee['job_code'], employee['location']))
                imported_employees += 1
            except Exception as e:
                print(f"Error importing employee {employee['name']}: {e}")
        
        # Import payroll data
        print("Importing payroll records...")
        imported_payroll = 0
        for payroll in payroll_data:
            try:
                # Get employee ID
                cursor.execute("SELECT id FROM employees WHERE name = ?", (payroll['employee_name'],))
                emp_result = cursor.fetchone()
                if emp_result:
                    emp_id = emp_result[0]
                    
                    # Create payroll run
                    cursor.execute("""
                        INSERT INTO payroll_runs 
                        (employee_id, employee_name, pay_date, regular_hours, overtime_hours, 
                         hourly_rate, regular_pay, overtime_pay, gross_pay, net_pay, 
                         net_sales, total_gratuity)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (emp_id, payroll['employee_name'], payroll['pay_date'], 
                          payroll['regular_hours'], payroll['overtime_hours'],
                          payroll['hourly_rate'], payroll['regular_pay'], payroll['overtime_pay'],
                          payroll['total_pay'], payroll['total_pay'],  # net_pay = gross_pay for now
                          payroll['net_sales'], payroll['total_gratuity']))
                    imported_payroll += 1
                else:
                    print(f"Employee not found: {payroll['employee_name']}")
            except Exception as e:
                print(f"Error importing payroll for {payroll['employee_name']}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"\n=== Import Complete ===")
        print(f"✓ Imported {imported_employees} employees")
        print(f"✓ Imported {imported_payroll} payroll records")
        print(f"✓ Database updated successfully")
        
        # Show sample of imported data
        print(f"\nSample employees imported:")
        for i, (name, data) in enumerate(list(employees_data.items())[:5]):
            print(f"  {i+1}. {name} - {data['position']} - ${data['hourly_rate']:.2f}/hr")
        
        if len(employees_data) > 5:
            print(f"  ... and {len(employees_data) - 5} more employees")
        
    except Exception as e:
        print(f"Import failed: {e}")

if __name__ == "__main__":
    import_master_payroll()
