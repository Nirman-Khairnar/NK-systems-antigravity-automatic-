---
description: Evaluate user proposal through multi-department review
---

# Evaluate User Proposal Workflow

## Purpose
When user proposes an idea/project, get fast, structured feedback from relevant departments to present the best path forward.

## Flow

### Step 1: Parse Proposal
**Orchestrator:** Extract key information from user proposal
- Project type (automation, product, campaign, etc.)
- Goals
- Constraints (budget, timeline, resources)
- Priority

**Output:** Structured proposal using `proposal_schema.json`

### Step 2: Route to Relevant Departments
**Orchestrator:** Determine which departments need to weigh in

**Routing Logic:**
- Contains "automation" or "workflow" → Engineering + Operations
- Contains "lead" or "sales" → Research + Sales
- Contains "content" or "marketing" → Content + Marketing
- Contains "client" or "project" → Client Management + Project Management
- Financial impact → All departments

**At minimum:** 2-3 departments review every proposal

### Step 3: Department Evaluations (Parallel)

Each department runs their evaluation **simultaneously**:

#### Research Team
**Directive:** `research-team/directives/evaluate_proposal.md` *(to be created)*

**Evaluates:**
- Market viability
- Competitive landscape
- Data availability

**Outputs:**
- Market validation (yes/no with data)
- Key insights
- Risks identified

#### Engineering Team  
**Directive:** `engineering-team/directives/evaluate_proposal.md` *(to be created)*

**Evaluates:**
- Technical feasibility
- Time estimate
- Resource requirements
- Better technical approaches

**Outputs:**
- Feasibility assessment
- Time/complexity estimate
- Alternative approaches if applicable

#### Sales Team
**Directive:** `sales-team/directives/evaluate_proposal.md` *(to be created)*

**Evaluates:**
- Revenue potential
- Market fit
- Pricing viability

**Outputs:**
- Revenue estimate
- Sales process implications
- Priority recommendation

#### Operations Team
**Directive:** `operations-team/directives/evaluate_proposal.md` *(to be created)*

**Evaluates:**
- Resource allocation
- Timeline feasibility
- Dependencies
- Coordination requirements

**Outputs:**
- Resource assessment
- Timeline validation
- Coordination plan

### Step 4: Collect Challenges
**Orchestrator:** Gather all department responses

**Format:** Each department uses `propose_improvement.py` to submit structured feedback

**Consolidate:**
- Risks identified (all departments)
- Alternative approaches proposed
- Impact analyses
- Recommendations

### Step 5: Synthesize Best Path
**Orchestrator:** Analyze all feedback and determine optimal approach

**Synthesis Logic:**
1. **If zero risks + all approve** → Proceed as proposed
2. **If low risks + improvements suggested** → Present improved version
3. **If high risks + alternatives exist** → Present alternative approach
4. **If critical risks + no viable path** → Recommend rejection with reasoning

**Create Recommendation:**
- Original proposal summary
- Department feedback highlights
- Recommended approach (original or modified)
- Risks and mitigations
- Time/cost implications
- Next steps

### Step 6: Present to User
**Orchestrator:** Use `notify_user` to present consolidated recommendation

**Format:**
```markdown
## Proposal Evaluation: [Project Name]

### Summary
[Brief recap of user's proposal]

### Department Feedback
- **Research:** [Key findings]
- **Engineering:** [Feasibility + time estimate]
- **Sales:** [Revenue potential]
- **Operations:** [Resource implications]

### Recommended Approach
[Either original or improved version]

**Why This is Better:**
[First-principles reasoning]

### Trade-offs
- Time: [estimate]
- Cost: [estimate]
- Risk: [level with mitigations]

### Next Steps
1. [First action]
2. [Second action]
3. [Third action]

**Ready to proceed?**
```

### Step 7: Track in Notion
**Orchestrator:** Once user approves, create Notion project page

```bash
python shared-resources/execution/track_project.py \
  --name "[Project Name]" \
  --department "[Lead Department]" \
  --status "not_started" \
  --description "[Approved approach]"
```

---

## Timing Expectations

**Total Time:** 15-30 minutes for full evaluation

**Per Step:**
- Step 1 (Parse): 2 min
- Step 2 (Route): 1 min
- Step 3 (Evaluate): 5-15 min (parallel)
- Step 4 (Collect): 2 min
- Step 5 (Synthesize): 5-10 min
- Step 6 (Present): Immediate
- Step 7 (Track): 1 min

**Why Fast:** Departments run in parallel, not serial. Use existing knowledge/data, don't do deep research.

---

## Example Execution

**User Proposal:**
"Let's build a real estate lead scraper for Australian market that finds agents running Facebook ads"

**Step 1 - Parse:**
```json
{
  "proposal_type": "automation",
  "title": "Real Estate Lead Scraper - Australia",
  "goals": ["Find real estate agents", "Target FB ad runners", "Australian market"],
  "priority": "high"
}
```

**Step 2 - Route:**
- Research Team ✓
- Engineering Team ✓
- Sales Team ✓
- Operations Team ✓

**Step 3 - Evaluations:**

*Research Team:*
- Market validation: YES - Australia has 20K+ agents, FB ads common
- Risk: Low - Market is accessible
- Time: 5 min (used existing research)

*Engineering Team:*
- Feasibility: YES - Have scraping infrastructure
- Time estimate: 4-6 hours
- Alternative: Use existing `scrape_single_site.py` as base
- Risk: None

*Sales Team:*
- Revenue potential: HIGH - Real estate = high LTV clients
- Priority: Urgent (matches mission)
- Risk: None

*Operations Team:*
- Resources: Available
- Timeline: Can start immediately
- Dependencies: None

**Step 4 - Collect:**
All departments: APPROVE with minor improvements
- Engineering suggested using existing scraper
- Research provided target criteria
- Sales confirmed market fit

**Step 5 - Synthesize:**
✅ Recommended Approach: Proceed with proposed project
- Use existing scraper infrastructure (faster)
- Focus on FB ad detection (Research's insight)
- Target 50-100 qualified leads initially (Sales input)
- Time: 4-6 hours total
- Risk: LOW

**Step 6 - Present:**
[Formatted recommendation to user via notify_user]

**Step 7 - Track:**
Notion project page created, ready to execute

---

## Notes

- **Speed is priority:** Don't do comprehensive research, use existing knowledge
- **Challenges are encouraged:** Departments should propose improvements
- **First principles:** Focus on fundamental problem, not surface request
- **Notion tracking:** Always log the evaluation and decision
