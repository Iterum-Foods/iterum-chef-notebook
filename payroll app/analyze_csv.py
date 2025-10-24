#!/usr/bin/env python3
"""
Analyze the Master Payroll CSV structure
"""

import csv
import os

def analyze_csv():
    """Analyze the CSV structure"""
    print("=== Analyzing Master Payroll CSV ===")
    
    csv_file = "Master Payroll.csv"
    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        return
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            # Read first few rows to understand structure
            rows = []
            for i, row in enumerate(reader):
                if i < 20:  # Read first 20 rows
                    rows.append(row)
                else:
                    break
            
            print(f"Total rows read: {len(rows)}")
            print("\n=== CSV Structure Analysis ===")
            
            for i, row in enumerate(rows):
                if len(row) > 0 and row[0].strip():
                    print(f"\nRow {i+1}:")
                    print(f"  Content: {row}")
                    print(f"  Length: {len(row)}")
                    
                    # Check if it's a date row
                    if len(row) > 0 and row[0].strip():
                        if row[0].strip().replace('/', '').isdigit() and len(row[0].strip()) <= 8:
                            print(f"  Type: Date row - {row[0]}")
                        elif row[0] == "Employee":
                            print(f"  Type: Header row")
                        elif row[0].startswith('"') and len(row) >= 5:
                            print(f"  Type: Employee data row")
                            print(f"  Employee: {row[0].strip('\"')}")
                            print(f"  Position: {row[1] if len(row) > 1 else 'N/A'}")
                            print(f"  Regular Hours: {row[2] if len(row) > 2 else 'N/A'}")
                            print(f"  Overtime Hours: {row[3] if len(row) > 3 else 'N/A'}")
                            print(f"  Hourly Rate: {row[4] if len(row) > 4 else 'N/A'}")
                            print(f"  Regular Pay: {row[5] if len(row) > 5 else 'N/A'}")
                            print(f"  Overtime Pay: {row[6] if len(row) > 6 else 'N/A'}")
                            print(f"  Total Pay: {row[7] if len(row) > 7 else 'N/A'}")
                            print(f"  Net Sales: {row[8] if len(row) > 8 else 'N/A'}")
                            print(f"  Gratuity: {row[9] if len(row) > 9 else 'N/A'}")
                            print(f"  Employee ID: {row[10] if len(row) > 10 else 'N/A'}")
                            print(f"  Job Code: {row[11] if len(row) > 11 else 'N/A'}")
                            print(f"  Location: {row[12] if len(row) > 12 else 'N/A'}")
                        else:
                            print(f"  Type: Other")
            
            # Count unique employees and pay periods
            print("\n=== Summary ===")
            employees = set()
            pay_periods = set()
            
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                current_date = None
                
                for row in reader:
                    if len(row) > 0 and row[0].strip():
                        # Check if this is a date row
                        if row[0].strip().replace('/', '').isdigit() and len(row[0].strip()) <= 8:
                            current_date = row[0].strip()
                            pay_periods.add(current_date)
                        # Check if this is employee data
                        elif row[0].startswith('"') and len(row) >= 5:
                            employee_name = row[0].strip('"')
                            employees.add(employee_name)
            
            print(f"Unique employees found: {len(employees)}")
            print(f"Pay periods found: {len(pay_periods)}")
            print(f"Pay periods: {sorted(pay_periods)}")
            
    except Exception as e:
        print(f"Error analyzing CSV: {e}")

if __name__ == "__main__":
    analyze_csv()
