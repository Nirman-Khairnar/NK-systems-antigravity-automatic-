import json

# Validate the generated workflow JSON
json_path = r"d:\n8n automation - antigravity (DND)\urgent lead requirement\rate_sourcing_demo_workflow.json"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
print(f"Valid JSON: {len(data['nodes'])} nodes, {len(data['connections'])} connection groups")
print("\nNodes:")
for node in data['nodes']:
    print(f"  - {node['name']} ({node['type']})")
print("\nConnections:")
for source, targets in data['connections'].items():
    print(f"  - {source}: {list(targets.keys())}")
