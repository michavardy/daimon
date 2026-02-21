# OpenHands agent interface

Daimon now focuses entirely on coaching an OpenHands-style agent that continuously learns from merge request feedback instead of building and packaging Docker artifacts. This document explains the files, CLI behavior, and SDK usage required to inject system prompts, run a feedback-driven plan, and capture new learning signals.

## Required files

- **`daimon.yml`** – serialized persona, goals, and plan templates. The `init` command scaffolds this file so your CLI knows how to describe the feedback loop to OpenHands.
- **`merge_request_feedback.md`** – a simple changelog of reviewer comments, test failures, or product reasoning that drives the next cycle.
- **`system_prompt.md`** – the cleaned-up system instructions that the OpenHands runtime ingests; it is rewritten on every run using the trimmed learning signal from `merge_request_feedback.md`.
- **`openhands-agent-plan.md`** (or similar) – the atomic steps the CLI emits so the runtime knows what actions to take. It links back to the MR feedback that seeded it.
- **Optional artifacts**: `openhands-agent-trace.md`, `openhands-agent-plan.json`, etc., capture traces, plan metadata, or additional prompts for debugging.

## CLI contract

1. Running `daimon init` seeds `daimon.yml`, creates placeholders for the plan and prompt, and adds instructions about feeding MR feedback.
2. `daimon run` performs the learning loop:
   - Reads the delta in `merge_request_feedback.md` to determine what changed since the previous run.
   - Summarizes that feedback into the next `system_prompt.md` entry, thereby injecting the latest review guidance as the new system prompt.
   - Builds `openhands-agent-plan.md` with explicit steps tied to the feedback and the plan schema (summary, learning signal, steps, acceptance).
   - Logs the plan and prompt updates via `src/daimon/utils/logging_utils.py` to keep the trace short and deterministic.
3. The CLI purposefully avoids building binaries or Docker images; it simply orchestrates prompts, plans, and traceable logs for the OpenHands runtime.

## OpenHands SDK usage

Follow these steps when integrating with the OpenHands SDK:

1. Install the SDK (e.g., `pip install openhands-agent` or the appropriate package referenced in your docs).
2. Instantiate the agent using the persona and goal from `daimon.yml`.
3. Load the latest `system_prompt.md` as the `system_content`, `openhands-agent-plan.md` as the `plan`, and `merge_request_feedback.md` for additional context.
4. Run the agent loop; the SDK will follow the plan steps while keeping the injected system prompt active.
5. After the run completes, examine outputs (commits, comments, trace logs), summarize key takeaways, and append them to `merge_request_feedback.md` with dates, reviewer IDs, or any other metadata.

## Continual learning loop (system prompt injection)

1. **Capture** – maintain `merge_request_feedback.md`; each entry represents a new learning signal from reviewer comments or observed failures.
2. **Inject** – `daimon run` trims those entries into `system_prompt.md` so the agent's system prompt always reflects the freshest feedback.
3. **Plan** – the CLI writes `openhands-agent-plan.md`, explicitly linking the plan steps to the feedback-derived system prompt and noting the acceptance criteria.
4. **Execute** – the OpenHands SDK consumes the plan and system prompt, executes actions, and produces work artifacts.
5. **Review** – add results back to `merge_request_feedback.md`, noting what worked and what still needs attention. This additional feedback becomes the next system prompt injection, closing the learning loop.

By keeping the schema minimal—only the essential prompts, plans, and feedback files—you maintain a tight, repeatable OpenHands-driven cycle without additional packaging overhead.
