# Daimon 

Schema-constrained, reproducible, PR-native autonomous software engineering.

Pronounced DYE-mon

A daimon is an inner guiding intelligence.

**Daimon** is a CLI-driven autonomous coding agent that runs inside your project, connects to a remote Docker host over SSH, and executes development tasks end-to-end including:

- planning
- execution
- testing

while opening Pull Requests (GitHub) or Merge Requests (GitLab) with full execution logs.

Daimon is designed for deterministic, observable, and reproducible agentic software development.

## What Daimon Does

From inside a project directory, Daimon:

1. Reads structured task instructions 

2. Loads global schema constraints (markdown-based spec system)

3. Ships code to a remote host via SSH

4. builds a docker in remote host 

5. Executes an autonomous plan:
    
    - plan
    - code
    - test
    - cleanup

6. Captures full LLM input/output logs and execution traces

7. Commits changes to a new branch

8. Opens a PR (GitHub) or MR (GitLab) upon completion of every step of autonomy plan with options of skipping approval steps

9. Stores structured logs for audit and replay

## Usage


```bash
cd <project_dir>
daimon run
```

**Note**:
- run in project dir
- must have daimon.yml in project dir
- must have .env in project dir

### Daimon Yaml Spec

```yml

# required, must have docker
remote_environment:
    user: <username>
    host: <host_ip>
    # password in .env -> REMOTE_PASSWORD
    # remote_env_key in .env -> REMOTE_PASSWORD_KEY

# required
repository:
    url: <url>
    # personal access token in .env -> PERSONAL_ACCESS_TOKEN
    default_branch: <branch_name>

# Optional (defaults to all required)
approval:
    plan: required
    code: required
    tests: required

# required
task: """
# Task

task description

## Requirements
- list of requirments

## Acceptance Criteria
- List of acceptance criteria
"""

# Optional
reference_docs: 
    - <url_to_doc>
    - <local_path_to_doc>
```

**Note**: All secrets must be kept in .env in project dir including LLM key


### Schema Example Structure

file_path: `~/.config/daimon/schema`

```bash
planning.md
architecture.md
coding_standards.md
testing_policy.md
commit_rules.md
pr_format.md
```
**Note** 
- Schema is imutable during phase
- Schema gets updated locally per phase and is merged into main branch at the end
- Schema may be pulled from main branch into .config/schema
- Changes to schema produce schema_diff.patch

## Installation

### Developers

```bash
git clone daimon
```

### Users (not available yet)

```bash
pip install daimon-cli
```

## Execution Lifecycle

1. Validate
    a. remote connection
    b. remote docker
    c. repository credentials
    d. config integrity
2. package and transfer:
    a. zip project source
    b. zip schema constraints
    c. upload artifacts to remote host
3. env setup
    a. clone OpenHands agent runtime
    b. build docker image
    c. inject env variables
4. Phase 1: Planning
    a. generate structured plan
    b. open draft PR 
        - generates plan.md for approval
        if success:
            i. update schema
            ii. move to phase 2
        if modification:
            i. update schema
            ii. iterate again
        if rejected:
            i. update schema
            ii. move to phase 4
5. Phase 2: Code Execution
    a. apply modification plan
    b. run incremental tests
    c. run linting 
    d. run static analysis tests
    e. Update PR
        if success:
            i. update schema
            ii. move to phase 3
        if modifications:
            i. update schema
            ii. iterate
        if rejected:
            i. update schema
            ii. move back to phase 1

6. phase 3 - testing and validation
    a. Generate comprehensive unit tests
    b. write edge case tests where appropiate
    c. write integration tests convering all flows
    d. write scale tests
    e. run full test suite
        if tests fail and problem is with test:
            i. update schema
            ii. rewrite tests
            iii. iterate
        if tests fail and problem is with code execution
            i. update schema
            ii. move back to phase 2
        if all tests pass:
            i. update schema
            ii. write test report, add to logs
    f. Update PR
        if success:
            i. update schema
            ii. move to phase 4
        if modification:
            i. update schema
            ii. iterate
        if rejected:
            i. update schema
            ii. move back to phase 1
7. phase 4 - cleanup
    a. archive logs
    b. keep updated schema
    c. change MR / PR from draft to real
    d. remove remote container
    e. remove temp artifacts

## Logs and Observability

Example
```bash
.daimon_logs/
    run_<timestamp>/
        llm/
            prompts.jsonl
            responses.jsonl
        retrieval/
            queries.jsonl
            extracted_chunks.jsonl
        execution/
            stdout.log
            stderr.log
        git/
            diff.patch
            branch.json
        review/
        p   r_metadata.json
```
logs are also available in github or gitlab draft branches

## Security
- no direct pushes to human branches
- all changes via PR/MR
- secrets injected at runtime only via .env (not stored in git)
- secrets masked in logs
- remote container isolated
- schema versioned and hashed

## Roadmap
- Coach agent that updates schema every feedback cycle
- deep graph rag
- multi-layer rag extraction updated by schema_diff
- git approval confidence regression model
- task suggestor agent that can spawn tasks and spawn additional Daimon process
- researcher agent that can spawn resources for task suggestor agent.
- generalize schema approach for different use cases