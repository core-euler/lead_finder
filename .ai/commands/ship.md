# Command: /ship

## Goal
Prepare and approve release to target environment (staging/production) after all quality gates pass.

## When to use
- After `/test` passes (QA approves, no blockers)
- After `/review` passes (code quality approved)
- When ready to deploy to staging or production
- For hotfixes that need immediate deployment
- **Final gate before production** - ensures everything is ready

## Agents involved
- **tech_lead**: Final technical approval, verifies all gates passed, approves release
- **devops**: Validates docker-compose setup, verifies deployment readiness, prepares release notes

## Input required
- Test report (from `/test`) - must show QA approval
- Code review verdict (from `/review`) - must show approval
- Architecture plan (from `/plan`) - for verification
- Target environment (staging/production)

## Preconditions
- `/test` passed - QA approved, no blocker issues
- `/review` passed - code quality approved
- All tests passing
- No unresolved blocker issues
- Code committed and pushed to repository
- Docker-compose configuration complete

## Process

### Step 1: Verify Quality Gates
**Owner**: tech_lead
**Actions**:
- Verify `/test` passed with QA approval
- Verify `/review` passed with reviewer approval
- Check that all blocker issues are resolved
- Confirm all acceptance criteria met
- Verify no scope creep beyond approved plan
- Check that framework standards followed (CLAUDE.md, `.claude/standards/`)
**Output**: Quality gates verification checklist

### Step 2: Docker-Compose Validation
**Owner**: devops
**Actions**:
- Test cold start: `docker-compose down -v && docker-compose up`
- Verify all services start and become healthy
- Check health endpoints return correct status
- Verify service dependencies work (depends_on with health checks)
- Test database migrations run successfully
- Verify environment variables loaded from `.env.example`
- Check logs are visible with `docker-compose logs`
- Verify no hardcoded secrets in configuration
- Test service restart behavior (crash recovery)
**Output**: Docker validation report

### Step 3: Release Notes Preparation
**Owner**: devops + tech_lead
**Actions**:
- Document what changed (features, fixes, improvements)
- List any breaking changes or migrations needed
- Document new environment variables (if any)
- Include deployment instructions
- Note any manual steps required (if unavoidable)
- Link to related issues/PRs
- Credit contributors
**Output**: Release notes document

### Step 4: Deployment Checklist Review
**Owner**: tech_lead + devops
**Actions**:
- **Infrastructure**:
  - [ ] docker-compose.yml complete and tested
  - [ ] All services have health checks
  - [ ] .env.example up to date
  - [ ] No hardcoded secrets
  - [ ] Volumes configured for persistent data
  - [ ] Database migrations tested
- **Code Quality**:
  - [ ] All tests pass (>80% coverage)
  - [ ] No blocker issues
  - [ ] Code reviewed and approved
  - [ ] Architecture matches approved plan
  - [ ] Standards compliance verified
- **AI-Specific** (if applicable):
  - [ ] All prompts versioned
  - [ ] Cost implications documented
  - [ ] Fallback behavior tested
  - [ ] AI requests logged with metadata
- **Security**:
  - [ ] No secrets in code or logs
  - [ ] Input validation implemented
  - [ ] No known vulnerabilities
  - [ ] Rate limiting in place
- **Documentation**:
  - [ ] .env.example updated
  - [ ] Release notes complete
  - [ ] Deployment instructions clear
  - [ ] README updated (if needed)
**Output**: Deployment checklist status

### Step 5: Final Approval and Deployment Authorization
**Owner**: tech_lead
**Actions**:
- Review all verification results
- Confirm deployment checklist complete
- Assess risk level (low/medium/high)
- Decide: **Approve** or **Reject** release
- If approved: Authorize deployment
- If rejected: Document blocking issues and required fixes
- Sign off on release with approval verdict
**Output**: **Ship approval** or **rejection with feedback**

### Step 6: Deployment Confirmation (Post-Deployment)
**Owner**: devops
**Actions**:
- Execute deployment (`docker-compose up -d` or CI/CD pipeline)
- Monitor service startup and health checks
- Verify all services running and healthy
- Check application logs for errors
- Test critical user flows in target environment
- Monitor for immediate issues (first 15-30 minutes)
- Confirm rollback plan is ready (if production)
**Output**: Deployment confirmation report

## Output artifacts
- **Ship approval**: Explicit approval or rejection from Tech Lead
- **Release notes**: What changed, breaking changes, deployment instructions
- **Deployment confirmation**: Proof that deployment succeeded and services are healthy
- **Rollback plan**: Steps to revert if issues occur (for production)

## Success criteria
- All quality gates passed (test, review)
- Docker-compose validated (cold start works)
- Deployment checklist complete
- No hardcoded secrets or configuration
- Tech Lead approved release
- Deployment successful (all services healthy)
- No critical issues in first 30 minutes post-deployment

## Gate
- **Blocker**: `/test` not passed or QA did not approve
- **Blocker**: `/review` not passed or reviewer did not approve
- **Blocker**: Docker-compose cold start fails
- **Blocker**: Hardcoded secrets found
- **Blocker**: Missing environment variables in `.env.example`
- **Blocker**: Database migrations fail
- **Blocker**: Health checks not implemented
- **Blocker**: Critical bugs discovered during final validation

When blockers are found, return to appropriate stage (`/implement`, `/test`, `/review`) to fix.

## Final authority
**Tech Lead** has final authority to approve or reject release. For production deployments, Product Owner may also need to approve business readiness.

## Related commands
- **test**: Must pass before ship
- **review**: Must pass before ship
- **plan**: Reference for verification (did we build what was planned?)
- **implement**: Return here if critical issues found during ship validation

---

## Deployment Checklist Template

```markdown
# Ship Readiness: [Feature/Version Name]

**Date**: 2025-01-15
**Target**: Production
**Tech Lead**: [Name]
**DevOps**: [Name]

## Quality Gates
✅ `/test` passed - QA approved (no blockers)
✅ `/review` passed - Reviewer approved
✅ All acceptance criteria met
✅ No scope creep detected

## Infrastructure Validation
✅ Cold start works (`docker-compose down -v && up`)
✅ All services start and become healthy
✅ Health checks implemented and passing
✅ Database migrations successful
✅ Environment variables from `.env.example`
✅ No hardcoded secrets
✅ Logs visible and structured
✅ Service restart/recovery works

## Code Quality
✅ All tests pass (coverage: 87%)
✅ No blocker issues
✅ Architecture matches plan
✅ Standards compliance verified

## AI-Specific (if applicable)
✅ Prompts versioned (v1.0)
✅ Cost: $0.05 per digest generation
✅ Fallback behavior tested
✅ AI requests logged with metadata

## Security
✅ No secrets in code/logs
✅ Input validation implemented
✅ No known vulnerabilities
✅ Rate limiting in place

## Documentation
✅ .env.example updated (3 new vars)
✅ Release notes complete
✅ Deployment instructions clear

## Risk Assessment
**Risk Level**: Low
- No database schema changes
- Backward compatible
- Tested in staging for 2 days
- Rollback plan ready

## Approval
✅ **APPROVED FOR PRODUCTION DEPLOYMENT**

**Tech Lead**: [Signature]
**Date**: 2025-01-15
```

---

## Release Notes Template

```markdown
# Release Notes: v1.2.0

**Release Date**: 2025-01-15
**Environment**: Production

## What's New

### Features
- **Digest Generation**: Users can now generate AI-powered digests from subscribed channels
- **Channel Management**: Improved UI for adding/removing channels with validation

### Improvements
- **Performance**: Digest generation 30% faster with caching
- **Error Handling**: Better error messages for rate limit scenarios
- **Logging**: All AI requests now logged with cost tracking

### Bug Fixes
- Fixed timeout issue when generating digests for 10+ channels
- Resolved FSM state persistence bug on bot restart
- Fixed callback query acknowledgment delay

## Breaking Changes
**None** - This release is backward compatible

## New Environment Variables
```bash
# Add to your .env file:
OPENAI_API_KEY=your_openai_key_here
DIGEST_CACHE_TTL=3600  # Optional, defaults to 3600
```

## Deployment Instructions

1. **Pull latest code**:
   ```bash
   git pull origin main
   ```

2. **Update environment**:
   ```bash
   cp .env.example .env.new
   # Merge new variables into your .env
   ```

3. **Deploy with docker-compose**:
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

4. **Verify deployment**:
   ```bash
   docker-compose ps  # All services should be healthy
   docker-compose logs -f bot  # Check for startup errors
   ```

5. **Test critical flows**:
   - Send `/start` to bot
   - Add a channel
   - Generate digest

## Rollback Plan
If issues occur:
```bash
git checkout v1.1.0
docker-compose down
docker-compose up -d
```

## Contributors
- Backend Dev (implementation)
- AI Engineer (digest feature)
- QA (testing)
- Tech Lead (architecture review)

## Metrics to Monitor
- Digest generation success rate (target: >95%)
- Average generation time (target: <10s)
- AI cost per digest (target: <$0.10)
- Bot response time (target: <2s)
```

---

## Ship Decision Matrix

| Condition | Action |
|-----------|--------|
| All gates passed, no issues | ✅ **SHIP** |
| Minor issues, workarounds exist | ✅ **SHIP** with monitoring |
| Major issues, not blocking core features | ⚠️ **SHIP TO STAGING**, hold production |
| Blocker issues found | ❌ **DO NOT SHIP** - fix first |
| Tests failing | ❌ **DO NOT SHIP** - return to `/test` |
| Review blocked | ❌ **DO NOT SHIP** - return to `/review` |
| Docker-compose fails | ❌ **DO NOT SHIP** - fix infrastructure |
| Secrets hardcoded | ❌ **DO NOT SHIP** - security issue |

---

## Post-Deployment Monitoring

### First 15 Minutes
- [ ] All services healthy
- [ ] No error spikes in logs
- [ ] Critical user flows work
- [ ] Database connections stable

### First Hour
- [ ] Performance metrics normal
- [ ] Error rate <1%
- [ ] No user complaints
- [ ] AI costs within budget

### First 24 Hours
- [ ] No regressions detected
- [ ] Success metrics met
- [ ] User feedback positive
- [ ] System stable

---

## Examples

### Ship Approval
```markdown
✅ **APPROVED FOR PRODUCTION SHIP**

All quality gates passed:
- Test: QA approved
- Review: No blockers
- Docker: Cold start verified
- Security: No secrets found

Release authorized for deployment on 2025-01-15 16:00 UTC.

**Tech Lead**: [Signature]
```

### Ship Rejection
```markdown
❌ **SHIP REJECTED**

Blocking issues found:
1. Docker-compose cold start fails (database migration error)
2. AI prompts not versioned in services/digest_service.py:45

Required actions:
- Fix database migration script
- Version all AI prompts per standards
- Re-run `/test` after fixes
- Re-submit for ship approval

**Tech Lead**: [Signature]
```
