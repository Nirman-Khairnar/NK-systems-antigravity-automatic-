# Requirements Validation Directive

## Goal
Ensure client requirements are complete and unambiguous before workflow design begins.

## Inputs
- Raw client requirements (text, document, conversation transcript)
- Previous context (if this is an iteration)

## Execution Scripts
- `execution/parse_requirements.py` - Extracts structured data from natural language

## Process

### 1. Initial Parsing
Run the requirements parser:
```bash
python execution/parse_requirements.py "<requirements_text>"
```

Or if requirements are in a file:
```bash
python execution/parse_requirements.py path/to/requirements.txt
```

### 2. Review Structured Output
Check `.tmp/requirements.json` for completeness. Required fields:
- `workflow_name` - Descriptive name
- `goal` - Clear objective
- `triggers` - What starts the workflow
- `data_sources` - APIs/services accessed
- `actions` - Steps to execute
- `error_handling` - How to handle failures

### 3. Handle Missing Information
If `.tmp/questions.json` exists:
- Present questions to user (prioritize blocking questions first)
- Collect answers
- Re-run parser with updated requirements
- Repeat until no questions remain

### 4. Gate Criteria
**Do NOT proceed to next stage until:**
- ✅ All triggers clearly defined
- ✅ All data sources identified
- ✅ Actions sequenced logically
- ✅ Error handling strategy specified
- ✅ Success metrics defined
- ✅ No critical missing information

## Outputs
- `.tmp/requirements.json` - Structured requirements
- Gate status: APPROVED or NEEDS_CLARIFICATION

## Edge Cases

### Ambiguous Requirements
If AI identifies ambiguity, generate specific questions rather than making assumptions.

### Multiple Workflow Patterns
If requirements suggest multiple workflows, flag this and ask user if they want:
- One complex workflow
- Multiple simple workflows
- Phased approach

### Over-Specified Requirements
If user provides too much technical detail, validate it aligns with n8n capabilities. Flag incompatible requests.

## Learnings
*(Updated as system evolves)*

- **2025-12-26**: Using OpenRouter free Gemini model for cost efficiency
- **2025-12-26**: JSON parsing sometimes includes markdown code blocks - strip them before parsing
