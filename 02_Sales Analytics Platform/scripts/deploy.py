"""
Production deployment script for Sales Analytics Platform.

This script handles environment setup, dependency installation, 
data initialization, and system health checks for production deployment.

Usage:
    python deploy.py --env production --check-only
    python deploy.py --env staging --skip-data
"""
import argparse
import sys
import os
import subprocess
import logging
from pathlib import Path
from typing import List, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DeploymentManager:
    """Manages platform deployment process."""
    
    def __init__(self, environment: str = "production", skip_data: bool = False):
        self.environment = environment
        self.skip_data = skip_data
        self.root_dir = Path(__file__).parent
        self.errors: List[str] = []
        
    def run_deployment(self) -> bool:
        """
        Execute full deployment process.
        
        Returns:
            bool: True if deployment successful, False otherwise
        """
        logger.info(f"Starting deployment for environment: {self.environment}")
        
        steps = [
            ("Environment validation", self.validate_environment),
            ("Directory structure", self.create_directories),
            ("Python dependencies", self.install_dependencies),
            ("Configuration validation", self.validate_configuration),
            ("Database initialization", self.initialize_database),
            ("Data generation", self.generate_sample_data),
            ("ML model training", self.train_models),
            ("System health check", self.health_check)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"Executing: {step_name}")
            success, message = step_func()
            
            if not success:
                self.errors.append(f"{step_name}: {message}")
                logger.error(f"Failed: {step_name} - {message}")
                
                if self.environment == "production":
                    logger.critical("Deployment aborted due to errors")
                    self.print_summary()
                    return False
            else:
                logger.info(f"Completed: {step_name}")
        
        self.print_summary()
        return len(self.errors) == 0
    
    def validate_environment(self) -> Tuple[bool, str]:
        """Validate Python version and system requirements."""
        try:
            if sys.version_info < (3, 10):
                return False, f"Python 3.10+ required, found {sys.version_info.major}.{sys.version_info.minor}"
            
            required_env_vars = []
            if self.environment == "production":
                required_env_vars = ["SECRET_KEY"]
            
            missing_vars = [var for var in required_env_vars if not os.getenv(var)]
            if missing_vars:
                return False, f"Missing environment variables: {', '.join(missing_vars)}"
            
            return True, "Environment validated"
        except Exception as e:
            return False, str(e)
    
    def create_directories(self) -> Tuple[bool, str]:
        """Create required directory structure."""
        try:
            directories = [
                "data/raw",
                "data/processed",
                "models",
                "logs",
                "notebooks/data",
                "src/dashboard",
                "src/etl",
                "src/features",
                "src/models",
                "src/ai",
                "src/realtime",
                "src/utils"
            ]
            
            for directory in directories:
                Path(directory).mkdir(parents=True, exist_ok=True)
            
            return True, f"Created {len(directories)} directories"
        except Exception as e:
            return False, str(e)
    
    def install_dependencies(self) -> Tuple[bool, str]:
        """Install Python dependencies from requirements.txt."""
        try:
            requirements_file = self.root_dir / "requirements.txt"
            if not requirements_file.exists():
                return False, "requirements.txt not found"
            
            logger.info("Installing dependencies (this may take several minutes)")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file), "--quiet"],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode != 0:
                return False, f"pip install failed: {result.stderr}"
            
            return True, "Dependencies installed successfully"
        except subprocess.TimeoutExpired:
            return False, "Installation timed out (>10 minutes)"
        except Exception as e:
            return False, str(e)
    
    def validate_configuration(self) -> Tuple[bool, str]:
        """Validate configuration files and settings."""
        try:
            sys.path.insert(0, str(self.root_dir))
            from src.config import config
            
            if self.environment == "production":
                config.validate()
            
            return True, "Configuration validated"
        except Exception as e:
            return False, str(e)
    
    def initialize_database(self) -> Tuple[bool, str]:
        """Initialize database schema and tables."""
        try:
            # Placeholder for database initialization
            # In production, this would run SQL scripts or ORM migrations
            logger.info("Database initialization skipped (file-based storage)")
            return True, "Database initialization not required"
        except Exception as e:
            return False, str(e)
    
    def generate_sample_data(self) -> Tuple[bool, str]:
        """Generate sample data for testing and development."""
        if self.skip_data or self.environment == "production":
            return True, "Data generation skipped"
        
        try:
            data_generator = self.root_dir / "data" / "generate_sample_data.py"
            if not data_generator.exists():
                return False, "Data generator script not found"
            
            result = subprocess.run(
                [sys.executable, str(data_generator)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                return False, f"Data generation failed: {result.stderr}"
            
            return True, "Sample data generated"
        except subprocess.TimeoutExpired:
            return False, "Data generation timed out"
        except Exception as e:
            return False, str(e)
    
    def train_models(self) -> Tuple[bool, str]:
        """Train ML models on available data."""
        if self.skip_data:
            return True, "Model training skipped"
        
        try:
            logger.info("Model training skipped - train manually via notebooks")
            return True, "Manual training required"
        except Exception as e:
            return False, str(e)
    
    def health_check(self) -> Tuple[bool, str]:
        """Perform system health check."""
        try:
            checks = []
            
            # Check data files exist
            sales_data = Path("data/sales_data.csv")
            checks.append(("Sales data", sales_data.exists()))
            
            # Check required modules can be imported
            try:
                import pandas
                import numpy
                import plotly
                import dash
                import sklearn
                checks.append(("Core dependencies", True))
            except ImportError as e:
                checks.append(("Core dependencies", False))
            
            # Check configuration
            try:
                from src.config import config
                checks.append(("Configuration", True))
            except Exception:
                checks.append(("Configuration", False))
            
            failed_checks = [name for name, status in checks if not status]
            if failed_checks:
                return False, f"Failed checks: {', '.join(failed_checks)}"
            
            return True, f"All {len(checks)} health checks passed"
        except Exception as e:
            return False, str(e)
    
    def print_summary(self):
        """Print deployment summary."""
        logger.info("=" * 60)
        logger.info("DEPLOYMENT SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Environment: {self.environment}")
        logger.info(f"Errors: {len(self.errors)}")
        
        if self.errors:
            logger.error("Deployment FAILED with errors:")
            for error in self.errors:
                logger.error(f"  - {error}")
        else:
            logger.info("Deployment SUCCESSFUL")
            logger.info("")
            logger.info("Next steps:")
            logger.info("  1. Review configuration in src/config.py")
            logger.info("  2. Set environment variables (SECRET_KEY, OPENAI_API_KEY)")
            logger.info("  3. Generate data: python data/generate_sample_data.py")
            logger.info("  4. Launch dashboard: python run_dashboard.py")
            logger.info("  5. Access at http://localhost:8050")
        
        logger.info("=" * 60)

def main():
    """Main deployment entry point."""
    parser = argparse.ArgumentParser(description="Deploy Sales Analytics Platform")
    parser.add_argument(
        "--env",
        choices=["development", "staging", "production"],
        default="development",
        help="Deployment environment"
    )
    parser.add_argument(
        "--skip-data",
        action="store_true",
        help="Skip data generation and model training"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Run health checks only without deployment"
    )
    
    args = parser.parse_args()
    
    deployer = DeploymentManager(
        environment=args.env,
        skip_data=args.skip_data
    )
    
    if args.check_only:
        logger.info("Running health check only")
        success, message = deployer.health_check()
        logger.info(f"Health check: {'PASSED' if success else 'FAILED'} - {message}")
        sys.exit(0 if success else 1)
    
    success = deployer.run_deployment()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
