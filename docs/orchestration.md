# prompts
is a type of structured document set that holds markdown prompt document templates for each of the agents.
the templates have dynamic fields which allow for memory, document extraction injection or action 

### example document

```markdown
# planner

Role:
You are responsible for generating structured execution plans.

Constraints:
- Must obey schema policies.
- Must output JSON plan format.
- Must define atomic steps.

## Schema Policy:
{rag:schema}

## Project Code:
{rag:project_code}

## Plan:
{rag:planner}

## Memory:
{rag:tracer}
```

# Orchestration
is a type of structured document set that holds a yaml serialized representation of agent prompts and action maps, as well as directive emmiters.  this mapping is used in the inital stack to provide agent prompts and actions, and also as a condition to generate new directives to populate the stack.

#### Example Document

name: orchestration.yml

```yml
agents:
    - name: planner
    prompts: 
        - <document_set_name>:<document_name>
    actions:
        - <action_name>

    - name: coder
    prompts: 
        - <document_set_name>:<document_name>
    actions:
        - <action_name>

    - name: tester
    prompts: 
        - <document_set_name>:<document_name>
    actions:
        - <action_name>

    - name: reviewer
    prompts: 
        - <document_set_name>:<document_name>
    actions:
        - <action_name>

directive_emmiters:
    - from: planner
    to: coder
    success_criteria: str
    
    - from: planner
    to: planner
    success_criteria: str

  - from: coder
    to: tester
    success_criteria: str

  - from: coder
    to: planner
    success_criteria: str
  - from: tester
    to: reviewer
    success_criteria: str

  - from: tester
    to: coder
    success_criteria: str

  - from: reviewer
    to: cleanup
    success_criteria: str
```


