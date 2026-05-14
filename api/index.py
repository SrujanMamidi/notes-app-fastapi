import os
import sys

# Add the backend directory to Python path so internal imports (like 'routes.notes') work on Vercel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from backend.main import app
