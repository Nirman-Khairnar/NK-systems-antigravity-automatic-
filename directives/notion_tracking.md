# Notion Tracking Protocol

**Applies to:** ALL DEPARTMENTS  
**Mandatory:** YES  
**Last Updated:** 2026-01-13

## Core Principle

**Notion is the single source of truth for all project work.**

If it's not in Notion, it doesn't exist. Period.

---

## When to Update Notion

### ✅ MANDATORY Updates

1. **Starting New Project**
   - Use: `track_project.py`
   - When: Immediately when project begins
   - Creates Notion project page

2. **Status Changes**
   - Use: `update_task_status.py`
   - When: Task moves between states
   - Examples: not_started → in_progress, in_progress → blocked

3. **Hitting Milestones**
   - Use: `log_change.py --type completion`
   - When: Complete significant piece of work
   - Updates activity log

4. **Encountering Blockers**
   - Use: `update_task_status.py --status blocked`
   - When: Work is blocked
   - MUST include notes explaining blocker

5. **Making Significant Changes**
   - Use: `log_change.py --type requirement` or `--type approach`
   - When: Requirements evolve or approach changes
   - Ensures everyone sees current plan, not outdated version

6. **Completing Deliverables**
   - Use: `log_change.py --type completion`
   - When: Final delivery of project/task
   - Marks work as complete

---

## How to Update Notion

### Use Shared Scripts

**Track New Project:**
```bash
python shared-resources/execution/track_project.py \
  --name "Real Estate Lead Automation" \
  --department "engineering-team" \
  --status "in_progress" \
  --description "Building scraper for Australian real estate agents" \
  --team "engineering" "sales"
```

**Update Task Status:**
```bash
python shared-resources/execution/update_task_status.py \
  --task "Real Estate Lead Automation" \
  --status "in_progress" \
  --notes "Completed API integration, starting data processing" \
  --department "engineering-team"
```

**Log Change:**
```bash
python shared-resources/execution/log_change.py \
  --project "Real Estate Lead Automation" \
  --change "Client requested additional data fields" \
  --department "sales-team" \
  --type "requirement" \
  --impact "medium"
```

### Via Notion MCP (If Available)

If Notion MCP is configured, AI Orchestrator can update automatically using MCP tools.

---

## What Gets Tracked

### Project-Level

- **Name**: Clear, descriptive project name
- **Department**: Who owns it
- **Status**: not_started | in_progress | blocked | completed
- **Description**: What we're building/doing
- **Team Members**: Who's involved
- **Last Updated**: Automatic timestamp

### Task-Level

- **Task Name**: Specific work item
- **Status**: Current state
- **Progress Notes**: What's been done
- **Blockers**: What's preventing progress
- **Updated By**: Which department made the change

### Change Log

- **Timestamp**: When change occurred
- **Change Type**: requirement | approach | blocker | completion
- **Description**: What changed
- **Impact**: low | medium | high | critical
- **Department**: Who made the change

---

## Response Time Expectations

### Update Notion Within:

- **Project Start**: Immediately (before writing code)
- **Status Change**: Within 1 hour
- **Blocker Hit**: Immediately (same minute)
- **Milestone Complete**: Within 1 hour
- **Requirement Change**: Immediately (before implementing change)
- **Project Complete**: Within 1 hour

**Why fast updates matter:** NK needs real-time visibility. Delayed updates = NK makes decisions on stale data.

---

## Notion Database Structure

### Projects Database

Required in `.env`:
```
NOTION_PROJECTS_DB_ID=your-database-id
```

**Properties:**
- Name (title)
- Department (select)
- Status (select)
- Team (multi-select)
- Last Updated (date)

### Tasks Database (Optional)

Required in `.env`:
```
NOTION_TASKS_DB_ID=your-database-id
```

**Properties:**
- Name (title)
- Status (select)
- Project (relation to Projects)
- Updated By (text)
- Last Updated (date)

---

## Fallback Mode

If Notion API is unavailable:
- Scripts automatically fallback to local `.tmp/` logging
- Creates JSON files locally
- Logs to `logs/central_activity.log`
- **You MUST manually sync to Notion when API returns**

---

## Examples

### Example 1: Starting Project

```bash
cd "d:/NK systems (antigravity) DND"

python shared-resources/execution/track_project.py \
  --name "OTWL Rate Management Automation" \
  --department "engineering-team" \
  --status "in_progress" \
  --description "Build n8n workflow for tracking shipping rates" \
  --team "engineering" "operations"
```

**Result:** Notion page created with project tracking

### Example 2: Hitting Blocker

```bash
python shared-resources/execution/update_task_status.py \
  --task "OTWL Rate Management Automation" \
  --status "blocked" \
  --notes "Waiting for OTWL API credentials from client" \
  --department "engineering-team"
```

**Result:** Status updated to blocked, NK sees the blocker immediately

### Example 3: Requirement Change

```bash
python shared-resources/execution/log_change.py \
  --project "OTWL Rate Management Automation" \
  --change "Client wants daily reports instead of weekly" \
  --department "sales-team" \
  --type "requirement" \
  --impact "low"
```

**Result:** Change logged in project page, engineering team sees updated requirement

---

## Common Mistakes to Avoid

### ❌ **Updating at End of Day**
Don't: Work all day, update Notion at 5pm
Do: Update as you go, real-time

### ❌ **Vague Updates**
Don't: "Making progress"
Do: "Completed webhook setup, testing with sample data"

### ❌ **Skipping Updates for Small Tasks**
Don't: "It's just a small change, won't update Notion"
Do: Even small changes get logged

### ❌ **Not Logging Blockers**
Don't: Stay stuck for hours without updating status
Do: Hit blocker → Update immediately → Get help

---

## Integration with Workflows

When following `.agent/workflows/`:
- Each workflow step references Notion updates
- Handoffs between departments trigger Notion entries
- Progress tracked automatically

---

## Summary

**The Rule:**
Every time you:
- Start work
- Change status
- Hit blocker
- Make progress
- Change approach
- Complete work

**You update Notion.**

No exceptions. This is how we maintain high-velocity operations with clear communication.
