import json

json_path = r"d:\n8n automation - antigravity (DND)\urgent lead requirement\otwl_rate_management_workflow.json"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
print(f"Valid JSON: {len(data['nodes'])} nodes")
print(f"Connection groups: {len(data['connections'])}")
print("\nNodes:")
for node in data['nodes']:
    print(f"  - {node['name']} ({node['type']})")
print("\nConnection Summary:")
for source, targets in data['connections'].items():
    print(f"  {source} -> {list(targets.keys())}")
