# NetSage AI: Demo Script

**Duration:** 5-10 minutes
**Target Audience:** Cisco-AICTE VIP Reviewers

## 1. Introduction (1 min)
- Introduce the NetSage AI project.
- Explain the objective: to assist junior engineers in troubleshooting network configurations using AI and deterministic rules.
- Mention the dataset: 30 evidence-grounded Cisco Packet Tracer scenarios.

## 2. The Deterministic Rule Checker (2 mins)
- Explain that before we use AI, we run a deterministic Python script to catch obvious flaws safely.
- **Action:** Open terminal and run:
  `python rule_checker.py --csv ../data/cases/cases.csv --case_id VLAN-001`
- **Result:** Explain how the checker parses the CLI output deterministically, showing it defaults to `NOT_DETERMINED` safely when text matching isn't enough, proving it doesn't guess.

## 3. The AI Diagnosis Engine (3 mins)
- Explain the `VLAN-001` scenario: "PC1 and PC2 cannot ping. They should both be in VLAN 10."
- Show the raw `cases.csv` evidence: `show vlan brief` reveals Fa0/2 is stuck in VLAN 1.
- **Action:** Open the Streamlit Dashboard (`streamlit run app.py`).
- Navigate to the **Case Detail Explorer** and select `VLAN-001`.
- Walk the audience through the AI's diagnosis:
  - **Root Cause:** "PC2 is assigned to VLAN 1 instead of VLAN 10."
  - **Fix Steps:** Shows exactly which Cisco commands to run (`interface Fa0/2`, `switchport access vlan 10`).

## 4. Human-in-the-Loop & Responsible AI (2 mins)
- Highlight the **Human Review** section on the dashboard.
- Show the **Responsible AI Log** table in the UI.
- Explain that AI is advisory. Point out a case that was "Edited" or "Rejected" by a human reviewer to prove the HITL mechanism works.

## 5. Conclusion (1 min)
- Summarize the value: NetSage AI combines AI flexibility with rule-based deterministic safety and human oversight.
- End demo and open for Q&A.
