import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_children(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"Error: {resp.status_code} - {resp.text}")
        return []
    return resp.json().get("results", [])

def get_page_title(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        props = resp.json().get("properties", {})
        # Title property name varies, usually "Name" or "title"
        for key, val in props.items():
            if val["type"] == "title":
                return val["title"][0]["plain_text"] if val["title"] else "Untitled"
    return "Unknown Page"

def explore(block_id, depth=0):
    children = get_children(block_id)
    indent = "  " * depth
    
    for block in children:
        btype = block["type"]
        
        if btype == "child_page":
            title = block["child_page"]["title"]
            print(f"{indent}[PAGE] {title} ({block['id']})")
            explore(block["id"], depth + 1)
            
        elif btype == "child_database":
            title = block["child_database"]["title"]
            print(f"{indent}[DB] {title} ({block['id']})")
            
        elif btype == "column_list":
            # Recurse into columns
            explore(block["id"], depth) 
            
        elif btype == "column":
             explore(block["id"], depth)

# Start exploration
root_id = "27250cd5-29b6-8055-9183-ccd1ea622489"
print(f"Exploring Page: {root_id}")
explore(root_id)
