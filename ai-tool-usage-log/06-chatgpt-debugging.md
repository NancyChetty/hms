# ChatGPT — Debugging and Fixes

## Topics Covered
- CSRF errors
- Login redirect bugs
- Duplicate views
- Dashboard refresh problems
- Ghost database records

## Example Prompts

### Prompt
Why does dashboard redirect to login after reload?

### Response Summary
- Session issue
- Duplicate view definitions
- Missing login_required

---

### Prompt
Why does deleted user still appear?

### Response Summary
- PostgreSQL stale records
- Foreign key dependencies
- Delete related records first

---

### Prompt
Why is CSRF verification failing?

### Response Summary
- Old session cookies
- Missing csrf_token
- Clear browser cookies