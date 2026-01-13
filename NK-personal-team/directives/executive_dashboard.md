# NK Executive Dashboard - Daily Briefs & Reports

**Owner:** NK-Personal-Team (Chief of Staff)  
**Purpose:** Deliver daily briefs, weekly reports, and strategic reviews directly in Notion

---

## Notion Integration

### Executive Dashboard Location

**Page:** `Sellatica OS (updated)` → `NK Executive Dashboard`  
**Page ID:** To be created (set in `.env` as `NOTION_EXECUTIVE_PAGE_ID`)

---

## Daily Deliverables

### 1. Morning Brief (Every Day at 6 AM)

**Generated automatically via:**
```bash
python NK-personal-team/execution/generate_daily_brief.py
```

**Contains:**
- 🎯 **Top 3 Priorities** (checkboxes) - Pulled from tasks, filtered by Tier 1-2
- 📆 **Meetings Today** - Your calendar for the day
- ⚡ **Decisions Needed** - Escalated from teams (NK-only decisions)
- 👥 **Team Updates Summary** - 1-line status from each department
- 💡 **Focus Recommendation** - Best deep work time block

**Format:** Appended to Executive Dashboard as dated section

---

### 2. Weekly Report (Every Monday at 6 AM)

**Generated automatically via:**
```bash
python NK-personal-team/execution/generate_weekly_report.py
```

**Contains:**
- 📊 **Week Ahead Plan**
  - Key goals for the week
  - Critical meetings/deadlines
  - Resource allocation
  
- 📈 **Last Week Review**
  - What shipped
  - Wins (revenue, progress, achievements)
  - Misses (what didn't happen, why)
  - Productivity score (Tier 1-2 time %)
  
- 🚀 **Brand Activity**
  - LinkedIn/Twitter engagement
  - Network growth
  - Speaking/writing opportunities
  
- ⚙️ **System Improvements**
  - Process optimizations logged
  - Tools added/improved
  - Team velocity changes

**Format:** Separate weekly page linked from dashboard

---

### 3. Monthly Strategic Review (1st of Month)

**Generated automatically via:**
```bash
python NK-personal-team/execution/generate_monthly_review.py
```

**Contains:**
- 🎯 **Goal Progress** - 30-day cashflow + strategic objectives
- 💰 **Revenue Report** - Closed deals, pipeline, projections
- 📊 **Personal Brand Metrics** - Reach, influence, opportunities
- ⚡ **Energy & Life Balance** - Sustainability check
- 🔄 **Strategic Adjustments** - What to change based on data
- 📚 **Learning Progress** - Skills developed, knowledge gained

**Format:** Comprehensive monthly review page

---

## Setup Instructions

### Step 1: Create Executive Dashboard in Notion

**Manual (One-time):**
1. Go to "Sellatica OS (updated)" page
2. Add new page: "NK Executive Dashboard"
3. Copy page ID from URL
4. Add to `.env`: `NOTION_EXECUTIVE_PAGE_ID=your-page-id`

**OR Use Script:**
```bash
python NK-personal-team/execution/setup_executive_dashboard.py
```

This creates:
- Main dashboard page
- Daily briefs section
- Weekly reports section
- Monthly reviews section
- Quick links to all databases

---

### Step 2: Configure Environment

**Add to `.env`:**
```
NOTION_EXECUTIVE_PAGE_ID=your-executive-dashboard-page-id
```

---

### Step 3: Automate Daily/Weekly/Monthly Generation

**Option A: Manual Generation**
```bash
# Daily (run each morning)
python NK-personal-team/execution/generate_daily_brief.py

# Weekly (run Monday mornings)
python NK-personal-team/execution/generate_weekly_report.py

# Monthly (run 1st of month)
python NK-personal-team/execution/generate_monthly_review.py
```

**Option B: Automated (Recommended)**

**Windows Task Scheduler:**
1. Daily brief at 6 AM
2. Weekly report at 6 AM Mondays
3. Monthly review at 6 AM on 1st

**OR n8n Workflow:**
Create scheduled workflows that run these scripts

---

## What Gets Tracked

### Data Sources (Auto-pulled from Notion)

**From Various Databases:**
- Tasks → Top 3 priorities
- Projects → Status updates
- CRM/Prospects → Sales pipeline
- Team activity logs → Updates summary

**Filtering Logic:**

**Daily Brief:**
- Only Tier 1-2 priorities
- Only NK-needed decisions
- Only high-value meetings

**Weekly Report:**
- Revenue activities
- Strategic initiatives
- Brand building actions
- System improvements

**Monthly Review:**
- Long-term goal progress
- Strategic metrics
- Personal development

---

## Intelligence Layer

**NK-Personal-Team acts as filter:**

### What Reaches NK in Briefs

✅ Decisions only NK can make  
✅ High-value opportunities  
✅ Revenue-critical items  
✅ Strategic challenges  

### What Doesn't Reach NK

❌ Team can handle themselves  
❌ Low-priority requests  
❌ Automated progress updates (unless blocked)  
❌ Tier 3-4 work  

**Filter = 90% of noise, surface 10% of signal**

---

## Brief Evolution

**Briefs improve over time:**

1. **Week 1-2:** Manual template, basic structure
2. **Week 3-4:** Auto-pull from Notion databases
3. **Month 2:** Smart filtering (ML-based priority detection)
4. **Month 3+:** Predictive insights, trend analysis

**Continuous improvement mandate applies to briefs themselves.**

---

## Metrics

**Track brief effectiveness:**

- **NK Time Saved:** Minutes saved in daily planning
- **Decision Quality:** % of decisions in brief that NK acts on
- **Accuracy:** % of priorities identified correctly
- **Focus Time:** % of day spent on Tier 1-2 (target: 80%+)

---

## Example Daily Brief (In Notion)

```markdown
# 📅 Daily Brief - Monday, January 13, 2026

## 🎯 Top 3 Priorities

☐ **Close deal with Prospect X** (Sales - $25K opportunity)
☐ **Review & approve Client Y automation** (Engineering escalation)
☐ **Post LinkedIn thought leadership** (Brand - 30 min)

## 📆 Meetings Today

- 10:00 AM: Sales call with Prospect X (60 min)
- 2:00 PM: Client Y approval meeting (30 min)

## ⚡ Decisions Needed

- **Engineering:** Approve Airtable integration request (5 min decision)
- **Sales:** Which of 3 warm leads to prioritize this week

## 👥 Team Updates

- **Sales:** 2 warm leads, Prospect X ready to close
- **Engineering:** Client Y project 90% done, needs approval
- **Research:** Market validation complete for Product Z
- **Operations:** All teams on track, no blockers

💡 **Focus Recommendation:** Deep work block 3-5 PM - No meetings, focus on strategic planning

---
```

**This appears in your Sellatica OS automatically every morning at 6 AM.**

---

## Summary

**Deliverables automated in Notion:**
- ✅ Daily briefs (6 AM daily)
- ✅ Weekly reports (6 AM Mondays)
- ✅ Monthly reviews (6 AM on 1st)

**All appear in your Executive Dashboard in Sellatica OS.**

**Chief of Staff function = Filter everything → Surface only what matters → Deliver it where you work.**
