# Daimon repository memory

- Daimon is a CLI-driven autonomous coding agent that uses remote SSH Docker hosts and PR/MR workflows.
- Key docs live under `docs/`: `models.md`, `orchestration.md`, `policies.md`, `trace.md`, and `roadmap.md` describing runtime spec, orchestration, policies, logging, and roadmap.
- README now links to each document and summarizes the CLI prerequisites, installation, configuration, lifecycle, logging, and security guarantees that keep onboarding deterministic.
- `docs/openhands-integration.md` describes the OpenHands SDK entry point, agent interface, schema guards, and action wiring.
- Daimon now orchestrates an OpenHands-style agent via `daimon.yml`, `merge_request_feedback.md`, and the new `docs/openhands-agent-interface.md` so system prompts evolve with MR feedback instead of building Docker images.
- `daimon.yml` + `.env` are required config files, and the CLI is `daimon run`.
