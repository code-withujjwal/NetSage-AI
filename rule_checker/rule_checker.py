import json
import re
import argparse
import sys
import csv

class RuleChecker:
    """
    Deterministic rule checker for NetSage AI.
    Analyzes networking troubleshooting cases for common configuration issues using text/regex rules.
    """
    def __init__(self, case_data):
        self.case = case_data
        self.case_id = case_data.get('case_id', 'UNKNOWN')
        self.symptom = case_data.get('symptom', '')
        self.topology = case_data.get('topology_note', '')
        self.outputs = case_data.get('show_command_outputs', '')
        self.checks = []

    def run_all(self):
        self.checks.append(self.check_duplicate_ip())
        self.checks.append(self.check_subnet_mask())
        self.checks.append(self.check_gateway_mismatch())
        self.checks.append(self.check_admin_down())
        self.checks.append(self.check_missing_vlan())
        self.checks.append(self.check_missing_route())
        
        issues = sum(1 for c in self.checks if c['status'] == 'FAIL')
        
        return {
            "case_id": self.case_id,
            "checks": self.checks,
            "issues_found": issues,
            "summary": f"Found {issues} deterministic configuration issue(s)."
        }

    def check_duplicate_ip(self):
        match = re.search(r'(%IP-4-DUPADDR.*|Duplicate address.*|show ip dhcp conflict)', self.outputs, re.IGNORECASE)
        if match:
            return {
                "check": "Duplicate IP addresses", 
                "status": "FAIL", 
                "evidence": match.group(0).strip(), 
                "explanation": "A duplicate IP address warning or conflict was detected in the device output."
            }
        return {
            "check": "Duplicate IP addresses", 
            "status": "NOT_DETERMINED", 
            "evidence": "", 
            "explanation": "No duplicate IP warnings found."
        }

    def check_subnet_mask(self):
        # Check standard format: IP/Mask or IP Mask
        matches = re.finditer(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})[/ ]+(255\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', self.outputs)
        for m in matches:
            ip, mask = m.groups()
            if ip.startswith('192.168.') and mask != '255.255.255.0':
                return {
                    "check": "Wrong subnet mask", 
                    "status": "FAIL", 
                    "evidence": f"Found IP {ip} with mask {mask}", 
                    "explanation": "Class C private IP is using a non-standard mask, which may indicate a misconfiguration."
                }
                
        # Check ipconfig format
        ipconfig_ip = re.search(r'IPv4 Address[\.\s]+:\s+([0-9\.]+)', self.outputs, re.IGNORECASE)
        ipconfig_mask = re.search(r'Subnet Mask[\.\s]+:\s+([0-9\.]+)', self.outputs, re.IGNORECASE)
        if ipconfig_ip and ipconfig_mask:
            ip = ipconfig_ip.group(1)
            mask = ipconfig_mask.group(1)
            if ip.startswith('192.168.') and mask != '255.255.255.0':
                return {
                    "check": "Wrong subnet mask", 
                    "status": "FAIL", 
                    "evidence": f"Found IP {ip} with mask {mask}", 
                    "explanation": "Class C private IP is using a non-standard mask, which may indicate a misconfiguration."
                }
                
        return {
            "check": "Wrong subnet mask", 
            "status": "NOT_DETERMINED", 
            "evidence": "", 
            "explanation": "Insufficient evidence to determine if mask is wrong."
        }

    def check_gateway_mismatch(self):
        top_gw_match = re.search(r'gateway is ([0-9\.]+)', self.topology, re.IGNORECASE)
        out_gw_match = re.search(r'Default Gateway[\.\s]+:\s+([0-9\.]+)', self.outputs, re.IGNORECASE)
        
        if top_gw_match and out_gw_match:
            top_gw = top_gw_match.group(1)
            out_gw = out_gw_match.group(1)
            if top_gw != out_gw:
                return {
                    "check": "Gateway mismatch", 
                    "status": "FAIL", 
                    "evidence": f"Topology gateway {top_gw}, but host configured with {out_gw}", 
                    "explanation": "The host is configured with an incorrect default gateway."
                }
        return {
            "check": "Gateway mismatch", 
            "status": "NOT_DETERMINED", 
            "evidence": "", 
            "explanation": "Requires cross-device topology context, which cannot be definitively proven by static text analysis."
        }

    def check_admin_down(self):
        matches = re.findall(r'([A-Za-z0-9/\.]+)\s+.*?administratively down', self.outputs, re.IGNORECASE)
        if matches:
            return {
                "check": "Interface administratively down", 
                "status": "FAIL", 
                "evidence": f"Interfaces shut down: {', '.join(matches)}", 
                "explanation": "One or more interfaces are administratively down (shut down)."
            }
        
        if "administratively down" in self.outputs.lower():
            return {
                "check": "Interface administratively down", 
                "status": "FAIL", 
                "evidence": "Output contains 'administratively down'", 
                "explanation": "An interface is administratively shut down."
            }
            
        return {
            "check": "Interface administratively down", 
            "status": "NOT_DETERMINED", 
            "evidence": "", 
            "explanation": "No shut down interfaces detected."
        }

    def check_missing_vlan(self):
        if "show vlan brief" in self.outputs:
            if "does not exist" in self.outputs.lower():
                return {
                    "check": "Missing VLAN", 
                    "status": "FAIL", 
                    "evidence": "VLAN does not exist message found in output", 
                    "explanation": "Switch reported a missing VLAN."
                }
            
            # Check if a VLAN mentioned in the symptom is completely missing from the VLAN table
            vlans_expected = set(re.findall(r'VLAN\s+(\d+)', self.topology + " " + self.symptom, re.IGNORECASE))
            vlans_active = set(re.findall(r'^(\d+)\s+', self.outputs, re.MULTILINE))
            missing = vlans_expected - vlans_active
            if missing:
                return {
                    "check": "Missing VLAN",
                    "status": "FAIL",
                    "evidence": f"VLAN(s) {list(missing)} mentioned in topology but missing from show vlan brief output.",
                    "explanation": "A required VLAN has not been created on the switch."
                }
                
        return {
            "check": "Missing VLAN", 
            "status": "NOT_DETERMINED", 
            "evidence": "", 
            "explanation": "Could not definitively prove a missing VLAN."
        }

    def check_missing_route(self):
        if re.search(r'(Network not in table|unreachable|no route to host)', self.outputs, re.IGNORECASE):
            return {
                "check": "Missing route", 
                "status": "FAIL", 
                "evidence": "Output contains unreachable or missing route message.", 
                "explanation": "A routing failure is evident from the command output."
            }
        if "show ip route" in self.outputs and "ISP" in self.topology and "S*" not in self.outputs:
             return {
                "check": "Missing route", 
                "status": "FAIL", 
                "evidence": "Topology connects to ISP but no default route (S*) in show ip route", 
                "explanation": "A default route to the ISP is missing."
            }
        return {
            "check": "Missing route", 
            "status": "NOT_DETERMINED", 
            "evidence": "", 
            "explanation": "No definitive missing route evidence found."
        }

def process_case(case_dict):
    checker = RuleChecker(case_dict)
    return checker.run_all()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NetSage Deterministic Rule Checker")
    parser.add_argument("--csv", help="Path to cases.csv")
    parser.add_argument("--case_id", help="Case ID to check (e.g. VLAN-001)")
    parser.add_argument("--json", help="Direct JSON input string of a case")
    args = parser.parse_args()

    if args.csv and args.case_id:
        try:
            with open(args.csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('case_id') == args.case_id:
                        result = process_case(row)
                        print(json.dumps(result, indent=2))
                        sys.exit(0)
            print(f"Case {args.case_id} not found in {args.csv}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            sys.exit(1)
            
    elif args.json:
        try:
            case_dict = json.loads(args.json)
            result = process_case(case_dict)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            sys.exit(1)
    else:
        print("Please provide --csv and --case_id, or --json")
        sys.exit(1)
