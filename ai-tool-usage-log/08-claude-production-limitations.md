# Claude — Production Limitations

## Topics Covered
- Production scaling
- Security
- Async tasks
- Deployment risks

## Example Prompts

### Prompt
What would break in production?

### Response Summary
- Synchronous email sending
- No task queue
- Race conditions
- Weak notification system

---

### Prompt
What should be improved first?

### Response Summary
- Add Celery + Redis
- Secure OAuth tokens
- Add Docker
- Disable DEBUG mode