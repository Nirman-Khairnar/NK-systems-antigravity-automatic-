# Deploy n8n Workflow

## Purpose
Deploy n8n workflow JSON files to a running n8n instance via the API.

## Inputs
- Workflow JSON file path
- n8n instance URL (from .env: `N8N_URL`)
- n8n API key (from .env: `N8N_API_KEY`)

## Process

1. **Load workflow JSON**
   - Read the workflow file
   - Validate JSON structure
   - Extract workflow name

2. **Connect to n8n API**
   - Use n8n REST API
   - Endpoint: `POST /workflows`
   - Headers: `X-N8N-API-KEY: {api_key}`

3. **Upload workflow**
   - Send workflow JSON as request body
   - Handle existing workflows (update vs create)
   - Return workflow ID and webhook URLs

4. **Verify deployment**
   - Check workflow appears in n8n
   - Verify all nodes are connected
   - Output webhook URLs for configuration

## Tools & Scripts
- `execution/deploy_n8n_workflow.py` - Python script for deployment

## Expected Outputs
- Workflow ID from n8n
- Webhook URL for Stripe configuration
- Success/failure status
- Any error messages

## Edge Cases
- **Workflow already exists**: Update instead of create
- **Invalid credentials**: Clear error message to check .env
- **Network issues**: Retry with exponential backoff
- **Invalid JSON**: Validate before sending to API

## Environment Variables Required
```
N8N_URL=http://localhost:5678
N8N_API_KEY=your_api_key_here
```

## Example Usage
```bash
cd execution
python deploy_n8n_workflow.py --workflow-file "../payment_onboarding_workflow.json"
```
