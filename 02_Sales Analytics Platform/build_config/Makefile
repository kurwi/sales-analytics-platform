.PHONY: help install dev-install test coverage lint format clean run build docker-build docker-run docs

# Default target
help:
	@echo "Sales Analytics Platform - Make Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make dev-install  - Install development dependencies"
	@echo "  make test         - Run test suite"
	@echo "  make coverage     - Run tests with coverage report"
	@echo "  make lint         - Run code linters"
	@echo "  make format       - Format code with Black and isort"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo "  make run          - Run the dashboard application"
	@echo "  make build        - Build distribution packages"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make docs         - Generate documentation"

# Installation
install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install -r config/requirements-dev.txt

# Testing
test:
	pytest tests/

coverage:
	pytest --cov=src --cov-report=html --cov-report=term-missing tests/

# Code Quality
lint:
	flake8 src/ tests/
	mypy src/
	pylint src/

format:
	black src/ tests/
	isort src/ tests/

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Running
run:
	python run.py

# Building
build: clean
	python -m build

# Docker
docker-build:
	docker build -t sales-analytics-platform:latest -f docker/Dockerfile .

docker-run:
	docker-compose -f docker/docker-compose.yml up -d

docker-stop:
	docker-compose -f docker/docker-compose.yml down

# Documentation
docs:
	cd docs && make html

# Data
generate-data:
	python data/generate_sample_data.py

# Validation
validate:
	python scripts/validate_enterprise_systems.py

# Setup
setup: dev-install generate-data validate
	@echo "Setup complete! Run 'make run' to start the dashboard."
