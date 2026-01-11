# Command: /implement

## Goal
Build the feature or functionality following the approved plan without making architectural decisions or scope changes.

## When to use
- After `/plan` is approved by Tech Lead
- When implementing a specific task from the approved task list
- For building new features, endpoints, services, or components
- **Never start implementation without an approved plan** - this prevents scope creep and architectural drift

## Agents involved
- **backend_dev**: Implements handlers, services, models, repositories following the approved architecture
- **ai_engineer**: Implements LLM integrations, RAG pipelines, prompt versioning (when AI tasks are in the plan)

## Input required
- Approved plan from `/plan` (architecture, task list, acceptance criteria)
- Task-specific requirements and acceptance criteria
- Relevant standards from `.claude/standards/` (aiogram, docker, rag, telegram, testing)
- Environment variable specifications from the plan

## Preconditions
- `/plan` approved by Tech Lead
- Task has clear acceptance criteria
- Architecture is documented and approved
- Dependencies are available (APIs, services, infrastructure)
- docker-compose configuration is in place

## Process

### Step 1: Setup and Preparation
**Owner**: backend_dev or ai_engineer
**Actions**:
- Review the approved plan and specific task requirements
- Identify the exact scope of the current task (no additions or changes)
- Review relevant standards from `.claude/standards/`
- Prepare any necessary environment variables in `.env.example` (no hardcoding)
- Ensure docker-compose services are available and running
- Understand the integration points and dependencies
**Output**: Clear understanding of task scope and boundaries

### Step 2: Implementation
**Owner**: backend_dev or ai_engineer
**Actions**:
- Implement the functionality following the approved architecture exactly
- Follow separation of concerns (handlers → services → repositories)
- Use environment variables for all configuration (no hardcoded values or secrets)
- Implement structured JSON logging for all operations
- **For AI tasks**: version all prompts, implement retry logic with exponential backoff, add fallback behavior
- Ensure code runs in docker-compose environment
- Write clean, maintainable code with proper error handling
- Follow coding standards and patterns from `.claude/standards/`
**Output**: Working implementation

### Step 3: Local Testing
**Owner**: backend_dev or ai_engineer
**Actions**:
- Test the implementation in docker-compose environment
- Verify all acceptance criteria are met
- Test error handling, edge cases, and negative scenarios
- **For Telegram bots**: test FSM flows, callback handlers, commands
- **For AI features**: test with various inputs, test failure modes, verify fallback logic
- Ensure no secrets are hardcoded anywhere
- Verify logs are structured (JSON) and informative
- Test cold start (`docker-compose up` from scratch)
**Output**: Locally validated implementation

### Step 4: Documentation
**Owner**: backend_dev or ai_engineer
**Actions**:
- Update `.env.example` with any new environment variables and descriptions
- Document any API changes or new endpoints (if applicable)
- **For AI features**: document prompt versions, model choices, fallback logic
- Add inline comments **only where logic is not self-evident**
- Do not add unnecessary docstrings or type annotations to unchanged code
**Output**: Documented implementation

## Output artifacts
- **Working code**: Implemented functionality following the approved plan
- **Environment variables**: Updated `.env.example` with new variables and documentation
- **Structured logs**: JSON logs for all operations (requests, responses, errors, AI calls)
- **For AI features**: Versioned prompts, retry logic, fallback behavior, AI request logging (version, input, output, latency, cost)

## Success criteria
- Implementation follows the approved plan exactly (no scope changes)
- Code follows framework standards (CLAUDE.md, `.claude/standards/`)
- All acceptance criteria from the task are met
- Code runs successfully in docker-compose
- No hardcoded secrets or configuration
- Proper error handling and structured JSON logging
- Separation of concerns is maintained (handlers → services → repositories)
- **For AI features**: prompts are versioned, retry logic is implemented, failures are logged

## Gate
- **Blocker**: Implementation deviates from approved plan (scope change detected)
- **Blocker**: Code doesn't run in docker-compose
- **Blocker**: Hardcoded secrets or configuration found
- **Blocker**: Acceptance criteria not met
- **Blocker**: Architecture boundaries violated (e.g., handler calling repository directly)
- **Blocker**: AI prompts are not versioned (for AI features)

## Final authority
**None** - implementation must strictly follow the approved plan. Any architectural decisions or scope changes require going back to `/plan`.

If implementation reveals that the plan is insufficient or incorrect, **stop and return to `/plan`** for revision.

## Related commands
- **plan**: Previous step - provides the approved architecture and task list to follow
- **test**: Next step - QA validates the implementation against acceptance criteria
- **integrate_ai**: Called when AI-specific implementation is needed (prompts, models, RAG pipelines)
- **refactor**: Used if code quality needs improvement without changing external behavior
- **review**: May be called after implementation to check code quality before testing
