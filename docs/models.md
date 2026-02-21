# Models
- primitives
    - query
    - memory
    - archive
    - actions
- directives
- listeners
- stack
- listener pool
- phase

## primitives

### query: str

> query is a text description of the immediate goal of the current node.  the output of the node should satisfy the query.

### archive: dict[str, list[str]]

- archive is an object that holds document_sets.  

#### document_set properties

- name: str
- hash: str
- version: str
- documents: list[Document]
- summery: Optional[str]
- keywords: Optional[list[str]]
- graph: Optional[Graph]
- alternative_index: Optional[Any]

#### Document Properties
- name: str
- hash: str
- type: Literal['memory','file_system','url']
- version: str 
- contents: str | Path | url
- locked: bool

#### archive methods

**Note**: all methods update document and document_set properties

- lookup
- copy - can copy all remote documents to file_system
- checkout - locks and unlocks document
- update - not available to remote, maybe copied
- add 
- remove

## memory

- memory is an object that holds rag objects over the archive documents

### rag properties
- name: str
- hash: str
- version: str
- locked: bool
- document_set: archive[document_set_name]
- embedding_model: embedding_model
- database_location: path
- chunking_model: chunking_model_object
- extraction_model: extraction_model_object

### memory methods

- extraction(rag_name: str, query:str) -> chunk extraction
- add_rag (
    rag_name: str, 
    document_set, 
    embedding_model = default, 
    chunking_model = default, 
    extraction_model = default
    )
- remove_rag(rag_name:str)

### rag_methods

**Note**: all rag update methods update version

- checkout - locks and unlocks rag
- add_document
- remove_document
- modify_document
- update_chunking_model
- update_extraction_model
- update embedding_model

### chunking_model
chunking model takes a document or set of documents and returns chunks.
chunking models are python functions that are decorated using chunking_model and registered in the chunking model registry

#### k_character_chunking_model: default
- chunks every k characters with s character overlap
- metadata expose
    - k: int
    - s: int

#### similar embedding sliding window chunking model
- sliding window over text, chunks based on embedding vector difference between two windows using cutoff C
- metadata expose
    - max_characters: int
    - difference cuttoff: int or %
    - window_size: int

#### Semantic Hiarchy chunking 
#### structured_text chunking - python
#### structured_text chunking - markdown
#### structured_text chunking - yaml
#### structured_text chunking - 
#### keyword indexed chunking

### extraction model
takes a query, and large set of chunks and returns a list of strings that optimally provides context for the query.  extraction models are python functions that are decorated with extraction_model and are registered to the extraction_model registry

### similarity search extraction model: default
- vectorizes the query
- performs similarity search over the vector database and returns top k chunks
- metadata expose:
    - k: int

### keyword extraction model
### rerank extraction model
### graph extraction model
### alternative index extraction model
### local SLM assisted extraction model
### query enriched extraction model
### multi-step chain of though extraction
### reasoning extraction model 

## actions
actions are python functions that are decorated with action and are registered to the action model registry. 

### action properties
- name :given in decorator
- description: given in doc string
- function 

### Action list
- LLM prompt
- SLM prompt
- LLM chain-of-thought
- archive lookup
- archive copy 
- archive checkout
- archive update 
- archive add 
- archive remove
- memory - add rag
- memory - remove rag
- rag add_document
- rag remove_document
- rag modify_document
- rag update_chunking_model
- rag update_extraction_model
- rag update embedding_model
- os: execute_file
- os: shell_cmd
- os: pip install
- os: read_stdout
- os: read_stderr
- os: remote_shell_cmd: ssh
- git: add
- git: rm
- git: commit 
- git: push
- gh: PR
- gh: get_code_review
- gh: write_code_review_comments
- daimon: emit directive top
- daimon: emit directive bottom
- daimon: remove directive
- daimon: emit listener
- daimon: remove listener
- http: get request
- http: post request
- http: del request
- python function

## directives: primitive wrapper
directives are objects that provide necissary primitives to agents in order to recieve desired result

### directive properties
- agent: str
- query: Query
- actions_list:[Actions] *automatic
- status: Literal["pending", "in_process","completed"]

### directive methods
- do_action
- extract_rag
- inject_document
- evaluate_success_criteria(success_criteria: str) ->  bool

### listener:
a special directive that runs async / multi-threaded in the listener pool and emits directives to the stack.
all listeners inherit from directives

#### poll_listener:
a listener that is polled periodically and emits a directive to the stack upon sucesss criteria.  

### poll listener properties:
- success_criteria: str
- poll_cycle_time: int

#### web hook listener:
a listener that exposes a web server endpoint and emits a directive to the stack upon rest recieve

#### web hook listener properties:
- endpoint: str
- timeout_time: Optional[int]
- success_criteria: Optional[str]

## stack 
is stack of directives that are emmited during the workflow process, popped off the top and consumed in order.

## listener Pool
async multi-threaded pool of listener directives that are emmited during workflow process and emit directives and listeners.


## Phases
a phase is an initial stack of directives that hold very high level goals.
in general the following phases are initialized
1. planning
2. coding
3. testing
4. review