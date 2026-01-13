# SOP: Create n8n Workflow

**Goal**: Automatically generate, deploy, and document an n8n workflow from natural language requirements.

**Inputs**:
- Natural Language Requirement (Text or File)

**Tools**:
- `engineering-team/execution/n8n_pipeline.py`

**Environment**:
- Ensure `.env` in the root has `NOTION_API_KEY`, `N8N_API_KEY`, etc.

**Steps**:

1.  **Define Requirements**: Write down what you want the workflow to do.
2.  **Run Pipeline**:
    ```bash
    python engineering-team/execution/n8n_pipeline.py "your requirements here"
    ```
    OR with a file:
    ```bash
    python engineering-team/execution/n8n_pipeline.py path/to/requirements.txt
    ```

**Options**:
- `--no-deploy`: Skip deployment to n8n (Generation only).
- `--no-docs`: Skip Notion documentation.
- `--project-name`: Specify a custom name for the output folder in `.tmp/`.

**Output**:
- A generated workflow JSON in `.tmp/<project>/`.
- A deployed workflow in your n8n instance (unless skipped).
- A documented page in Notion (unless skipped).
