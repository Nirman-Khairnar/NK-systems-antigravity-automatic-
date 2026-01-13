#!/usr/bin/env python3
"""
Create OTWL Shipment Tracker Google Spreadsheet

This script creates a Google Sheets workbook with 4 sheets:
1. inquiries - Customer inquiry tracking
2. agent_rates - Rate quotes from agents
3. quotations - Quotation tracking
4. agents - Master agent list

Requirements:
- Google Sheets API enabled
- credentials.json in project root
- gspread and oauth2client packages
"""

import os
import sys
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_otwl_tracker():
    """Create the OTWL Shipment Tracker spreadsheet."""
    
    # Use credentials from project root
    creds_path = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
    
    # Check if credentials exist
    if not os.path.exists(creds_path):
        print("ERROR: credentials.json not found!")
        print("Please place your Google API credentials.json in the project root.")
        print("\nTo get credentials:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Enable Google Sheets API")
        print("3. Create credentials (OAuth 2.0 or Service Account)")
        print("4. Download as credentials.json")
        return None
    
    try:
        # Load credentials
        creds = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        service = build('sheets', 'v4', credentials=creds)
        
        # Create new spreadsheet
        spreadsheet = {
            'properties': {
                'title': 'OTWL Shipment Tracker'
            },
            'sheets': [
                {
                    'properties': {
                        'title': 'inquiries',
                        'gridProperties': {
                            'frozenRowCount': 1
                        }
                    }
                },
                {
                    'properties': {
                        'title': 'agent_rates',
                        'gridProperties': {
                            'frozenRowCount': 1
                        }
                    }
                },
                {
                    'properties': {
                        'title': 'quotations',
                        'gridProperties': {
                            'frozenRowCount': 1
                        }
                    }
                },
                {
                    'properties': {
                        'title': 'agents',
                        'gridProperties': {
                            'frozenRowCount': 1
                        }
                    }
                }
            ]
        }
        
        spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
        spreadsheet_id = spreadsheet['spreadsheetId']
        
        print(f"SUCCESS: Created spreadsheet!")
        print(f"Spreadsheet ID: {spreadsheet_id}")
        print(f"URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
        
        # Add headers to each sheet
        requests = []
        
        # Inquiries headers
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': spreadsheet['sheets'][0]['properties']['sheetId'],
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'rows': [{
                    'values': [
                        {'userEnteredValue': {'stringValue': 'inquiry_id'}},
                        {'userEnteredValue': {'stringValue': 'customer_email'}},
                        {'userEnteredValue': {'stringValue': 'customer_name'}},
                        {'userEnteredValue': {'stringValue': 'subject'}},
                        {'userEnteredValue': {'stringValue': 'received_date'}},
                        {'userEnteredValue': {'stringValue': 'status'}}
                    ]
                }],
                'fields': 'userEnteredValue'
            }
        })
        
        # Agent Rates headers
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': spreadsheet['sheets'][1]['properties']['sheetId'],
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'rows': [{
                    'values': [
                        {'userEnteredValue': {'stringValue': 'inquiry_id'}},
                        {'userEnteredValue': {'stringValue': 'agent_name'}},
                        {'userEnteredValue': {'stringValue': 'ocean_freight_usd'}},
                        {'userEnteredValue': {'stringValue': 'pol'}},
                        {'userEnteredValue': {'stringValue': 'pod'}},
                        {'userEnteredValue': {'stringValue': 'transit_time_days'}},
                        {'userEnteredValue': {'stringValue': 'routing'}},
                        {'userEnteredValue': {'stringValue': 'valid_until'}},
                        {'userEnteredValue': {'stringValue': 'earliest_etd'}},
                        {'userEnteredValue': {'stringValue': 'received_date'}}
                    ]
                }],
                'fields': 'userEnteredValue'
            }
        })
        
        # Quotations headers
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': spreadsheet['sheets'][2]['properties']['sheetId'],
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'rows': [{
                    'values': [
                        {'userEnteredValue': {'stringValue': 'inquiry_id'}},
                        {'userEnteredValue': {'stringValue': 'quote_sent_date'}},
                        {'userEnteredValue': {'stringValue': 'status'}}
                    ]
                }],
                'fields': 'userEnteredValue'
            }
        })
        
        # Agents headers + sample data
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': spreadsheet['sheets'][3]['properties']['sheetId'],
                    'startRowIndex': 0,
                    'endRowIndex': 4
                },
                'rows': [
                    {
                        'values': [
                            {'userEnteredValue': {'stringValue': 'agent_name'}},
                            {'userEnteredValue': {'stringValue': 'agent_email'}},
                            {'userEnteredValue': {'stringValue': 'region'}}
                        ]
                    },
                    {
                        'values': [
                            {'userEnteredValue': {'stringValue': 'Ocean Freight Ltd'}},
                            {'userEnteredValue': {'stringValue': 'quotes@oceanfreight.com'}},
                            {'userEnteredValue': {'stringValue': 'Asia-Europe'}}
                        ]
                    },
                    {
                        'values': [
                            {'userEnteredValue': {'stringValue': 'Global Trans'}},
                            {'userEnteredValue': {'stringValue': 'shipping@globaltrans.in'}},
                            {'userEnteredValue': {'stringValue': 'Asia-Middle East'}}
                        ]
                    },
                    {
                        'values': [
                            {'userEnteredValue': {'stringValue': 'Sea Bridge Logistics'}},
                            {'userEnteredValue': {'stringValue': 'info@seabridge.com'}},
                            {'userEnteredValue': {'stringValue': 'Global'}}
                        ]
                    }
                ],
                'fields': 'userEnteredValue'
            }
        })
        
        # Execute all requests
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()
        
        print("\nHeaders and sample agents added!")
        print("\nNext steps:")
        print("1. Update the 'agents' sheet with your real agent contacts")
        print("2. Share this spreadsheet with your n8n Gmail account")
        print("3. Use this Spreadsheet ID in your n8n workflow")
        
        return spreadsheet_id
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    create_otwl_tracker()
