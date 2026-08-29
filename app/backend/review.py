from pydantic import BaseModel
import csv
import os
from datetime import datetime

class ReviewRequest(BaseModel):
    case_id: str
    ai_root_cause: str
    ai_confidence: float
    human_decision: str
    human_correction: str
    reviewer_note: str

def save_review(req: ReviewRequest):
    review_file = 'data/reviews/reviews.csv'
    rai_file = 'data/reviews/responsible_ai_log.csv'
    
    file_exists = os.path.isfile(review_file)
    with open(review_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['case_id', 'ai_root_cause', 'ai_confidence', 'human_decision', 'human_correction', 'reviewer_note', 'timestamp'])
        writer.writerow([
            req.case_id, req.ai_root_cause, req.ai_confidence, req.human_decision, req.human_correction, req.reviewer_note, datetime.utcnow().isoformat()
        ])
        
    file_exists = os.path.isfile(rai_file)
    with open(rai_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['case_id', 'ai_diagnosis', 'human_decision', 'whether_ai_was_correct', 'correction_reason', 'safety_uncertainty_note'])
        
        is_correct = "Yes" if req.human_decision == "Accepted" else "No" if req.human_decision == "Rejected" else "Partially"
        writer.writerow([
            req.case_id, req.ai_root_cause, req.human_decision, is_correct, req.human_correction, "Human submitted review"
        ])

    return {"status": "success", "message": "Review saved successfully."}
