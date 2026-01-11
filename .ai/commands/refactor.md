# Command: /refactor

## Goal
Improve code quality, readability, and maintainability without changing external behavior or adding features.

## When to use
- After `/review` identifies technical debt (non-blocking suggestions)
- When code becomes hard to maintain or understand
- To reduce complexity before adding new features
- To eliminate code duplication (DRY violations)
- To improve performance without changing functionality
- **Never during active feature development** - refactor between features

## Agents involved
- **tech_lead**: Defines refactor goals, approves scope, validates no behavior changes
- **backend_dev**: Implements refactoring changes with minimal modifications

## Input required
- Code area to refactor
- Specific refactoring goals (reduce complexity, eliminate duplication, improve readability)
- Current issues or pain points
- Existing test suite (to verify no regressions)

## Preconditions
- Tests exist and pass (to verify no behavior changes)
- No active feature development (refactor between features)
- Clear scope defined (specific files or modules)
- Code is committed to version control

## Process

### Step 1: Define Refactor Scope and Goals
**Owner**: tech_lead
**Actions**:
- Identify specific code areas needing improvement
- Define clear refactoring goals:
  - Reduce function complexity (split large functions)
  - Eliminate code duplication (extract common logic)
  - Improve naming (make intent clearer)
  - Simplify logic (remove unnecessary complexity)
  - Improve structure (better separation of concerns)
- Set boundaries: What NOT to change (external behavior, APIs)
- Ensure tests exist to verify no regressions
- Define success criteria (metrics, readability)
**Output**: Refactor plan with scope, goals, and boundaries

### Step 2: Verify Test Coverage
**Owner**: backend_dev
**Actions**:
- Run existing test suite and verify all tests pass
- Check code coverage for areas being refactored (should be >80%)
- If coverage insufficient, write tests BEFORE refactoring
- Document current behavior with tests
- Ensure tests validate external behavior (not implementation details)
**Output**: Passing test suite with adequate coverage

### Step 3: Implement Refactoring
**Owner**: backend_dev
**Actions**:
- Make minimal, incremental changes
- Follow refactoring patterns:
  - **Extract Method**: Split large functions
  - **Extract Variable**: Clarify complex expressions
  - **Rename**: Improve variable/function names
  - **Remove Duplication**: Extract common logic
  - **Simplify Conditionals**: Reduce nesting, use early returns
- Run tests after each change to verify no regressions
- Keep commits small and focused (one refactoring pattern per commit)
- **DO NOT**:
  - Change external behavior or APIs
  - Add new features
  - Fix bugs (do that separately)
  - Expand scope beyond plan
**Output**: Refactored code with same external behavior

### Step 4: Verify No Behavioral Changes
**Owner**: backend_dev + tech_lead
**Actions**:
- Run full test suite and verify all tests still pass
- Test in docker-compose environment
- Compare behavior before/after refactoring
- Check logs and outputs match expected behavior
- Verify performance hasn't degraded significantly
- Run integration tests to verify system behavior unchanged
**Output**: Test results confirming no regressions

### Step 5: Review and Document Changes
**Owner**: tech_lead
**Actions**:
- Review refactored code for improvements
- Verify goals were achieved:
  - Complexity reduced?
  - Duplication eliminated?
  - Readability improved?
- Check that scope wasn't expanded (no new features)
- Document what was changed and why
- Approve or request further refinement
**Output**: Approved refactoring with summary

## Output artifacts
- **Refactor summary**: What was changed and why
- **Changed areas**: List of files and functions modified
- **Test results**: Proof that behavior unchanged (all tests pass)
- **Metrics**: Before/after complexity, duplication, coverage

## Success criteria
- External behavior unchanged (all tests pass)
- Code quality improved (measurable: complexity, duplication, readability)
- No new features added
- No bugs introduced
- Refactoring goals achieved
- Tech Lead approved changes
- Documentation updated if needed

## Gate
- **Blocker**: Tests fail (behavior changed unintentionally)
- **Blocker**: Scope expanded (new features added)
- **Blocker**: External APIs changed (breaking change)
- **Blocker**: Performance significantly degraded
- **Blocker**: New bugs introduced

## Final authority
**Tech Lead** has final authority to approve refactoring or request changes if scope expanded or behavior changed.

## Related commands
- **review**: May recommend refactoring as non-blocking suggestions
- **test**: Must run after refactoring to verify no regressions
- **implement**: Different - refactor improves existing code, implement adds new code

---

## Refactoring Patterns

### 1. Extract Method
**Before:**
```python
async def process_user_request(user_id: int, request: str):
    # Validate user
    user = await db.get_user(user_id)
    if not user:
        raise ValueError("User not found")
    if not user.is_active:
        raise ValueError("User inactive")

    # Process request
    request = request.strip().lower()
    if len(request) > 1000:
        raise ValueError("Request too long")

    # Log request
    logger.info("request_received", user_id=user_id, length=len(request))
```

**After:**
```python
async def process_user_request(user_id: int, request: str):
    user = await _validate_user(user_id)
    validated_request = _validate_request(request)
    _log_request(user_id, validated_request)

async def _validate_user(user_id: int) -> User:
    user = await db.get_user(user_id)
    if not user:
        raise ValueError("User not found")
    if not user.is_active:
        raise ValueError("User inactive")
    return user

def _validate_request(request: str) -> str:
    request = request.strip().lower()
    if len(request) > 1000:
        raise ValueError("Request too long")
    return request

def _log_request(user_id: int, request: str):
    logger.info("request_received", user_id=user_id, length=len(request))
```

### 2. Remove Duplication
**Before:**
```python
async def add_channel(user_id: int, channel: str):
    if not channel.startswith("@"):
        raise ValueError("Invalid channel")
    # ...

async def remove_channel(user_id: int, channel: str):
    if not channel.startswith("@"):
        raise ValueError("Invalid channel")
    # ...
```

**After:**
```python
def _validate_channel(channel: str):
    if not channel.startswith("@"):
        raise ValueError("Invalid channel")

async def add_channel(user_id: int, channel: str):
    _validate_channel(channel)
    # ...

async def remove_channel(user_id: int, channel: str):
    _validate_channel(channel)
    # ...
```

### 3. Simplify Conditionals
**Before:**
```python
if user is not None:
    if user.is_active:
        if user.has_subscription:
            return True
        else:
            return False
    else:
        return False
else:
    return False
```

**After:**
```python
return user is not None and user.is_active and user.has_subscription
```

### 4. Early Return
**Before:**
```python
async def get_digest(user_id: int) -> str:
    user = await db.get_user(user_id)
    if user:
        channels = await db.get_user_channels(user_id)
        if channels:
            posts = await fetch_posts(channels)
            if posts:
                digest = await generate_digest(posts)
                return digest
    return None
```

**After:**
```python
async def get_digest(user_id: int) -> str:
    user = await db.get_user(user_id)
    if not user:
        return None

    channels = await db.get_user_channels(user_id)
    if not channels:
        return None

    posts = await fetch_posts(channels)
    if not posts:
        return None

    return await generate_digest(posts)
```

---

## Refactoring Checklist

### Before Refactoring
- [ ] Tests exist and pass
- [ ] Code coverage adequate (>80%)
- [ ] Scope clearly defined
- [ ] Goals clearly stated
- [ ] No active feature development

### During Refactoring
- [ ] Make one change at a time
- [ ] Run tests after each change
- [ ] Keep commits small and focused
- [ ] Don't change external behavior
- [ ] Don't add new features
- [ ] Don't fix bugs (do separately)

### After Refactoring
- [ ] All tests pass
- [ ] Behavior unchanged (integration tests)
- [ ] Goals achieved (complexity reduced, etc.)
- [ ] Code more readable
- [ ] Documentation updated
- [ ] Tech Lead approved

---

## Examples

### Refactor Summary

```markdown
# Refactor: User Service Complexity Reduction

**Date**: 2025-01-15
**Developer**: Backend Dev
**Approved by**: Tech Lead

## Goals
- Reduce complexity in UserService.register_or_get_user
- Eliminate code duplication in channel validation
- Improve readability in digest generation

## Changes Made

### 1. Extract user validation logic
**File**: `services/user_service.py`
**Before**: Single 80-line function
**After**: Main function + 3 helper functions (15-20 lines each)
**Impact**: Cyclomatic complexity reduced from 12 → 4

### 2. Extract channel validation
**File**: `services/channel_service.py`
**Before**: Validation duplicated in 4 methods
**After**: Shared `_validate_channel_format()` helper
**Impact**: Removed 30 lines of duplication

### 3. Simplify digest logic
**File**: `services/digest_service.py`
**Before**: Deeply nested conditionals (5 levels)
**After**: Early returns, flat structure (2 levels max)
**Impact**: Readability improved significantly

## Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Cyclomatic Complexity | 45 | 22 | -51% |
| Lines of Code | 850 | 720 | -15% |
| Code Duplication | 18% | 3% | -83% |
| Test Coverage | 82% | 85% | +3% |

## Test Results
✅ All 127 tests pass
✅ No behavioral changes detected
✅ Performance: -2ms avg (slight improvement)

## Approval
✅ **APPROVED** by Tech Lead
Changes improve maintainability without affecting behavior.
```

---

## Rules

### MUST DO
- ✅ Run tests before and after
- ✅ Make incremental changes
- ✅ Verify behavior unchanged
- ✅ Stay within defined scope
- ✅ Get Tech Lead approval

### MUST NOT DO
- ❌ Change external behavior or APIs
- ❌ Add new features
- ❌ Fix bugs (do separately)
- ❌ Refactor without tests
- ❌ Expand scope beyond plan
