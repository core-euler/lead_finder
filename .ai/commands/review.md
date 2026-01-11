# Command: /review

## Goal
Ensure code quality, long-term maintainability, and compliance with framework standards before shipping to production.

## When to use
- After `/test` passes (QA approves)
- Before `/ship`
- For significant code changes or new features
- When code quality concerns are raised
- **Adversarial mindset**: Review as if maintaining for 1 year

## Agents involved
- **reviewer**: Reviews code quality, architecture compliance, readability, security, technical debt

## Input required
- Code changes (git diff or pull request)
- Related plan or task description
- Test results from `/test`
- Architecture from `/plan` (to verify compliance)

## Preconditions
- `/test` passed (QA approved, no blockers)
- Code is committed to version control
- All tests are passing
- Code runs in docker-compose

## Process

### Step 1: Architecture Compliance Review
**Owner**: reviewer
**Actions**:
- Verify code follows approved architecture from `/plan`
- Check separation of concerns (handlers → services → repositories)
- Validate component boundaries (no circular dependencies)
- Ensure no architectural shortcuts or violations
- Check that standards from `.claude/standards/` are followed:
  - aiogram patterns (if Telegram bot)
  - docker-compose configuration (if infrastructure changes)
  - RAG patterns (if AI features)
  - Testing standards (if test changes)
- Verify no scope creep beyond approved plan
**Output**: Architecture compliance assessment

### Step 2: Code Quality Review
**Owner**: reviewer
**Actions**:
- **Readability**: Code is clear, self-documenting, uses meaningful names
- **Complexity**: No overly complex functions (max 50 lines, single responsibility)
- **Error Handling**: All error paths covered, failures logged, user-friendly messages
- **Logging**: Structured JSON logs for important operations
- **Configuration**: Environment variables used, no hardcoded values
- **Comments**: Only where logic isn't self-evident, no commented-out code
- **Typing**: Proper type hints (for Python)
- **Consistency**: Follows existing code style and patterns
**Output**: Code quality assessment

### Step 3: Security and Safety Review
**Owner**: reviewer
**Actions**:
- **Secrets**: No hardcoded API keys, tokens, passwords
- **Input Validation**: User inputs validated and sanitized
- **SQL Injection**: Parameterized queries, no string concatenation
- **XSS Prevention**: Output escaped properly
- **Authentication**: Proper auth checks for protected operations
- **Rate Limiting**: Protection against abuse
- **Data Privacy**: Minimal data collection, no PII leaks in logs
- **Dependencies**: No known vulnerabilities in dependencies
**Output**: Security assessment

### Step 4: AI-Specific Review (if applicable)
**Owner**: reviewer
**Actions**:
- **Prompt Versioning**: All prompts versioned, no magic strings
- **Error Handling**: Retry logic, fallback behavior, timeout handling
- **Logging**: All AI requests logged (version, tokens, cost, latency)
- **Cost Awareness**: Token usage optimized, costs documented
- **Testing**: AI features tested with mocked responses
- **Observability**: Success rate, latency, cost tracked
**Output**: AI integration assessment

### Step 5: Technical Debt Assessment
**Owner**: reviewer
**Actions**:
- Identify code that will be hard to maintain
- Flag TODOs or FIXMEs that should be addressed
- Assess long-term scalability concerns
- Check for code duplication (DRY violations)
- Identify premature optimizations or over-engineering
- Note areas needing refactoring (but not blocking)
**Output**: Technical debt report

### Step 6: Verdict and Recommendations
**Owner**: reviewer
**Actions**:
- Provide review verdict:
  - **Approve**: Code meets standards, ready to ship
  - **Approve with suggestions**: Minor improvements suggested but not blocking
  - **Request changes**: Blocking issues must be fixed
- List blocking issues (must fix before ship)
- List suggestions (nice to have, not blocking)
- Provide clear feedback for each issue
**Output**: Review verdict with actionable feedback

## Output artifacts
- **Review verdict**: Approve / Approve with suggestions / Request changes
- **Blocking issues**: Critical problems that must be fixed before shipping
- **Suggestions**: Non-blocking improvements for future iterations
- **Technical debt notes**: Areas to improve in future refactoring

## Success criteria
- Code follows framework standards (CLAUDE.md, `.claude/standards/`)
- Architecture compliance verified (matches approved plan)
- No security vulnerabilities
- Error handling comprehensive
- Logging structured and complete
- No hardcoded secrets or configuration
- AI prompts versioned (if applicable)
- Reviewer approves or approves with suggestions

## Gate
- **Blocker**: Code violates framework standards (CLAUDE.md, `.claude/standards/`)
- **Blocker**: Architecture doesn't match approved plan (scope creep)
- **Blocker**: Security vulnerabilities found
- **Blocker**: Hardcoded secrets or configuration
- **Blocker**: AI prompts not versioned (magic strings)
- **Blocker**: No error handling for critical operations
- **Blocker**: Circular dependencies or architectural violations

When blocking issues are found, return to `/implement` to fix, then re-test and re-review.

## Final authority
**Reviewer** has authority to block shipping if code quality or architectural issues are found. Tech Lead may be consulted for architectural decisions.

## Related commands
- **test**: Previous step - must pass before review
- **ship**: Next step after review approval
- **implement**: Return here if blocking issues found
- **refactor**: For non-blocking quality improvements

---

## Review Checklist

### Architecture & Design
- [ ] Follows approved architecture from `/plan`
- [ ] Separation of concerns maintained (handlers → services → repositories)
- [ ] No circular dependencies
- [ ] Component boundaries clear and respected
- [ ] Standards from `.claude/standards/` followed
- [ ] No scope creep beyond approved plan

### Code Quality
- [ ] Code is readable and self-documenting
- [ ] Functions are small and single-purpose (< 50 lines)
- [ ] Meaningful variable and function names
- [ ] No commented-out code
- [ ] Consistent with existing codebase style
- [ ] Type hints used appropriately (Python)

### Error Handling & Logging
- [ ] All error paths covered
- [ ] Errors logged with structured JSON
- [ ] User-friendly error messages
- [ ] No silent failures
- [ ] Proper exception handling (no bare except)
- [ ] Logs include context (user_id, request_id, etc.)

### Configuration & Security
- [ ] Environment variables used (no hardcoded values)
- [ ] No secrets in code or logs
- [ ] Input validation implemented
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Rate limiting where needed
- [ ] Authentication/authorization proper

### AI-Specific (if applicable)
- [ ] All prompts versioned
- [ ] Retry logic implemented
- [ ] Fallback behavior defined
- [ ] AI requests logged (version, tokens, cost)
- [ ] Cost implications documented
- [ ] Tests with mocked AI responses

### Testing & Docker
- [ ] Tests pass
- [ ] Code coverage meets threshold (>80%)
- [ ] Edge cases tested
- [ ] Runs in docker-compose
- [ ] Health checks implemented (if new service)

### Documentation
- [ ] `.env.example` updated
- [ ] API changes documented
- [ ] Complex logic has comments
- [ ] README updated if needed

---

## Examples

### Review Feedback Format

```markdown
# Code Review: Feature Name

**Reviewer**: Code Reviewer
**Date**: 2025-01-15
**Commit**: abc123

## Verdict
❌ **REQUEST CHANGES** - 2 blocking issues found

## Blocking Issues

### BLOCK-001: Hardcoded API key in service
**File**: `services/ai_service.py:15`
**Issue**: OpenAI API key hardcoded as string
**Required Fix**: Use environment variable from settings
```python
# Current (BAD)
client = OpenAI(api_key="sk-...")

# Required (GOOD)
client = OpenAI(api_key=settings.openai_api_key)
```

### BLOCK-002: AI prompts not versioned
**File**: `services/summarization.py:45`
**Issue**: Prompt defined as magic string, not versioned
**Required Fix**: Create versioned prompt in `prompts/` directory
```python
# Current (BAD)
prompt = f"Summarize: {text}"

# Required (GOOD)
from prompts.summarization import SUMMARIZE_V1
prompt = SUMMARIZE_V1.template.format(text=text)
```

## Suggestions (Non-blocking)

### SUGGEST-001: Extract duplicate code
**File**: `handlers/channels.py:30-45, 70-85`
**Suggestion**: Extract channel validation logic to shared function
**Impact**: Improves maintainability

### SUGGEST-002: Add type hints
**File**: `services/user_service.py`
**Suggestion**: Add return type hints to all public methods
**Impact**: Better IDE support and type checking

## Technical Debt
- Large function in `services/digest_service.py:100-200` should be split
- Consider caching channel metadata to reduce database queries

## Approval Criteria
Fix BLOCK-001 and BLOCK-002, then re-submit for review.
```

### Review Comments on Code

```python
# services/ai_service.py

# ❌ BLOCKER: Hardcoded API key
client = OpenAI(api_key="sk-proj-...")

# ✅ SUGGESTION: Add type hint
async def generate_summary(text):  # ← Add return type
    ...

# ❌ BLOCKER: Prompt not versioned
prompt = "Summarize the following text: " + text

# ⚠️ SUGGESTION: Consider adding retry logic
response = await client.chat.completions.create(...)

# ✅ GOOD: Structured logging
logger.info("ai_request", model="gpt-4", tokens=response.usage.total_tokens)
```

### Approval Examples

**Approve:**
```markdown
✅ **APPROVED**
Code meets all standards. Ready to ship.
```

**Approve with suggestions:**
```markdown
✅ **APPROVED WITH SUGGESTIONS**
No blockers. Consider addressing suggestions in future refactoring:
- Add type hints to service methods
- Extract duplicate validation logic
```

**Request changes:**
```markdown
❌ **REQUEST CHANGES**
2 blocking issues must be fixed:
1. Hardcoded API key (BLOCK-001)
2. Prompts not versioned (BLOCK-002)

Fix these issues and re-submit for review.
```
