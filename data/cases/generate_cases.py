import csv
import os

cases = [
    # VLAN Cases
    {
        "case_id": "VLAN-001",
        "symptom": "PC1 cannot ping PC2. They are on the same switch and same subnet (192.168.10.0/24).",
        "topology_note": "PC1 on Fa0/1, PC2 on Fa0/2. Both should be in VLAN 10.",
        "show_command_outputs": "Switch#show vlan brief\nVLAN Name                             Status    Ports\n---- -------------------------------- --------- -------------------------------\n1    default                          active    Fa0/2, Fa0/3\n10   Sales                            active    Fa0/1",
        "expected_fault": "PC2 is assigned to VLAN 1 instead of VLAN 10.",
        "osi_layer": "Layer 2",
        "concept_tag": "VLAN",
        "severity": "Medium"
    },
    {
        "case_id": "VLAN-002",
        "symptom": "PCs in VLAN 20 cannot reach the router.",
        "topology_note": "Switch is connected to Router via Gi0/1.",
        "show_command_outputs": "Switch#show interfaces trunk\n\nPort        Mode             Encapsulation  Status        Native vlan\n\nSwitch#show interfaces Gi0/1 switchport\nName: Gi0/1\nSwitchport: Enabled\nAdministrative Mode: static access\nOperational Mode: static access\nAccess Mode VLAN: 1 (default)",
        "expected_fault": "Uplink port to router is configured as access mode instead of trunk.",
        "osi_layer": "Layer 2",
        "concept_tag": "VLAN",
        "severity": "High"
    },
    {
        "case_id": "VLAN-003",
        "symptom": "Inter-VLAN routing is failing between VLAN 10 and VLAN 20.",
        "topology_note": "Router-on-a-stick topology. Router Gi0/0 is connected to Switch Gi0/1.",
        "show_command_outputs": "Router#show ip interface brief\nInterface              IP-Address      OK? Method Status                Protocol\nGigabitEthernet0/0     unassigned      YES unset  up                    up\nGigabitEthernet0/0.10  192.168.10.1    YES manual up                    up\nGigabitEthernet0/0.20  192.168.20.1    YES manual up                    up\n\nSwitch#show vlan brief\nVLAN Name                             Status    Ports\n---- -------------------------------- --------- -------------------------------\n1    default                          active    \n10   Sales                            active    Fa0/1",
        "expected_fault": "VLAN 20 is missing from the VLAN database on the switch.",
        "osi_layer": "Layer 2",
        "concept_tag": "VLAN",
        "severity": "Medium"
    },
    {
        "case_id": "VLAN-004",
        "symptom": "CDP errors reported on switch console.",
        "topology_note": "Switch1 Gi0/1 connected to Switch2 Gi0/1 via trunk.",
        "show_command_outputs": "Switch1#show interfaces trunk\nPort        Mode             Encapsulation  Status        Native vlan\nGi0/1       on               802.1q         trunking      99\n\nSwitch2#show interfaces trunk\nPort        Mode             Encapsulation  Status        Native vlan\nGi0/1       on               802.1q         trunking      1",
        "expected_fault": "Native VLAN mismatch on the trunk link.",
        "osi_layer": "Layer 2",
        "concept_tag": "VLAN",
        "severity": "Low"
    },

    # Gateway Cases
    {
        "case_id": "GW-001",
        "symptom": "PC1 can ping other PCs in the same subnet but cannot ping 8.8.8.8.",
        "topology_note": "PC1 is at 10.0.0.10/24, Router gateway is 10.0.0.1.",
        "show_command_outputs": "C:\\>ipconfig\n\nEthernet adapter Ethernet0:\n   IPv4 Address. . . . . . . . . . . : 10.0.0.10\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n   Default Gateway . . . . . . . . . : 10.0.0.2",
        "expected_fault": "Incorrect default gateway configured on PC1.",
        "osi_layer": "Layer 3",
        "concept_tag": "Gateway",
        "severity": "Medium"
    },
    {
        "case_id": "GW-002",
        "symptom": "No hosts in VLAN 30 can access the Internet.",
        "topology_note": "Router provides inter-VLAN routing.",
        "show_command_outputs": "Router#show ip interface brief\nInterface              IP-Address      OK? Method Status                Protocol\nGigabitEthernet0/0.10  192.168.10.1    YES manual up                    up\nGigabitEthernet0/0.30  unassigned      YES unset  up                    up",
        "expected_fault": "Router sub-interface for VLAN 30 is missing an IP address.",
        "osi_layer": "Layer 3",
        "concept_tag": "Gateway",
        "severity": "High"
    },
    {
        "case_id": "GW-003",
        "symptom": "Router cannot ping internet addresses, but LAN works.",
        "topology_note": "Router connected to ISP.",
        "show_command_outputs": "Router#show ip route\nC    192.168.1.0/24 is directly connected, GigabitEthernet0/1\nC    10.0.0.0/30 is directly connected, GigabitEthernet0/0",
        "expected_fault": "Missing default route to the ISP on the router.",
        "osi_layer": "Layer 3",
        "concept_tag": "Gateway",
        "severity": "High"
    },
    {
        "case_id": "GW-004",
        "symptom": "Host can ping gateway IP but cannot reach remote networks.",
        "topology_note": "Host subnet is 172.16.1.0/24. Router LAN is 172.16.1.254.",
        "show_command_outputs": "C:\\>ipconfig\n   IPv4 Address. . . . . . . . . . . : 172.16.1.50\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n   Default Gateway . . . . . . . . . : 0.0.0.0",
        "expected_fault": "Default Gateway missing on the host.",
        "osi_layer": "Layer 3",
        "concept_tag": "Gateway",
        "severity": "Medium"
    },

    # DHCP Cases
    {
        "case_id": "DHCP-001",
        "symptom": "New PCs cannot get an IP address.",
        "topology_note": "Router acts as DHCP server for 192.168.1.0/24. Network has 250 hosts.",
        "show_command_outputs": "Router#show ip dhcp pool\nPool LAN_POOL :\n Utilization mark (high/low)    : 100 / 0\n Subnet size (first/next)       : 0 / 0 \n Total addresses                : 254\n Leased addresses               : 254\n Excluded addresses             : 0",
        "expected_fault": "DHCP pool exhausted.",
        "osi_layer": "Layer 7",
        "concept_tag": "DHCP",
        "severity": "Medium"
    },
    {
        "case_id": "DHCP-002",
        "symptom": "PCs in VLAN 10 receive APIPA (169.254.x.x) addresses.",
        "topology_note": "DHCP server is at 10.1.1.10 in VLAN 100. Router does routing.",
        "show_command_outputs": "Router#show run interface Gi0/0.10\ninterface GigabitEthernet0/0.10\n encapsulation dot1Q 10\n ip address 192.168.10.1 255.255.255.0",
        "expected_fault": "Missing ip helper-address command on the router interface.",
        "osi_layer": "Layer 3",
        "concept_tag": "DHCP",
        "severity": "High"
    },
    {
        "case_id": "DHCP-003",
        "symptom": "DHCP conflict detected in syslog.",
        "topology_note": "Router acts as DHCP server for 10.0.0.0/24. Gateway is 10.0.0.1.",
        "show_command_outputs": "Router#show ip dhcp conflict\nIP address        Detection method   Detection time\n10.0.0.1          Ping               Mar 01 2026 10:00 AM\n\nRouter#show run | inc ip dhcp excluded\nRouter#",
        "expected_fault": "DHCP server is attempting to assign the gateway IP because excluded addresses are not configured.",
        "osi_layer": "Layer 7",
        "concept_tag": "DHCP",
        "severity": "Medium"
    },
    {
        "case_id": "DHCP-004",
        "symptom": "PCs get IP addresses but can't ping PCs above .128 in same network.",
        "topology_note": "Subnet is designed as 192.168.2.0/24.",
        "show_command_outputs": "C:\\>ipconfig\n   IPv4 Address. . . . . . . . . . . : 192.168.2.50\n   Subnet Mask . . . . . . . . . . . : 255.255.255.128\n   Default Gateway . . . . . . . . . : 192.168.2.1",
        "expected_fault": "DHCP pool configured with incorrect subnet mask (/25 instead of /24).",
        "osi_layer": "Layer 3",
        "concept_tag": "DHCP",
        "severity": "Medium"
    },

    # DNS Cases
    {
        "case_id": "DNS-001",
        "symptom": "PC can ping 8.8.8.8 but cannot browse www.google.com.",
        "topology_note": "PC is statically configured.",
        "show_command_outputs": "C:\\>nslookup www.google.com\nDNS request timed out.\n\nC:\\>ipconfig /all\n   IPv4 Address. . . . . . . . . . . : 192.168.1.10\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n   Default Gateway . . . . . . . . . : 192.168.1.1\n   DNS Servers . . . . . . . . . . . : ",
        "expected_fault": "DNS server address is missing in PC IP configuration.",
        "osi_layer": "Layer 7",
        "concept_tag": "DNS",
        "severity": "Medium"
    },
    {
        "case_id": "DNS-002",
        "symptom": "Router cannot ping servers by hostname.",
        "topology_note": "Router is configured with name server 8.8.8.8.",
        "show_command_outputs": "Router#ping server1.cisco.com\nTranslating \"server1.cisco.com\"...domain server (8.8.8.8)\n% Unrecognized host or address, or protocol not running.\n\nRouter#show run | inc ip domain\nno ip domain-lookup",
        "expected_fault": "ip domain-lookup is disabled globally on the router.",
        "osi_layer": "Layer 7",
        "concept_tag": "DNS",
        "severity": "Low"
    },
    {
        "case_id": "DNS-003",
        "symptom": "Hosts receive DHCP properly but cannot resolve names.",
        "topology_note": "Router acts as DHCP. DNS Server is at 8.8.8.8.",
        "show_command_outputs": "Router#show run | sec dhcp pool\nip dhcp pool LAN\n network 10.1.1.0 255.255.255.0\n default-router 10.1.1.1",
        "expected_fault": "DNS server option missing from DHCP pool configuration.",
        "osi_layer": "Layer 7",
        "concept_tag": "DNS",
        "severity": "Medium"
    },

    # Routing Cases
    {
        "case_id": "ROUT-001",
        "symptom": "OSPF neighbor relationship is stuck in EXSTART.",
        "topology_note": "R1 connected to R2 via GigabitEthernet links.",
        "show_command_outputs": "R1#show ip ospf neighbor\nNeighbor ID     Pri   State           Dead Time   Address         Interface\n2.2.2.2           1   EXSTART/BDR     00:00:32    10.0.0.2        GigabitEthernet0/0\n\nR1#show interfaces Gi0/0 | inc MTU\n  MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec,\n\nR2#show interfaces Gi0/0 | inc MTU\n  MTU 1400 bytes, BW 1000000 Kbit, DLY 10 usec,",
        "expected_fault": "MTU mismatch on interfaces participating in OSPF.",
        "osi_layer": "Layer 3",
        "concept_tag": "Routing",
        "severity": "High"
    },
    {
        "case_id": "ROUT-002",
        "symptom": "R1 is not forming an OSPF neighbor relationship with R2.",
        "topology_note": "R1 Gi0/0 (10.0.0.1/30) connected to R2 Gi0/0 (10.0.0.2/30).",
        "show_command_outputs": "R1#show ip ospf interface brief\nInterface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C\n\nR1#show run | sec router ospf\nrouter ospf 1\n network 192.168.1.0 0.0.0.255 area 0",
        "expected_fault": "Missing OSPF network command for the link connecting to R2.",
        "osi_layer": "Layer 3",
        "concept_tag": "Routing",
        "severity": "High"
    },
    {
        "case_id": "ROUT-003",
        "symptom": "EIGRP neighbors flapping continuously.",
        "topology_note": "R1 and R2 connected via WAN link.",
        "show_command_outputs": "R1#show log\n%DUAL-5-NBRCHANGE: EIGRP-IPv4 100: Neighbor 10.1.1.2 (GigabitEthernet0/0) is down: K-value mismatch\n%DUAL-5-NBRCHANGE: EIGRP-IPv4 100: Neighbor 10.1.1.2 (GigabitEthernet0/0) is up: new adjacency",
        "expected_fault": "EIGRP K-values mismatch between routers.",
        "osi_layer": "Layer 3",
        "concept_tag": "Routing",
        "severity": "Medium"
    },
    {
        "case_id": "ROUT-004",
        "symptom": "Static route fails to forward traffic to remote network.",
        "topology_note": "R1 needs to reach 10.5.5.0/24 via next hop 192.168.12.2.",
        "show_command_outputs": "R1#show ip route\nS    10.5.5.0/24 [1/0] via 192.168.12.3\nC    192.168.12.0/24 is directly connected, GigabitEthernet0/0",
        "expected_fault": "Static route is configured with the wrong next-hop IP.",
        "osi_layer": "Layer 3",
        "concept_tag": "Routing",
        "severity": "High"
    },
    {
        "case_id": "ROUT-005",
        "symptom": "R2 is not receiving RIP routes from R1.",
        "topology_note": "R1 and R2 running RIPv2. Connected via Gi0/0.",
        "show_command_outputs": "R1#show run | sec router rip\nrouter rip\n version 2\n passive-interface GigabitEthernet0/0\n network 10.0.0.0\n network 192.168.1.0\n no auto-summary",
        "expected_fault": "Passive-interface is configured on the link connecting to the neighbor.",
        "osi_layer": "Layer 3",
        "concept_tag": "Routing",
        "severity": "Medium"
    },

    # ACL Cases
    {
        "case_id": "ACL-001",
        "symptom": "Users cannot access the internal web server on port 80.",
        "topology_note": "Router applies ACL 100 inward on LAN interface.",
        "show_command_outputs": "Router#show access-lists 100\nExtended IP access list 100\n    10 deny tcp any host 192.168.1.100 eq www (25 matches)\n    20 permit ip any any (500 matches)",
        "expected_fault": "ACL is explicitly denying HTTP traffic to the web server.",
        "osi_layer": "Layer 4",
        "concept_tag": "ACL",
        "severity": "High"
    },
    {
        "case_id": "ACL-002",
        "symptom": "Admin cannot SSH into the router from the management PC.",
        "topology_note": "Management PC is 10.1.1.50.",
        "show_command_outputs": "Router#show run | sec line vty\nline vty 0 4\n access-class 10 in\n login local\n transport input ssh\n\nRouter#show access-lists 10\nStandard IP access list 10\n    10 permit 10.1.1.100",
        "expected_fault": "Access-class ACL does not permit the management PC IP.",
        "osi_layer": "Layer 4",
        "concept_tag": "ACL",
        "severity": "High"
    },
    {
        "case_id": "ACL-003",
        "symptom": "All traffic from VLAN 10 to the Internet is dropped.",
        "topology_note": "ACL 101 applied inbound on VLAN 10 sub-interface.",
        "show_command_outputs": "Router#show access-lists 101\nExtended IP access list 101\n    10 permit tcp 192.168.10.0 0.0.0.255 host 10.0.0.5 eq 443 (20 matches)",
        "expected_fault": "Implicit deny at the end of the ACL blocks all other traffic.",
        "osi_layer": "Layer 3",
        "concept_tag": "ACL",
        "severity": "High"
    },
    {
        "case_id": "ACL-004",
        "symptom": "ACL applied to block telnet, but telnet still works.",
        "topology_note": "ACL 102 applied to Gi0/0.",
        "show_command_outputs": "Router#show run interface Gi0/0\ninterface GigabitEthernet0/0\n ip address 10.0.0.1 255.255.255.0\n ip access-group 102 out\n\nRouter#show access-lists 102\nExtended IP access list 102\n    10 deny tcp any any eq telnet\n    20 permit ip any any",
        "expected_fault": "ACL is applied in the wrong direction (out instead of in).",
        "osi_layer": "Layer 4",
        "concept_tag": "ACL",
        "severity": "Medium"
    },

    # NAT Cases
    {
        "case_id": "NAT-001",
        "symptom": "Internal users cannot browse the internet using NAT overload.",
        "topology_note": "Router Gi0/0 is inside, Gi0/1 is outside connected to ISP.",
        "show_command_outputs": "Router#show run interface Gi0/0\ninterface GigabitEthernet0/0\n ip address 192.168.1.1 255.255.255.0\n\nRouter#show run interface Gi0/1\ninterface GigabitEthernet0/1\n ip address 203.0.113.2 255.255.255.252\n ip nat outside",
        "expected_fault": "The 'ip nat inside' command is missing on the Gi0/0 interface.",
        "osi_layer": "Layer 3",
        "concept_tag": "NAT",
        "severity": "High"
    },
    {
        "case_id": "NAT-002",
        "symptom": "Only one internal user can access the internet at a time.",
        "topology_note": "PAT is intended for the internal network 192.168.1.0/24.",
        "show_command_outputs": "Router#show run | inc ip nat inside source\nip nat inside source list 1 interface GigabitEthernet0/1",
        "expected_fault": "The 'overload' keyword is missing in the NAT statement.",
        "osi_layer": "Layer 4",
        "concept_tag": "NAT",
        "severity": "High"
    },
    {
        "case_id": "NAT-003",
        "symptom": "External users cannot reach the internal web server via public IP.",
        "topology_note": "Web server internal IP is 192.168.1.100. Public IP is 203.0.113.5.",
        "show_command_outputs": "Router#show run | inc ip nat inside source static\nip nat inside source static 192.168.1.10 203.0.113.5",
        "expected_fault": "Static NAT is mapped to the wrong inside local IP (.10 instead of .100).",
        "osi_layer": "Layer 3",
        "concept_tag": "NAT",
        "severity": "High"
    },
    {
        "case_id": "NAT-004",
        "symptom": "NAT translations failing dynamically.",
        "topology_note": "Dynamic NAT pool configured with 5 IPs for a network of 50 users.",
        "show_command_outputs": "Router#show ip nat statistics\nTotal active translations: 5 (0 static, 5 dynamic; 0 extended)\nOutside interfaces:\n  GigabitEthernet0/1\nInside interfaces:\n  GigabitEthernet0/0\nHits: 450  Misses: 250\n\nRouter#show run | inc ip nat inside source\nip nat inside source list 1 pool PUBLIC_IPS",
        "expected_fault": "NAT pool is exhausted and PAT (overload) is not configured.",
        "osi_layer": "Layer 3",
        "concept_tag": "NAT",
        "severity": "Medium"
    },

    # Wireless Cases
    {
        "case_id": "WIFI-001",
        "symptom": "Laptop cannot see or connect to the corporate Wi-Fi.",
        "topology_note": "WLC configured. Laptop is trying to connect to 'CorpNet'.",
        "show_command_outputs": "WLC> show wlan 1\nWLAN Identifier.................................. 1\nProfile Name..................................... Corp_Network\nNetwork Name (SSID).............................. CorpNet_5G\nStatus........................................... Enabled\nMAC Filtering.................................... Disabled",
        "expected_fault": "SSID mismatch (configured as CorpNet_5G, laptop searching for CorpNet).",
        "osi_layer": "Layer 2",
        "concept_tag": "Wireless",
        "severity": "Medium"
    },
    {
        "case_id": "WIFI-002",
        "symptom": "Laptop sees SSID but authentication repeatedly fails.",
        "topology_note": "WPA2-PSK is used for authentication.",
        "show_command_outputs": "Laptop Event Logs:\nTime: 10:05:00 - WLAN AutoConfig failed to connect to network. \nReason: The pre-shared key provided is incorrect.\n\nWLC> show wlan 1\nSecurity Policy.................................. WPA2\nAuthentication Key Management.................... PSK",
        "expected_fault": "Incorrect WPA2 Pre-Shared Key entered on the client.",
        "osi_layer": "Layer 2",
        "concept_tag": "Wireless",
        "severity": "High"
    }
]

# Ensure data directory exists
os.makedirs('c:/Users/ASUS/.gemini/antigravity-ide/scratch/NetSage-AI/data/cases', exist_ok=True)

with open('c:/Users/ASUS/.gemini/antigravity-ide/scratch/NetSage-AI/data/cases/cases.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["case_id", "symptom", "topology_note", "show_command_outputs", "expected_fault", "osi_layer", "concept_tag", "severity"])
    writer.writeheader()
    for case in cases:
        writer.writerow(case)

print("Created cases.csv")
