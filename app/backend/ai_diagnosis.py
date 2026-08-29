import os
import json
import google.genai as genai
from google.genai import types
from pydantic import ValidationError
from .config import GEMINI_API_KEY
from .models import TroubleshootingCase, DiagnosisResponse

def get_system_prompt() -> str:
    # Try to load prompt from the prompts directory
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "..", "prompts", "diagnose_prompt.md")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not load prompt from {prompt_path}: {e}")
        return "You are an AI network troubleshooter. Return valid JSON only."

def diagnose_case(case: TroubleshootingCase) -> DiagnosisResponse:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured. Cannot diagnose.")

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        raise ValueError(f"Failed to initialize Gemini client: {e}")
        
    system_prompt = get_system_prompt()
    
    user_message = f"""
Please diagnose the following case based on the provided evidence.

Symptom: {case.symptom}
Topology Note: {case.topology_note}
Concept Tag: {case.concept_tag}
Severity: {case.severity}

Show Command Outputs:
{case.show_command_outputs}
"""

    try:
        response = client.models.generate_content(
            model='gemini-3.7-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )
        )
        response_text = response.text
        
        # Parse JSON
        response_json = json.loads(response_text)
        
        # Validate with Pydantic
        diagnosis = DiagnosisResponse(**response_json)
        return diagnosis
        
    except json.JSONDecodeError as e:
        raise ValueError(f"AI returned malformed JSON: {e}")
    except ValidationError as e:
        raise ValueError(f"AI response validation failed: {e}")
    except Exception as e:
        raise ValueError(f"Gemini API failure: {e}")
