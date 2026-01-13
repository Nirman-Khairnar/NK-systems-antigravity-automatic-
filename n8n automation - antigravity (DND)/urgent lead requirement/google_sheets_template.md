# OTWL Shipment Tracker - Google Sheets Template

## Overview
This document describes the structure for the "OTWL Shipment Tracker" Google Sheets workbook that the n8n workflow uses.

---

## Sheet 1: Inquiries

**Purpose**: Track all incoming customer inquiries

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| inquiry_id | Text | Unique identifier | INQ-1735993800000-A3F2 |
| customer_email | Email | Customer's email address | customer@example.com |
| customer_name | Text | Customer's name | John Doe |
| subject | Text | Email subject line | Rate Request - Mumbai to Hamburg |
| received_date | DateTime | When inquiry was received | 2026-01-05T01:30:00Z |
| status | Text | Current status | pending_rates, quoted, nominated |

**Sample Row**:
```
INQ-1735993800000-A3F2 | customer@example.com | ABC Trading Co | Rate Request - JNPT to Rotterdam | 2026-01-04T10:30:00Z | pending_rates
```

---

## Sheet 2: Agent Rates

**Purpose**: Store all rate quotes received from agents

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| inquiry_id | Text | Links to Inquiries sheet | INQ-1735993800000-A3F2 |
| agent_name | Text | Name of the agent | Ocean Freight Ltd |
| ocean_freight_usd | Number | Freight cost in USD | 2450 |
| pol | Text | Port of Loading | JNPT |
| pod | Text | Port of Discharge | Hamburg |
| transit_time_days | Number | Transit time | 28 |
| routing | Text | Shipping line/route | Direct via MSC |
| valid_until | Text | Rate validity date | 2026-01-15 |
| earliest_etd | Text | Earliest departure | 2026-01-10 |
| received_date | DateTime | When rate was received | 2026-01-04T15:20:00Z |

**Sample Row**:
```
INQ-1735993800000-A3F2 | Ocean Freight Ltd | 2450 | JNPT | Hamburg | 28 | Direct via MSC | 2026-01-15 | 2026-01-10 | 2026-01-04T15:20:00Z
```

---

## Sheet 3: Quotations

**Purpose**: Track quotations sent to customers

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| inquiry_id | Text | Links to Inquiries sheet | INQ-1735993800000-A3F2 |
| quote_sent_date | DateTime | When quotation was sent | 2026-01-04T18:00:00Z |
| follow_up_date | DateTime | When to follow up | 2026-01-07T18:00:00Z |
| status | Text | Current status | pending_customer_response, nominated, rejected |

**Sample Row**:
```
INQ-1735993800000-A3F2 | 2026-01-04T18:00:00Z | 2026-01-07T18:00:00Z | pending_customer_response
```

---

## Sheet 4: Agents

**Purpose**: Master list of freight agents

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| agent_name | Text | Company name | Ocean Freight Ltd |
| agent_email | Email | Contact email | quotes@oceanfreight.com |
| region | Text | Coverage area | Asia-Europe |

**Sample Rows**:
```
Ocean Freight Ltd | quotes@oceanfreight.com | Asia-Europe
Global Trans | shipping@globaltrans.in | Asia-Middle East
Sea Bridge Logistics | info@seabridge.com | Global
```

---

## Setup Instructions

### Method 1: Manual Creation

1. Create a new Google Sheets workbook named "OTWL Shipment Tracker"
2. Create 4 sheets with the names above
3. Add the column headers as specified in each table
4. Populate the "Agents" sheet with your actual agent list
5. Share the sheet with the Gmail account used in n8n
6. Copy the Spreadsheet ID from the URL

### Method 2: Template Import (Recommended)

1. Use the provided Google Sheets template link (if available)
2. Make a copy to your Google Drive
3. Update the "Agents" sheet with your actual agents
4. Share with n8n Gmail account

---

## n8n Configuration

After creating the sheet:

1. In n8n, edit each Google Sheets node
2. Authenticate with your Google account
3. Select "OTWL Shipment Tracker" from the dropdown
4. For each node, select the correct sheet name (inquiries, agent_rates, quotations, agents)
5. Save and activate the workflow

---

## Data Flow

```
Customer Email → Inquiries Sheet
                      ↓
                 [inquiry_id generated]
                      ↓
Agent Emails ← Bulk send (from Agents sheet)
                      ↓
Agent Responses → AI Parse → Agent Rates Sheet
                                     ↓
                              [linked by inquiry_id]
                                     ↓
                         Check if 3+ rates received
                                     ↓
                         Generate Quotation → Quotations Sheet
                                     ↓
                              Send to Customer
```

---

## Maintenance

- **Add new agents**: Simply add rows to the "Agents" sheet
- **Archive old inquiries**: Filter by date and move to separate archive sheet
- **Rate validity**: Could add a scheduled workflow to flag expired rates
- **Analytics**: Use Google Sheets formulas/charts to track:
  - Average response time per agent
  - Lowest rates by route
  - Inquiry-to-nomination conversion rate
