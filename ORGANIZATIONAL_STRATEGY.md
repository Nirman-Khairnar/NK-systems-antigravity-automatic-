# Organizational Strategy & Optimization

## 1. Cross-Department Execution
**Question:** Will the system execute tasks across departments?  
**Answer:** **Yes.** 

As the **Orchestrator (Layer 2)**, I sit above the folder structure. I am not bound to a single folder. 

**How it works:**
If the `sales-team` has a directive that requires a case study from the `content-team`, I will:
1. Read the `sales-team/directives/close_deal.md`.
2. See a step: "Fetch relevant case study from Content Team".
3. Pause the Sales process.
4. Switch context to `content-team/execution/get_case_study.py`.
5. Execute the script to get the file.
6. Pass that file back to the `sales-team` workflow.

I act as the bridge, passing data outputs from one team's execution as inputs to another team's directive.

---

## 2. Efficiency Improvements
To make this structure robust and efficient, I recommend (and have started implementing) the following:

### A. The `shared-resources` Department (Implemented)
**Problem:** Every team shouldn't write their own "Send Email" or "Read GSheet" script.  
**Solution:** I have created a `shared-resources` folder.
- **Use Case:** Reusable scripts (Utils) go here.
- **Example:** `shared-resources/execution/gmail_client.py`.
- **Logic:** Teams call these shared scripts for generic actions, keeping their own folders focused on *business logic* specific to them.

### B. Standardized Input/Output (Protocol)
**Proposal:** Define a "Protocol" for hand-offs.
- When `research-team` passes a lead to `sales-team`, it should be in a standard JSON format (e.g., `lead_schema.json`).
- This prevents "translation errors" between departments.

### C. The `workflows/` Map
**Proposal:** specific `workflows` folder to map high-level Business Processes that span multiple teams.
- **File:** `.agent/workflows/onboarding_new_client.md`
- **Content:** 
  1. `sales-team`: Mark deal won.
  2. `finance-team`: Generate invoice.
  3. `client-management`: Send welcome packet.
This keeps complex multi-department processes documented in one place, rather than scattered across 3 different team folders.

### D. Centralized Logging (The "Audit Team")
**Proposal:** A `logs/` directory at the root.
- Every script in every `execution/` folder should write to a central log.
- This gives you a "Company Wide Activity Feed".

### E. Global "Memory" (Knowledge Base)
**Proposal:** A `knowledge-base/` folder.
- Stores static data: Brand Voice Guidelines (for Content & Marketing), Pricing Sheets (for Sales), Tech Stack Docs (for Engineering).
- Directives simply reference `[Brand Voice](../knowledge-base/brand_voice.md)` instead of re-explaining it.
