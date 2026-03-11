# Common Knowledge — Index & Quick Guide

Everyday guides shared by all AnimaWorks Animas.
When you are stuck or unsure of a procedure, use this file to identify the relevant document,
then read it with `read_memory_file(path="common_knowledge/...")`.

> 💡 Detailed technical references (file specifications, model configuration, authentication setup, use cases, etc.) have been moved to `reference/`.
> Index: `reference/00_index.md`

---

## Quick Guide — When You Are Stuck

### Communication

| Problem | Reference |
|---------|-----------|
| Don't know how to use Board (shared channels) | `communication/board-guide.md` |
| Don't know how to notify humans | `communication/call-human-guide.md` |
| Message sending was limited | `communication/sending-limits.md` |
| Don't know how to send messages | `reference/communication/messaging-guide.md` (technical reference) |
| Don't know how to give instructions or report | `reference/communication/instruction-patterns.md` / `reference/communication/reporting-guide.md` (technical reference) |
| Don't know how to configure Slack bot tokens | `reference/communication/slack-bot-token-guide.md` (technical reference) |

### Organization & Hierarchy

| Problem | Reference |
|---------|-----------|
| Don't know communication rules across hierarchy | `organization/hierarchy-rules.md` |
| Want to check roles and responsibilities | `reference/organization/roles.md` (technical reference) |
| Don't know the org structure or who to contact | `reference/organization/structure.md` (technical reference) |

### Tasks & Operations

| Problem | Reference |
|---------|-----------|
| Want to use the task board (human-facing dashboard) | `operations/task-board-guide.md` |
| Don't know how to run long-running tools | `operations/background-tasks.md` |
| Don't know how to manage tasks | `reference/operations/task-management.md` (technical reference) |
| Don't know how to configure Heartbeat or cron | `reference/operations/heartbeat-cron-guide.md` (technical reference) |
| Want to change project settings | `reference/operations/project-setup.md` (technical reference) |

### Tools, Models & Technical

| Problem | Reference |
|---------|-----------|
| Don't know how to use or call tools | `reference/operations/tool-usage-overview.md` (technical reference) |
| Don't know how to choose or change models | `reference/operations/model-guide.md` (technical reference) |
| Want to change Mode S authentication method | `reference/operations/mode-s-auth-guide.md` (technical reference) |
| Don't know how to set up or use voice chat | `reference/operations/voice-chat-guide.md` (technical reference) |

### Understanding Yourself

| Problem | Reference |
|---------|-----------|
| Want to know what an Anima is | `anatomy/what-is-anima.md` |
| Want to understand how memory works | `reference/anatomy/memory-system.md` (technical reference) |
| Want to understand your configuration files | `reference/anatomy/anima-anatomy.md` (technical reference) |

### Troubleshooting

| Problem | Reference |
|---------|-----------|
| Tools or commands don't work / getting errors | `reference/troubleshooting/common-issues.md` (technical reference) |
| Task is blocked / unsure what to do | `reference/troubleshooting/escalation-flowchart.md` (technical reference) |
| Gmail tool credential setup not working | `reference/troubleshooting/gmail-credential-setup.md` (technical reference) |

### Security

| Problem | Reference |
|---------|-----------|
| Concerned about external data reliability | `security/prompt-injection-awareness.md` |

### Use Cases

| Problem | Reference |
|---------|-----------|
| Want to know what AnimaWorks can do | `reference/usecases/usecase-overview.md` (technical reference) |

**None of the above?** → Search with `search_memory(query="keyword", scope="common_knowledge")`

---

## Document Listing

### anatomy/ — Anima Anatomy & Components

| File | Description |
|------|-------------|
| `what-is-anima.md` | What is an Anima (concept, design philosophy, lifecycle, execution paths) |

### organization/ — Organization & Structure

| File | Description |
|------|-------------|
| `hierarchy-rules.md` | Rules across hierarchy (communication paths, supervisor tools, emergency exceptions) |

### communication/ — Communication

| File | Description |
|------|-------------|
| `board-guide.md` | Board (shared channels) guide (post_channel / read_channel usage, posting rules) |
| `call-human-guide.md` | Human notification guide (call_human usage, receiving replies, notification channels) |
| `sending-limits.md` | Sending limits in detail (3-layer rate limit, 30/h and 100/day caps, cascade detection) |

### operations/ — Operations & Task Management

| File | Description |
|------|-------------|
| `task-board-guide.md` | Task board (human-facing dashboard) — structure and operational guidelines |
| `background-tasks.md` | Background task guide (using submit, when to use it, how to get results) |

### security/ — Security

| File | Description |
|------|-------------|
| `prompt-injection-awareness.md` | Prompt injection defense (trust levels, boundary tags, handling untrusted data) |

---

## Keyword Index

| Keywords | Reference |
|----------|-----------|
| Board, channel, post_channel, read_channel | `communication/board-guide.md` |
| DM history, read_dm_history, past conversation | `communication/board-guide.md` |
| call_human, human notification, notify human | `communication/call-human-guide.md` |
| rate limit, sending limit, 30/hour, 100/day, one-round rule | `communication/sending-limits.md` |
| message, send_message, reply, thread, inbox | `reference/communication/messaging-guide.md` |
| instruction, delegation, task request | `reference/communication/instruction-patterns.md` |
| report, daily report, summary, escalation | `reference/communication/reporting-guide.md` |
| Slack, bot token, SLACK_BOT_TOKEN, not_in_channel | `reference/communication/slack-bot-token-guide.md` |
| hierarchy, communication path, org_dashboard, ping_subordinate | `organization/hierarchy-rules.md` |
| delegate_task, task delegation, task_tracker | `organization/hierarchy-rules.md`, `reference/operations/task-management.md` |
| role, responsibility, speciality, specialty | `reference/organization/roles.md` |
| organization, supervisor, subordinate, peer | `reference/organization/structure.md` |
| task board, dashboard, human-facing | `operations/task-board-guide.md` |
| background, submit, long-running tool | `operations/background-tasks.md` |
| task, current_task, pending, progress, priority | `reference/operations/task-management.md` |
| add_task, task queue, plan_tasks, TaskExec | `reference/operations/task-management.md` |
| Heartbeat, heartbeat, periodic check | `reference/operations/heartbeat-cron-guide.md` |
| cron, schedule, scheduled task | `reference/operations/heartbeat-cron-guide.md` |
| tool, animaworks-tool, MCP, mcp__aw__, skill | `reference/operations/tool-usage-overview.md` |
| execution mode, S-mode, A-mode, B-mode, C-mode | `reference/operations/tool-usage-overview.md` |
| config, status.json, SSoT, reload, settings | `reference/operations/project-setup.md` |
| model, models.json, credential, set-model, context window | `reference/operations/model-guide.md` |
| background_model, background model, cost optimization | `reference/operations/model-guide.md` |
| Mode S, authentication, API direct, Bedrock, Vertex AI, Max plan | `reference/operations/mode-s-auth-guide.md` |
| voice, STT, TTS, VOICEVOX, ElevenLabs | `reference/operations/voice-chat-guide.md` |
| WebSocket, /ws/voice, barge-in, VAD, PTT | `reference/operations/voice-chat-guide.md` |
| Anima, self, anatomy, composition, lifecycle | `anatomy/what-is-anima.md` |
| memory, episodes, knowledge, procedures, skills | `reference/anatomy/memory-system.md` |
| Priming, RAG, Consolidation, Forgetting | `reference/anatomy/memory-system.md` |
| search_memory, write_memory_file, memory search | `reference/anatomy/memory-system.md` |
| identity, injection, personality, guidelines, immutable, mutable | `reference/anatomy/anima-anatomy.md` |
| permissions.md, bootstrap, heartbeat.md, cron.md | `reference/anatomy/anima-anatomy.md` |
| prompt injection, trust, untrusted, boundary tag | `security/prompt-injection-awareness.md` |
| error, problem, not working, permission, blocked command | `reference/troubleshooting/common-issues.md` |
| flowchart, decision, unsure, urgent, security | `reference/troubleshooting/escalation-flowchart.md` |
| Gmail, token.json, OAuth, pickle | `reference/troubleshooting/gmail-credential-setup.md` |
| tier, tiered, T1, T2, T3, T4 | `reference/troubleshooting/common-issues.md` |
| use case, examples, what can it do | `reference/usecases/usecase-overview.md` |

---

## How to Use

```
# Search by keyword
search_memory(query="message sending", scope="common_knowledge")

# Specify path directly
read_memory_file(path="common_knowledge/communication/board-guide.md")

# Read a technical reference
read_memory_file(path="reference/anatomy/anima-anatomy.md")

# Reference this file
read_memory_file(path="common_knowledge/00_index.md")
```
