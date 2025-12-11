---
sidebar_position: 3
title: Architecture
description: System architecture and data flow diagrams for Claude Agent Manager
---

# Architecture

This document provides comprehensive architecture diagrams showing how all components of the agent ecosystem work together, from the skillchain entry point through to Claude AI execution.

## System Overview

```mermaid
graph TB
    subgraph "Entry Points"
        SC["/skillchain:start"]
        CLI["claude-agent CLI"]
        API["Python API"]
    end

    subgraph "Skillchain System"
        direction TB
        ROUTER[Skillchain Router<br/>start.md]
        BP[Blueprints<br/>12 pre-configured]
        CAT[Category Orchestrators<br/>12 domains]
        DEL[Delegated Orchestrator<br/>4+ skills]
        REG[Skill Registries<br/>76 skills, 10 domains]
    end

    subgraph "Agent Manager Package"
        direction TB
        subgraph "Core Layer"
            DET[AgentDetector]
            EVT[EventEmitter]
            PARSER[StreamJsonParser]
            PM[ProcessManager]
        end

        subgraph "Session Layer"
            SM[SessionManager]
            SW[SessionWatcher]
            SS[SessionStorage]
        end

        subgraph "Orchestration Layer"
            COORD[AgentCoordinator]
            TQ[TaskQueue]
            CB[CircuitBreaker]
        end

        subgraph "Skillchain Layer"
            SE[SkillchainExecutor]
            PRG[ProgressManager]
            RGM[RegistryManager]
        end
    end

    subgraph "Execution"
        CC[Claude Code CLI]
        CLAUDE[Claude AI]
        FS[Session Files<br/>~/.claude/projects/]
    end

    SC --> ROUTER
    CLI --> PM
    API --> PM

    ROUTER --> BP
    ROUTER --> CAT
    ROUTER --> DEL
    ROUTER --> REG

    BP --> SE
    CAT --> SE
    DEL --> SE

    SE --> RGM
    SE --> PRG
    SE --> PM

    COORD --> TQ
    COORD --> CB
    COORD --> PM

    PM --> DET
    PM --> EVT
    PM --> PARSER
    PM --> SM

    SM --> SS
    SW --> FS

    DET --> CC
    PM --> CC
    CC --> CLAUDE
    CC --> FS
```

## Component Data Flow

### Process Execution Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant PM as ProcessManager
    participant DET as AgentDetector
    participant Parser as StreamJsonParser
    participant EVT as EventEmitter
    participant CC as Claude Code CLI
    participant AI as Claude AI

    App->>PM: execute(ProcessConfig)
    PM->>DET: detect()
    DET-->>PM: DetectionResult

    PM->>PM: build_args()
    PM->>PM: build_env()

    PM->>CC: spawn(claude, args)
    PM->>EVT: emit(PROCESS_SPAWNED)

    CC->>AI: API Request

    loop Streaming Response
        AI-->>CC: response chunk
        CC-->>PM: stdout stream-json
        PM->>Parser: process_chunk(data)

        alt system init
            Parser->>EVT: emit(SESSION_STARTED)
        else assistant message
            Parser->>EVT: emit(MESSAGE_CHUNK)
        else tool use
            Parser->>EVT: emit(TOOL_CALLED)
        else result
            Parser->>EVT: emit(MESSAGE_RECEIVED)
        end
    end

    AI-->>CC: complete
    CC-->>PM: exit(0)
    PM->>EVT: emit(SESSION_COMPLETE)
    PM-->>App: ProcessResult
```

### Skillchain Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant SC as /skillchain:start
    participant Router as Skillchain Router
    participant Orch as Orchestrator
    participant SE as SkillchainExecutor
    participant PM as ProcessManager
    participant Claude as Claude AI

    User->>SC: /skillchain:start "dashboard with charts"
    SC->>Router: route(goal)
    Router->>Router: detect domains
    Router->>Router: match blueprint
    Router->>Router: load skills from registry

    alt 1-3 skills
        Router->>Orch: standard execution
    else 4+ skills
        Router->>Orch: delegated execution
    end

    Orch->>SE: execute(skills, project_path)
    SE->>SE: create .skillchain-progress.json

    loop For each skill
        SE->>PM: execute(skill_prompt)
        PM->>Claude: spawn agent
        Claude-->>PM: response
        PM-->>SE: SkillExecutionResult
        SE->>SE: update progress
    end

    SE-->>Orch: SkillchainResult
    Orch-->>Router: complete
    Router-->>User: summary
```

## Module Architecture

### Core Module

```mermaid
classDiagram
    class EventEmitter {
        -_handlers: Dict[EventType, List]
        +on(event_type) decorator
        +emit(event) async
        +off(event_type, handler)
        +clear()
    }

    class EventType {
        <<enumeration>>
        SESSION_STARTED
        SESSION_COMPLETE
        MESSAGE_CHUNK
        MESSAGE_RECEIVED
        TOOL_CALLED
        USAGE_UPDATE
        ...
    }

    class Event {
        +type: EventType
        +session_id: str
        +timestamp: datetime
        +data: Dict
    }

    class AgentDetector {
        -_cached_result: DetectionResult
        +detect() async DetectionResult
        -_check_path(path) bool
        -_get_version(path) str
    }

    class DetectionResult {
        +available: bool
        +path: str
        +version: str
        +error: str
    }

    class StreamJsonParser {
        -_session_id: str
        -_claude_session_id: str
        -_usage: UsageStats
        -_buffer: str
        +process_chunk(chunk) List[ParsedMessage]
        +process_line(line) ParsedMessage
    }

    class ProcessManager {
        -_detector: AgentDetector
        -_emitter: EventEmitter
        -_active_processes: Dict
        +execute(config) ProcessResult
        +execute_streaming(config) AsyncIterator
        +interrupt(session_id)
    }

    EventEmitter --> EventType
    EventEmitter --> Event
    AgentDetector --> DetectionResult
    ProcessManager --> AgentDetector
    ProcessManager --> EventEmitter
    ProcessManager --> StreamJsonParser
```

### Session Module

```mermaid
classDiagram
    class SessionState {
        <<enumeration>>
        IDLE
        BUSY
        ERROR
        CLOSED
    }

    class Message {
        +role: str
        +content: str
        +timestamp: datetime
        +tool_calls: List
        +usage: UsageStats
    }

    class Session {
        +id: str
        +cwd: str
        +state: SessionState
        +claude_session_id: str
        +messages: List[Message]
        +total_cost_usd: float
        +created_at: datetime
        +updated_at: datetime
        +metadata: Dict
    }

    class SessionManager {
        -_emitter: EventEmitter
        -_storage: SessionStorage
        -_process_manager: ProcessManager
        -_sessions: Dict[str, Session]
        +create_session(cwd) Session
        +get_session(id) Session
        +execute(session_id, prompt) ProcessResult
        +list_sessions() List[Session]
        +delete_session(id) bool
    }

    class SessionWatcher {
        -_cwd: str
        -_emitter: EventEmitter
        -_poll_interval: float
        -_running: bool
        +start() async
        +stop() async
        +list_sessions() List[SessionInfo]
    }

    class SessionStorage {
        -_storage_dir: Path
        +save(session) Path
        +load(session_id) Session
        +delete(session_id) bool
        +list_all() List[str]
    }

    Session --> SessionState
    Session --> Message
    SessionManager --> Session
    SessionManager --> SessionStorage
    SessionManager --> ProcessManager
    SessionWatcher --> SessionInfo
```

### Orchestration Module

```mermaid
classDiagram
    class AgentRole {
        <<enumeration>>
        CODER
        REVIEWER
        TESTER
        PLANNER
        RESEARCHER
    }

    class AgentConfig {
        +name: str
        +role: AgentRole
        +cwd: str
        +model: str
        +timeout: float
        +metadata: Dict
    }

    class AgentResult {
        +agent_name: str
        +task: str
        +success: bool
        +result: ProcessResult
        +duration_seconds: float
        +error: str
    }

    class TaskPriority {
        <<enumeration>>
        CRITICAL = 0
        HIGH = 1
        NORMAL = 2
        LOW = 3
        BACKGROUND = 4
    }

    class Task {
        +id: str
        +priority: TaskPriority
        +payload: Dict
        +created_at: datetime
    }

    class TaskQueue {
        -_heap: List
        -_lock: Lock
        +put(task) async
        +get() async Task
        +peek() Task
        +size() int
    }

    class CircuitState {
        <<enumeration>>
        CLOSED
        OPEN
        HALF_OPEN
    }

    class CircuitBreaker {
        -_state: CircuitState
        -_failure_count: int
        -_failure_threshold: int
        -_recovery_timeout: float
        +record_success()
        +record_failure()
        +can_execute() bool
        +state: CircuitState
    }

    class AgentCoordinator {
        -_emitter: EventEmitter
        -_agents: Dict[str, AgentConfig]
        -_sessions: Dict[str, Session]
        -_semaphore: Semaphore
        +register_agent(config)
        +execute_task(agent, task) AgentResult
        +execute_pipeline(tasks) List[AgentResult]
        +shutdown() async
    }

    AgentConfig --> AgentRole
    AgentResult --> ProcessResult
    Task --> TaskPriority
    CircuitBreaker --> CircuitState
    AgentCoordinator --> AgentConfig
    AgentCoordinator --> TaskQueue
    AgentCoordinator --> CircuitBreaker
```

### Skillchain Module

```mermaid
classDiagram
    class SkillInfo {
        +name: str
        +domain: str
        +invocation: str
        +description: str
        +keywords: List[str]
        +dependencies: List[str]
        +priority: int
        +defaults: Dict
    }

    class RouteResult {
        +goal: str
        +domains: List[str]
        +primary_domain: str
        +matched_skills: List[SkillInfo]
        +blueprint: str
        +confidence: float
    }

    class RegistryManager {
        -_repo_root: Path
        -_registries: Dict
        -_skills: Dict[str, SkillInfo]
        +load_registries()
        +get_skill(name) SkillInfo
        +get_skills_by_domain(domain) List
        +route_goal(goal) RouteResult
    }

    class SkillProgress {
        +name: str
        +invocation: str
        +status: str
        +agent_id: str
        +files_created: List[str]
        +decisions: Dict
        +error: str
    }

    class ProgressFile {
        +session_id: str
        +goal: str
        +blueprint: str
        +maturity: str
        +skills: List[SkillProgress]
        +execution: ExecutionState
    }

    class ProgressManager {
        +create(project_path, goal, skills) ProgressFile
        +save(progress) Path
        +load(project_path) ProgressFile
        +update_skill(progress, index, ...)
        +get_resumable_skills(progress) List
    }

    class SkillExecutionResult {
        +skill_name: str
        +invocation: str
        +success: bool
        +files_created: List[str]
        +decisions: Dict
        +cost_usd: float
        +duration_seconds: float
    }

    class SkillchainExecutor {
        -_repo_root: Path
        -_emitter: EventEmitter
        -_process_manager: ProcessManager
        -_registry: RegistryManager
        -_progress_mgr: ProgressManager
        +execute(goal, project_path) SkillchainResult
        +resume(project_path) SkillchainResult
        +route(goal) RouteResult
    }

    RegistryManager --> SkillInfo
    RegistryManager --> RouteResult
    ProgressFile --> SkillProgress
    ProgressManager --> ProgressFile
    SkillchainExecutor --> RegistryManager
    SkillchainExecutor --> ProgressManager
    SkillchainExecutor --> SkillExecutionResult
```

## Integration Architecture

### Skillchain + Agent Manager Integration

```mermaid
graph TB
    subgraph "Skillchain Commands"
        START["/skillchain:start"]
        BP["/skillchain:blueprints:*"]
        CAT["/skillchain:categories:*"]
    end

    subgraph "Skillchain Data"
        REG[Skill Registries<br/>10 domain YAML files]
        GRAPH[Skill Graph<br/>Dependencies]
        SCHEMA[Progress Schema<br/>Chain Context]
    end

    subgraph "Agent Manager"
        SE[SkillchainExecutor]
        RGM[RegistryManager]
        PGM[ProgressManager]
        PM[ProcessManager]
    end

    subgraph "Execution"
        CC[Claude Code CLI]
        PRG[.skillchain-progress.json]
    end

    START --> SE
    BP --> SE
    CAT --> SE

    REG --> RGM
    GRAPH --> RGM

    SE --> RGM
    SE --> PGM
    SE --> PM

    PGM --> PRG
    PM --> CC

    SCHEMA --> PGM
```

### File System Layout

```
~/.claude/
├── projects/                    # Session files by project
│   └── -Users-you-project/      # Encoded project path
│       ├── abc123.jsonl         # Session 1
│       └── def456.jsonl         # Session 2
│
└── skillchain-data/             # Skillchain data (NOT commands)
    ├── registries/              # Skill definitions
    └── shared/                  # Schemas, protocols

~/.claude_agent_manager/
└── sessions/                    # Agent manager persistence
    └── session-abc123.json

/your/project/
└── .skillchain-progress.json    # Active skillchain state
```

## Event Flow

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> Spawning : execute()
    Spawning --> Initializing : process started
    Initializing --> Processing : init received

    Processing --> Streaming : assistant message
    Processing --> ToolCalling : tool_use detected
    Processing --> Complete : result received

    Streaming --> Processing : chunk processed
    ToolCalling --> Processing : tool result

    Complete --> Idle : cleanup

    state Processing {
        [*] --> Parsing
        Parsing --> EmittingEvents
        EmittingEvents --> UpdatingUsage
        UpdatingUsage --> [*]
    }
```

## Next Steps

- [Skillchain Integration](./skillchain-integration) - Deep dive into skill execution
- [Real-World Usage](./real-world-usage) - Practical examples
- [CLI Reference](./cli-reference) - Command-line interface
