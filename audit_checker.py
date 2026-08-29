import csv
from rule_checker.rule_checker import process_case
import json

checks_found = {}

with open('data/cases/cases.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        result = process_case(row)
        for check in result['checks']:
            if check['status'] == 'FAIL':
                if check['check'] not in checks_found:
                    checks_found[check['check']] = []
                checks_found[check['check']].append(row['case_id'])

print(json.dumps(checks_found, indent=2))
