# Command: /integrate_ai

## Goal
Add or modify AI functionality (LLM, RAG, embeddings) with proper prompt versioning, error handling, and observability.

## When to use
- Adding new AI-powered features (chat, summarization, classification)
- Integrating LLM providers (OpenAI, Anthropic, local models)
- Building RAG pipelines for knowledge retrieval
- Implementing AI-based validation or processing
- Modifying existing AI prompts or models
- Adding new embeddings or vector search capabilities

## Agents involved
- **ai_engineer**: Designs and implements LLM integrations, RAG pipelines, prompt engineering, fallback logic
- **tech_lead**: Reviews AI architecture, validates prompt versioning, approves model choices and costs

## Input required
- Feature requirements (what AI should do)
- Expected input/output format
- Performance requirements (latency, cost)
- Fallback behavior specification
- Relevant standards from `.claude/standards/rag.md`

## Preconditions
- AI feature is scoped in `/discovery` or `/plan`
- Budget for API costs is approved
- Acceptance criteria are clear
- Test scenarios are defined (including failure modes)

## Process

### Step 1: AI Architecture Design
**Owner**: ai_engineer
**Actions**:
- Choose appropriate model (GPT-4, GPT-4o-mini, Claude, etc.)
- Design prompt template with versioning
- Define input validation and sanitization
- Plan token budget and cost estimation
- Design retry logic with exponential backoff
- Define fallback behavior for AI failures
- Plan structured output format (JSON mode if applicable)
- Document expected latency and cost per request
**Output**: AI architecture document with model choices, prompts, fallbacks

### Step 2: Prompt Engineering
**Owner**: ai_engineer
**Actions**:
- Create versioned prompt template (see `.claude/standards/rag.md`)
- Test prompt with various inputs (edge cases, adversarial inputs)
- Optimize for token efficiency
- Add system instructions and constraints
- Define output format and validation
- Test for hallucinations and incorrect outputs
- Document prompt version, creation date, and purpose
**Output**: Versioned prompt template with metadata

### Step 3: Implementation
**Owner**: ai_engineer
**Actions**:
- Implement AI service with proper error handling
- Add retry logic with exponential backoff (max 3 retries)
- Implement fallback behavior for failures
- Add structured logging (prompt version, input, output, tokens, cost, latency)
- Use environment variables for API keys (never hardcode)
- Implement request/response validation
- Add timeout handling (set reasonable timeouts)
- Test with edge cases and failure scenarios
**Output**: Working AI integration with error handling

### Step 4: Observability and Testing
**Owner**: ai_engineer
**Actions**:
- Log all AI requests with structured format:
  - Prompt version
  - Model used
  - Input/output
  - Token usage (prompt, completion, total)
  - Cost estimate
  - Latency
  - Success/failure status
- Implement monitoring for:
  - Success rate
  - Average latency
  - Cost per request
  - Hallucination detection (if applicable)
- Write tests with mocked AI responses
- Test failure modes (timeout, rate limit, invalid response)
- Document cost implications
**Output**: Monitored AI service with comprehensive logging

### Step 5: Tech Lead Review
**Owner**: tech_lead
**Actions**:
- Review prompt versioning compliance
- Validate error handling and retry logic
- Check logging completeness
- Assess cost implications
- Verify fallback behavior
- Approve or request changes
**Output**: Approval verdict with feedback

## Output artifacts
- **Versioned prompt templates**: All prompts with version, date, description
- **AI service implementation**: Code with retry, fallback, logging
- **Cost estimates**: Expected cost per request and monthly projections
- **Monitoring dashboards**: Success rate, latency, cost tracking
- **Test coverage**: Unit tests with mocked AI, failure scenario tests

## Success criteria
- All prompts are versioned (no magic strings)
- Retry logic implemented with exponential backoff
- Fallback behavior defined and tested
- All AI requests logged with full metadata
- Error handling covers all failure modes (timeout, rate limit, invalid response)
- Cost per request is documented and approved
- Tests cover success and failure scenarios
- Tech Lead has approved the implementation

## Gate
- **Blocker**: Prompts are not versioned (magic strings found)
- **Blocker**: No retry logic or fallback behavior
- **Blocker**: AI requests not logged with metadata
- **Blocker**: Cost implications not documented
- **Blocker**: Failure modes not tested
- **Blocker**: API keys hardcoded (must use environment variables)
- **Blocker**: Tech Lead has not approved

## Final authority
**Tech Lead** has final authority to approve or reject AI integration based on:
- Prompt versioning compliance
- Error handling completeness
- Cost implications
- Observability standards

## Related commands
- **plan**: May call `/integrate_ai` during planning if AI architecture needs detailed design
- **implement**: Calls `/integrate_ai` when implementing AI-specific tasks
- **test**: Tests AI features with mocked responses and failure scenarios
- **review**: Reviews AI code for compliance with standards

---

## Examples

### LLM Integration
```python
# prompts/summarization.py
SUMMARIZE_V1 = PromptVersion(
    version="v1.0",
    created_at="2025-01-15",
    description="Summarize Telegram channel posts",
    template="Summarize the following posts in 3-5 sentences:\n\n{posts}"
)
```

### RAG Pipeline
```python
# services/rag_service.py
async def generate_answer(question: str) -> dict:
    chunks = await retrieval.retrieve(question, top_k=5)
    prompt = RAG_PROMPT_V1.template.format(context=chunks, question=question)
    response = await llm.generate(prompt)
    logger.info("rag_request", prompt_version="v1.0", tokens=response.usage.total_tokens)
    return {"answer": response.content, "sources": chunks}
```

### Error Handling
```python
# Retry with exponential backoff
for attempt in range(3):
    try:
        response = await openai.chat.completions.create(...)
        break
    except RateLimitError:
        await asyncio.sleep(2 ** attempt)
    except Exception as e:
        logger.error("ai_request_failed", error=str(e))
        return fallback_response()
```
