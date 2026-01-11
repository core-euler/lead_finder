# Command: /plan

## Goal
Produce implementation-ready architecture and task breakdown that developers can execute without making architectural decisions.

## When to use
- After successful `/discovery` with clear requirements
- Before any implementation work begins
- When adding significant new features or modules
- When technical approach needs validation
- **Never skip planning** for non-trivial features - this prevents "vibe coding"

## Agents involved
- **architect**: Designs system architecture, component boundaries, data flows, integration points, folder structure
- **tech_lead**: Reviews and validates architecture, enforces framework standards, **approves or rejects the plan**

## Input required
- Discovery output (problem statement, scope, constraints, assumptions)
- Acceptance criteria from Product Owner
- Technical constraints and dependencies
- Relevant standards from `.claude/standards/`

## Preconditions
- `/discovery` completed with clear scope and requirements
- Acceptance criteria are defined and measurable
- Technical constraints are documented
- Stakeholders agree on the problem statement

## Process

### Step 1: Architecture Design
**Owner**: architect
**Actions**:
- Design component boundaries and module structure
- Define data models, schemas, and relationships
- Document API contracts and integration points
- Plan folder structure following framework conventions
- Ensure docker-compose deployability (services, volumes, networks)
- Create architecture diagrams (component, sequence, data flow)
- Identify which standards apply from `.claude/standards/` (aiogram, docker, rag, etc.)
- Define environment variables needed (with `.env.example` plan)
**Output**: Architecture document with diagrams and data models

### Step 2: Task Breakdown
**Owner**: architect
**Actions**:
- Break architecture into granular implementation tasks
- Sequence tasks with clear dependencies
- Assign complexity level (simple/medium/complex)
- Identify tasks requiring AI Engineer involvement
- Flag tasks needing DevOps involvement (docker-compose, health checks, env vars)
- Create task list where each task has clear acceptance criteria
- Ensure tasks can be implemented without scope changes
**Output**: Sequenced task list with dependencies and acceptance criteria

### Step 3: Risk Assessment
**Owner**: architect + tech_lead
**Actions**:
- Identify technical risks and challenges
- Assess architectural complexity and unknowns
- Flag potential bottlenecks or performance concerns
- Evaluate third-party dependencies and integration risks
- Propose mitigation strategies for high-severity risks
- Document assumptions requiring validation during implementation
**Output**: Risk register with severity levels and mitigation plan

### Step 4: Technical Validation
**Owner**: tech_lead
**Actions**:
- Review architecture against framework standards (CLAUDE.md, `.claude/standards/`)
- Validate component boundaries and separation of concerns (handlers → services → repositories)
- Check for technical debt, circular dependencies, or complexity issues
- Verify docker-compose compatibility and deployment feasibility
- Assess long-term maintainability and scalability
- **Approve or reject** the plan with clear reasoning
- If rejected: provide specific feedback on required changes
**Output**: **Approval verdict** (approve/reject) with detailed feedback

## Output artifacts
- **Architecture document**: Component diagram, data models, integration points, folder structure
- **Task list**: Sequenced implementation tasks with dependencies, complexity, and acceptance criteria
- **API contracts**: Endpoint definitions, request/response schemas (if applicable)
- **Environment variables**: List of required env vars with descriptions
- **Risk register**: Technical risks with severity assessment and mitigation strategies
- **Tech Lead approval**: Explicit approval or rejection with reasoning

## Success criteria
- Architecture follows framework standards and conventions
- Component boundaries are clear with no circular dependencies
- All tasks have clear acceptance criteria and can be implemented independently
- Docker-compose deployment is feasible with zero manual setup
- Tech Lead has **approved** the plan
- Developers can implement without needing to make architectural decisions
- No hardcoded secrets or configuration in the plan

## Gate
- **Blocker**: Tech Lead rejects the plan - must be revised and resubmitted
- **Blocker**: Architecture violates framework standards (CLAUDE.md, `.claude/standards/`)
- **Blocker**: Critical technical risks have no mitigation strategy
- **Blocker**: Tasks are unclear, overlapping, or missing acceptance criteria
- **Blocker**: Plan requires hardcoded secrets or manual configuration

## Final authority
**Tech Lead** has final authority to approve or reject the architecture and plan. Rejection requires specific feedback for revision.

## Related commands
- **discovery**: Previous step - must be completed first
- **implement**: Next step after plan approval - developers follow the approved plan strictly
- **integrate_ai**: May be called during planning if AI architecture needs detailed design (prompts, models, fallbacks)
- **review**: May be used to review the plan document itself before approval
