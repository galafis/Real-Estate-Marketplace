"""Configuration settings for Real-Estate-Marketplace.

Author: Gabriel Demetrios Lafis
Date: September 2025
Description: Centralized configuration management for the application.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Application Configuration
APP_CONFIG = {
    'debug': True,
    'host': '0.0.0.0',
    'port': 5000,
    'max_file_size': '16MB',
    'secret_key': os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
    'environment': os.environ.get('ENVIRONMENT', 'development')
}

# Database Configuration
DATABASE_CONFIG = {
    'type': 'sqlite',
    'name': 'real_estate.db',
    'path': BASE_DIR / 'data' / 'real_estate.db',
    'echo': False  # Set to True for SQL query logging
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    'enable_r_integration': True,
    'auto_visualization': True,
    'export_formats': ['json', 'csv', 'pdf'],
    'cache_results': True,
    'cache_ttl': 3600  # Time to live in seconds
}

# File Upload Configuration
UPLOAD_CONFIG = {
    'allowed_extensions': ['csv', 'xlsx', 'xls', 'json', 'txt'],
    'max_file_size': 16 * 1024 * 1024,  # 16MB in bytes
    'upload_folder': BASE_DIR / 'data' / 'uploads',
    'temp_folder': BASE_DIR / 'data' / 'temp'
}

# API Configuration
API_CONFIG = {
    'rate_limit': '100 per hour',
    'enable_cors': True,
    'cors_origins': ['*'],  # Configure appropriately for production
    'api_version': 'v1',
    'base_url': '/api'
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': BASE_DIR / 'logs' / 'app.log',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'enable_caching': True,
    'cache_type': 'simple',  # Options: simple, redis, memcached
    'enable_compression': True,
    'workers': 4,  # Number of worker processes for production
    'threads': 2   # Number of threads per worker
}

# Security Configuration
SECURITY_CONFIG = {
    'enable_https': False,  # Set to True in production
    'session_timeout': 3600,  # Session timeout in seconds
    'password_min_length': 8,
    'enable_2fa': False,  # Two-factor authentication
    'allowed_hosts': ['localhost', '127.0.0.1']
}

# Data Processing Configuration
DATA_CONFIG = {
    'chunk_size': 1000,  # Rows to process at a time
    'max_rows': 100000,  # Maximum rows to process
    'encoding': 'utf-8',
    'date_format': '%Y-%m-%d',
    'datetime_format': '%Y-%m-%d %H:%M:%S'
}

# R Integration Configuration
R_CONFIG = {
    'r_script_path': BASE_DIR / 'analytics.R',
    'r_packages': ['ggplot2', 'dplyr', 'corrplot', 'plotly'],
    'output_dir': BASE_DIR / 'data' / 'reports',
    'figure_width': 10,
    'figure_height': 8,
    'dpi': 300
}

# Ensure required directories exist
def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        BASE_DIR / 'data',
        BASE_DIR / 'data' / 'uploads',
        BASE_DIR / 'data' / 'temp',
        BASE_DIR / 'data' / 'reports',
        BASE_DIR / 'logs'
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories on import
create_directories()
