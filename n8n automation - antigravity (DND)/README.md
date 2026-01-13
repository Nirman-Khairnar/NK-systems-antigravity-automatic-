# 3-Layer Architecture

This project uses a 3-layer architecture to separate concerns and maximize reliability.

## 🚀 Quick Start

**NEW: Agentic N8N Workflow System**

See [QUICK_START.md](QUICK_START.md) for installation and usage.

Generate complete n8n workflows from natural language:
```powershell
python run_pipeline.py "I need to sync Airtable to Google Sheets daily" --project-name sync_workflow
```

## Architecture Overview

**Layer 1: Directive (What to do)**
- SOPs written in Markdown, stored in `directives/`
- Define goals, inputs, tools/scripts, outputs, and edge cases
- Natural language instructions

**Layer 2: Orchestration (Decision making)**
- The AI agent reads directives and orchestrates execution
- Handles intelligent routing, error handling, and system improvements

**Layer 3: Execution (Doing the work)**
- Deterministic Python scripts in `execution/`
- Handle API calls, data processing, file operations
- Reliable, testable, fast

## Directory Structure

```
.
├── run_pipeline.py      # Master orchestrator for n8n workflows
├── directives/          # SOPs and instruction sets
│   ├── requirements_validation.md
│   ├── workflow_generation.md
│   ├── mvp_deployment.md
│   ├── optimization_analysis.md
│   └── notion_documentation.md
├── execution/           # Python scripts for deterministic tasks
│   ├── parse_requirements.py
│   ├── generate_workflow.py
│   ├── deploy_to_n8n.py
│   ├── analyze_logs.py
│   └── create_notion_docs.py
├── .tmp/               # Temporary/intermediate files (gitignored)
├── .env                # Environment variables (gitignored)
└── sample_requirements.txt  # Example client requirements
```

## Setup Instructions

### 1. Install Python
Download Python 3.8+ from https://www.python.org/downloads/

### 2. Install dependencies
```powershell
python -m pip install -r requirements.txt
```

### 3. Configure API keys
All credentials are already in `.env`:
- OpenRouter API (free Gemini model)
- Notion API + database ID
- n8n API + instance URL

### 4. Run test workflow
```powershell
python run_pipeline.py sample_requirements.txt --project-name test
```

## Operating Principles

1. **Check for tools first** - Before creating new scripts, check `execution/` directory
2. **Self-anneal when things break** - Fix errors, update scripts, improve directives
3. **Update directives as you learn** - Directives are living documents

## File Organization

- **Deliverables**: Google Sheets, Slides, or cloud-based outputs
- **Intermediates**: Temporary files in `.tmp/` (never committed, always regenerated)
