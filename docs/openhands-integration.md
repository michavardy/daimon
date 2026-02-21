# OpenHands integration

This document explains how **Daimon integrates into the OpenHands agent stack** through the OpenHands SDK. The integration layers the CLI-driven, remote-SSH/Docker workflow described in the README on top of the OpenHands runtime so that the same agent APIs, schemas, and tooling can schedule plans, emit directives, and ship PRs/MRs just like any other OpenHands agent.

## Core idea

- Daimon exposes an SDK-compatible agent (`DaimonAgent`) that OpenHands can instantiate, configure, and execute locally.
- The agent wires together the remote networking (`ssh`, `scp`, Docker build/execution), Git operations, schema validation, and CLI components described elsewhere in this repo.
- The OpenHands event loop treats the Daimon agent like any other agentic workload: it calls `plan`, `run`, `test`, and `publish` hooks while the agent emits directives into the shared stack.

## Prerequisites

1. Python environment with the OpenHands SDK installed (`pip install openhands-sdk`).
2. Access to the `daimon` package (installed from this repo using `pip install -e .`).
3. A `daimon.yml` and `.env` in the project root that describe the remote host, repository, approvals, task description, and secrets.
4. `gh`/`gitlab` CLI configured with tokens so the agent can create PRs/MRs and review comments.

## Installation and configuration

```bash
git clone https://github.com/michavardy/daimon.git
cd daimon
uv sync
source .venv/Scripts/activate
pip install -e .
pip install openhands-sdk
```

Create an OpenHands agent configuration (YAML or Python) that references the Daimon integration:

```yaml
agents:
  - name: daimon
    type: openhands.sdk.agent.Agent
    runtime: daimon.sdk.integration.DaimonOpenHandsAgent
    config:
      daimon_config: ./daimon.yml
      workspace: ./workspace
      repo_token_env: PERSONAL_ACCESS_TOKEN
```

`daimon.sdk.integration.DaimonOpenHandsAgent` is the entry point that the SDK loads. It expects the following config fields:

| field | type | description |
| --- | --- | --- |
| `daimon_config` | `Path` | Path to the project-local `daimon.yml`. |
| `workspace` | `Path` | Directory where files are packaged before transfer. |
| `repo_token_env` | `str` | Environment variable name that stores the PAT for GitHub/GitLab. |
| `ssh_key_env` | `Optional[str]` | Environment variable holding the SSH key (if any). |
| `schema_dir` | `Path` | Base schema directory (`~/.config/daimon/schema`). |
| `log_dir` | `Path` | Where `.daimon_logs/` should live. |

The agent loads the configuration, builds the schema context, and registers the actions listed below.

## Interface definition

### Agent class

```python
from openhands.sdk.agent import Agent

class DaimonOpenHandsAgent(Agent):
    def configure(self, config: Mapping[str, Any]) -> None:
        """Load daimon.yml, secrets, schema dir, and log path."""

    def plan(self, task: str) -> Dict[str, Any]:
        """Emit a plan document and open a draft PR/MR via GitHub/GitLab."""

    def execute(self, plan: Dict[str, Any]) -> ExecutionReport:
        """Ship source & schema to the remote host, run the docker build, and capture stdout/stderr."""

    def test(self, plan: Dict[str, Any]) -> TestReport:
        """Run `daimon run`'s test phase in the remote container, streaming `.daimon_logs`."""

    def publish(self, plan: Dict[str, Any]) -> PullRequestSummary:
        """Push changes and open a PR/MR with the final logs attached."""
```

Each method returns structured data (e.g., `ExecutionReport` contains `stdout`, `stderr`, `exit_code`, `artifacts`) and raises `AgentError` on failure so the OpenHands stack can re-emit directives.

### Actions and tools

Daimon exposes the following OpenHands actions via the SDK:

1. **`DaimonSSHAction`** – uses the `ssh` module to copy archives to the remote host, run Docker commands, and stream output.
2. **`SchemaValidationAction`** – inspects `~/.config/daimon/schema`, ensures required directories exist, and records hashes for auditing.
3. **`GitPublishAction`** – commits, pushes, and uses `gh`/`gitlab` to open PRs/MRs with the logs captured under `.daimon_logs/`.
4. **`LogExportAction`** – uploads `.daimon_logs/` contents as artifacts or attaches them to the GitHub/GitLab PR/MR.

All actions implement the `openhands.sdk.action.Action` interface so they can be injected into policies or reused by other agents.

### Schema interface

The integration relies on the schema directories documented elsewhere:

- `schema/rag/` – chunking/retrieval definitions that planners and coders use via RAG prompts.
- `schema/graph/` – nodes/edges describing the planning → coding → testing → review transitions.
- `schema/agents/` – custom directives, listeners, and policies that Daimon emits.
- `schema/policies/` – governance rules that get automatically injected when `SchemaValidationAction` runs.

The agent publishes a `schema_diff.patch` in `.daimon_logs/` each time the schema changes so reviewers can see evolutions.

## Example usage with OpenHands SDK

```python
from openhands.sdk.agent import AgentRuntime
from daimon.sdk.integration import DaimonOpenHandsAgent

runtime = AgentRuntime(
    agents=[
        {
            "name": "daimon",
            "cls": DaimonOpenHandsAgent,
            "config": {
                "daimon_config": "./daimon.yml",
                "workspace": "./workspace",
                "repo_token_env": "PERSONAL_ACCESS_TOKEN",
                "schema_dir": "~/.config/daimon/schema",
                "log_dir": "./.daimon_logs",
            },
        }
    ],
)

runtime.start(task="Implement schema-driven autonomous tasks")
```

The OpenHands runtime will call `configure`, `plan`, `execute`, `test`, and `publish` in sequence. Each step emits directives to the shared stack, and `DaimonOpenHandsAgent` guarantees:

- `plan` writes a `plan.md` file and opens a PR in draft.
- `execute` pushes the remote container, runs the Docker image, and captures structured logs.
- `test` replays the trace files and publishes results into the PR discussion.
- `publish` marks the draft PR ready for review, attaching `.daimon_logs/` for auditing.

## Troubleshooting

- **Missing documents**: run `uv run python -m daimon schema dump` to regenerate missing schema files before invoking the SDK.
- **Agent interface mismatch**: ensure the OpenHands SDK version matches the `openhands.sdk.agent.Agent` interface version expected by this repo.
- **Secrets not injected**: confirm the `.env` referenced in `daimon.yml` exports `PERSONAL_ACCESS_TOKEN`, `REMOTE_PASSWORD`, and any LLM keys before starting the runtime.

By following this interface, other OpenHands agents can coordinate with Daimon without needing to know the internal CLI steps—`DaimonOpenHandsAgent` encapsulates the remote execution, schema guards, and PR publishing logic in one reusable SDK-friendly component.
