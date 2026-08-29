# NetSage AI – AI-Assisted Network Troubleshooting System

**Project Type:** Networking + Artificial Intelligence  
**Prepared For:** Cisco AICTE Virtual Internship Program 2026 – Networking Track  

**Student Name:** Ujjwal Pandey  
**AICTE ID:** STU69f279047b0211777498372  
**College:** Lakshmi Narain College of Technology (LNCT)  
**Branch:** Computer Science and Engineering  
**Semester:** 4th Semester (2nd Year)  

---

## 1. Executive Summary
Network troubleshooting in enterprise environments requires substantial domain expertise to map raw Command Line Interface (CLI) outputs to logical configuration faults. **NetSage AI** is an advanced, AI-assisted network troubleshooting engine designed to accelerate fault isolation and resolution. The system leverages Google Gemini to process symptom descriptions, network topologies, and Cisco `show` command evidence to generate accurate, actionable diagnoses. To ensure reliability, NetSage AI operates on a hybrid architecture combining a deterministic rule-validation layer with generative AI analysis, all governed by a strict human-in-the-loop review workflow.

This project was developed collaboratively by a two-member team. The final deliverable includes a functional FastAPI backend, a comprehensive troubleshooting dataset, and an interactive Streamlit dashboard that visualizes the end-to-end Responsible AI workflow.

## 2. Problem Statement
Identifying root causes of network disruptions often involves manually parsing extensive device logs and configuration outputs. Junior engineers and students frequently struggle to correlate symptoms (e.g., unreachable gateways) with the underlying CLI evidence (e.g., misconfigured VLANs or missing ACLs). Relying solely on manual analysis increases Mean Time to Resolution (MTTR) and operational overhead. Conversely, relying entirely on unfiltered generative AI introduces the risk of "hallucinations" and unverified configuration changes. 

## 3. Objectives
- **Accelerate Fault Diagnosis:** Build an AI pipeline capable of rapidly analyzing Cisco `show` command outputs to identify network faults.
- **Ensure Deterministic Reliability:** Implement pre-screening rule checks to statically validate common misconfigurations prior to AI processing.
- **Maintain Responsible AI Standards:** Enforce a strict human-in-the-loop workflow where all AI-generated diagnoses are treated as advisory and require human review.
- **Provide Actionable Insights:** Present the diagnosis, evidence, and review logs in an interactive, user-friendly dashboard.

## 4. System Architecture
NetSage AI follows a modular, decoupled architecture:
1. **Frontend (Streamlit):** An interactive dashboard for visualizing case metrics, AI performance, and the review audit trail.
2. **Backend (FastAPI):** A high-performance REST API that orchestrates incoming case requests.
3. **Deterministic Rule Checker:** A Python-based validation layer that scans incoming evidence for explicit configuration violations (e.g., duplicated IPs, missing routes).
4. **AI Diagnosis Engine (Google Gemini):** A generative AI module configured with strict system prompts to analyze complex CLI evidence and output structured JSON using Pydantic validation.
5. **Human Review / RAI Logger:** A governance module that logs human decisions (Accept/Edit/Reject) alongside the AI's confidence scores.

## 5. Technology Stack
- **Programming Language:** Python
- **Backend Framework:** FastAPI
- **AI Integration:** Google Gemini (via `google-genai` SDK)
- **Data Validation:** Pydantic
- **Frontend/Visualization:** Streamlit
- **Network Simulation:** Cisco Packet Tracer

## 6. Dataset Design
A robust, custom dataset consisting of 30 networking troubleshooting scenarios was developed to validate the system. The dataset covers a wide spectrum of enterprise networking concepts:
- VLANs and Trunking
- Static and Dynamic Routing
- DHCP Configurations
- DNS Resolution
- Network Address Translation (NAT)
- Access Control Lists (ACLs)
- Default Gateway Validation
- Wireless Networking

Each case in the dataset includes a realistic symptom description, topology context, and evidence-grounded Cisco `show` command outputs.

## 7. Hybrid Analysis Workflow
### 7.1. Deterministic Rule Validation
To mitigate the risk of AI hallucination, incoming cases are first processed by a deterministic rule-checking algorithm. This module utilizes regex-based static analysis to identify glaring misconfigurations—such as subnet mask mismatches or administratively down interfaces—providing a highly reliable, zero-hallucination baseline.

### 7.2. AI Diagnosis Workflow
Cases that require deeper logical correlation are processed by the Google Gemini engine. The AI is constrained by a highly structured system prompt, instructing it to act as a senior network engineer. It is strictly mandated to base its conclusions entirely on the provided CLI evidence, outputting a structured JSON response containing the root cause, suggested fix commands, and a calculated confidence score.

## 8. Responsible AI Framework
Safety and accountability are central to NetSage AI.
- **Human Oversight:** AI outputs are strictly advisory. The system enforces a simulated human-review workflow where an operator must accept, edit, or reject the diagnosis.
- **Audit Logging:** Every interaction is securely recorded in a Responsible AI log, tracking the AI's uncertainty statements and human corrections.
- **Evidence-Based Constraints:** The AI is explicitly instructed to output "Insufficient Evidence" if the provided `show` commands do not prove a fault.

## 9. Dashboard Visualization
The Streamlit dashboard serves as the operational interface for NetSage AI. It provides an interactive visualization of the 30-case dataset, breaking down AI accuracy across different networking concepts, severity distributions, and an end-to-end trace of the Case -> Evidence -> AI Diagnosis -> Human Review lifecycle.

## 10. Testing, Validation, and Results
The system successfully processed the troubleshooting dataset. The hybrid architecture proved highly effective: the deterministic rule checker reliably acted as a safety net for basic configuration flaws, while the Gemini engine accurately diagnosed complex, multi-variable issues. The implementation of Pydantic validation ensured that the AI consistently returned correctly formatted JSON data for backend consumption. 

## 11. Project Limitations
To maintain factual transparency, the following technical limitations apply to the current iteration of the system:
- **Packet Tracer Deliverables:** While the text dataset successfully documents 30 troubleshooting cases, only **one** corresponding Cisco Packet Tracer topology (`NetSage-AI-VLAN-001.pkt`) is provided as a demonstrated simulation artifact.
- **API Constraints:** During testing and batch processing, intermittent Google Gemini API availability and free-tier quota limitations required the implementation of deterministic fallback logic. Consequently, some cases in the final output dataset are explicitly labeled as `[DEMO FALLBACK]` where the rule-checker successfully bypassed the unavailable AI.
- **Static Evidence:** The system currently analyzes static, pre-collected CLI text outputs rather than establishing live SSH connections to networking hardware.

## 12. Future Scope
Subsequent phases of development could introduce direct SSH/Netmiko integration, allowing the engine to dynamically pull live `show` command outputs from Cisco devices. Additionally, integrating a local, open-source Large Language Model (LLM) could resolve external API quota dependencies and improve data privacy for enterprise environments.

## 13. Conclusion
NetSage AI successfully demonstrates the potential of combining deterministic engineering principles with generative AI to solve complex networking challenges. By enforcing strict human-in-the-loop oversight and Responsible AI guidelines, the project proves that AI can safely and effectively reduce troubleshooting overhead in modern network operations.

---

## 14. Individual Contribution (Ujjwal Pandey)
As a key contributor in a two-member team, I played a central role in the technical implementation and architectural design of NetSage AI. My specific contributions include:
- **System Architecture & Backend:** Participated in designing the decoupled architecture and implemented the core FastAPI backend logic to handle diagnosis requests.
- **AI Integration & Prompt Engineering:** Structured the system prompts and integrated the Google Gemini SDK. Implemented Pydantic data models to enforce strict, parsable JSON outputs from the LLM.
- **Deterministic Validation:** Programmed the Python-based rule-checker to execute static regex validation on networking evidence prior to AI processing.
- **Dashboard & RAI Implementation:** Integrated the Streamlit dashboard and engineered the Responsible AI workflow, ensuring human review actions were correctly tracked and logged.
- **Testing & Debugging:** Led the dataset validation, managed API quota fallback logic (`batch_diagnose.py`), and debugged integration issues across the stack to ensure submission readiness.
