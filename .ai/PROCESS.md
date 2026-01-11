# Development Process Overview

## Purpose
This document defines the **agent-based development process** for our projects.
It provides a **constitutional framework** for both human developers and AI agents, ensuring predictable, high-quality delivery of Telegram bots, Mini Apps, AI integrations, RAG pipelines, and Docker-based environments.

This is **not a step-by-step tutorial**.
It describes the rules, invariants, and responsibilities that govern all actions within the repository.

---

## Core Concepts

### Roles (`.claude/agents/`)
Each agent or human participant has a clearly defined responsibility:

- **Product Owner** (`product_owner.md`) — Translates client needs into actionable requirements, defines user stories and acceptance criteria
- **System Architect** (`architect.md`) — Designs component boundaries, data flows, and system architecture
- **Tech Lead** (`tech_lead.md`) — **Final technical authority**, validates architecture, approves/rejects plans, manages scope
- **Backend Developer** (`backend_dev.md`) — Implements handlers, services, models following approved architecture
- **AI Engineer** (`ai_engineer.md`) — Implements LLM integrations, RAG pipelines, prompt versioning
- **DevOps Engineer** (`devops.md`) — Manages docker-compose, health checks, deployments
- **QA Engineer** (`qa.md`) — Tests from user perspective, validates acceptance criteria
- **Code Reviewer** (`reviewer.md`) — Enforces code quality, maintainability, and framework standards

> **Rule:** No agent can operate outside its role unless explicitly authorized by a workflow or command.

### Commands (`.claude/commands/`)
Commands define **atomic operations** that orchestrate agents through the development lifecycle:

**Core Cycle:**
1. **`/discovery`** — Understand what needs to be built (Product Owner + Architect)
2. **`/plan`** — Produce implementation-ready architecture (Architect + Tech Lead approval)
3. **`/implement`** — Build features following approved plan (Backend Dev + AI Engineer)

**Specialized:**
4. **`/integrate_ai`** — Add/modify AI functionality with prompt versioning (AI Engineer + Tech Lead)
5. **`/test`** — Validate correctness from user perspective (QA)
6. **`/review`** — Ensure code quality and standards compliance (Reviewer)
7. **`/refactor`** — Improve code quality without changing behavior (Tech Lead + Backend Dev)
8. **`/ship`** — Approve and deploy to production (Tech Lead + DevOps)

> **Rule:** Commands act as **quality gates**. Actions cannot bypass these gates.

### Standards (`.claude/standards/`)
Technology-specific best practices and patterns:

- **`aiogram.md`** — Telegram bot patterns (FSM, handlers, middleware, dependency injection)
- **`docker.md`** — Docker-compose infrastructure (health checks, volumes, migrations, zero manual setup)
- **`telegram.md`** — Telegram API integration (rate limits, webhooks, Mini Apps, deep links)
- **`rag.md`** — RAG systems (chunking, embeddings, prompt versioning, observability)
- **`testing.md`** — Test-driven development (unit/integration/e2e, coverage >80%, docker-based)

> **Rule:** All implementations must follow relevant standards from `.claude/standards/`.

### Workflows (`.claude/workflows/`)
Workflows define allowed **execution sequences** of commands for common scenarios:
- `tg_bot_feature.md` — Telegram bot feature workflow
- `tg_mini_app.md` — Mini app workflow
- `ai_feature.md` — AI feature workflow
- `hotfix.md` — Emergency hotfix workflow

> **Rule:** Workflows are templates. Deviations must be explicitly approved by Tech Lead.

---

## Process Invariants

1. **Architecture before implementation** — No code is written before Tech Lead approves the plan (`/plan`).
2. **Gated execution** — All critical actions must pass through commands and workflows.
3. **Role boundaries** — Each agent acts only within its defined role.
4. **Testing and review are mandatory** — Features cannot ship without QA verification (`/test`) and reviewer approval (`/review`).
5. **No hidden assumptions** — All design decisions, constraints, and dependencies must be documented.
6. **Docker-first mindset** — The final working environment is always defined in `docker-compose.yml`. Cold start (`docker-compose down -v && docker-compose up`) must work.
7. **AI prompt governance** — All AI prompts are versioned (no magic strings), logged with metadata (tokens, cost, latency), and tested with mocked responses.
8. **No hardcoded secrets** — All configuration via environment variables, `.env.example` must be complete and documented.
9. **Separation of concerns** — Handlers → Services → Repositories. No business logic in handlers.
10. **Structured logging** — All operations logged as JSON with context (user_id, request_id, etc.).

---

## Development Lifecycle

### Typical Feature Flow

```
/discovery → /plan → /implement → /integrate_ai (if AI) → /test → /review → /ship
    ↓          ↓          ↓              ↓                   ↓       ↓        ↓
 Problem    Tech Lead  Backend Dev   AI Engineer           QA    Reviewer  DevOps
  Analysis  Approval   + AI Eng      Prompt Version              Approval  Validation
```

### Quality Gates

| Gate | Owner | Blocks If |
|------|-------|-----------|
| **Plan Approval** | Tech Lead | Architecture violates standards, unclear scope |
| **Test Pass** | QA | Acceptance criteria not met, blocker bugs found |
| **Review Approval** | Reviewer | Code quality issues, security vulnerabilities, prompts not versioned |
| **Ship Approval** | Tech Lead + DevOps | Docker validation fails, tests failing, secrets hardcoded |

### Gate Authority

- **Tech Lead** can reject plans and block shipping (final technical authority)
- **QA** can block shipping if blocker issues found
- **Reviewer** can block shipping if code quality issues found
- **DevOps** validates docker-compose before shipping

---

## Human-in-the-loop

Humans are required to:
- Initiate commands and workflows
- Approve critical decisions (architecture approval in `/plan`, ship approval in `/ship`)
- Override AI agents when necessary
- Monitor adherence to standards and invariants
- Make business decisions (scope, priorities, timelines)

> **Rule:** AI can assist, but **final authority always resides with humans** for:
> - Architecture approval (Tech Lead)
> - Shipping decisions (Tech Lead + DevOps)
> - Business priorities (Product Owner)

---

## Framework Principles

### From CLAUDE.md

1. **No "vibe coding"** — Architecture before implementation, always
2. **Tests and observability are mandatory** — >80% coverage, structured JSON logs
3. **Docker is the source of truth** — Code must run in docker-compose
4. **Follow role boundaries** — Defined in `.claude/agents/`
5. **Never change architecture without `/plan`** — No shortcuts
6. **Prefer simple, explicit solutions** — Avoid over-engineering
7. **Ask for clarification only if blocking** — Don't make assumptions

### Definition of Done

A feature is "done" when:
- [ ] Code works in docker-compose (cold start tested)
- [ ] No hardcoded secrets (all in `.env.example`)
- [ ] Clear separation of layers (handlers → services → repositories)
- [ ] All tests pass (>80% coverage)
- [ ] QA approved (`/test` passed)
- [ ] Reviewer approved (`/review` passed)
- [ ] Tech Lead approved (`/ship` approved)
- [ ] All AI prompts versioned (if AI feature)
- [ ] Structured logging implemented
- [ ] Documentation updated (`.env.example`, README if needed)

---

## Common Anti-Patterns

**Process Violations:**
- ❌ Skipping planning or architecture validation
- ❌ Implementing without Tech Lead approval on plan
- ❌ Shipping without `/test` and `/review` passing
- ❌ Ignoring workflow-defined command sequences
- ❌ Mixing roles in a single step (e.g., Backend Dev making architectural changes)

**Technical Violations:**
- ❌ Hardcoding secrets or environment configurations
- ❌ No health checks in docker-compose
- ❌ Business logic in handlers
- ❌ AI prompts as magic strings (not versioned)
- ❌ Silent failures (no error handling or logging)
- ❌ Skipping tests or accepting <80% coverage

**AI-Specific Violations:**
- ❌ Prompts not versioned
- ❌ No retry logic or fallback behavior
- ❌ AI requests not logged (tokens, cost, latency)
- ❌ No testing with mocked AI responses
- ❌ Cost implications not documented

---

## Extension Policy

- The process is **modular**: new roles, commands, or workflows may be added when justified by repeated needs or observed bottlenecks.
- Any extension must **document its invariants** and **not violate existing rules**.
- Changes to the core process require **Tech Lead approval** and alignment with agency standards.
- New standards can be added to `.claude/standards/` for new technologies (e.g., `fastapi.md`, `nextjs.md`).

---

## Quick Reference

### When to Use Each Command

| Situation | Command | Next Step |
|-----------|---------|-----------|
| New feature request | `/discovery` | → `/plan` |
| Need architecture plan | `/plan` | → `/implement` |
| Ready to code | `/implement` | → `/test` |
| Adding AI features | `/integrate_ai` | → `/test` |
| Feature complete | `/test` | → `/review` |
| Tests passed | `/review` | → `/ship` or `/refactor` |
| Code quality issues | `/refactor` | → `/test` |
| Ready to deploy | `/ship` | Deploy! |

### Framework File Locations

```
.claude/
├── CLAUDE.md                 # Operating contract and core principles
├── PROCESS.md               # This file - development process
├── agents/                  # 8 role definitions (fully specified)
│   ├── product_owner.md
│   ├── architect.md
│   ├── tech_lead.md
│   ├── backend_dev.md
│   ├── ai_engineer.md
│   ├── devops.md
│   ├── qa.md
│   └── reviewer.md
├── commands/                # 8 workflow commands (fully detailed)
│   ├── discovery.md
│   ├── plan.md
│   ├── implement.md
│   ├── integrate_ai.md
│   ├── test.md
│   ├── review.md
│   ├── refactor.md
│   └── ship.md
├── standards/               # Technology best practices (complete)
│   ├── aiogram.md
│   ├── docker.md
│   ├── telegram.md
│   ├── rag.md
│   └── testing.md
└── workflows/               # Project-specific flows (templates)
    ├── tg_bot_feature.md
    ├── tg_mini_app.md
    ├── ai_feature.md
    └── hotfix.md
```

---

## Summary

This document acts as:
- **A constitution** for AI agents in the project
- **A guideline** for human developers
- **A guardrail** for consistent, high-quality delivery
- **A foundation** for future process extensions across multiple projects and AI models

> Always treat this document as authoritative over workflow deviations or informal practices.

---

## Compliance Verification

Before shipping any feature, verify compliance:

**Process Compliance:**
- [ ] All commands executed in correct sequence
- [ ] Tech Lead approved plan before implementation
- [ ] QA tested and approved
- [ ] Reviewer approved code quality
- [ ] Tech Lead approved shipping

**Technical Compliance:**
- [ ] Code follows standards from `.claude/standards/`
- [ ] Docker-compose cold start works
- [ ] No hardcoded secrets
- [ ] All tests pass (>80% coverage)
- [ ] Structured JSON logging implemented
- [ ] AI prompts versioned (if applicable)

**Documentation Compliance:**
- [ ] `.env.example` updated
- [ ] Architecture documented in `/plan`
- [ ] Release notes prepared for `/ship`

Non-compliance with this process may result in:
- Rejected plans (Tech Lead)
- Failed QA (`/test`)
- Blocked review (`/review`)
- Rejected ship (`/ship`)

**The process exists to ensure quality. Follow it.**
