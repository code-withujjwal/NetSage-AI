import os
from dotenv import load_dotenv

# Load environment variables from app/backend/.env file securely
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Do NOT expose this key to the frontend or log it.
