# Organization Structure

The workspace is organized into the following departments/teams. Each team has its own `directives/` (SOPs) and `execution/` (Scripts) directories.

## Teams

- **content-team/**: Content creation and strategy.
- **sales-team/**: Sales processes and pipelines.
- **operations-team/**: General operations and logistics.
- **client-management-team/**: Client relations and account management.
- **research-team/**: Market and lead research.
- **project-management/**: Project tracking and management.
- **engineering-team/**: Software development and technical engineering.
- **analytics-reporter/**: Data analysis and reporting.
- **marketing-team/**: Marketing campaigns and outreach.
- **testing-experimenting/**: QA, testing, and experimental workflows.
- **NK-personal-team/**: Personal tasks for NK.

## Structure Pattern

Each team folder contains:
- `directives/`: Markdown files defining the team's Standard Operating Procedures (Layer 1).
- `execution/`: Python scripts for automating the team's tasks (Layer 3).

## Infrastructure

### Shared Resources & Protocols
- **shared-resources/**: Utilities used by all teams (e.g., `logger.py` in `execution/`).
- **knowledge-base/**: Static assets and definitions.
    - `protocols/`: Standard JSON schemas for communication (e.g., `standard_response.schema.json`).
    - `resources/`: Brand voice, pricing, etc.
- **logs/**: Centralized logs for all execution scripts (`central_activity.log`).
- **.agent/workflows/**: High-level maps for multi-team business processes.
