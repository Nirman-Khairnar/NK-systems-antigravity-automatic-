# Quick Start Guide - Agentic N8N Workflow System

## Prerequisites

### 1. Install Python
Download and install Python 3.8+ from https://www.python.org/downloads/

During installation, **CHECK "Add Python to PATH"**

Verify installation:
```powershell
python --version
```

### 2. Install Dependencies
```powershell
cd "d:\Workspace - Demo"
python -m pip install -r requirements.txt
```

### 3. Verify Credentials
Check `.env` file has all API keys:
- ✅ OPENROUTER_API_KEY
- ✅ NOTION_API_KEY
- ✅ NOTION_WORKFLOWS_DB_ID
- ✅ N8N_API_URL
- ✅ N8N_API_KEY

---

## Running the Pipeline

### Full Pipeline (Recommended for First Use)
```powershell
python run_pipeline.py sample_requirements.txt --project-name customer_enrichment
```

This will:
1. Parse requirements → `.tmp/customer_enrichment/requirements.json`
2. Generate workflow → `.tmp/customer_enrichment/workflow.json`
3. Deploy to n8n staging
4. Create Notion documentation

### Step-by-Step (For Learning)

#### Step 1: Parse Requirements
```powershell
python execution/parse_requirements.py sample_requirements.txt
```

Output: `.tmp/requirements.json`

If questions generated: `.tmp/questions.json` - answer these and re-run.

#### Step 2: Generate Workflow
```powershell
python execution/generate_workflow.py .tmp/requirements.json
```

Output: `.tmp/workflow.json` and `.tmp/implementation_notes.md`

#### Step 3: Deploy to n8n
```powershell
python execution/deploy_to_n8n.py .tmp/workflow.json staging
```

Output: `.tmp/deployment_info.json`

**⚠️ CRITICAL**: Go to n8n UI and configure credentials manually!

#### Step 4: (After 24hrs) Analyze Performance
```powershell
python execution/analyze_logs.py
```

Output: `.tmp/performance_report.json` and `.tmp/optimization_suggestions.md`

#### Step 5: Create Documentation
```powershell
python execution/create_notion_docs.py
```

Output: Notion page URL in `.tmp/notion_page_info.json`

---

## Usage Patterns

### For New Client Project
```powershell
# Save client requirements to a file
# Run full pipeline
python run_pipeline.py client_requirements.txt --project-name client_name
```

### Generate Workflow Without Deploying
```powershell
python run_pipeline.py requirements.txt --no-deploy --project-name test_workflow
```

### Deploy Existing Workflow
```powershell
python execution/deploy_to_n8n.py .tmp/existing_project/workflow.json production
```

### Optimize Existing Workflow
```powershell
python execution/analyze_logs.py WORKFLOW_ID 48
# Review suggestions
# Update workflow
python execution/deploy_to_n8n.py .tmp/workflow.json staging
```

---

## Troubleshooting

### "Module not found" errors
```powershell
python -m pip install -r requirements.txt
```

### OpenRouter API errors
- Check API key in `.env`
- Verify free model is available: `google/gemini-2.0-flash-exp:free`
- Check OpenRouter dashboard for usage limits

### n8n deployment fails
- Verify n8n instance is running
- Check API URL and key in `.env`
- Test API manually: `curl <N8N_API_URL>/api/v1/workflows -H "X-N8N-API-KEY: <key>"`

### Notion API errors
- Verify integration has access to database
- Check database ID is correct
- Ensure integration permissions include "Insert content"

### Workflow executions not found
- Ensure workflow was activated in n8n
- Wait for sufficient executions (minimum 10)
- Check workflow ID matches deployment

---

## Understanding the Output

### `.tmp/` Directory Structure
```
.tmp/
  project_name/
    requirements.json           # Structured requirements
    questions.json             # Clarifying questions (if needed)
    workflow.json              # n8n workflow
    implementation_notes.md    # Setup guide
    deployment_info.json       # Deployment details
    performance_report.json    # Metrics (after monitoring)
    optimization_suggestions.md # AI recommendations
    notion_page_info.json      # Notion doc link
```

### Key Files Explained

**requirements.json** - AI-extracted structure:
- workflow_name
- triggers, actions, data_sources
- error_handling strategy
- success metrics

**workflow.json** - Import this to n8n:
- Complete node definitions
- Connections between nodes
- Credential placeholders

**deployment_info.json** - Track deployed workflows:
- workflow_id (use for monitoring)
- environment (staging/production)
- n8n_url

**performance_report.json** - Metrics:
- success_rate_percent
- average_duration_seconds
- error patterns

---

## Next Steps After Installation

1. **Install Python** (if not already)
2. **Install dependencies**: `python -m pip install -r requirements.txt`
3. **Test with sample**: `python run_pipeline.py sample_requirements.txt --project-name test`
4. **Check outputs** in `.tmp/test/`
5. **Visit Notion page** to see documentation

For detailed process, see:
- `directives/` - Step-by-step SOPs
- `implementation_plan.md` - Full system architecture
