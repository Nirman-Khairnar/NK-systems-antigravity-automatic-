#!/usr/bin/env python3
"""
Fetch 15+ reference business n8n workflow templates via RAW URLs.
Bypasses GitHub API rate limits by using direct raw.githubusercontent.com links.
Target: AI Agents, Security/Guardrails, CRM, Sales, Marketing.
"""

import os
import requests
import json
import logging
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

OUTPUT_DIR = "templates"

# Hardcoded list of high-quality templates to verify standards
# These are gathered from known repository structures (Zie619, simealdana, n8n-io)
RAW_URLS = [
    # --- AI AGENTS (Modern n8n 2.0) ---
    # Notion Task Capture (Verified)
    "https://raw.githubusercontent.com/Kris-Turk/ai-stuff/main/n8n_templates/virtual_assistant/Notion_Task_Capture.json",
    
    # --- CRM & SALES (Zie619 - Master Branch Verified) ---
    # Airtable: Create Triggered
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Airtable/0756_Airtable_Create_Triggered.json",
    # HubSpot: Create Contact
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Hubspot/0134_Hubspot_Create_Triggered.json",
    # Pipedrive: Create Deal
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Pipedrive/0139_Pipedrive_Create_Triggered.json",
    # Salesforce: Create Lead
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Salesforce/1089_Salesforce_Create_Triggered.json",
    # Zoho CRM: Create Contact
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Zohocrm/0760_Zohocrm_Create_Triggered.json",

    # --- MARKETING & EMAIL ---
    # ActiveCampaign: Create Contact
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Activecampaign/0057_Activecampaign_Create_Triggered.json",
    # Mailchimp: Add Subscriber
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Mailchimp/0155_Mailchimp_Create_Triggered.json",
    # SendGrid: Send Email
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Sendgrid/0001_Sendgrid_Send_Triggered.json",
    # GetResponse: Create Contact
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Getresponse/0268_Getresponse_Create_Triggered.json",
    
    # --- COMMUNICATION ---
    # Slack: Post Message
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Slack/0168_Slack_Post_Triggered.json",
    # Gmail: Send Email
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Gmail/0001_Gmail_Send_Triggered.json",
    # Telegram: Transfer Message
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Telegram/0004_Telegram_Transfer_Triggered.json",
    # Microsoft Teams: Post Message
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Microsoftteams/0989_Microsoftteams_Post_Triggered.json",

    # --- FINANCE & OPS ---
    # Xero: Create Invoice
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Xero/0458_Xero_Create_Triggered.json",
    # QuickBooks: Create Customer
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Quickbooks/0448_Quickbooks_Create_Triggered.json",
    # Google Sheets: Read Sheet
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Googlesheets/0008_Googlesheets_Read_Triggered.json",
    # Google Calendar: Create Event
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Googlecalendar/0001_Googlecalendar_Create_Triggered.json",
    
    # --- UTILITIES ---
    # AWS S3: Example
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Awss3/0149_Awss3_Wait_Automate_Triggered.json",
    # Postgres: Insert
    "https://raw.githubusercontent.com/Zie619/n8n-workflows/master/workflows/Postgres/1500_Postgres_Create_Triggered.json"
]

def main():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        logger.info(f"Cleaned up {OUTPUT_DIR}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    count = 0
    for url in RAW_URLS:
        try:
            # Construct a nice filename
            name_parts = url.split('/')
            # e.g., "0756_Airtable_Create_Triggered.json" or "Lead_Qualification_AI_Agent.json"
            filename = name_parts[-1].replace("%20", "_")
            if "workflows/" in url:
                # Add category prefix for Zie619 files (e.g. Airtable_...)
                category = name_parts[-2]
                filename = f"{category}_{filename}"
            
            filename = filename.lower()
            
            logger.info(f"Downloading {filename}...")
            r = requests.get(url, timeout=10)
            
            if r.status_code == 200:
                # Verify it is valid JSON
                try:
                    data = r.json()
                    with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                    count += 1
                except json.JSONDecodeError:
                    logger.warning(f"Skipping {filename}: Not valid JSON")
            else:
                logger.warning(f"Failed to fetch {url}: {r.status_code}")
                
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")

    logger.info(f"Successfully downloaded {count} templates.")

if __name__ == "__main__":
    main()
