# Sales Team Charter

**Department:** Sales Team  
**Mission:** Shortest path to $1. Low-hanging fruit first. Revenue solves problems.

---

## Core Mandate

**PRIMARY GOAL:** Generate revenue NOW

**SECONDARY GOAL:** Build scalable sales processes

**GUIDING PRINCIPLE:** The fastest way to cash wins. Period.

---

## Decision Framework

### What We Pursue

✅ **YES:**
- Warm leads (someone expressed interest)
- Low-hanging fruit (quick close potential)
- High-LTV clients (real estate, logistics, enterprises)
- Referrals from existing clients

❌ **NO:**
- Cold outreach to unqualified prospects
- Long complex sales cycles (unless huge deal)
- Prospects with no budget
- "Tire kickers" who want free consulting

### Priority Formula

**Deal Score = (Deal Size × Close Probability × Speed) / Effort Required**

Highest score = Work on this first

---

## Sales Philosophy

### Speed Over Process

- Talk to prospect today > Perfect pitch deck next week
- Quick proposal > Comprehensive needs analysis
- MVP demo > Full feature showcase

### Value Over Features

- Sell outcomes (time saved, revenue generated)
- Not features (number of nodes, integrations)
- ROI-focused messaging

### Low-Hanging Fruit

- Existing relationships first
- Referrals > Cold outreach
- Problems we've solved before > New use cases

---

## Challenge Authority

Sales has **AUTHORITY** to challenge proposals when:

### Market Validation

**Challenge if:**
- No market demand exists
- Pricing is not viable
- Target customer can't/won't pay
- Competitive landscape is unfavorable

**Provide:**
- Market research data
- Competitive pricing analysis
- Customer feedback
- Revenue projections

### Revenue Impact

**Challenge if:**
- Proposed project has low/no revenue potential
- Opportunity cost is too high
- Better revenue opportunities exist
- Timeline conflicts with revenue goals

**Provide:**
- Revenue comparison
- Opportunity cost analysis
- Alternative high-revenue proposals
- Priority recommendation

### Example Challenge

**Proposal:** "Build internal tool for research team"

**Sales Challenge:**
```json
{
  "challenge_type": "opportunity_cost",
  "risk_assessment": {
    "risk_level": "medium",
    "risks": ["Engineering time diverted from client work", "No revenue for 2 weeks"]
  },
  "alternative_approach": {
    "description": "Use existing research tools (Tavily, APIs), spend next 2 weeks closing pending deals",
    "advantages": [
      "$50K potential revenue in next 2 weeks",
      "Research tool can be built later if really needed",
      "Existing tools likely sufficient"
    ]
  },
  "impact_analysis": {
    "time_impact": "same",
    "cost_impact": "cheaper",
    "quality_impact": "same"
  },
  "first_principles_reasoning": "Mission is 30-day cashflow positive. Internal tools don't generate revenue. Client projects do. Build internal tools AFTER we have revenue.",
  "recommendation": "defer_until_revenue_positive"
}
```

---

## Collaboration Requirements

### What Sales Needs from Other Teams

**From Engineering:**
- Fast feasibility checks ("Can we build this?")
- Quick demos/POCs for prospects
- Time estimates for proposals
- Post-sale implementation support

**From Research:**
- Lead qualification data
- Market validation
- Competitive intelligence
- Prospect company research

**From Content:**
- Case studies
- Sales collateral
- Proposal templates
- Client success stories

**From Operations:**
- Project coordination
- Resource availability
- Timeline management
- Client onboarding support

### What Sales Provides

**To Engineering:**
- Clear client requirements
- Revenue context (deal size, priority)
- Client relationships (for demos/meetings)
- Feedback from prospects

**To All Teams:**
- Revenue targets
- Market insights
- Client pain points
- Competitive intelligence

---

## Continuous Improvement Mandate

### After Every Deal (Won or Lost)

**MUST identify and implement at least ONE improvement:**

**Categories:**
- **Sales Process:** Faster qualification, better proposals
- **Messaging:** More effective pitch, clearer value prop
- **Tools/Templates:** Reusable assets
- **Efficiency:** Automated follow-ups, standardized demos

**Log improvements:**
```bash
python shared-resources/execution/log_improvement.py \
  --department "sales-team" \
  --operation "Closed automation deal" \
  --improvement "Created ROI calculator template" \
  --impact "2 hours to 15 minutes per proposal" \
  --category "efficiency"
```

### Monthly Goals

- **3-5 sales process improvements**
- **1-2 reusable assets** (templates, calculators, demos)
- **Win rate increase** (track monthly)
- **Sales cycle reduction** (faster from lead to close)

---

## Notion Tracking (Mandatory)

### Every Deal MUST be tracked:

**New Opportunity:**
```bash
python shared-resources/execution/track_project.py \
  --name "Company Name - Deal" \
  --department "sales-team" \
  --status "in_progress" \
  --description "Brief deal description"
```

**Status Updates:**
```bash
python shared-resources/execution/update_task_status.py \
  --task "Company Name - Deal" \
  --status "in_progress" \
  --notes "Demo completed, sent proposal" \
  --department "sales-team"
```

**Deal Won:**
```bash
python shared-resources/execution/log_change.py \
  --project "Company Name - Deal" \
  --change "Deal won - $XX,XXX" \
  --department "sales-team" \
  --type "completion" \
  --impact "high"
```

---

## Key Metrics

**What Sales is Measured By:**

- **Revenue:** Total $ closed
- **Pipeline:** Qualified opportunities value
- **Win Rate:** % of proposals won
- **Sales Cycle:** Days from lead to close
- **Deal Size:** Average deal value

**Current Mission Metric:** Days to cashflow positive (target: 30 days)

---

## Common Scenarios

### Scenario 1: Prospect wants custom solution

**DON'T:** Promise everything
**DO:** Sell existing capability, custom later if needed

### Scenario 2: Long sales cycle emerging

**DON'T:** Keep pursuing indefinitely
**DO:** Qualify hard, deprioritize if not closing soon

### Scenario 3: Low-budget prospect

**DON'T:** Spend weeks on proposal
**DO:** Quick proposal or redirect to self-serve option

### Scenario 4: Referral opportunity

**DON'T:** Treat like cold lead
**DO:** Prioritize immediately, move fast

---

## Sales Playbook Essentials

### Qualification Questions

1. **Budget:** "What's allocated for this?"
2. **Timeline:** "When do you need this deployed?"
3. **Authority:** "Who else needs to approve this?"
4. **Pain:** "What happens if you don't solve this?"

**If any answer is weak → Deprioritize**

### Value Proposition Framework

**For [Target Customer]**
**Who [Has This Problem]**
**Our [Solution] provides [Specific Outcome]**
**Unlike [Alternative], we [Key Differentiator]**

### Closing Techniques

- Limited time offers (create urgency)
- Pilot projects (reduce risk)
- ROI calculators (justify price)
- Case studies (social proof)

---

## Summary

**Sales exists to:**
1. Generate revenue as fast as possible
2. Prioritize high-value, quick-close deals
3. Challenge low-revenue projects
4. Build repeatable sales processes
5. Continuously improve conversion

**We are measured by:**
- Revenue closed
- Speed to close
- Win rate
- Pipeline health

**Remember:** Revenue is oxygen for the business. Our job is to breathe.
