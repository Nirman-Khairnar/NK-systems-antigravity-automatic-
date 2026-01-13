# MVP Deployment Directive

## Goal
Deploy workflow MVP to n8n staging environment and begin monitoring.

## Inputs
- `.tmp/workflow.json` - Generated workflow
- Environment: `staging` (default) or `production`

## Execution Scripts
- `execution/deploy_to_n8n.py` - Deploys via n8n API

## Process

### 1. Deploy to Staging
Run deployment script:
```bash
python execution/deploy_to_n8n.py .tmp/workflow.json staging
```

### 2. Review Deployment Info
Check `.tmp/deployment_info.json` for:
- `workflow_id` - Use this for monitoring
- `status` - Should be "active" for staging
- `n8n_url` - Where workflow is deployed

### 3. Manual Credential Configuration
**CRITICAL**: Credentials cannot be automated for security.

In n8n UI:
1. Navigate to deployed workflow
2. Configure each node requiring credentials
3. Test credential connections
4. Save workflow

### 4. Test Execution
Manually trigger workflow:
- If webhook trigger: Send test request
- If schedule trigger: Run manually via n8n UI
- If manual trigger: Execute and verify

Watch execution logs for errors.

### 5. Monitoring Period
Let workflow run for 24-48 hours (or until 10+ executions).

**Do NOT proceed to optimization until sufficient data collected.**

## Outputs
- `.tmp/deployment_info.json` - Deployment details
- Workflow active in n8n
- Minimum 10 executions logged

## Edge Cases

### Deployment Conflicts
If workflow with same name exists:
- Script will UPDATE existing workflow
- Previous version is overwritten
- Consider versioning strategy for production

### Credential Errors
If credentials fail to connect:
- Check API keys are valid
- Verify permissions/scopes
- Test outside n8n first

### Webhook URLs
If using webhook trigger, note the URL from n8n and provide to client.

## Best Practices

### Staging First
**Always deploy to staging before production**, even for simple workflows.

### Test Data
Use non-production data for testing. Never test with live customer data in staging.

### Monitoring
Check n8n execution dashboard daily during monitoring period.

## Learnings
*(Updated as system evolves)*

- **2025-12-26**: n8n API requires exact workflow structure - validate JSON before deployment
- **2025-12-26**: Tags (staging/production) help filter workflows in n8n UI
- **API Constraints**: Creation payload MUST NOT include `active: true` or `tags` (read-only).
- **Update Method**: Use `PUT` (not PATCH) for updating existing workflows.
- **Node Property Sanitization**: Sanitize node properties to allowlist (id, name, type, parameters, etc.) to avoid "additional properties" errors.
