"""Configuration module for Relaxo application"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Server Configuration
PORT = int(os.getenv('PORT', 8000))
HOST = os.getenv('HOST', 'localhost')
WEB_FOLDER = os.getenv('WEB_FOLDER', 'web')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

# App Configuration
WORK_TIME_MINUTES = int(os.getenv('WORK_TIME_MINUTES', 60))
BREAK_TIME_MINUTES = int(os.getenv('BREAK_TIME_MINUTES', 5))
REMIND_AGAIN_MINUTES = int(os.getenv('REMIND_AGAIN_MINUTES', 10))

# Logging Configuration
LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

# Validation
assert 1 <= PORT <= 65535, "PORT must be between 1 and 65535"
assert WORK_TIME_MINUTES >= 1, "WORK_TIME_MINUTES must be >= 1"
assert BREAK_TIME_MINUTES >= 1, "BREAK_TIME_MINUTES must be >= 1"
