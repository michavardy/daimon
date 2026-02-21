# Daimon repository memory

- Daimon orchestrates an OpenHands-style agent that stays inside the repo, injects system prompts from merge request feedback, emits atomic plans, and no longer builds Docker artifacts.
- Key docs also live under `docs/`: `models.md`, `orchestration.md`, `policies.md`, `trace.md`, and `roadmap.md` spell out the runtime primitives, directives, policies, observability, and roadmap.
- `docs/openhands-agent-interface.md` is the canonical contract: it lists the minimal files (`daimon.yml`, `merge_request_feedback.md`, `system_prompt.md`, `openhands-agent-plan.md`, optional traces), explains the CLI loop, and sketches how to wire the OpenHands SDK.
- README links to those docs and now summarizes the CLI prerequisites (`uv`/`pixi`, OpenHands runtime guidance), installation, configuration, lifecycle, logs, and security guardrails that keep onboarding deterministic.
- `daimon.yml` defines `agent.name`, `agent.runtime`, `agent.interface_doc`, `schema.path`, `schema.minimal`, `feedback.log`, and the `task` string that becomes the `Task` field in `system_prompt.md`.
- `merge_request_feedback.md` is the living log of reviewer comments; the CLI trims it into `system_prompt.md` and writes out `openhands-agent-plan.md` and the minimal schema under `.schema` or system config each run.
- CLI commands are `daimon init` (scaffolds `daimon.yml`, `.env`, `merge_request_feedback.md`, and `.schema`) and `daimon run` (summarizes feedback, emits prompts, and records plan artifacts).
