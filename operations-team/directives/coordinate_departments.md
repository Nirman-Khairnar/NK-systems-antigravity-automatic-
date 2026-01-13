# Coordinate Departments

**When to use:** Multi-team projects requiring coordination across departments

**Goal:** Enable smooth cross-department collaboration with zero friction

---

## When This Directive Applies

Use this when:
- Project involves 2+ departments
- Clear dependencies exist between teams
- Handoffs are required
- Timeline coordination needed

---

## Process

### Step 1: Map the Project

**Actions:**
1. Identify all teams involved
2. Map dependencies (who needs what from whom)
3. Identify handoff points
4. Spot potential bottlenecks

**Output:** Dependency map (can be simple list or diagram)

**Example:**
```
Project: Real Estate Lead Automation

Teams Involved:
- Research (validate market)
- Engineering (build scraper)
- Sales (define criteria)
- Operations (coordinate)

Dependencies:
1. Sales → Research: Target criteria
2. Research → Engineering: Data sources validated
3. Engineering → Sales: Scraper built, demo ready
4. All → Operations: Status updates

Potential Bottlenecks:
- Research data source validation (could take time)
- Engineering resource availability
```

### Step 2: Create Timeline

**Actions:**
1. Get time estimates from each team
2. Add buffer for handoffs (20% minimum)
3. Identify parallel work opportunities
4. Set milestones

**Output:** Timeline with clear milestones and handoffs

**Example:**
```
Week 1:
- Sales: Define criteria (Day 1-2)
- Research: Validate market + data sources (Day 1-5) [PARALLEL]

Week 2:
- Engineering: Build scraper (Day 6-12)
- HANDOFF: Day 12 - Demo to Sales

Week 3:
- Sales: Test with real prospects (Day 13-17)
- Engineering: Iterate based on feedback (Day 18-21)
```

### Step 3: Set Up Notion Tracking

**Actions:**
1. Create central project page
2. Link all team tasks
3. Set up activity log
4. Configure notifications

**Script:**
```bash
python shared-resources/execution/track_project.py \
  --name "Real Estate Lead Automation" \
  --department "operations-team" \
  --status "in_progress" \
  --description "Cross-team project: Research validates market, Engineering builds scraper, Sales uses for outreach" \
  --team "research-team" "engineering-team" "sales-team"
```

### Step 4: Kick Off Project

**Actions:**
1. Brief all teams (async via Notion or sync meeting)
2. Clarify goals and expectations
3. Confirm timeline
4. Establish check-in cadence

**Communication:**
- What we're building
- Why it matters (revenue/efficiency impact)
- Each team's role
- Timeline and milestones
- How to report blockers

### Step 5: Monitor Progress

**Actions:**
1. Daily: Check Notion for updates
2. Identify risks early
3. Coordinate handoffs
4. Escalate blockers immediately

**Daily Check:**
- Is each team on track?
- Any blockers reported?
- Are handoffs approaching?
- Any risks emerging?

### Step 6: Facilitate Handoffs

**Actions:**
1. Confirm deliverable is ready
2. Notify receiving team
3. Ensure clarity on expectations
4. Log handoff in Notion

**Handoff Checklist:**
- [ ] Deliverable complete and tested
- [ ] Documentation provided
- [ ] Receiving team notified
- [ ] Questions answered
- [ ] Logged in Notion

**Script:**
```bash
python shared-resources/execution/log_change.py \
  --project "Real Estate Lead Automation" \
  --change "Research completed market validation, handed off to Engineering with data source documentation" \
  --department "operations-team" \
  --type "update"
```

### Step 7: Unblock Immediately

**When blocker reported:**

**Response Time:** Within 1 hour maximum

**Actions:**
1. Assess severity and impact
2. Identify who can resolve
3. Coordinate resolution
4. Update all affected teams

**Escalation:**
- Can resolve in-house? → Coordinate fix
- Need external resource? → Escalate to user
- Impacts timeline? → Communicate to all teams

### Step 8: Complete & Retrospective

**At project completion:**

**Actions:**
1. Confirm all deliverables complete
2. Update Notion to "completed"
3. Gather team feedback
4. Document improvements

**Retrospective Questions:**
- What went well?
- What slowed us down?
- What should we change next time?
- What can we automate?

**Log Improvement:**
```bash
python shared-resources/execution/log_improvement.py \
  --department "operations-team" \
  --operation "Coordinated cross-team automation project" \
  --improvement "Created standard handoff checklist" \
  --impact "Reduced handoff delays by 50%" \
  --category "simplification"
```

---

## Coordination Anti-Patterns

### ❌ Waiting for Perfect Information
Don't: Wait until everything is 100% clear
Do: Start with 80%, iterate as you learn

### ❌ Over-Communicating
Don't: Daily sync meetings with all teams
Do: Async updates in Notion, sync only when needed

### ❌ Ignoring Small Blockers
Don't: "That's a small issue, they'll figure it out"
Do: Address immediately before it grows

### ❌ Rigid Timelines
Don't: Hold teams to original estimate when reality changes
Do: Adjust based on data, communicate changes

---

## Tools & Templates

### Dependency Map Template

```
Project: [Name]
Teams: [List]

Dependencies:
- [Team A] → [Team B]: [What is needed]
- [Team B] → [Team C]: [What is needed]

Handoff Points:
1. [Date/Milestone]: [Team A] delivers [X] to [Team B]
2. [Date/Milestone]: [Team B] delivers [Y] to [Team C]

Risks:
- [Potential blocker 1]
- [Potential blocker 2]
```

### Handoff Checklist

```
Handoff: [Team A] → [Team B]
Deliverable: [What is being handed off]
Due: [Date]

Pre-Handoff:
[ ] Deliverable complete
[ ] Quality checked
[ ] Documentation ready
[ ] Receiving team notified

Handoff:
[ ] Deliverable provided
[ ] Walkthrough if needed
[ ] Questions answered
[ ] Logged in Notion

Post-Handoff:
[ ] Receiving team confirms receipt
[ ] Any issues addressed
[ ] Next steps clear
```

---

## Success Metrics

**Good Coordination:**
- Zero handoff delays
- No surprises
- Teams feel supported
- On-time delivery

**Poor Coordination:**
- Teams waiting on each other
- Missed handoffs
- Unclear expectations
- Blame shifting

---

## Summary

**Coordination is about:**
1. Clear dependencies and timelines
2. Proactive blocker resolution
3. Smooth handoffs
4. Continuous communication (via Notion)
5. Learning and improving

**Remember:** Your job is to make teams' jobs easier. If they're frustrated with coordination, you're failing.
