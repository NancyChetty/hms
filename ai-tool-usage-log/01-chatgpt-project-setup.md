# ChatGPT — Project Setup

## Topics Covered
- Django project creation
- PostgreSQL setup
- Custom user model
- Authentication system
- Migrations

## Example Prompts

### Prompt
How do I connect PostgreSQL with Django?

### Response Summary
- Install psycopg2
- Configure DATABASES in settings.py
- Create database
- Run migrations

---

### Prompt
How do I create a custom user model with doctor and patient roles?

### Response Summary
- Extend AbstractUser
- Add role field
- Configure AUTH_USER_MODEL

---

### Prompt
Why is createsuperuser failing?

### Response Summary
- Missing migrations
- Undefined database column
- Run makemigrations and migrate

---

### Prompt
How do I fix login redirect issues?

### Response Summary
- Use role-based redirects
- Protect dashboards using login_required