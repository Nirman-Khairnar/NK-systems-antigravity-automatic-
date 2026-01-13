# NK Systems: AntiGravity (DND)

**"Turning Operational Chaos into Predictable Execution."**

This repository houses the entire operating system for **NK Systems (AntiGravity)**. It is designed to function not just as a file storage, but as a living "Neural Architecture" where AI Agents and Humans collaborate to execute complex business logic at high velocity.

---

## 🏗 The 3-Layer Architecture

We operate on a strict 3-layer architecture to separate **Intent** (Human) from **Execution** (Machine).

### Layer 1: Directives (The "SOPs")
*   **Location:** `[team-name]/directives/`
*   **Format:** Markdown (`.md`)
*   **Function:** Structured Operating Procedures. These files tell the AI *what* to do, but not *how* to code it. They are the "Policy."
*   **Example:** `sales-team/directives/close_deal.md`

### Layer 2: Orchestration (The "Agent")
*   **Location:** The Agent (Me)
*   **Function:** The Intelligent Router. I read the Directives (Layer 1), decide which Tools (Layer 3) to use, handle errors, and pass data between departments. I am the "Glue."

### Layer 3: Execution (The "Tools")
*   **Location:** `[team-name]/execution/`
*   **Format:** Python Scripts (`.py`)
*   **Function:** Deterministic, bulletproof logic. These scripts do the heavy lifting (API calls, Database writes, Scrapers). They either work or they fail; they do not "hallucinate."
*   **Example:** `sales-team/execution/crm_update_deal.py`

---

## 🏢 Department Structure

The organization is divided into specialized "Teams." Each team is self-contained with its own Directives and Execution scripts, but shares a central nervous system.

*   **engineering-team/**: Software development, automation pipelines, and infrastructure.
*   **operations-team/**: Logistics, coordination, and general "friction removal."
*   **sales-team/**: Pipeline management, deal closing, and revenue generation.
*   **content-team/**: Strategy, production, and distribution (The "Harvey Specter" Brand).
*   **research-team/**: Deep-dive market analysis and lead enrichment.
*   **marketing-team/**: Campaign management and outreach.
*   **client-management-team/**: Retention and account success.
*   **project-management/**: Tracking and velocity metrics.
*   **analytics-reporter/**: Data synthesis and BI.
*   **testing-experimenting/**: R&D and sandbox.
*   **NK-personal-team/**: High-level strategy and personal brand execution.

---

## 🧠 The Central Nervous System

To prevent silos, we use shared infrastructure:

1.  **Orchestrator Logic (`ORGANIZATIONAL_STRATEGY.md`)**
    *   Defines how data flows from *Sales* -> *Engineering* -> *Client Success*.
    *   The Agent (Me) handles the hand-offs.

2.  **Shared Resources (`shared-resources/`)**
    *   Utilities used by all teams (e.g., `logger.py`, `gmail_client.py`).
    *   Prevents code duplication.

3.  **Knowledge Base (`knowledge-base/`)**
    *   **Protocols:** JSON Schemas for communication (e.g., `standard_response.schema.json`).
    *   **Resources:** Static assets (Brand Voice, Pricing Models).

4.  **Central Logs (`logs/`)**
    *   A single source of truth for all system activity.

---

## 🚀 "Elon Musk" Velocity Principles

1.  **No Bureaucracy:** Direct communication between departments.
2.  **Challenge Everything:** Every directive is subject to improvement. "The best process is no process."
3.  **Automate or Die:** If it's a repetitive task, it belongs in Layer 3 (Execution Scripts), not on a human's to-do list.

---

*System maintained by NK & The AntiGravity Agent.*
