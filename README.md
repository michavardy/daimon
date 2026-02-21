# Daimon

Schema-constrained, reproducible, PR-native autonomous software engineering.

Daimon is a CLI-driven autonomous coding agent that lives inside your project, ships source and schema to a remote SSH+Docker host, and drives development from planning through testing and PR/MR publication while keeping every decision fully auditable.

## Architecture at a glance

- **[Models](docs/models.md)** document the runtime primitives (queries, archives, directives, listeners, and stacks) plus the registries for actions, chunking/extraction, and retrieval that agents use to build structured plans.
- **[Orchestration](docs/orchestration.md)** explains how prompts, action maps, and directive emitters form the phase graph so that planning, coding, testing, and review agents fire in the right order with concrete success criteria.
- **[Policies](docs/policies.md)** defines the rules that get injected into prompts or RAG documents to keep code quality, testing, and review standards consistent across every agentic action.
- **[Trace](docs/trace.md)** captures the full directive lifecycle, including inputs, outputs, memory and archive interactions, and execution artifacts so every autonomous step can be audited or replayed.
- **[Roadmap](docs/roadmap.md)** outlines upcoming ideas such as evolutionary branch directives and richer multi-model experimentation to strengthen autonomous resilience.

## Getting started

### Prerequisites

- `uv` for managing the virtual environment (see `uv.lock` in this repo).
- A reachable SSH host with Docker installed so Daimon can build and execute inside an isolated container.
- A GitHub or GitLab repository configured to receive PRs/MRs from Daimon.
- Project-local `daimon.yml` and `.env` files describing the run configuration and secrets.

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

Run inside the project directory that contains `daimon.yml` and `.env`. The CLI packages your source and schema, transfers them to the remote Docker host, executes the autonomous plan, records all logs, and opens a PR/MR when the workflow completes.

## Configuration

### `daimon.yml`

Defines the remote environment (`remote_environment`), repository metadata (`repository`), approval overrides, the multi-line `task` description, and optional `reference_docs` that Daimon can fetch during planning. Keep secrets off the YAML and point to values stored in `.env`.

### `.env`

Holds secrets referenced from `daimon.yml`, such as `PERSONAL_ACCESS_TOKEN`, `REMOTE_PASSWORD`, encrypted SSH keys, and any LLM credentials. Values are injected at runtime and never committed.

### Schema directory

`~/.config/daimon/schema` stores the immutable runtime spec for each phase. Key subdirectories include `rag/`, `graph/`, `agents/`, and `policies/` so agents can look up directives, prompts, and constraints without carrying mutable global state.

## Execution lifecycle

1. **Validate** remote connectivity, Docker availability, credentials, and config integrity.
2. **Package & transfer** the local source, schema, and instructions to the remote host.
3. **Environment setup**: clone the OpenHands agent runtime, build the Docker image, and inject environment variables.
4. **Phase 1 – Planning**: emit directives, craft a structured plan, open a draft PR/MR, and refresh the schema if the plan is accepted.
5. **Phase 2 – Coding**: apply planned changes, run incremental tests and linters, update the branch, and evolve the schema as progress is made.
6. **Phase 3 – Testing & validation**: run comprehensive tests, capture results, and loop back if failures occur.
7. **Phase 4 – Cleanup**: archive logs, keep the schema in sync, promote the PR/MR out of draft, and tear down remote artifacts.

See [Orchestration](docs/orchestration.md) for the full mapping between agents, prompts, actions, and directive emitters that powers this lifecycle.

## Logs & observability

`.daimon_logs/run_<timestamp>/` contains directories for LLM I/O, retrieval traces, execution stdout/stderr, git diffs, and review metadata. Traces are also stored on the remote draft branch so reviewers can replay every response. Refer to [Trace](docs/trace.md) for the trace format and auditing guidance.

## Security & guarantees

- No direct pushes to mainline branches—Daimon always opens PRs/MRs.
- Secrets live solely in `.env` and are masked in logs and remote containers.
- The remote container is isolated, and the schema is versioned and hashed to prevent drift.
- Policies listed in [Policies](docs/policies.md) are injected into prompts or referenced via RAG to keep agents compliant.

## Learn more

- [Models](docs/models.md): runtime primitives, archives, memories, and action registries.
- [Orchestration](docs/orchestration.md): prompt templates, agent mappings, and directive emitters.
- [Policies](docs/policies.md): governance rules for coding, testing, review, and execution.
- [Trace](docs/trace.md): audit-friendly logs for every directive, action, and artifact.
- [Roadmap](docs/roadmap.md): upcoming work on evolutionary branches and multi-model experimentation.

Inspect `schema/` under `~/.config/daimon/` after bootstrapping to see how these documents take effect during each phase.
