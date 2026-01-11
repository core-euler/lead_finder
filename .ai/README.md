# AI-Driven Development Framework

**Production-ready framework** for building Telegram bots, Mini Apps, AI/LLM integrations, RAG pipelines, and Docker-based systems using an **agent-based development process**.

---

## What is This?

This framework provides a **constitutional approach** to software development where:

- **Roles are clearly defined** (Product Owner, Architect, Tech Lead, Backend Dev, AI Engineer, QA, Reviewer, DevOps)
- **Commands act as quality gates** (/discovery → /plan → /implement → /test → /review → /ship)
- **Standards ensure consistency** (Telegram bots, Docker, RAG, Testing)
- **AI integrations are governed** (prompt versioning, observability, cost tracking)

The framework is designed for **agencies and teams** building:
- Telegram bots (aiogram 3.x)
- Telegram Mini Apps
- AI-powered systems (OpenAI, Claude, RAG pipelines)
- docker-compose based infrastructure

---

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd <your-repo>

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Start services
docker-compose up -d

# Verify all services are healthy
docker-compose ps
```

### 2. Understand the Framework Structure

```
.claude/
├── CLAUDE.md                 # Operating contract and core principles
├── PROCESS.md               # Development process and workflow
├── README.md                # This file
│
├── agents/                  # 8 role definitions (fully specified)
│   ├── product_owner.md     # Defines requirements and acceptance criteria
│   ├── architect.md         # Designs system architecture
│   ├── tech_lead.md         # Validates and approves plans (final authority)
│   ├── backend_dev.md       # Implements features
│   ├── ai_engineer.md       # Implements AI/LLM/RAG integrations
│   ├── devops.md            # Manages docker-compose and deployments
│   ├── qa.md                # Tests from user perspective
│   └── reviewer.md          # Enforces code quality
│
├── commands/                # 8 workflow commands (fully detailed)
│   ├── discovery.md         # Understand requirements
│   ├── plan.md              # Create architecture (Tech Lead approval)
│   ├── implement.md         # Build features
│   ├── integrate_ai.md      # Add AI functionality
│   ├── test.md              # QA validation
│   ├── review.md            # Code quality review
│   ├── refactor.md          # Improve code quality
│   └── ship.md              # Deploy to production
│
├── standards/               # Technology best practices (complete)
│   ├── aiogram.md           # Telegram bot patterns (FSM, handlers, DI)
│   ├── docker.md            # Docker-compose (health checks, migrations)
│   ├── telegram.md          # Telegram API (webhooks, Mini Apps, rate limits)
│   ├── rag.md               # RAG systems (chunking, embeddings, observability)
│   └── testing.md           # TDD (unit/integration/e2e, >80% coverage)
│
└── workflows/               # Project-specific flows (templates)
    ├── tg_bot_feature.md    # Telegram bot feature workflow
    ├── tg_mini_app.md       # Mini app workflow
    ├── ai_feature.md        # AI feature workflow
    └── hotfix.md            # Emergency hotfix workflow
```

---

## Development Workflow

### Standard Feature Flow

```
/discovery → /plan → /implement → /integrate_ai (if AI) → /test → /review → /ship
    ↓          ↓          ↓              ↓                   ↓       ↓        ↓
 Problem    Tech Lead  Backend Dev   AI Engineer           QA    Reviewer  DevOps
  Analysis  Approval   + AI Eng      Prompt Version              Approval  Validation
```

### Command Overview

| Command | Purpose | Key Outputs | Next Step |
|---------|---------|-------------|-----------|
| `/discovery` | Understand requirements | Problem statement, scope, constraints | → `/plan` |
| `/plan` | Design architecture | Architecture, tasks, Tech Lead approval | → `/implement` |
| `/implement` | Build features | Working code in docker-compose | → `/test` |
| `/integrate_ai` | Add AI features | Versioned prompts, fallback logic | → `/test` |
| `/test` | QA validation | Test report, ship recommendation | → `/review` |
| `/review` | Code quality check | Review verdict (approve/reject) | → `/ship` |
| `/refactor` | Improve code quality | Refactored code, no behavior changes | → `/test` |
| `/ship` | Deploy to production | Release notes, deployment confirmation | Done! |

---

## Roles and Responsibilities

| Role | Responsibilities | Authority |
|------|------------------|-----------|
| **Product Owner** | Define requirements, acceptance criteria, priorities | Final say on scope |
| **Architect** | Design system architecture, component boundaries | Proposes architecture |
| **Tech Lead** | Validate architecture, approve/reject plans | **Can block shipping** |
| **Backend Dev** | Implement handlers, services, repositories | Executes plan |
| **AI Engineer** | Implement LLM/RAG, version prompts | AI integrations |
| **DevOps** | Docker-compose, deployments, health checks | Infrastructure |
| **QA** | Test from user perspective, validate acceptance criteria | **Can block shipping** |
| **Reviewer** | Code quality, standards compliance, security | **Can block shipping** |

---

## Key Features

### 🚀 Production-Ready Standards

All standards are **fully documented** with code examples:

- **Telegram Bots** (aiogram.md): FSM, handlers, middleware, dependency injection
- **Docker** (docker.md): Health checks, volumes, migrations, zero manual setup
- **Telegram API** (telegram.md): Rate limits, webhooks, Mini Apps, deep links
- **RAG Systems** (rag.md): Chunking, embeddings, prompt versioning, observability
- **Testing** (testing.md): Unit/integration/e2e, >80% coverage, docker-based

### 🔒 Quality Gates

Every feature must pass through multiple gates:

1. **Tech Lead approves plan** (prevents vibe coding)
2. **QA validates functionality** (no blocker bugs)
3. **Reviewer approves code quality** (standards compliance)
4. **Tech Lead + DevOps approve shipping** (docker validation)

### 🤖 AI Governance

All AI integrations follow strict rules:

- ✅ **Prompts are versioned** (no magic strings)
- ✅ **Retry logic** with exponential backoff
- ✅ **Fallback behavior** for failures
- ✅ **Observability**: All requests logged (tokens, cost, latency)
- ✅ **Cost tracking** and documentation
- ✅ **Testing** with mocked responses

### 🐳 Docker-First

Everything runs in docker-compose:

- ✅ **Cold start works**: `docker-compose down -v && docker-compose up`
- ✅ **Health checks** for all services
- ✅ **Zero manual setup** (migrations run automatically)
- ✅ **No hardcoded secrets** (all in `.env.example`)

---

## Using the Framework

### Example: Adding a New Feature

```bash
# 1. Understand requirements
/discovery "Add user analytics dashboard"

# 2. Create architecture plan
/plan "Design analytics data pipeline and UI"
# Tech Lead reviews and approves

# 3. Implement the feature
/implement "Analytics dashboard"

# 4. Test the feature
/test "Analytics dashboard"
# QA validates and approves

# 5. Code review
/review "Analytics dashboard"
# Reviewer checks quality and approves

# 6. Ship to production
/ship "Analytics dashboard v1.0"
# Tech Lead + DevOps validate and deploy
```

### Example: Adding AI Feature

```bash
# 1. Plan AI integration
/discovery "Add AI-powered content summarization"
/plan "Design RAG pipeline for summarization"

# 2. Implement AI feature
/integrate_ai "Content summarization with prompt versioning"
# - Version prompts (SUMMARIZE_V1)
# - Add retry logic
# - Implement fallback
# - Log tokens and cost

# 3. Test and ship
/test "AI summarization"
/review "AI summarization"
/ship "AI summarization v1.0"
```

---

## Process Invariants (The Rules)

These rules **cannot be broken**:

1. **Architecture before implementation** — No code without Tech Lead approved plan
2. **Testing and review are mandatory** — No shipping without QA + Reviewer approval
3. **Docker is the source of truth** — Code must run in docker-compose
4. **AI prompts must be versioned** — No magic strings
5. **No hardcoded secrets** — All config via environment variables
6. **Separation of concerns** — Handlers → Services → Repositories
7. **Structured logging** — All operations logged as JSON
8. **>80% test coverage** — Quality over speed

See `PROCESS.md` for full details.

---

## Common Workflows

### New Telegram Bot Feature

1. `/discovery` — Define feature requirements
2. `/plan` — Design bot handlers and FSM states
3. `/implement` — Code handlers → services → repositories
4. `/test` — Test commands, FSM flows, callbacks
5. `/review` — Check aiogram standards compliance
6. `/ship` — Deploy with docker-compose

### AI Integration

1. `/discovery` — Define AI use case and requirements
2. `/plan` — Design prompt strategy and fallback logic
3. `/integrate_ai` — Implement with prompt versioning
4. `/test` — Test with mocked responses and failure modes
5. `/review` — Verify prompt versioning and observability
6. `/ship` — Deploy with cost monitoring

### Hotfix

1. `/discovery` — Analyze bug and impact
2. `/plan` — Design minimal fix (no scope creep)
3. `/implement` — Fix bug only
4. `/test` — Verify fix + no regressions
5. `/review` — Quick review (fast-track)
6. `/ship` — Deploy ASAP

---

## Definition of Done

A feature is "done" when:

- [ ] Code works in docker-compose (cold start tested)
- [ ] No hardcoded secrets (all in `.env.example`)
- [ ] Separation of concerns (handlers → services → repositories)
- [ ] All tests pass (>80% coverage)
- [ ] QA approved (`/test` passed)
- [ ] Reviewer approved (`/review` passed)
- [ ] Tech Lead approved (`/ship` approved)
- [ ] AI prompts versioned (if AI feature)
- [ ] Structured JSON logging implemented
- [ ] Documentation updated

---

## Technology Stack

**Supported Technologies:**

- **Telegram Bots**: aiogram 3.x
- **Backend**: Python (async), FastAPI
- **Database**: PostgreSQL + SQLAlchemy
- **Cache**: Redis
- **Background Jobs**: Celery + Celery Beat
- **AI/LLM**: OpenAI, Anthropic Claude
- **Vector DB**: Qdrant (for RAG)
- **Infrastructure**: Docker Compose
- **Testing**: pytest, pytest-asyncio

---

## Best Practices

### DO ✅

- Follow the command sequence (don't skip gates)
- Get Tech Lead approval before implementing
- Version all AI prompts
- Write tests before shipping (TDD)
- Use docker-compose for everything
- Log all operations as structured JSON
- Document environment variables in `.env.example`
- Keep code simple and explicit

### DON'T ❌

- Skip `/plan` (no vibe coding)
- Hardcode secrets or configuration
- Put business logic in handlers
- Use magic strings for AI prompts
- Skip tests or accept <80% coverage
- Ship without QA and Review approval
- Make architectural changes during `/implement`
- Ignore framework standards

---

## Extending the Framework

### Adding a New Role

1. Create `agents/new_role.md` based on `_TEMPLATE.md`
2. Define responsibilities and boundaries
3. Update `PROCESS.md`
4. Get Tech Lead approval

### Adding a New Command

1. Create `commands/new_command.md` based on `_TEMPLATE.md`
2. Define process steps, gates, and outputs
3. Update workflows if needed
4. Get Tech Lead approval

### Adding a New Standard

1. Create `standards/new_tech.md`
2. Document patterns, examples, and anti-patterns
3. Reference from commands and roles
4. Get Tech Lead approval

---

## Troubleshooting

### "My code doesn't run in docker-compose"

- Check `.env.example` has all required variables
- Verify health checks are implemented
- Check service dependencies (`depends_on`)
- Test cold start: `docker-compose down -v && docker-compose up`

### "QA blocked my feature"

- Review test report for blocker issues
- Fix issues and re-run `/test`
- Don't skip this gate

### "Reviewer blocked my code"

- Review feedback for specific issues
- Fix blocking issues (hardcoded secrets, prompts not versioned, etc.)
- Re-submit for `/review`

### "Tech Lead rejected my plan"

- Architecture may violate framework standards
- Scope may be unclear or too broad
- Revise plan and resubmit

---

## Resources

- **PROCESS.md** — Detailed development process and invariants
- **CLAUDE.md** — Operating contract and core principles
- **agents/** — Role definitions and responsibilities
- **commands/** — Command specifications and processes
- **standards/** — Technology best practices and patterns

---

## Support

For questions or issues:

1. Check `PROCESS.md` for process questions
2. Check `standards/` for technology questions
3. Check `commands/` for workflow questions
4. Consult Tech Lead for architectural decisions

---

## Summary

This framework enables:

- ✅ **Predictable delivery** through gated workflows
- ✅ **High quality** through mandatory testing and review
- ✅ **AI governance** through prompt versioning and observability
- ✅ **Team alignment** through clear roles and responsibilities
- ✅ **Production readiness** through docker-first approach
- ✅ **Scalability** across multiple projects and teams

**The framework works. Follow it.**

---

## License

[Your License Here]

## Contributors

Built by [Your Agency Name] for professional Telegram bot and AI system development.
