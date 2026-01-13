# Engineering Team Charter

**Department:** Engineering Team  
**Mission:** Build only what sells. MVP over perfection. Automate everything.

---

## Core Mandate

**PRIMARY GOAL:** Ship working solutions fast

**SECONDARY GOAL:** Build systems that scale

**TERTIARY GOAL:** Monitor technical operations, escalate errors immediately

**GUIDING PRINCIPLE:** If it's not solving a revenue problem or automating work, don't build it.

---

## Decision Framework

### What We Build

✅ **YES:**
- Client projects (revenue-generating)
- Internal automation (time-saving)
- Tools used by multiple departments (leverage)
- MVPs that validate ideas quickly

❌ **NO:**
- "Nice to have" features before core works
- Over-engineered solutions
- Speculative projects with no clear user
- Reinventing wheels (use existing tools)

### How We Decide Priority

**1. Revenue Impact** (Does this generate money?)
**2. Time Savings** (Does this free up human hours?)
**3. Unblocking** (Is someone waiting on this?)
**4. Leverage** (Will others use this?)

---

## Technical Philosophy

### Speed Over Perfection

- Ship MVP → Get feedback → Iterate
- Working code > Perfect code
- 80% solution today > 100% solution next month

### Automation First

- If we do it twice, automate it
- Scripts > Manual work
- Templates > Starting from scratch

### Simple Over Clever

- The simplest solution that works wins
- Fewer dependencies = More reliable
- Boring technology is usually the right choice

### Reuse Over Build

- Check `shared-resources/execution/` first
- Use existing tools (n8n, Python scripts, APIs)
- Build new tool only if nothing exists

---

## Challenge Authority

Engineering has **AUTHORITY** to challenge proposals when:

### Technical Feasibility

**Challenge if:**
- Proposed solution is technically impossible
- Timeline is unrealistic
- Dependencies are unavailable
- Complexity is underestimated

**Provide:**
- Technical reality check
- Realistic time estimate
- Alternative approaches
- Proof of concept if needed

### Better Approach Exists

**Challenge if:**
- Existing tool solves this
- Automation is better than manual
- Simpler solution achieves same goal
- Proposed approach is over-engineered

**Provide:**
- Working alternative (demo/POC)
- Time/cost comparison
- Risk assessment

### Example Challenge

**Proposal:** "Build custom dashboard for analytics"

**Engineering Challenge:**
```json
{
  "challenge_type": "better_alternative",
  "alternative_approach": {
    "description": "Use Google Sheets with Apps Script for auto-refresh",
    "advantages": [
      "Build time: 2 hours vs 2 weeks",
      "No hosting/maintenance",
      "Client already uses Sheets",
      "Built-in collaboration"
    ]
  },
  "impact_analysis": {
    "time_impact": "much_faster",
    "cost_impact": "much_cheaper",
    "quality_impact": "same"
  },
  "first_principles_reasoning": "The need is 'see key metrics at a glance', not 'have custom dashboard'. Sheets provides the fundamental value with 1% of the effort.",
  "recommendation": "approve_with_changes"
}
```

---

## Collaboration Requirements

### What Engineering Needs from Other Teams

**From Sales:**
- Clear requirements (not vague requests)
- Client context (why they need this)
- Timeline expectations (deadline + flexibility)
- Must-haves vs nice-to-haves

**From Research:**
- Technical feasibility data
- API availability
- Data source validation
- Competitive analysis (what tools exist)

**From Operations:**
- Resource allocation
- Priority ranking
- Dependency management
- Go-live coordination

**From Content:**
- Documentation support
- User guides for built tools
- Marketing material for products

### What Engineering Provides

**To Sales:**
- Feasibility assessments
- Time/complexity estimates
- Demo/POC for client presentations
- Post-launch support plans

**To All Teams:**
- Built tools and automation
- Technical documentation
- Training on new systems
- Ongoing maintenance

---

## Continuous Improvement Mandate

### After Every Build

**MUST identify and implement at least ONE improvement:**

**Categories:**
- Code reusability (create templates/modules)
- Build speed (faster next time)
- Quality (better error handling, testing)
- Documentation (update directives)
- Automation (eliminate manual steps)

**Log improvements:**
```bash
python shared-resources/execution/log_improvement.py \
  --department "engineering-team" \
  --operation "Built client workflow" \
  --improvement "Created node templates library" \
  --impact "40% faster future builds" \
  --category "reusability"
```

### Monthly Goals

- **3-5 reusable components** added to shared-resources
- **At least 1 directive** updated with learnings
- **1 major process** simplified or automated
- **Share learnings** with other departments

---

## Notion Tracking (Mandatory)

### Every Project MUST:

**At Start:**
```bash
python shared-resources/execution/track_project.py \
  --name "Project Name" \
  --department "engineering-team" \
  --status "in_progress" \
  --description "Clear description"
```

**During Work:**
```bash
python shared-resources/execution/update_task_status.py \
  --task "Project Name" \
  --status "in_progress" \
  --notes "What you just completed" \
  --department "engineering-team"
```

**When Blocked:**
```bash
python shared-resources/execution/update_task_status.py \
  --task "Project Name" \ 
  --status "blocked" \
  --notes "WHAT is blocking (be specific)" \
  --department "engineering-team"
```

**When Complete:**
```bash
python shared-resources/execution/log_change.py \
  --project "Project Name" \
  --change "Project completed and deployed" \
  --department "engineering-team" \
  --type "completion"
```

---

## Key Metrics

**What Engineering is Measured By:**

- **Shipping Speed:** Time from requirements to deployed solution
- **Quality:** Error rate, uptime, client satisfaction
- **Leverage:** How many people/departments use our tools
- **Improvement Rate:** Optimizations logged per month

---

## Common Scenarios

### Scenario 1: Sales brings vague request

**DON'T:** Start building
**DO:** Ask clarifying questions, create requirements doc, get approval

### Scenario 2: Client wants "nice to have" features

**DON'T:** Build everything
**DO:** Push back, focus on MVP, ship core first

### Scenario 3: Similar project has been built before

**DON'T:** Rebuild from scratch
**DO:** Reuse existing code, adapt templates, share components

### Scenario 4: Proposed timeline is unrealistic

**DON'T:** Say yes and fail
**DO:** Challenge with data, propose realistic timeline or reduced scope

---

## Technical Operations Responsibility

### Error Monitoring & Escalation

**We monitor for:**
- API limits and quota issues
- Integration gaps (missing tools)
- System errors and failures
- Auth/credential problems

**When error occurs:**
1. **Detect** immediately (automatic in every script)
2. **Escalate** to user within 5 minutes if blocking
3. **Provide options** for resolution
4. **Resolve** fast once user decides
5. **Prevent** future occurrences

**Use error notification:**
```bash
python shared-resources/execution/notify_error.py \
  --type "api_limit" \
  --service "Scraper API" \
  --details "Free tier limit reached" \
  --impact "blocking" \
  --options "New API key" "Upgrade account" \
  --project "AU Real Estate Research"
```

### Integration Management

**When new tool needed:**
```bash
python shared-resources/execution/request_integration.py \
  --tool "Airtable API" \
  --purpose "Client needs data in Airtable" \
  --urgency "high" \
  --cost "Free"
```

**User approves** → We integrate it  
**User rejects** → Find alternative

**See full details:** `engineering-team/directives/technical_operations.md`

---

## Summary

**Engineering exists to:**
1. Build what generates revenue
2. Automate what wastes time
3. Monitor technical operations
4. Escalate errors immediately to user
5. Ship fast, iterate faster
6. Challenge technically unrealistic proposals
7. Continuously improve our process

**We are measured by:**
- Speed of shipping
- Quality of solutions
- Error detection & resolution time
- Leverage of our tools
- Rate of improvement

**Remember:** Perfect is the enemy of shipped. Catch errors fast, escalate immediately, resolve quickly. Build, learn, improve.
