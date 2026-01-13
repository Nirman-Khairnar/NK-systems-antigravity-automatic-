#!/usr/bin/env python3
"""
Test Notion API connection and configuration.
Diagnoses all potential issues with Notion integration.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print("NOTION INTEGRATION DIAGNOSTIC")
print("="*60)

# Check 1: Environment variables
print("\n1. Environment Variables Check:")
notion_api_key = os.getenv('NOTION_API_KEY')
exec_page_id = os.getenv('NOTION_EXECUTIVE_PAGE_ID')
projects_db_id = os.getenv('NOTION_PROJECTS_DB_ID')
tasks_db_id = os.getenv('NOTION_TASKS_DB_ID')

print(f"   NOTION_API_KEY: {'✓ SET' if notion_api_key else '✗ MISSING'}")
print(f"   NOTION_EXECUTIVE_PAGE_ID: {'✓ ' + exec_page_id if exec_page_id else '✗ MISSING'}")
print(f"   NOTION_PROJECTS_DB_ID: {'✓ ' + projects_db_id if projects_db_id else '✗ MISSING (optional)'}")
print(f"   NOTION_TASKS_DB_ID: {'✓ ' + tasks_db_id if tasks_db_id else '✗ MISSING (optional)'}")

if not notion_api_key:
    print("\n❌ CRITICAL: NOTION_API_KEY is missing!")
    print("   Add to .env: NOTION_API_KEY=your-secret-key")
    sys.exit(1)

# Check 2: notion_client library
print("\n2. Notion Client Library Check:")
try:
    from notion_client import Client
    print("   ✓ notion_client library installed")
except ImportError:
    print("   ✗ notion_client library NOT installed")
    print("   Fix: pip install notion-client")
    sys.exit(1)

# Check 3: API Connection Test
print("\n3. Notion API Connection Test:")
try:
    notion = Client(auth=notion_api_key)
    user = notion.users.me()
    print(f"   ✓ Connected successfully!")
    print(f"   User: {user.get('name', 'Unknown')}")
    print(f"   Type: {user.get('type', 'Unknown')}")
except Exception as e:
    print(f"   ✗ Connection FAILED: {e}")
    print("   Check if your NOTION_API_KEY is valid")
    sys.exit(1)

# Check 4: Executive Page Access
if exec_page_id:
    print("\n4. Executive Dashboard Access Test:")
    try:
        page = notion.pages.retrieve(page_id=exec_page_id)
        page_title = page['properties'].get('title', {})
        if page_title.get('title'):
            title_text = page_title['title'][0]['plain_text']
        else:
            title_text = "No title"
        print(f"   ✓ Can access Executive Dashboard: {title_text}")
    except Exception as e:
        print(f"   ✗ Cannot access page: {e}")
        print(f"   Page ID: {exec_page_id}")
        print("   Make sure the integration has access to this page")
else:
    print("\n4. Executive Dashboard: Not configured yet")

# Check 5: Database Access (if configured)
if projects_db_id:
    print("\n5. Projects Database Access Test:")
    try:
        db = notion.databases.retrieve(database_id=projects_db_id)
        db_title = db.get('title', [{}])[0].get('plain_text', 'Unknown')
        print(f"   ✓ Can access Projects DB: {db_title}")
    except Exception as e:
        print(f"   ✗ Cannot access database: {e}")
else:
    print("\n5. Projects Database: Not configured (optional)")

# Check 6: Write Permission Test
print("\n6. Write Permission Test:")
if exec_page_id:
    try:
        # Try to append a test block
        notion.blocks.children.append(
            block_id=exec_page_id,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": "✓ Notion integration test successful"}}],
                        "color": "green"
                    }
                }
            ]
        )
        print("   ✓ Can write to Executive Dashboard")
    except Exception as e:
        print(f"   ✗ Cannot write: {e}")
        print("   Check integration permissions")
else:
    print("   ⊘ Skipped (no executive page configured)")

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)
