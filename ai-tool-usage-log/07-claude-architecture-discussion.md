# Claude — Architecture Discussion

## Topics Covered
- System architecture
- Database relationships
- Microservice separation
- Scalability discussion

## Example Prompts

### Prompt
Should email handling stay inside Django or be separated?

### Response Summary
- Separate service recommended
- Better modularity
- Easier scaling
- Cleaner architecture

---

### Prompt
How should booking approval workflow work?

### Response Summary
- Use pending → confirmed lifecycle
- Prevent direct booking confirmation
- Better hospital workflow realism

---

### Prompt
How should notifications be structured?

### Response Summary
- Create Notification model
- Store user-based alerts
- Add timestamp tracking