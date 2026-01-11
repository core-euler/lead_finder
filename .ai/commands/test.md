# Command: /test

## Goal
Validate correctness of implemented functionality from the user perspective before shipping to production.

## When to use
- After `/implement` completes a feature or fix
- Before `/review` and `/ship`
- When validating bug fixes
- After refactoring to ensure no regressions
- For acceptance testing against defined criteria
- **Never skip testing** - quality gate before shipping

## Agents involved
- **qa**: Tests from user perspective, validates acceptance criteria, tests edge cases and failure scenarios

## Input required
- Implemented feature or fix
- Acceptance criteria (if available from `/discovery` or `/plan`)
- Test scenarios (positive, negative, edge cases)
- Environment (docker-compose setup)

## Preconditions
- Code is implemented and runs in docker-compose
- Acceptance criteria are defined
- Test environment is available (test database, test bot, etc.)
- Test data or fixtures are prepared

## Process

### Step 1: Test Planning
**Owner**: qa
**Actions**:
- Review acceptance criteria from `/discovery` or `/plan`
- Identify test scenarios (happy path, edge cases, error cases)
- Prepare test data and fixtures
- Plan both functional and non-functional tests
- Identify Telegram-specific flows to test (FSM, callbacks, commands)
- Plan AI feature tests (with mocked responses and failure modes)
- Determine severity levels for potential issues (blocker/major/minor)
**Output**: Test plan with scenarios and expected outcomes

### Step 2: Functional Testing
**Owner**: qa
**Actions**:
- Test happy path scenarios (expected user flows)
- Verify acceptance criteria are met
- Test user inputs (valid, invalid, boundary values)
- **For Telegram bots**: Test commands, FSM state transitions, callback handlers
- **For APIs**: Test endpoints with various payloads
- **For background jobs**: Test Celery tasks and scheduled jobs
- Verify data persistence and retrieval
- Check error messages are user-friendly
**Output**: Functional test results with pass/fail status

### Step 3: Edge Case and Failure Testing
**Owner**: qa
**Actions**:
- Test boundary conditions (empty inputs, max length, special characters)
- Test concurrent operations (race conditions)
- Test failure scenarios:
  - Database unavailable
  - External API failures (Telegram API, OpenAI API)
  - Rate limits exceeded
  - Invalid user inputs
  - Network timeouts
- **For AI features**: Test with unexpected inputs, test fallback behavior
- Test error handling and recovery
- Verify logs are generated for failures
**Output**: Edge case test results with issues found

### Step 4: Integration Testing
**Owner**: qa
**Actions**:
- Test complete user flows end-to-end
- Verify integration points (bot ↔ backend ↔ database)
- Test data flow across services
- Verify docker-compose cold start works (`docker-compose down -v && docker-compose up`)
- Check health endpoints return correct status
- Test service dependencies (does bot wait for database to be ready?)
- Verify environment variables are used correctly
**Output**: Integration test results

### Step 5: Issue Reporting and Ship Decision
**Owner**: qa
**Actions**:
- Document all issues found with:
  - Severity (blocker/major/minor)
  - Steps to reproduce
  - Expected vs actual behavior
  - Screenshots or logs
- Classify issues by severity:
  - **Blocker**: Prevents core functionality, must fix before shipping
  - **Major**: Significant impact but has workaround
  - **Minor**: Cosmetic or low-impact issue
- Make ship recommendation:
  - **Ship**: No blockers, ready for review
  - **Don't ship**: Blockers found, must fix first
**Output**: Test report with issues and ship recommendation

## Output artifacts
- **Test report**: Summary of tests executed, pass/fail status
- **Issue list**: All bugs found with severity, steps to reproduce, screenshots
- **Ship recommendation**: Yes (no blockers) or No (blockers found)
- **Test coverage**: Which acceptance criteria were verified

## Success criteria
- All acceptance criteria are tested and pass
- No blocker issues found
- Edge cases and error scenarios are tested
- Telegram-specific flows work correctly (if applicable)
- AI features tested with mocked responses and failure modes (if applicable)
- Docker-compose cold start works without errors
- Logs are generated for important operations
- QA recommends shipping (no blockers)

## Gate
- **Blocker**: Core functionality doesn't work (critical bug)
- **Blocker**: Acceptance criteria not met
- **Blocker**: Docker-compose cold start fails
- **Blocker**: Data loss or corruption possible
- **Blocker**: Security vulnerability found
- **Blocker**: Hardcoded secrets discovered

When blockers are found, return to `/implement` to fix, then re-test.

## Final authority
**QA** has authority to block shipping if critical issues are found. Product Owner may override for minor issues if business needs require it.

## Related commands
- **implement**: Previous step - provides the code to test
- **review**: Next step after QA approves - code quality review
- **ship**: Final step after both test and review pass
- **refactor**: If code quality issues need improvement without behavior changes

---

## Testing Checklist

### Telegram Bot Testing
- [ ] `/start` command works for new users
- [ ] All commands respond correctly
- [ ] FSM flows work (state transitions, data persistence)
- [ ] Callback buttons work and acknowledge
- [ ] Error messages are user-friendly
- [ ] Bot handles invalid inputs gracefully
- [ ] Rate limits are respected

### API Testing
- [ ] All endpoints return correct status codes
- [ ] Request validation works (400 for invalid data)
- [ ] Authentication/authorization works
- [ ] Error responses have clear messages
- [ ] Pagination works correctly
- [ ] Health endpoint returns correct status

### AI Feature Testing
- [ ] AI responses are relevant and coherent
- [ ] Fallback behavior works when AI fails
- [ ] Retry logic handles rate limits
- [ ] Prompts are versioned (no magic strings)
- [ ] AI requests are logged with metadata
- [ ] Cost per request is within budget

### Infrastructure Testing
- [ ] `docker-compose up` works from scratch
- [ ] All services start and become healthy
- [ ] Database migrations run successfully
- [ ] Environment variables are loaded correctly
- [ ] Logs are visible with `docker-compose logs`
- [ ] Services restart on failure

### Data Testing
- [ ] Data is persisted correctly
- [ ] No data loss on restart
- [ ] Database queries are efficient
- [ ] No hardcoded data or secrets

---

## Examples

### Test Report Format

```markdown
# Test Report: Feature Name

**Date**: 2025-01-15
**Tester**: QA
**Environment**: Docker Compose (test)

## Summary
- Total tests: 25
- Passed: 23
- Failed: 2
- Blocked: 0

## Acceptance Criteria Status
✅ User can register via /start
✅ User can add channels
❌ Digest generation sends to user (timeout error)
⚠️ Digest formatting could be improved (minor)

## Issues Found

### BLOCKER-001: Digest generation times out
**Severity**: Blocker
**Steps to reproduce**:
1. Add 10+ channels
2. Trigger digest generation
3. Wait for response

**Expected**: Digest sent within 30 seconds
**Actual**: Timeout after 60 seconds, no digest sent
**Logs**: `CeleryTimeout: Task exceeded time limit`

### MINOR-001: Digest formatting inconsistent
**Severity**: Minor
**Description**: Some digests have extra line breaks

## Ship Recommendation
❌ **DO NOT SHIP** - 1 blocker issue must be fixed
```

### Test Execution Log

```
Test: User Registration Flow
  ✓ /start creates new user in database
  ✓ User receives welcome message
  ✓ /start for existing user returns to main menu
  ✓ User data persists after bot restart

Test: Channel Management
  ✓ Add valid channel via callback
  ✓ Reject invalid channel username
  ✗ Remove channel from list (timeout)
  ✓ List all user channels

Test: Digest Generation
  ✓ Manual digest triggers Celery task
  ✗ Scheduled digest completes (timeout)
  ✓ AI summarization called with correct prompt
  ✓ Fallback works when AI fails

Test: Error Handling
  ✓ Invalid command shows help message
  ✓ Database error logged and user notified
  ✓ Rate limit error handled gracefully
```
