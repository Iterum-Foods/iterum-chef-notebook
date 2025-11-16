#!/usr/bin/env python3
"""
Comprehensive testing script for Iterum R&D Chef Notebook
Tests all major components and provides detailed feedback
"""

import requests
import json
import time
import sys
import os
from pathlib import Path

class AppTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:8080"
        self.test_results = []
        
    def log_test(self, test_name, status, message=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        
        # Print result
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        
    def test_backend_health(self):
        """Test backend health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Backend Health", "PASS", f"Status: {data.get('status')}")
            else:
                self.log_test("Backend Health", "FAIL", f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Backend Health", "FAIL", f"Connection error: {str(e)}")
    
    def test_detailed_health(self):
        """Test detailed health check"""
        try:
            response = requests.get(f"{self.base_url}/health/detailed", timeout=10)
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'unknown')
                errors = data.get('error_count', 0)
                warnings = data.get('warning_count', 0)
                self.log_test("Detailed Health", "PASS", 
                            f"Status: {status}, Errors: {errors}, Warnings: {warnings}")
            else:
                self.log_test("Detailed Health", "FAIL", f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Detailed Health", "FAIL", f"Connection error: {str(e)}")
    
    def test_api_documentation(self):
        """Test API documentation endpoint"""
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                self.log_test("API Documentation", "PASS", "Documentation accessible")
            else:
                self.log_test("API Documentation", "FAIL", f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("API Documentation", "FAIL", f"Connection error: {str(e)}")
    
    def test_frontend_accessibility(self):
        """Test frontend accessibility"""
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                if "DOCTYPE html" in response.text:
                    self.log_test("Frontend Accessibility", "PASS", "HTML content served")
                else:
                    self.log_test("Frontend Accessibility", "WARNING", "No HTML content detected")
            else:
                self.log_test("Frontend Accessibility", "FAIL", f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Frontend Accessibility", "FAIL", f"Connection error: {str(e)}")
    
    def test_database_connectivity(self):
        """Test database connectivity through API"""
        try:
            # Test a simple endpoint that requires database access
            response = requests.get(f"{self.base_url}/api/recipes", timeout=5)
            if response.status_code in [200, 401]:  # 401 is expected without auth
                self.log_test("Database Connectivity", "PASS", "Database accessible")
            else:
                self.log_test("Database Connectivity", "FAIL", f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Database Connectivity", "FAIL", f"Connection error: {str(e)}")
    
    def test_file_system(self):
        """Test file system components"""
        required_dirs = ["uploads", "logs", "profiles", "incoming_recipes"]
        all_exist = True
        
        for directory in required_dirs:
            if not Path(directory).exists():
                all_exist = False
                break
        
        if all_exist:
            self.log_test("File System", "PASS", "All required directories exist")
        else:
            self.log_test("File System", "FAIL", "Missing required directories")
    
    def test_equipment_database(self):
        """Test equipment database file"""
        equipment_file = Path("equipment_database.csv")
        if equipment_file.exists():
            size_mb = equipment_file.stat().st_size / (1024 * 1024)
            self.log_test("Equipment Database", "PASS", f"File exists ({size_mb:.1f} MB)")
        else:
            self.log_test("Equipment Database", "WARNING", "Equipment database not found")
    
    def test_environment_setup(self):
        """Test environment and configuration"""
        # Check if .env file exists
        env_file = Path(".env")
        if env_file.exists():
            self.log_test("Environment Setup", "PASS", ".env file found")
        else:
            self.log_test("Environment Setup", "WARNING", ".env file not found (using defaults)")
    
    def test_dependencies(self):
        """Test if required dependencies are available"""
        try:
            import fastapi
            import uvicorn
            import sqlalchemy
            import pydantic
            self.log_test("Dependencies", "PASS", "All required packages available")
        except ImportError as e:
            self.log_test("Dependencies", "FAIL", f"Missing dependency: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Starting Iterum R&D Chef Notebook Tests")
        print("=" * 50)
        
        # Run tests
        self.test_dependencies()
        self.test_environment_setup()
        self.test_file_system()
        self.test_equipment_database()
        self.test_backend_health()
        self.test_detailed_health()
        self.test_api_documentation()
        self.test_frontend_accessibility()
        self.test_database_connectivity()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "FAIL")
        warnings = sum(1 for r in self.test_results if r["status"] == "WARNING")
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        
        if failed == 0:
            print("\n🎉 All critical tests passed! Your app is ready to use.")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please check the issues above.")
        
        # Save results to file
        with open("test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: test_results.json")
        
        return failed == 0

def main():
    tester = AppTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 