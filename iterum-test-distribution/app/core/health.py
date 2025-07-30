"""
Health check and monitoring system for Iterum R&D Chef Notebook
"""

import os
import psutil
import sqlite3
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from .settings import get_settings

class HealthChecker:
    """System health checker for the application"""
    
    def __init__(self):
        self.settings = get_settings()
    
    def check_system_health(self) -> Dict[str, Any]:
        """Comprehensive system health check"""
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "checks": {
                "database": self._check_database(),
                "file_system": self._check_file_system(),
                "system_resources": self._check_system_resources(),
                "services": self._check_services(),
                "configuration": self._check_configuration()
            }
        }
    
    def _check_database(self) -> Dict[str, Any]:
        """Check database connectivity and integrity"""
        try:
            db_path = self.settings.database_url.replace("sqlite:///", "")
            if not Path(db_path).exists():
                return {"status": "error", "message": "Database file not found"}
            
            # Test connection
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            
            return {
                "status": "healthy",
                "message": "Database connection successful",
                "tables": tables,
                "size_mb": round(Path(db_path).stat().st_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Database error: {str(e)}"}
    
    def _check_file_system(self) -> Dict[str, Any]:
        """Check file system and required directories"""
        checks = {}
        
        # Check required directories
        required_dirs = [
            self.settings.upload_dir,
            self.settings.incoming_recipes_dir,
            "logs",
            "profiles"
        ]
        
        for directory in required_dirs:
            path = Path(directory)
            if path.exists():
                checks[directory] = {
                    "status": "healthy",
                    "exists": True,
                    "writable": os.access(path, os.W_OK)
                }
            else:
                checks[directory] = {
                    "status": "error",
                    "exists": False,
                    "writable": False
                }
        
        # Check equipment database
        equipment_path = Path(self.settings.equipment_database_path)
        if equipment_path.exists():
            checks["equipment_database"] = {
                "status": "healthy",
                "exists": True,
                "size_mb": round(equipment_path.stat().st_size / (1024 * 1024), 2)
            }
        else:
            checks["equipment_database"] = {
                "status": "warning",
                "exists": False,
                "message": "Equipment database not found"
            }
        
        return checks
    
    def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('.')
            
            return {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "percent_used": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "percent_used": round((disk.used / disk.total) * 100, 2)
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": f"System resource check failed: {str(e)}"}
    
    def _check_services(self) -> Dict[str, Any]:
        """Check if required services are running"""
        services = {}
        
        # Check if ports are in use
        import socket
        
        # Backend port
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', self.settings.port))
            services[f"backend_port_{self.settings.port}"] = {
                "status": "healthy" if result == 0 else "error",
                "message": "Port in use" if result == 0 else "Port not in use"
            }
            sock.close()
        except Exception as e:
            services[f"backend_port_{self.settings.port}"] = {
                "status": "error",
                "message": f"Port check failed: {str(e)}"
            }
        
        # Frontend port
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', self.settings.frontend_port))
            services[f"frontend_port_{self.settings.frontend_port}"] = {
                "status": "healthy" if result == 0 else "error",
                "message": "Port in use" if result == 0 else "Port not in use"
            }
            sock.close()
        except Exception as e:
            services[f"frontend_port_{self.settings.frontend_port}"] = {
                "status": "error",
                "message": f"Port check failed: {str(e)}"
            }
        
        return services
    
    def _check_configuration(self) -> Dict[str, Any]:
        """Check configuration settings"""
        return {
            "app_name": self.settings.app_name,
            "app_version": self.settings.app_version,
            "debug_mode": self.settings.debug,
            "environment": "development" if self.settings.is_development else "production",
            "database_url": self.settings.database_url,
            "upload_dir": self.settings.upload_dir,
            "max_file_size_mb": round(self.settings.max_file_size / (1024 * 1024), 2),
            "auto_process_uploads": self.settings.auto_process_uploads,
            "folder_watcher_enabled": self.settings.folder_watcher_enabled
        }
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get a summary of system health"""
        health = self.check_system_health()
        
        # Count issues
        error_count = 0
        warning_count = 0
        
        for check_type, checks in health["checks"].items():
            if isinstance(checks, dict):
                if checks.get("status") == "error":
                    error_count += 1
                elif checks.get("status") == "warning":
                    warning_count += 1
            elif isinstance(checks, list):
                for check in checks:
                    if check.get("status") == "error":
                        error_count += 1
                    elif check.get("status") == "warning":
                        warning_count += 1
        
        # Determine overall status
        if error_count > 0:
            overall_status = "error"
        elif warning_count > 0:
            overall_status = "warning"
        else:
            overall_status = "healthy"
        
        return {
            "timestamp": health["timestamp"],
            "status": overall_status,
            "error_count": error_count,
            "warning_count": warning_count,
            "checks": health["checks"]
        }

# Global health checker instance
health_checker = HealthChecker() 