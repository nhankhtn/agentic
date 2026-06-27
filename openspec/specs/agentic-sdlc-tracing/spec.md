# Purpose
Track and log AI agent activities during the SDLC for auditing and review.

## Input / Output

**Input:**
- AI agent interactions during development: tool used, task description, input summary, output summary
- Human review decisions: accepted / accepted with edits / rejected

**Output:**
- `outputs/run_log.json`: JSON array of trace entries, each with 10 required fields
- Audit trail enabling reviewers to verify AI agent contributions across SDLC phases

## AI Agent Roles in SDLC Phases

| SDLC Phase | Agent Role | Tasks | Example |
|---|---|---|---|
| **Requirements & Planning** | Research Agent | Literature review, dataset schema design, metric definition, spec drafting | "Research faithfulness metrics from XAI literature" |
| **Design** | Research Agent | Architecture decisions, pipeline design, technology comparison | "Compare rule-based vs FinBERT for evidence extraction" |
| **Implementation** | Coding Agent | Write source code, implement functions, integrate modules | "Implement `filter_news_by_time()` in retriever.py" |
| **Testing & QA** | Testing Agent | Write unit tests, run edge case tests, validate output schemas | "Write 5 boundary tests for temporal leakage filter" |
| **Review & Reflection** | All Agents | Self-evaluate output quality, suggest improvements, retrospective | "Review test coverage and suggest missing edge cases" |

## Requirements

### Requirement: System SHALL maintain agent trace log
The system SHALL maintain a JSON file (`outputs/run_log.json`) recording every AI agent interaction during development.

#### Scenario: Trace log file exists
- **WHEN** the project is submitted
- **THEN** `outputs/run_log.json` SHALL exist and be valid JSON

#### Scenario: Minimum entry count
- **WHEN** `outputs/run_log.json` is inspected
- **THEN** it SHALL contain at least 6 entries

### Requirement: Trace log SHALL cover all agent roles
The trace log SHALL include entries from at least 3 different AI agent roles to demonstrate diverse use of agents across SDLC phases.

#### Scenario: Role diversity
- **WHEN** entries are grouped by `agent_role`
- **THEN** at least 3 distinct roles SHALL be present: "Research Agent", "Coding Agent", "Testing Agent"

### Requirement: Each trace entry SHALL have complete fields
Every entry in the trace log SHALL contain all required fields for auditing the AI-human interaction.

#### Scenario: Required fields present
- **WHEN** a single entry in `run_log.json` is inspected
- **THEN** it SHALL contain: `run_id`, `task_id`, `timestamp`, `agent_role`, `tool_used`, `task`, `input_summary`, `output_summary`, `human_review`, `quality_gate`

#### Scenario: Valid human_review values
- **WHEN** `human_review` field is inspected
- **THEN** its value SHALL be one of: "accepted", "accepted with edits", "rejected"

#### Scenario: Valid quality_gate values
- **WHEN** `quality_gate` field is inspected
- **THEN** its value SHALL be one of: "passed", "failed"

### Requirement: Quality gates SHALL be enforced for AI-generated code
All AI-assisted code and test artifacts SHALL pass through a quality gate (human review) before being used in the project.

#### Scenario: Code quality gate
- **WHEN** an AI agent generates code for any module
- **THEN** a human reviewer SHALL verify the code runs correctly and logic matches design.md before it is merged

#### Scenario: Failed quality gate
- **WHEN** `quality_gate = "failed"` for any entry
- **THEN** the AI agent output SHALL be rejected or regenerated — it SHALL NOT be used as-is

### Requirement: Trace log SHALL include agent reflection entries
The trace log SHALL include entries where agents reflect on their own output quality, identifying what worked well and what could be improved.

#### Scenario: Reflection entry exists
- **WHEN** `outputs/run_log.json` is inspected
- **THEN** at least 1 entry SHALL have `task` describing self-evaluation or retrospective analysis of previous agent outputs

#### Scenario: Reflection covers improvement suggestions
- **WHEN** a reflection entry is inspected
- **THEN** `output_summary` SHALL contain at least 1 specific improvement suggestion or lesson learned
