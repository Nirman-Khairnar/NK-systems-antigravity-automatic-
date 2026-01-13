# Workflow Generation Directive

## Goal
Convert validated requirements into production-ready n8n workflow JSON.

## Inputs
- `.tmp/requirements.json` - Structured requirements (from previous stage)

## Execution Scripts
- `execution/generate_workflow.py` - Creates n8n workflow JSON

## Process

### 1. Generate Workflow
Run the workflow generator:
```bash
python execution/generate_workflow.py .tmp/requirements.json
```

### 2. Review Outputs
Check generated files:
- `.tmp/workflow.json` - n8n importable JSON
- `.tmp/implementation_notes.md` - Setup instructions

### 3. Validate Workflow Structure
Verify workflow has:
- ✅ Proper trigger node
- ✅ All action nodes configured
- ✅ Error handler nodes
- ✅ Logging nodes (for monitoring)
- ✅ Valid connections (no orphaned nodes)
- ✅ Credential placeholders (not hardcoded)

### 4. Review with User (optional)
If workflow complexity is high, generate visual diagram and request review.

### 5. Gate Criteria
**Do NOT proceed to deployment until:**
- ✅ Workflow JSON is valid n8n format
- ✅ All required nodes present
- ✅ Error handling configured
- ✅ No hardcoded credentials
- ✅ Implementation notes complete

## Outputs
- `.tmp/workflow.json` - Ready for deployment
- `.tmp/implementation_notes.md` - Setup guide
- Gate status: APPROVED

## Edge Cases

### Complex Data Transformations
If requirements involve complex data mapping, AI may generate JavaScript code nodes. Validate syntax before deployment.

### API Rate Limits
If workflow involves high-volume API calls, ensure rate limiting nodes are included.

### Missing n8n Node Types
If AI suggests a node type that doesn't exist in n8n, flag this and propose alternatives.

## Best Practices

### Node Naming
Use descriptive names: "Fetch Customer Data" not "HTTP Request 1"

### Error Handling
Every external API call should have error handler with:
- Retry logic (for transient failures)
- Notification (for persistent failures)
- Fallback behavior

### Logging
Add logging nodes after critical steps for debugging.

## Learnings
*(Updated as system evolves)*

- **2025-12-26**: AI sometimes generates invalid node connections - validate all node names match exactly
- **Schema Validation**: AI often hallucinates node parameters (e.g. `pollTimes` in Google Sheets). Use validated `n8n-nodes-base.manualTrigger` and standard logic nodes (`Switch` v3, `Merge` v3, `If` v2).
- **JSON Syntax**: Ensure all regex and Windows paths are DOUBLE-ESCAPED (`\\\\`) in the JSON string or parsing will fail.
- **Complexity Limit**: For workflows > 15 nodes, LLM generation is unreliable (timeout/syntax errors). Use **Programmatic Generation** (Layer 3 Python scripts) to algorithmically build the JSON instead of relying on AI. This is the "Employee Onboarding" pattern.
