# Responsible AI Implementation

NetSage AI is designed with strict Responsible AI (RAI) principles to ensure safe and reliable network automation.

## Principles
1. **Human-in-the-Loop (HITL):** AI-generated troubleshooting advice is strictly advisory. It requires manual review by an operator before any commands are run on network equipment.
2. **Deterministic Fallbacks:** We run deterministic rule checks (e.g. for duplicate IPs, subnet mismatches) before AI diagnosis to ensure ground-truth accuracy on well-known problems.
3. **Auditability:** All AI predictions, human decisions, and corrections are logged in `data/reviews/responsible_ai_log.csv` for continuous monitoring and improvement.
4. **Transparency:** AI confidence scores and uncertainty notes are surfaced directly in the dashboard to warn operators about low-confidence diagnoses.
