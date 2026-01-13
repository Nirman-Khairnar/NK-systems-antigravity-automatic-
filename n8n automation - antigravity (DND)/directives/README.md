# Directives

This directory contains Standard Operating Procedures (SOPs) written in Markdown.

## What Goes Here

Each directive should define:
- **Goal**: What this directive accomplishes
- **Inputs**: What information/data is needed
- **Tools/Scripts**: Which execution scripts to use
- **Outputs**: What gets produced (deliverables)
- **Edge Cases**: Known limitations, error handling, special scenarios

## Directive Template

Create new directives using this structure:

```markdown
# [Directive Name]

## Goal
What this directive accomplishes.

## Inputs
- Input 1: Description
- Input 2: Description

## Execution Scripts
- `execution/script_name.py` - What it does

## Process
1. Step 1
2. Step 2
3. Step 3

## Outputs
- Deliverable 1: Description (location)
- Deliverable 2: Description (location)

## Edge Cases
- Edge case 1: How to handle
- Known limitation: Workaround

## Learnings
(This section gets updated as the AI discovers better approaches)
- Learning 1: Date - Description
```

## Best Practices

1. **Living Documents**: Update directives as you learn better approaches
2. **Be Specific**: Include exact commands, API constraints, timing expectations
3. **Document Failures**: When something breaks, document the fix in the directive
4. **Natural Language**: Write like you're instructing a competent colleague
