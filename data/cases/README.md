# NetSage AI - Case Dataset

## Purpose of the Dataset
This dataset (`cases.csv`) contains the foundational troubleshooting scenarios for the NetSage AI project. These scenarios are designed to simulate realistic networking issues found in Cisco Packet Tracer or physical lab environments. They provide the necessary context (symptoms, topology details, and CLI outputs) for both the AI diagnosis engine and the human reviewer to analyze and identify the root cause.

## Column Definitions
The `cases.csv` file contains the following columns:

- **case_id**: A unique identifier for the troubleshooting scenario (e.g., VLAN-001).
- **symptom**: A realistic networking symptom reported by a user or monitoring system (e.g., "PC1 cannot ping PC2").
- **topology_note**: A concise description of the relevant network topology (e.g., "PC1 is on Fa0/1, PC2 is on Fa0/2").
- **show_command_outputs**: The realistic Cisco show-command outputs containing evidence of the fault.
- **expected_fault**: The known, actual root cause of the issue. **This represents the ground truth used for evaluation.**
- **osi_layer**: The OSI layer where the primary fault resides (e.g., Layer 2, Layer 3).
- **concept_tag**: The overarching networking concept category (e.g., VLAN, Routing, DHCP).
- **severity**: The impact level of the issue (Low, Medium, or High).

## Case Coverage
The dataset includes exactly 30 original cases, ensuring diverse coverage across eight critical CCNA-level networking domains:

- **VLAN**: 4 cases
- **Gateway**: 4 cases
- **DHCP**: 4 cases
- **DNS**: 3 cases
- **Routing**: 5 cases
- **ACL**: 4 cases
- **NAT**: 4 cases
- **Wireless**: 2 cases

## How the Dataset Will Be Used by NetSage AI
1. **Application Ingestion**: The NetSage AI backend will read this CSV file to populate the application's available troubleshooting scenarios.
2. **AI Diagnosis**: For a selected case, the `symptom`, `topology_note`, and `show_command_outputs` will be packaged into a prompt and sent to the Gemini API. The AI is expected to analyze this evidence and determine the root cause, confidence, and fix steps without seeing the `expected_fault`.
3. **Deterministic Rules**: The `show_command_outputs` will be parsed by the Python rule checker to explicitly detect configuration mistakes (like incorrect IP addresses or down interfaces) to supplement the AI.
4. **Evaluation**: The `expected_fault` column acts as the objective ground truth. It will be used by the human reviewer (and the dashboard metrics) to evaluate whether the AI successfully and accurately diagnosed the problem.
