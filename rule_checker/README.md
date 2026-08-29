# NetSage AI Deterministic Rule Checker

This module provides a deterministic, regex-based Python rule checker that analyzes networking troubleshooting cases for common configuration problems. It runs locally and does NOT use the Gemini API.

## Checks Performed
The Rule Checker currently looks for explicit evidence of:
1. Duplicate IP addresses
2. Wrong subnet mask (e.g. Class C with Class A mask)
3. Gateway mismatch
4. Interface administratively down
5. Missing VLANs (VLAN not created on switch)
6. Missing routes (Destination unreachable / Network not in table)

If the provided evidence (`show_command_outputs`) is insufficient to definitively prove a problem, the checker strictly defaults to returning `NOT_DETERMINED`.

## How to Run

### Run against a specific case from the CSV dataset:
```bash
python rule_checker.py --csv ../data/cases/cases.csv --case_id VLAN-001
```

### Run against a raw JSON string:
```bash
python rule_checker.py --json '{"case_id": "TEST", "show_command_outputs": "GigabitEthernet0/1 is administratively down"}'
```

## Output Format
The checker outputs structured JSON conforming to the following format:
```json
{
  "case_id": "VLAN-001",
  "checks": [
    {
      "check": "Missing route",
      "status": "NOT_DETERMINED",
      "evidence": "",
      "explanation": "No definitive missing route evidence found."
    }
  ],
  "issues_found": 0,
  "summary": "Found 0 deterministic configuration issue(s)."
}
```
