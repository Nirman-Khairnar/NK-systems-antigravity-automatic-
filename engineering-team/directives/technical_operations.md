# Technical Operations Monitoring

**Owner:** Engineering Team  
**Purpose:** Catch technical errors, notify user immediately, enable fast resolution

---

## What We Monitor

### 1. API Limits & Quota Issues

**Scenarios:**
- Free scraper account hits limit
- API rate limits exceeded
- Credits/tokens exhausted
- Service quota reached

**Response:**
- Detect immediately
- Notify user with details
- Provide solution options

### 2. Integration Gaps

**Scenarios:**
- New tool/service needed but not integrated
- Existing integration broken
- API changes requiring updates
- New data source required

**Response:**
- Document integration need
- Request user approval
- Implement once approved

### 3. System Errors

**Scenarios:**
- Script failures
- Workflow breaks
- Data pipeline issues
- Credential/auth failures

**Response:**
- Log error details
- Attempt auto-fix if possible
- Escalate to user if blocking

---

## Error Detection

### Automatic Detection

**In Every Script:**
```python
try:
    # Operation
    result = api_call()
except APILimitError as e:
    # Log error
    logger.log(f"API LIMIT HIT: {e}", "ERROR")
    
    # Notify user immediately
    notify_user_error(
        error_type="api_limit",
        service="scraper_service",
        details=str(e),
        impact="blocking",
        options=["Provide new API key", "Upgrade account", "Switch provider"]
    )
```

**Error Categories:**
- `api_limit` - Quota/rate limits
- `integration_missing` - Tool not integrated
- `auth_failure` - Credentials invalid
- `system_error` - Technical failure

### Manual Detection

**When team notices:**
- New tool needed during work
- Current tool insufficient
- Better alternative exists

**Action:**
- Use `request_integration.py` to notify user

---

## Immediate Escalation Protocol

### When to Escalate to User

**IMMEDIATELY (Within 5 minutes):**
- ✅ API limits blocking work
- ✅ Missing integration preventing task
- ✅ Critical error stopping operations
- ✅ Credentials/auth failures

**SAME DAY (Within 4 hours):**
- ⚠️ Non-blocking errors
- ⚠️ Integration improvements (nice-to-have)
- ⚠️ Performance degradation

**NOT URGENT:**
- ℹ️ Minor improvements
- ℹ️ Optional optimizations

### How to Escalate

**Use the error notification script:**
```bash
python shared-resources/execution/notify_error.py \
  --type "api_limit" \
  --service "Scraper API" \
  --details "Free tier limit reached (1000/1000 requests)" \
  --impact "blocking" \
  --options "New API key" "Upgrade account" "Switch to alternative scraper"
```

**Script will:**
1. Log to central log
2. Create Notion alert
3. Use AI `notify_user` tool to escalate immediately
4. Track resolution status

---

## Integration Request Workflow

### When New Tool Needed

**Step 1: Identify Need**
- Team discovers tool during work
- Tool would solve current problem
- Or: Tool would prevent future problems

**Step 2: Request Integration**
```bash
python shared-resources/execution/request_integration.py \
  --tool "Tool Name" \
  --purpose "Why we need it" \
  --alternatives "What we use now" \
  --urgency "blocking|high|medium|low" \
  --cost "Free|$XX/month"
```

**Step 3: User Decides**
- User approves → Engineering integrates
- User rejects → Find alternative
- User defers → Add to backlog

**Step 4: Integrate & Document**
- Add to `.env` if API needed
- Create wrapper script if applicable
- Update relevant directives
- Log completion

---

## Error Notification Format

### To User (via notify_user)

```markdown
## ⚠️ Technical Issue Required Your Attention

**Error Type:** API Limit Reached  
**Service:** Scraper API (free tier)  
**Impact:** BLOCKING - Cannot continue lead research

**Details:**
- Hit 1000/1000 monthly request limit
- 15 days until reset
- Current project blocked: AU Real Estate Lead Research

**Options:**
1. **Provide new API key** (different account) - 5 min setup
2. **Upgrade to paid tier** ($49/month, 10K requests) - Today
3. **Switch to alternative** (ScraperAPI or Bright Data) - 2 hour setup

**Recommendation:** Option 1 (fastest) or Option 2 (permanent solution)

**Your decision?**
```

### To Notion

Create alert block in project page:
- 🔴 Critical error callout
- Error details
- Impact assessment
- Resolution options
- Status tracking

---

## Error Resolution Tracking

### Track Every Error

**When Error Occurs:**
```bash
python shared-resources/execution/track_error.py \
  --error-type "api_limit" \
  --service "Scraper API" \
  --project "AU Real Estate Research" \
  --impact "blocking" \
  --status "escalated"
```

**When User Responds:**
```bash
python shared-resources/execution/update_error.py \
  --error-id "error-123" \
  --status "resolved" \
  --solution "User provided new API key" \
  --resolution-time "15min"
```

**Metrics Tracked:**
- Error frequency
- Resolution time
- User response time
- Most common issues

---

## Prevention & Learning

### After Every Error

**MUST document:**
1. What caused it
2. How we detected it
3. How we resolved it
4. How to prevent next time

**Improvement Actions:**
- Add monitoring if not detected automatically
- Create fallback if possible
- Update documentation
- Share learnings with team

**Example Improvement:**
```bash
python shared-resources/execution/log_improvement.py \
  --department "engineering-team" \
  --operation "Handled API limit error" \
  --improvement "Added proactive limit monitoring (alert at 80%)" \
  --impact "Future errors caught before blocking work" \
  --category "automation"
```

---

## Common Scenarios

### Scenario 1: API Limit Hit

**Detection:**
```python
if remaining_requests < 10:
    notify_user_error(
        error_type="api_limit_warning",
        service="Scraper API",
        details=f"Only {remaining_requests} requests remaining",
        impact="warning",
        options=["Prepare backup API", "Reduce usage", "Upgrade account"]
    )
```

**User Options:**
1. Provide new API → Engineering switches
2. Upgrade account → Engineering updates credentials
3. Reduce usage → Engineering optimizes

### Scenario 2: New Integration Needed

**Team discovers:** "We need Airtable integration for client project"

**Action:**
```bash
python shared-resources/execution/request_integration.py \
  --tool "Airtable API" \
  --purpose "Client needs data in Airtable, we need to write records" \
  --alternatives "Currently manual CSV export" \
  --urgency "high" \
  --cost "Free (included in client's plan)"
```

**User decides:** "Approved - integrate it"

**Engineering:**
1. Get Airtable API key from user
2. Create wrapper script
3. Test integration
4. Update documentation
5. Mark complete

### Scenario 3: Auth Failure

**Detection:** Google Sheets API returns 401

**Immediate Fix Attempt:**
1. Check token expiry → Refresh if possible
2. Check credentials → Alert if invalid

**If unfixable:**
```bash
python shared-resources/execution/notify_error.py \
  --type "auth_failure" \
  --service "Google Sheets API" \
  --details "Token expired, refresh failed" \
  --impact "blocking" \
  --options "Re-authenticate Google account"
```

---

## Integration Management

### Current Integrations Inventory

**Maintain list in:**
`engineering-team/integrations.md`

**Track:**
- Service name
- API type (free/paid tier)
- Limits (requests/day, quotas)
- Credentials location
- Usage monitoring
- Backup options

### Proactive Monitoring

**Weekly Check:**
- API usage vs limits
- Approaching quotas
- Expiring credentials
- Service health

**Monthly Review:**
- Underutilized services (can we downgrade?)
- Missing integrations (should we add?)
- Better alternatives available?

---

## Summary

**Technical Operations means:**
1. **Monitor** for errors continuously
2. **Detect** issues before they block
3. **Escalate** immediately to user
4. **Resolve** fast once user decides
5. **Prevent** future occurrences
6. **Learn** from every error

**Key Principles:**
- Speed: Notify user within 5 minutes of blocking error
- Clarity: User gets options, not just problems
- Resolution tracking: Measure fix time
- Prevention: Learn and improve

**This keeps operations smooth and fast - exactly Elon-style.**
