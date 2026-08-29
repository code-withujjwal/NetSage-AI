import csv
import json

with open('data/cases/cases.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        out = (row['show_command_outputs'] + " " + row['symptom'] + " " + row['topology_note']).lower()
        if 'down' in out:
            print(f"[{row['case_id']}] Fault: {row['expected_fault']}")
            print(f"Outputs: {row['show_command_outputs']}")
            print(f"Symptom: {row['symptom']}")
            print("---")
