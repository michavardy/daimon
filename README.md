# Daimon

Schema-constrained, reproducible, PR-native autonomous software engineering.

Daimon is a CLI-driven autonomous coding agent that runs inside your project, ships code to a remote Docker host over SSH, and drives development tasks end-to-end. It plans, executes, tests, and publishes PRs/MRs with full execution logs while strictly enforcing schema constraints.

## Architecture at a glance

- **Models** (see `docs/models.md`): primitives such as queries, archives, directives, and listeners form the runtime data structures. Memory, RAG datasets, and chunking/extraction models are registered by name so every agent in the stack can look up context without carrying global state.
- **Orchestration** (see `docs/orchestration.md`): prompts, agents, directive emitters, and actions are described in YAML. Each phase (planning, coding, testing, review) initializes a stack of directives that drive which agents execute which actions and when new directives fire.
- **Policies** (see `docs/policies.md`): coding, architectural, testing, review, and execution rules are modeled as injectables or RAG documents inside prompts so every LLM call is evaluated according to the latest guidelines.
- **Trace** (see `docs/trace.md`): each directive emits a complete log of inputs, outputs, memory and archive interactions, and artifact snapshots. Traces allow replaying, auditing, and debugging every autonomous session.
- **Roadmap** (see `docs/roadmap.md`): future work includes evolutionary branch directives, richer multi-model experimentation, and more resilient schema workflows.

## Prerequisites

- `uv` for managing the virtual environment (see `uv.lock`).
- Access to a remote SSH host with Docker.
- A GitHub or GitLab repository ready to receive autonomous PRs/MRs.
- A `daimon.yml` config file plus a `.env` file containing secrets (SSH password/key, PAT, LLM key, etc.).

## Installation

### For developers

```bash
git clone <repo>
uv sync
source .venv/Scripts/activate
pip install -e .
```

### Running without an activated environment

```bash
uv run python -m daimon
```

## Configuration

Daimon relies on two documents in the project root:

### `daimon.yml`

- `remote_environment`: SSH user/host and optional encrypted keys (credentials live only in `.env`).
- `repository`: remote URL, default branch, and PAT reference.
- `approval`: optional override for plan/code/tests approvals (defaults to required).
- `task`: multi-line task description with requirements/acceptance criteria.
- `reference_docs`: optional list of URLs or local markdown used during planning/code.

### `.env`

Supports secrets referenced from `daimon.yml`, including `PERSONAL_ACCESS_TOKEN`, `REMOTE_PASSWORD`, and any LLM API keys. Secrets are injected at runtime and never committed.

### Schema directory

`~/.config/daimon/schema` defines the runtime spec that governs planning, execution, testing, policies, and logging. Key directories include `rag/`, `graph/`, `agents/`, and `policies/`. The schema is immutable during a phase but can be incrementally updated and merged at phase boundaries.

## Typical execution lifecycle

1. **Validate** remote connectivity, Docker availability, credentials, and config integrity.
2. **Package & transfer** source, schema, and instructions to the remote host.
3. **Environment setup**: clone the OpenHands agent runtime, build the Docker image, and inject environment variables.
4. **Phase 1 – Planning**: produce a structured plan, open a draft PR/MR, and refresh the schema on success or iteration.
5. **Phase 2 – Coding**: apply planned changes, run incremental tests, linting, and static analysis, update the PR, and evolve the schema.
6. **Phase 3 – Testing & validation**: generate and run comprehensive tests, log the results, and loop back if failures occur.
7. **Phase 4 – Cleanup**: archive logs, keep the schema current, promote the PR/MR out of draft, and tear down remote artifacts.

Every phase updates structured logs (`.daimon_logs/run_<timestamp>/...`) so human reviewers can inspect prompts, retrieval traces, execution output, diffs, and review metadata.

## Usage

```bash
cd <project_dir>
daimon run
```

- Run inside the project directory containing `daimon.yml` and `.env`.
- The CLI packages the project, ships it to the remote Docker host, executes the autonomous plan, and opens PRs/MRs on completion.

## Logs & observability

Logs are written under `.daimon_logs/run_<timestamp>/` with subdirectories for LLM I/O, retrieval traces, execution stdout/stderr, git diffs, and review metadata. Logs are also stored on the remote GitHub/GitLab draft branch.

## Security & guarantees

- No direct pushes to mainline branches—only PRs/MRs.
- Secrets live solely in `.env` and are masked in logs and remote containers.
- The remote container is isolated, and the schema is versioned/hashed to prevent drift.

## Learn more

- Consult `docs/models.md`, `docs/orchestration.md`, `docs/policies.md`, `docs/trace.md`, and `docs/roadmap.md` for the full runtime spec.
- Inspect `schema/` under `~/.config/daimon/` after bootstrapping to see how the schema constrains each phase.
