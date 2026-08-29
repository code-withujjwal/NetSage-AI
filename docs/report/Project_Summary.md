# NetSage AI: Project Summary

## 1. Problem
Network troubleshooting is a complex, time-consuming process that requires deep domain expertise. Junior engineers and students often struggle to map raw CLI outputs from Cisco devices to logical configuration errors.

## 2. Objective
To build an AI-assisted network troubleshooting engine that analyzes symptom descriptions, network topologies, and Cisco `show` command outputs to accurately diagnose the root cause, while maintaining strict Responsible AI oversight.

## 3. Architecture
- **Backend:** FastAPI handles REST endpoints and orchestrates the logic.
- **AI Engine:** Google Gemini (via `google-genai` SDK) processes structured prompts and returns validated JSON using Pydantic schemas.
- **Rule Checker:** A deterministic, regex-based Python script that pre-screens cases for glaring errors (e.g., subnet mask mismatches) before AI diagnosis.
- **Frontend:** A Streamlit dashboard visualizes the dataset, AI predictions, and human-in-the-loop actions.

## 4. Dataset
We created a custom dataset of 30 networking troubleshooting cases (`data/cases/cases.csv`), covering VLANs, Routing, Gateways, DHCP, DNS, ACLs, NAT, and Wireless. Each case contains a realistic symptom, topology note, and evidence-grounded Cisco `show` command outputs. Note: While 30 cases exist in the text dataset, only 1 corresponding Cisco Packet Tracer topology (`packet_tracer/NetSage-AI-VLAN-001.pkt`) is provided as a demonstrated simulation artifact. The remaining 29 `.pkt` topology files were not created and are not claimed as completed.

## 5. AI Prompt Design
The system uses a highly structured system prompt (`prompts/diagnose_prompt.md`) instructing the AI to act as a senior network engineer. It enforces deterministic reasoning, ensuring the AI only flags faults that are explicitly proven by the provided CLI output, avoiding hallucinations.

## 6. Rule Checker
To enhance reliability, a deterministic Rule Checker (`rule_checker/rule_checker.py`) processes the text to catch common misconfigurations (Duplicate IPs, Missing Routes) statically. This acts as a reliable fallback and sanity check alongside the LLM.

## 7. Human Review
All AI outputs are strictly advisory. The system features a simulated human review step (`data/reviews/reviews.csv`) where an operator accepts, edits, or rejects the AI's diagnosis before generating actual configuration fixes.

## 8. Responsible AI
A Responsible AI log (`docs/responsible_ai.md`, `data/reviews/responsible_ai_log.csv`) explicitly tracks the AI's confidence, uncertainty statements, and human corrections, ensuring transparency and alignment with safety guidelines.

## 9. Dashboard
The Streamlit dashboard (`dashboard/app.py`) provides an interactive visualization of the 30 cases, breaking down AI accuracy, severity distributions, and an end-to-end trace of Case -> Evidence -> AI Diagnosis -> Human Review.

## 10. Results
The Gemini engine effectively processes the Cisco output, accurately diagnosing cases and structuring its response into actionable steps. The deterministic rule checker successfully acts as a safety net for basic configuration flaws.

## 11. Limitations
- The system currently relies on static text outputs rather than live SSH access to devices.
- The AI's performance is strictly bound by the quality and completeness of the provided `show` command evidence.

## 12. Future Scope
Future enhancements could include direct SSH/Netmiko integration to dynamically pull `show` commands from live Cisco devices based on the AI's `next_command` recommendations.
