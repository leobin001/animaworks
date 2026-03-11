# Reference — Technical Reference Index

Detailed technical specifications and admin configuration guides for AnimaWorks.
Not indexed by RAG. Use `read_memory_file(path="reference/...")` to read directly when needed.

## How to Access

```
read_memory_file(path="reference/00_index.md")          # This index
read_memory_file(path="reference/anatomy/anima-anatomy.md")  # Example
```

## Categories

### anatomy/ — Structure & Architecture

| File | Content |
|------|---------|
| `anima-anatomy.md` | Complete guide to Anima configuration files (roles, change rules, encapsulation) |
| `memory-system.md` | Memory system details (memory types, RAG, Priming, Consolidation, Forgetting) |

### communication/ — Messaging & Integration

| File | Content |
|------|---------|
| `messaging-guide.md` | Full messaging reference (send_message parameters, thread management, 1-round rule) |
| `instruction-patterns.md` | Instruction pattern library (clear instructions, delegation patterns, progress checks) |
| `reporting-guide.md` | Reporting & escalation methods (timing, format, urgent vs routine) |
| `slack-bot-token-guide.md` | Slack bot token configuration (per-Anima vs shared) |

### internals/ — Framework Internals

| File | Content |
|------|---------|
| `common-knowledge-access-paths.md` | 5 access paths for common_knowledge and RAG indexing mechanism |

### operations/ — Admin & Operations Setup

| File | Content |
|------|---------|
| `project-setup.md` | Project initial setup (`animaworks init`, directory structure) |
| `task-management.md` | Task management reference (add_task / update_task / plan_tasks / delegate_task full parameters) |
| `heartbeat-cron-guide.md` | Periodic execution details (heartbeat mechanism, cron syntax, hot reload, self-update) |
| `tool-usage-overview.md` | Tool usage reference (S/A/B/C mode tool systems, invocation methods) |
| `model-guide.md` | Model selection, execution modes, context window details |
| `mode-s-auth-guide.md` | Mode S authentication modes (API/Bedrock/Vertex/Max) |
| `voice-chat-guide.md` | Voice chat architecture, STT/TTS, installation |

### organization/ — Organization Structure

| File | Content |
|------|---------|
| `structure.md` | Organization data sources, supervisor/speciality resolution |
| `roles.md` | Roles and responsibilities (top-level / middle management / execution Anima duties) |

### troubleshooting/ — Troubleshooting

| File | Content |
|------|---------|
| `common-issues.md` | Common issues and solutions (message delivery, rate limits, permissions, tools, context) |
| `escalation-flowchart.md` | Decision flowchart (problem classification, urgency assessment, escalation targets) |
| `gmail-credential-setup.md` | Gmail Tool OAuth credential setup procedure |

### usecases/ — Use Case Guides

| File | Content |
|------|---------|
| `usecase-overview.md` | What AnimaWorks can do, getting started, full theme list |
| `usecase-communication.md` | Communication automation (chat/email monitoring, escalation, regular contacts) |
| `usecase-development.md` | Software development support (code review, CI/CD monitoring, Issue implementation) |
| `usecase-monitoring.md` | Infrastructure/service monitoring (health checks, resource monitoring, SSL, logs) |
| `usecase-secretary.md` | Secretary/admin support (schedule management, coordination, daily reports) |
| `usecase-research.md` | Research & analysis (web search, competitive analysis, market research, reports) |
| `usecase-knowledge.md` | Knowledge management & documentation (procedure creation, FAQ building) |
| `usecase-customer-support.md` | Customer support (first response, auto-FAQ, escalation management) |

## Related

- Everyday practical guides → `common_knowledge/00_index.md`
- Common skills → `common_skills/`
