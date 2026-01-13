# Optimization Analysis Directive

## Goal
Analyze workflow performance and iteratively improve based on real execution data.

## Inputs
- Workflow ID (from deployment)
- Monitoring period (default: 24 hours)

## Execution Scripts
- `execution/analyze_logs.py` - Fetches execution data and generates AI recommendations

## Process

### 1. Fetch and Analyze Logs
Run analysis script:
```bash
python execution/analyze_logs.py <workflow_id> 24
```

Or if deployment info exists:
```bash
python execution/analyze_logs.py
```
(Script will auto-load workflow ID from `.tmp/deployment_info.json`)

### 2. Review Performance Report
Check `.tmp/performance_report.json`:
- `success_rate_percent` - Target: >95%
- `average_duration_seconds` - Compare to baseline
- `failed_executions` - Investigate patterns
- `sample_errors` - Common failure reasons

### 3. Review AI Suggestions
Read `.tmp/optimization_suggestions.md` for:
- High priority: Critical fixes (errors, security)
- Medium priority: Performance improvements
- Low priority: Code quality, cleanup

### 4. Prioritize Changes
Focus on:
1. **Errors first**: Fix anything causing failures
2. **Performance**: Reduce slow nodes (API calls, data processing)
3. **Scalability**: Batch operations, add caching

### 5. Implement Improvements
- Update workflow based on suggestions
- Re-run `generate_workflow.py` if major changes
- Or manually edit `.tmp/workflow.json` for minor tweaks

### 6. Redeploy and Monitor
```bash
python execution/deploy_to_n8n.py .tmp/workflow.json staging
```

Wait for another monitoring period and repeat analysis.

### 7. Iteration Exit Criteria
Stop optimizing when:
- ✅ Success rate > 95%
- ✅ No critical errors
- ✅ Performance acceptable for use case
- ✅ Diminishing returns on further optimization

## Outputs
- `.tmp/performance_report.json` - Metrics
- `.tmp/optimization_suggestions.md` - AI recommendations
- Updated workflow (if changes made)
- Gate status: OPTIMIZED (ready for production)

## Edge Cases

### Insufficient Data
If <10 executions, wait longer. Cannot optimize without data.

### Sporadic Errors
If errors are rare (<5%), investigate root cause before optimizing. May be external service issues.

### Performance Regression
If optimization makes performance worse, roll back to previous version.

## Best Practices

### Baseline Metrics
Record initial metrics before optimization for comparison.

### Incremental Changes
Make one optimization at a time. Test each change before adding more.

### Document Changes
Update implementation notes with each optimization round.

## Common Optimizations

### Slow API Calls
- Batch multiple requests into single call
- Add caching layer
- Run calls in parallel (if independent)

### High Error Rate
- Add retry logic with exponential backoff
- Validate inputs before API calls
- Add error notifications

### Resource Usage
- Remove unnecessary data transformations
- Limit data fetched from APIs (pagination)
- Clean up unused nodes

## Learnings
*(Updated as system evolves)*

- **2025-12-26**: Free AI models work well for optimization analysis - no need for expensive models
