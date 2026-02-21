# Daimon

Schema-constrained, reproducible, PR-native autonomous agent focused on continual learning.

Daimon is a CLI-driven orchestrator for an OpenHands-style agent that stays inside your project, injects system prompts from merge request feedback, emits atomic plans, and captures every learning cycle.

## Architecture at a glance

- **[OpenHands agent interface](docs/openhands-agent-interface.md)** defines the prompt, plan, and logging contract so every run injects the latest merge request feedback as a system prompt.
- **[Models](docs/models.md)** document the runtime primitives (queries, archives, directives, listeners, and stacks) plus the registries for actions, chunking/extraction, and retrieval that agents use to build structured plans.
- **[Orchestration](docs/orchestration.md)** explains how prompts, action maps, and directive emitters form the phase graph so that planning, coding, testing, and review agents fire in the right order with concrete success criteria.
- **[Policies](docs/policies.md)** defines the rules that get injected into prompts or RAG documents to keep code quality, testing, and review standards consistent across every agentic action.
- **[Trace](docs/trace.md)** captures the full directive lifecycle, including inputs, outputs, memory and archive interactions, and execution artifacts so every autonomous step can be audited or replayed.
- **[Roadmap](docs/roadmap.md)** outlines upcoming ideas such as evolutionary branch directives and richer multi-model experimentation to strengthen autonomous resilience.

## Getting started

### Prerequisites

- `uv` (or `pixi`) for managing the virtual environment (see `uv.lock` in this repo) so the CLI stays deterministic.
- Access to an OpenHands runtime or SDK; integration is evolving, so consult the [OpenHands agent interface](docs/openhands-agent-interface.md) for the current wiring guidance.
- A GitHub or GitLab repository configured to receive the PR/MR opened by the OpenHands runtime.
- Project-local `daimon.yml`, `.env`, `merge_request_feedback.md`, and the prompt/plan files described in [OpenHands agent interface](docs/openhands-agent-interface.md).

### Installation

#### For developers

```bash
git clone <repo>
uv sync
source .venv/Scripts/activate
pip install -e .
```

#### Running without an activated environment

```bash
uv run python -m daimon
```

### Running Daimon

```bash
cd <project_dir>
daimon run
```

Run inside the project directory that contains `daimon.yml`, `.env`, and the feedback files described earlier. The CLI summarizes the latest entries from `merge_request_feedback.md`, injects them into `system_prompt.md`, emits `openhands-agent-plan.md`, and logs every plan step so the OpenHands runtime can execute, comment, and open a PR/MR in the next phase.

## Configuration

### `daimon.yml`

Bootstraps the minimal OpenHands runtime configuration:

```
agent:
  name: daimon-openhands
  runtime: openhands.sdk.agent.Agent
  interface_doc: docs/openhands-agent-interface.md
schema:
  path: .schema
  minimal: true
feedback:
  log: merge_request_feedback.md
task: |
  Improve the OpenHands agent with the latest merge request feedback.
```

`agent` declares the runtime, `schema.path` points to the minimal schema that gets refreshed before every run, `feedback.log` tells the CLI where to read reviewer comments, and `task` becomes the `Task` field injected into `system_prompt.md`. Keep secrets out of this YAML—place them in `.env` so the CLI and SDK can pull them securely.

### `.env`

Holds secrets such as GitHub/GitLab tokens, OpenHands SDK credentials, LLM API keys, or SSH keys that the plan runner needs. Values stay private and are injected at run time so they never appear in the repo.

### Schema directory

`src/daimon/schema/` keeps the minimal runtime spec for this feedback-driven agent. Files such as `planning.md`, `coding_standard.md`, and `commit_rules.md` define how plans, prompts, and commits must be shaped so the OpenHands loop stays focused.

## Execution lifecycle

1. **Validate** `daimon.yml`, `.env`, and `merge_request_feedback.md` to ensure the persona, secrets, and new learning signals are available.
2. **Prompt & plan synthesis** – `daimon run` trims the latest feedback into `system_prompt.md`, builds `openhands-agent-plan.md`, and logs every step for traceability.
3. **Agent execution** – the OpenHands runtime ingests the plan and prompt, executes actions (code changes, comments, tests), and captures artifacts.
4. **Review & capture** – summarize results/traces, append them to `merge_request_feedback.md`, and describe what will seed the next system prompt injection.
5. **Loop** – repeat `daimon run` so each additional MR comment injects a fresh prompt and keeps the agent continually learning.

See [Orchestration](docs/orchestration.md) for the full mapping between agents, prompts, actions, and directive emitters that powers this lifecycle.

## Logs & observability

`.daimon_logs/run_<timestamp>/` contains directories for LLM I/O, retrieval traces, execution stdout/stderr, git diffs, and review metadata. The logs feed into `merge_request_feedback.md` and the OpenHands runtime so reviewers can replay every response. Refer to [Trace](docs/trace.md) for the trace format and auditing guidance.

## Security & guarantees

- No direct pushes to mainline branches—Daimon always opens PRs/MRs via the OpenHands runtime.
- Secrets live solely in `.env` and are masked in logs and plan outputs.
- The schema stored in `src/daimon/schema/` is versioned and hashed to prevent drift between runs.
- Policies listed in [Policies](docs/policies.md) are injected into prompts or referenced via RAG to keep agents compliant.

## Learn more

- [OpenHands agent interface](docs/openhands-agent-interface.md): CLI contract, prompt injection strategy, and SDK usage for continual learning from MRs.
- [Models](docs/models.md): runtime primitives, archives, memories, and action registries.
- [Orchestration](docs/orchestration.md): prompt templates, agent mappings, and directive emitters.
- [Policies](docs/policies.md): governance rules for coding, testing, review, and execution.
- [Trace](docs/trace.md): audit-friendly logs for every directive, action, and artifact.
- [Roadmap](docs/roadmap.md): upcoming work on evolutionary branches and multi-model experimentation.

Inspect `src/daimon/schema/` to see how the schema documents described above shape each run.
