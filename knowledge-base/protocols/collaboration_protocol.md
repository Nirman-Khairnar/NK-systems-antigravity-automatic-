# Collaboration Protocol

**Version:** 1.0  
**Last Updated:** 2026-01-13

## Purpose

This protocol defines HOW departments communicate, challenge ideas, and collaborate in our high-velocity organization. We operate like an Elon Musk company: fast, first-principles driven, zero bureaucracy.

---

## Core Principles

### 1. **Challenge Everything**
Every department has the **DUTY** to challenge proposals if they see:
- A better approach
- Hidden risks
- Inefficiencies
- Assumptions that need validation

**Challenging is not insubordination. It's your job.**

### 2. **First Principles Thinking**
Don't say "we've always done it this way." Ask:
- What problem are we REALLY solving?
- What's the simplest solution?
- Can we eliminate steps entirely?

### 3. **Speed Over Perfection**
- Quick feedback > Perfect analysis
- Working prototype > Comprehensive specs
- Ship and iterate > Wait for perfect

### 4. **Data Over Opinions**
Back your challenge with:
- Research findings
- Time/cost estimates
- Technical constraints
- Market data

---

## Communication Standards

### Request Format

When one department needs something from another:

```json
{
  "from": "sales-team",
  "to": "content-team",
  "request_type": "case_study",
  "description": "Need client success story for real estate automation",
  "deadline": "2026-01-15",
  "priority": "high",
  "context": "Closing deal with similar prospect"
}
```

### Response Format

Use the existing `standard_response.schema.json`:
```json
{
  "status": "success" | "error" | "pending",
  "data": { ... },
  "message": "Human-readable response",
  "source_department": "content-team",
  "timestamp": "2026-01-13T15:10:00Z"
}
```

### Response Time Expectations

- **Urgent**: 2 hours
- **High**: Same day
- **Medium**: 24 hours
- **Low**: 48 hours

**If you can't meet the deadline, respond IMMEDIATELY with why and new ETA.**

---

## Challenge Protocol

### When to Challenge

Submit a challenge when:
1. **Risk Identified**: Proposal has technical, market, or execution risks
2. **Better Alternative**: You know a faster/cheaper/better way
3. **Optimization**: Proposal works but can be improved
4. **Feasibility Concern**: Technically/operationally not viable
5. **Need Clarification**: Requirements unclear

### How to Challenge

**Use the `challenge_schema.json` format:**

```json
{
  "challenge_id": "unique-id",
  "proposal_id": "ref-to-proposal",
  "department": "engineering-team",
  "challenge_type": "better_alternative",
  "risk_assessment": {
    "risk_level": "medium",
    "risks": ["Manual process will take 40hrs/week"]
  },
  "alternative_approach": {
    "description": "Build n8n automation instead",
    "advantages": ["90% time savings", "Scalable", "Can deploy in 2 days"]
  },
  "impact_analysis": {
    "time_impact": "much_faster",
    "cost_impact": "same",
    "quality_impact": "better"
  },
  "first_principles_reasoning": "The problem is repetitive data entry. Humans are bad at repetitive tasks. Automation is the right tool.",
  "recommendation": "approve_with_changes",
  "confidence_level": "very_high"
}
```

### Challenge Escalation

1. **Normal**: Department challenges, Orchestrator synthesizes
2. **Conflict**: Two departments disagree → Operations facilitates
3. **Critical**: High-risk proposal → Escalate to user immediately

---

## Cross-Team Workflows

### Multi-Department Projects

When a project requires multiple teams:

1. **Operations Team** creates coordination workflow
2. **Each department** owns their piece
3. **Dependencies** are explicitly mapped
4. **Handoffs** use standard schemas
5. **Notion** tracks everything centrally

### Data Handoffs

When passing data between departments:

**Research → Sales:** Use structured lead format
```json
{
  "lead_id": "...",
  "company": "...",
  "qualification_score": 8,
  "pain_points": [...],
  "recommended_approach": "..."
}
```

**Sales → Engineering:** Use requirements format
```json
{
  "client": "...",
  "requirements": [...],
  "deadline": "...",
  "must_haves": [...],
  "nice_to_haves": [...]
}
```

**No custom formats unless absolutely necessary. Reuse existing schemas.**

---

## Notion Integration

### MANDATORY: Track Everything in Notion

Every department MUST update Notion when:
- ✅ Starting new project
- ✅ Hitting milestones  
- ✅ Encountering blockers
- ✅ Making significant changes
- ✅ Completing deliverables

**Use shared scripts:**
- `track_project.py` - Create/update project pages
- `update_task_status.py` - Real-time status updates
- `log_change.py` - Log all changes

**Why?** Notion is the single source of truth. If it's not in Notion, it doesn't exist.

---

## Decision-Making Framework

### Quick Decisions (< $100, < 1 day work)
- Department decides
- Log in Notion
- Move fast

### Medium Decisions (< $1000, < 1 week work)
- Orchestrator evaluates
- Relevant departments challenge
- Synthesize best approach
- Execute

### Major Decisions (> $1000, > 1 week work)
- Full department review
- Present options to user
- User decides
- Document in Notion

---

## Failure Modes to Avoid

### ❌ **Analysis Paralysis**
Don't: Spend 3 days researching before starting
Do: Spend 30 mins, make decision, iterate

### ❌ **Silent Disagreement**
Don't: Think "this won't work" but stay silent
Do: Submit challenge immediately

### ❌ **Building in Silos**
Don't: Build without checking if others need input
Do: Quick check with operations before starting

### ❌ **Outdated Documentation**
Don't: Finish project, forget to update Notion
Do: Update Notion as you go

---

## Examples

### Example 1: Good Challenge

**Proposal:** "Manually research 100 leads"

**Engineering Challenge:**
```json
{
  "challenge_type": "better_alternative",
  "alternative_approach": {
    "description": "Use research_lead_adaptive.py script - automated",
    "advantages": ["2-3 min per lead vs 20-30 min manual", "Consistent quality", "Can run overnight"]
  },
  "impact_analysis": {
    "time_impact": "much_faster",
    "cost_impact": "much_cheaper"
  },
  "first_principles_reasoning": "Research is data aggregation. Scripts aggregate data faster than humans.",
  "recommendation": "approve_with_changes"
}
```

**Result:** Proposal improved, time saved

### Example 2: Good Cross-Team Workflow

**Project:** Launch real estate lead gen campaign

**Flow:**
1. Research: Validate market → Create target list
2. Content: Write messaging → Create templates  
3. Engineering: Build scraper → Set up automation
4. Sales: Define follow-up process → Create sequences
5. Operations: Coordinate launches → Track metrics

**Each team:**
- Uses shared Notion project page
- Updates status real-time
- Logs blockers immediately
- Hands off using standard formats

---

## Summary

**This is how we work:**
- Challenge ideas fearlessly
- Think from first principles
- Move fast, iterate
- Use data, not opinions
- Track everything in Notion
- Zero bureaucracy

**If a rule slows you down, challenge it.**
