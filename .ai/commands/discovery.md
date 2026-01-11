# Command: /discovery

## Goal
Understand what needs to be built and document the problem space before any implementation work begins.

## When to use
- At the start of a new feature or project
- When client request is high-level without detailed requirements
- When requirements are unclear or ambiguous
- Before any architecture or planning work begins
- When pivoting direction or adding major functionality

## Agents involved
- **product_owner**: Extracts business requirements, defines acceptance criteria, clarifies scope and priorities
- **architect**: Identifies technical constraints, existing system dependencies, data flow requirements, integration points

## Input required
- Client request or feature description
- Business context (optional)
- Timeline or budget constraints (optional)
- Existing documentation or specifications (optional)

## Preconditions
None - this is the entry point of the development workflow.

## Process

### Step 1: Problem Analysis
**Owner**: product_owner
**Actions**:
- Interview stakeholders or analyze the request
- Identify user needs and business goals
- Define success metrics and KPIs
- Document non-functional requirements (performance, security, compliance)
- Clarify business value and expected outcomes
**Output**: Problem statement with clear business context

### Step 2: Scope Definition
**Owner**: product_owner
**Actions**:
- Define what is IN scope and OUT of scope
- Set priorities for MVP vs future iterations
- Identify clear acceptance criteria for each requirement
- Document assumptions and dependencies
- Establish priorities using MoSCoW or similar framework
**Output**: Scope boundaries with acceptance criteria

### Step 3: Technical Context
**Owner**: architect
**Actions**:
- Review existing system architecture and codebase
- Identify integration points and dependencies
- Assess data requirements, schemas, and flows
- Flag technical constraints (APIs, infrastructure, third-party services)
- Check compatibility with docker-compose infrastructure
- Review relevant standards from `.claude/standards/`
**Output**: Technical context document with constraints

### Step 4: Risk and Assumptions
**Owner**: product_owner + architect
**Actions**:
- Document all assumptions being made
- Identify blockers and external dependencies
- Assess technical and business risks
- Evaluate complexity and effort implications
- Propose mitigation strategies for high-severity risks
**Output**: Risk register with assumptions and mitigation plan

## Output artifacts
- **Problem statement**: Clear description of what needs to be solved and why
- **Scope document**: What is included/excluded, priorities, measurable acceptance criteria
- **Constraints**: Technical, business, timeline, compliance, infrastructure constraints
- **Assumptions**: Documented assumptions requiring validation
- **Risk register**: Known risks with severity assessment and mitigation strategies

## Success criteria
- Stakeholders agree on the problem statement
- Scope is clearly defined with measurable acceptance criteria
- All technical and business constraints are documented
- Dependencies and integration points are identified
- Assumptions are explicit and documented
- Next steps are clear (proceed to `/plan` or gather more information)

## Gate
- **Blocker**: Critical information is missing and cannot proceed to planning
- **Blocker**: Problem statement is unclear or stakeholders disagree on scope
- **Pause**: External dependencies need clarification before proceeding

## Final authority
- **Product Owner** has final say on scope, priorities, and business requirements
- **Architect** has final say on technical feasibility and constraints

## Related commands
- **plan**: Next step after successful discovery - creates detailed implementation plan
- **integrate_ai**: May be called during discovery if AI capabilities need to be scoped and validated
