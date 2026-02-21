# OpenHands agent interface

Daimon focuses entirely on coaching an OpenHands-style agent that continuously learns from merge request feedback instead of building and packaging Docker artifacts. This document explains the files, CLI behavior, and SDK usage required to inject system prompts, run a feedback-driven plan, and capture new learning signals.

## Required files

- **`daimon.yml`** – the minimal bootstrap that tells the CLI which OpenHands runtime to call and where to read/write the feedback loop. It only needs `agent.name`, `agent.runtime`, `agent.interface_doc`, the `schema` location (`path` and `minimal`), `feedback.log`, and a `task` string. `task` becomes the `Task` field in `system_prompt.md`, `schema.path` is copied before every run, and `feedback.log` points at the merge request feedback log documented here.
- **`merge_request_feedback.md`** – append the latest reviewer comments, test failures, and product reasoning so the CLI can summarize the delta and turn it into a fresh learning signal.
- **`system_prompt.md`** – rewritten on every `daimon run`, this file holds the high-level task plus the summarized feedback. It is the system prompt the OpenHands runtime ingests for the next cycle.
- **`openhands-agent-plan.md`** – the atomic plan the CLI emits; it lists the goal, learning signal, system-prompt guardrails, and a numbered set of steps (planning, coding, testing, review) that the OpenHands runtime executes.
- **Optional artifacts** – `openhands-agent-trace.md`, `openhands-agent-plan.json`, `system_prompt_planning.md`, and similar files can capture traces, step-specific prompts, or metadata for debugging.

### Example `merge_request_feedback.md` entry

```
2026-02-20 | Reviewer @alex | Tests failed in `src/daimon/commands/run.py` when `merge_request_feedback.md` was empty; agent should warn before rendering the plan.
2026-02-22 | Product | Expect every cycle to quote the latest CI learnings when describing the new system prompt.
```

## Task types and prompt granularity

`daimon run` accepts a `--task` string and pushes it into `system_prompt.md` as the `Task` value. Each plan step is already typed (planning, coding, testing, reviewing), and you can include step-specific guardrails inside the plan or optional files like `system_prompt_planning.md`. The OpenHands runtime can treat a plan step as a discrete task and wrap it with its own sub-prompt while referencing the shared system prompt the CLI produced. Keeping the CLI output deterministic means there is a single canonical system prompt per run, but the plan describes how to split the work into different task types.

## CLI contract

1. Running `daimon init` seeds `daimon.yml`, copies the minimal schema under `.schema`, creates placeholders for prompts and plans, and documents how to feed merge request feedback into the loop.
2. `daimon run` performs the learning loop:
   - Reads the delta in `merge_request_feedback.md` to determine what changed since the previous run.
   - Summarizes that feedback into the next `system_prompt.md` entry, thereby injecting the freshest reviewer guidance as the new system prompt.
   - Builds `openhands-agent-plan.md` with explicit steps tied to the feedback and the plan schema (summary, learning signal, steps, acceptance).
   - Logs the plan and prompt updates via `src/daimon/utils/logging_utils.py` and writes deterministic plan steps that the OpenHands runtime follows.
3. The CLI purposefully avoids building binaries or Docker images; it simply orchestrates prompts, plans, and traceable logs for the OpenHands runtime.

## OpenHands SDK usage

OpenHands SDK integration is still an active research topic, but the current guidance is:

1. Install the SDK (e.g., `pip install openhands-agent` or the package referenced in your SDK docs).
2. Instantiate the agent using the runtime and name from `daimon.yml` and point it to this interface doc.
3. Load `system_prompt.md` as the `system_content`, `openhands-agent-plan.md` as the `plan`, and `merge_request_feedback.md` for additional context.
4. Run the agent loop; the SDK will obey the plan steps while keeping the injected system prompt active and track any traces.
5. After the run completes, append the results (diffs, comments, test outcomes) to `merge_request_feedback.md` with metadata so the next loop sees the freshest learning signal.

## Continual learning loop (system prompt injection)

1. **Capture** – maintain `merge_request_feedback.md`; each entry represents a new learning signal from reviewer comments, approvals, or failure logs.
2. **Inject** – `daimon run` trims those entries into `system_prompt.md` so the agent's system prompt always reflects the freshest feedback.
3. **Plan** – the CLI writes `openhands-agent-plan.md`, explicitly linking the plan steps to the feedback-derived system prompt and noting the acceptance criteria.
4. **Execute** – the OpenHands SDK consumes the plan and system prompt, executes actions, and produces work artifacts.
5. **Review** – add results back to `merge_request_feedback.md`, noting what worked and what still needs attention. This additional feedback becomes the next system prompt injection, closing the learning loop.

By keeping the schema minimal—only the essential prompts, plan, and feedback files—you keep a tight, repeatable OpenHands-driven cycle without additional packaging overhead.
