#!/usr/bin/env python3
"""
Comprehensive test runner for the Iterum R&D Chef Notebook application.
This script provides various testing options and detailed reporting.
"""

import os
import sys
import argparse
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Optional
import psutil


class TestRunner:
    """Main test runner class"""
    
    def __init__(self):
        self.start_time = time.time()
        self.test_results = {}
        self.project_root = Path(__file__).parent
        
    def setup_test_environment(self):
        """Setup the testing environment"""
        print("🔧 Setting up test environment...")
        
        # Create test directories
        test_dirs = ["test_uploads", "test_logs", "test_coverage"]
        for dir_name in test_dirs:
            test_dir = self.project_root / dir_name
            test_dir.mkdir(exist_ok=True)
        
        # Set environment variables
        os.environ["TESTING"] = "1"
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        
        print("✅ Test environment setup complete")
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        print("🧹 Cleaning up test environment...")
        
        # Clean up test directories
        test_dirs = ["test_uploads", "test_logs"]
        for dir_name in test_dirs:
            test_dir = self.project_root / dir_name
            if test_dir.exists():
                import shutil
                shutil.rmtree(test_dir)
        
        # Remove environment variables
        test_env_vars = ["TESTING", "DATABASE_URL"]
        for var in test_env_vars:
            if var in os.environ:
                del os.environ[var]
        
        print("✅ Test environment cleanup complete")
    
    def run_python_tests(self, test_type: str = "all", verbose: bool = False) -> bool:
        """Run Python/pytest tests"""
        print(f"🐍 Running Python tests ({test_type})...")
        
        cmd = ["python", "-m", "pytest"]
        
        if verbose:
            cmd.append("-v")
        
        if test_type == "unit":
            cmd.extend(["-m", "unit"])
        elif test_type == "integration":
            cmd.extend(["-m", "integration"])
        elif test_type == "auth":
            cmd.extend(["-m", "auth"])
        elif test_type == "recipes":
            cmd.extend(["-m", "recipes"])
        elif test_type == "api":
            cmd.extend(["-m", "api"])
        elif test_type == "fast":
            cmd.extend(["-m", "not slow"])
        
        # Add coverage reporting
        cmd.extend([
            "--cov=app",
            "--cov-report=html:test_coverage/python",
            "--cov-report=term-missing",
            "--cov-fail-under=60"
        ])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.test_results["python"] = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "command": " ".join(cmd)
            }
            
            if result.returncode == 0:
                print("✅ Python tests passed")
                return True
            else:
                print("❌ Python tests failed")
                print(result.stdout)
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error running Python tests: {e}")
            return False
    
    def run_javascript_tests(self, verbose: bool = False) -> bool:
        """Run JavaScript/Jest tests"""
        print("📜 Running JavaScript tests...")
        
        # Check if npm is available
        try:
            subprocess.run(["npm", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ npm not found, skipping JavaScript tests")
            return True
        
        # Install dependencies if needed
        if not (self.project_root / "node_modules").exists():
            print("📦 Installing npm dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        cmd = ["npm", "run", "test:frontend"]
        if verbose:
            cmd.append("--", "--verbose")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.test_results["javascript"] = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "command": " ".join(cmd)
            }
            
            if result.returncode == 0:
                print("✅ JavaScript tests passed")
                return True
            else:
                print("❌ JavaScript tests failed")
                print(result.stdout)
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error running JavaScript tests: {e}")
            return False
    
    def run_linting(self) -> bool:
        """Run code linting"""
        print("🔍 Running code linting...")
        
        results = []
        
        # Python linting with flake8
        try:
            result = subprocess.run(
                ["python", "-m", "flake8", "app/", "--max-line-length=88"],
                capture_output=True,
                text=True
            )
            results.append(("flake8", result.returncode == 0, result.stdout))
        except Exception as e:
            results.append(("flake8", False, str(e)))
        
        # Python type checking with mypy
        try:
            result = subprocess.run(
                ["python", "-m", "mypy", "app/", "--ignore-missing-imports"],
                capture_output=True,
                text=True
            )
            results.append(("mypy", result.returncode == 0, result.stdout))
        except Exception as e:
            results.append(("mypy", False, str(e)))
        
        # Security check with bandit
        try:
            result = subprocess.run(
                ["python", "-m", "bandit", "-r", "app/", "-f", "json"],
                capture_output=True,
                text=True
            )
            # Bandit returns 0 for no issues, 1 for issues found
            results.append(("bandit", result.returncode == 0, result.stdout))
        except Exception as e:
            results.append(("bandit", False, str(e)))
        
        # JavaScript linting (if available)
        if (self.project_root / "node_modules").exists():
            try:
                result = subprocess.run(
                    ["npm", "run", "lint"],
                    capture_output=True,
                    text=True
                )
                results.append(("eslint", result.returncode == 0, result.stdout))
            except Exception as e:
                results.append(("eslint", False, str(e)))
        
        self.test_results["linting"] = results
        
        all_passed = all(result[1] for result in results)
        if all_passed:
            print("✅ All linting checks passed")
        else:
            print("❌ Some linting checks failed:")
            for name, passed, output in results:
                if not passed:
                    print(f"  - {name}: FAILED")
                    if output:
                        print(f"    {output}")
        
        return all_passed
    
    def run_performance_tests(self) -> bool:
        """Run basic performance tests"""
        print("⚡ Running performance tests...")
        
        try:
            from fastapi.testclient import TestClient
            from app.main import app
            
            client = TestClient(app)
            
            # Test response times for key endpoints
            endpoints = [
                "/",
                "/health",
                "/api/auth/login",
                "/api/recipes/",
                "/api/vendors/"
            ]
            
            performance_results = []
            
            for endpoint in endpoints:
                start_time = time.time()
                
                if endpoint == "/api/auth/login":
                    # POST request for login
                    response = client.post(endpoint, data={"username": "test", "password": "test"})
                else:
                    # GET request for others
                    response = client.get(endpoint)
                
                end_time = time.time()
                response_time = end_time - start_time
                
                performance_results.append({
                    "endpoint": endpoint,
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "passed": response_time < 1.0  # Less than 1 second
                })
            
            self.test_results["performance"] = performance_results
            
            all_passed = all(result["passed"] for result in performance_results)
            
            if all_passed:
                print("✅ All performance tests passed")
            else:
                print("❌ Some performance tests failed:")
                for result in performance_results:
                    if not result["passed"]:
                        print(f"  - {result['endpoint']}: {result['response_time']:.2f}s (too slow)")
            
            return all_passed
            
        except Exception as e:
            print(f"❌ Error running performance tests: {e}")
            return False
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        end_time = time.time()
        total_time = end_time - self.start_time
        
        print("\n" + "="*60)
        print("📊 TEST REPORT")
        print("="*60)
        
        print(f"⏱️  Total test time: {total_time:.2f} seconds")
        print(f"🖥️  System: {psutil.cpu_count()} CPUs, {psutil.virtual_memory().total // (1024**3)}GB RAM")
        print(f"🐍 Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        
        # Overall results
        all_results = []
        for test_type, result in self.test_results.items():
            if isinstance(result, dict) and "success" in result:
                all_results.append(result["success"])
            elif isinstance(result, list):
                all_results.extend([r[1] for r in result])
            elif isinstance(result, bool):
                all_results.append(result)
        
        if all_results:
            success_rate = (sum(all_results) / len(all_results)) * 100
            print(f"✅ Overall success rate: {success_rate:.1f}%")
        
        # Detailed results
        for test_type, result in self.test_results.items():
            print(f"\n📋 {test_type.upper()} RESULTS:")
            if isinstance(result, dict) and "success" in result:
                status = "✅ PASSED" if result["success"] else "❌ FAILED"
                print(f"   {status}")
            elif isinstance(result, list):
                for name, passed, output in result:
                    status = "✅ PASSED" if passed else "❌ FAILED"
                    print(f"   {name}: {status}")
        
        # Save report to file
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_time": total_time,
            "results": self.test_results,
            "system_info": {
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "cpu_count": psutil.cpu_count(),
                "memory_gb": psutil.virtual_memory().total // (1024**3)
            }
        }
        
        report_file = self.project_root / "test_coverage" / "test_report.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        print("="*60)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Iterum R&D Chef Notebook Test Runner")
    parser.add_argument("--type", choices=["all", "unit", "integration", "auth", "recipes", "api", "fast"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--skip-js", action="store_true", help="Skip JavaScript tests")
    parser.add_argument("--skip-lint", action="store_true", help="Skip linting")
    parser.add_argument("--skip-perf", action="store_true", help="Skip performance tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--no-cleanup", action="store_true", help="Skip cleanup after tests")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    try:
        # Setup
        runner.setup_test_environment()
        
        print("🚀 Starting Iterum R&D Chef Notebook Test Suite")
        print("="*60)
        
        success = True
        
        # Run Python tests
        if not runner.run_python_tests(args.type, args.verbose):
            success = False
        
        # Run JavaScript tests
        if not args.skip_js:
            if not runner.run_javascript_tests(args.verbose):
                success = False
        
        # Run linting
        if not args.skip_lint:
            if not runner.run_linting():
                success = False
        
        # Run performance tests
        if not args.skip_perf:
            if not runner.run_performance_tests():
                success = False
        
        # Generate report
        runner.generate_report()
        
        if success:
            print("\n🎉 All tests completed successfully!")
            return 0
        else:
            print("\n❌ Some tests failed. Please check the report above.")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        return 130
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1
    finally:
        if not args.no_cleanup:
            runner.cleanup_test_environment()


if __name__ == "__main__":
    sys.exit(main()) 