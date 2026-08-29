from pydantic import BaseModel, Field
from typing import List

class TroubleshootingCase(BaseModel):
    symptom: str
    topology_note: str
    show_command_outputs: str
    concept_tag: str
    severity: str

class DiagnosisResponse(BaseModel):
    root_cause: str = Field(description="Detailed explanation of the root cause.")
    confidence: float = Field(description="Confidence level between 0.0 and 1.0.")
    osi_layer: str = Field(description="The OSI layer of the fault.")
    evidence: List[str] = Field(description="Specific quotes/references from the show outputs.")
    next_command: str = Field(description="Recommended next Cisco show command.")
    fix_steps: List[str] = Field(description="Step-by-step fix instructions (Cisco IOS CLI).")
    verification_command: str = Field(description="Command to verify the fix.")
    uncertainty: str = Field(description="Explanation of uncertainty if evidence is insufficient.")
