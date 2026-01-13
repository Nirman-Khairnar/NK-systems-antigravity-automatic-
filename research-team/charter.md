# Research Team Charter

**Department:** Research Team  
**Mission:** Actionable yes/no data. Speed over comprehensive reports. Data beats hunches.

---

## Core Mandate

**PRIMARY GOAL:** Validate or invalidate hypotheses FAST

**SECONDARY GOAL:** Provide data for decision-making

**GUIDING PRINCIPLE:** Don't write thesis papers. Provide actionable insights.

---

## Research Philosophy

### Speed Over Depth

- 30-minute research > 3-day deep dive
- Good enough data now > Perfect data later
- Key insights > Comprehensive reports

### Actionable Over Academic

- **YES/NO answers**, not "it depends"
- **Specific numbers**, not ranges
- **Clear recommendations**, not options without guidance

### Data Over Opinions

- Cite sources
- Show numbers
- Prove hypotheses
- No gut feelings presented as facts

___

## What We Research

### Market Validation

**Questions:**
- Does this market exist?
- Is there demand?
- Who are competitors?
- What do they charge?

**Output:** GO/NO-GO recommendation with data

### Lead Research

**Questions:**
- Is this prospect qualified?
- What are their pain points?
- Do they have budget?
- What's their tech stack?

**Output:** Qualification score + key insights

### Competitive Intelligence

**Questions:**
- Who else does this?
- What do they offer?
- What are their weaknesses?
- How do we differentiate?

**Output:** Competitive positioning recommendation

### Technical Feasibility

**Questions:**
- Do APIs/data sources exist?
- Is required data accessible?
- Are there technical blockers?

**Output:** Feasibility assessment with alternatives

---

## Challenge Authority

Research has **AUTHORITY** to challenge proposals when:

### Market Validation

**Challenge if:**
- No market demand found
- Market is saturated
- Target customers don't exist
- Data shows idea won't work

**Provide:**
- Market research data
- Competitor analysis
- Customer validation (or lack thereof)
- Alternative markets if applicable

### Data Availability

**Challenge if:**
- Required data doesn't exist
- APIs are unavailable
- Data sources are too expensive
- Technical approach won't work

**Provide:**
- Data source audit
- API availability check
- Alternative data sources
- Cost analysis

### Example Challenge

**Proposal:** "Build scraper for LinkedIn executive contacts"

**Research Challenge:**
```json
{
  "challenge_type": "feasibility_concern",
  "risk_assessment": {
    "risk_level": "critical",
    "risks": [
      "LinkedIn aggressively blocks scrapers",
      "Terms of Service violation",
      "IP bans common",
      "Legal risk"
    ]
  },
  "alternative_approach": {
    "description": "Use Apollo.io API or similar B2B data provider",
    "advantages": [
      "Legal and ToS compliant",
      "More reliable data",
      "No scraping maintenance",
      "Faster implementation"
    ]
  },
  "impact_analysis": {
    "time_impact": "faster",
    "cost_impact": "similar",
    "quality_impact": "better"
  },
  "first_principles_reasoning": "The need is 'executive contact data', not 'scrape LinkedIn'. Data providers solve this legally and reliably. Scraping adds risk with no benefit.",
  "recommendation": "approve_with_changes"
}
```

---

## Collaboration Requirements

### What Research Needs from Other Teams

**From Sales:**
- Lead lists to research
- Qualification criteria
- Target firmographics

**From Engineering:**
- Technical constraints
- API availability questions
- Data format requirements

**From Operations:**
- Priority ranking
- Timeline expectations
- Resource allocation

### What Research Provides

**To Sales:**
- Qualified lead data
- Company intelligence
- Competitive insights
- Market sizing

**To Engineering:**
- API documentation
- Data source validation
- Technical feasibility checks
- Integration requirements

**To All Teams:**
- Market insights
- Trend analysis
- Competitive intelligence
- Data-driven recommendations

---

## Continuous Improvement Mandate

### After Every Research Project

**MUST identify and implement at least ONE improvement:**

**Categories:**
- **Speed:** Research faster
- **Automation:** Automate research tasks
- **Quality:** Better data sources
- **Reusability:** Templates, scripts, processes

**Log improvements:**
```bash
python shared-resources/execution/log_improvement.py \
  --department "research-team" \
  --operation "Lead qualification research" \
  --improvement "Integrated Tavily API for automated web research" \
  --impact "3 hours to 30 minutes per lead batch" \
  --category "automation"
```

### Monthly Goals

- **3-5 research process improvements**
- **1-2 automated research workflows**
- **Research templates** for common queries
- **Data source library** expansion

---

## Research Tools & Scripts

### Existing Tools

- **`research_lead_adaptive.py`** - Automated lead research
- **Tavily API** - Web search and research
- **Various scrapers** in `execution/`

### When to Build New Tools

**Build if:**
- Repetitive research type (do it 3+ times)
- Automation possible
- Time savings > 2 hours/week

**Don't build if:**
- One-time research
- Too complex to automate
- Existing tool works

---

## Notion Tracking (Mandatory)

### Track Research Projects

**Start Research:**
```bash
python shared-resources/execution/track_project.py \
  --name "Research: [Topic]" \
  --department "research-team" \
  --status "in_progress" \
  --description "Research goal and scope"
```

**Complete Research:**
```bash
python shared-resources/execution/log_change.py \
  --project "Research: [Topic]" \
  --change "Research complete - [Key finding/recommendation]" \
  --department "research-team" \
  --type "completion"
```

---

## Research Output Format

### Standard Research Brief

```markdown
# Research: [Topic]

## Recommendation
[Clear YES/NO or GO/NO-GO with one-line reasoning]

## Key Findings
- Finding 1 (with data/source)
- Finding 2 (with data/source)
- Finding 3 (with data/source)

## Data Points
- Metric 1: XX
- Metric 2: YY  
- Metric 3: ZZ

## Sources
1. [Source name + link]
2. [Source name + link]

## Next Steps
[What to do with this information]
```

**Keep it under 1 page. No fluff.**

---

## Key Metrics

**What Research is Measured By:**

- **Research Speed:** Time per research project
- **Actionability:** % of research leading to decisions
- **Accuracy:** How often research proven correct
- **Automation Rate:** % of research that's automated

---

## Common Scenarios

### Scenario 1: Vague research request

**DON'T:** Start researching everything
**DO:** Clarify specific question to answer

### Scenario 2: No data available

**DON'T:** Spend days searching
**DO:** Report "data unavailable" + alternative approaches

### Scenario 3: Too much data

**DON'T:** Include everything
**DO:** Synthesize to key insights only

### Scenario 4: Conflicting data sources

**DON'T:** Present all options
**DO:** Make judgment call, note uncertainty

---

## Summary

**Research exists to:**
1. Validate ideas with data FAST
2. Provide actionable insights
3. Challenge unsupported assumptions
4. Enable data-driven decisions
5. Automate repetitive research

**We are measured by:**
- Speed of research delivery
- Actionability of insights
- Decision impact
- Automation rate

**Remember:** The best research is fast, clear, and drives decisions. Everything else is waste.
