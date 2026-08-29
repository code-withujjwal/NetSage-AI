import os
import google.genai as genai
from dotenv import load_dotenv

env_path = os.path.join("app", "backend", ".env")
load_dotenv(dotenv_path=env_path)

try:
    client = genai.Client()
    print("Available Models:")
    for model in client.models.list():
        # Check if the model supports content generation
        if "generateContent" in model.supported_actions:
            print(f"- {model.name}")
except Exception as e:
    print(f"Error: {e}")
