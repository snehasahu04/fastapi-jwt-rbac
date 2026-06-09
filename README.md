# FastAPI JWT RBAC

A complete FastAPI project implementing **JWT-based authentication** with **Role-Based Access Control (RBAC)**, email notifications, and CI/CD pipeline.

## Features

✅ **User Authentication**
- Signup with email and password
- Login with JWT token generation
- Password hashing with bcrypt

✅ **Role-Based Access Control (RBAC)**
- 4 user roles: `admin`, `team_leader`, `trainee`, `intern`
- Permission-based endpoint protection
- Role-based data visibility

✅ **User Management**
- Admin can assign admin rights
- Team leaders can promote trainees to interns
- User profile retrieval (`/me`)

✅ **Email Notifications**
- Signup alerts
- Login alerts
- Promotion notifications

✅ **Automated Testing & CI/CD**
- Unit tests with pytest
- GitHub Actions CI workflow
- Automated validation on push/PR

---

## Installation

### Prerequisites
- Python 3.12+
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/snehasahu04/fastapi-jwt-rbac.git
   cd fastapi-jwt-rbac
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional)
   ```bash
   set SECRET_KEY=your-secret-key
   set DATABASE_URL=sqlite:///./test.db
   set SENDER_EMAIL=your-email@gmail.com
   set EMAIL_APP_PASSWORD=your-app-password
   set INITIAL_ADMIN_EMAIL=admin@example.com
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

Server runs on `http://localhost:8000`

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register new user |
| POST | `/login` | Login and get JWT token |
| GET | `/me` | Get current user profile |

### User Management (Admin only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/assign-admin/{user_id}` | Assign admin role |

### Team Leader & Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/trainees` | View all trainees |
| GET | `/interns` | View all interns |
| PUT | `/promote/{user_id}` | Promote trainee to intern |

---

## Example Usage

### Signup
```bash
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret12"}'
```

### Login
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret12"}'
```

Response includes `access_token`:
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGc...",
  "user_id": 1,
  "role": "trainee"
}
```

### Get Current User (with Bearer token)
```bash
curl -X GET http://localhost:8000/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Role Permissions

```
trainee:       []  (no special permissions)
intern:        []  (no special permissions)
team_leader:   ["promote_to_intern", "view_trainees", "view_interns"]
admin:         ["promote_to_intern", "view_trainees", "view_interns", "assign_admin"]
```

---

## Testing

Run the test suite:
```bash
pytest -q
```

All tests pass locally and via CI/CD on GitHub Actions.

---

## CI/CD Pipeline

GitHub Actions workflow runs on every `push` and `pull_request`:

1. ✅ Checkout code
2. ✅ Set up Python 3.12
3. ✅ Install dependencies
4. ✅ Run pytest
5. ✅ Validate Python syntax
6. ✅ Import FastAPI app

View workflow: `.github/workflows/ci.yml`

---

## Database

- **Type**: SQLite (default: `test.db`)
- **Schema**: User model with `id`, `email`, `hashed_password`, `role`
- **ORM**: SQLAlchemy

---

## Security

- 🔐 Passwords hashed with bcrypt
- 🔐 JWT tokens with expiry (60 mins default)
- 🔐 Role-based authorization on all protected endpoints
- 🔐 Email validation

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `supersecretkey123` | JWT signing key |
| `DATABASE_URL` | `sqlite:///./test.db` | Database connection string |
| `SENDER_EMAIL` | `snehademo4@gmail.com` | Gmail sender email |
| `EMAIL_APP_PASSWORD` | (Gmail App Password) | Gmail app password |
| `ADMIN_EMAIL` | SENDER_EMAIL | Admin notification email |
| `INITIAL_ADMIN_EMAIL` | (empty) | Email to make admin on first signup |

---

## Project Structure

```
fastapi-jwt-rbac/
├── main.py                 # App entry point
├── routes.py               # API endpoints
├── auth.py                 # JWT & password hashing
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── database.py             # Database config
├── dependencies.py         # Auth dependencies
├── email_utils.py          # Email notifications
├── roles.py                # Role permissions
├── requirements.txt        # Python dependencies
├── .github/workflows/ci.yml # GitHub Actions CI
└── tests/                  # Test suite
    ├── conftest.py
    └── test_app.py
```

---

## License

MIT

---

## Support

For issues or questions, create a GitHub issue or contact the maintainer.

**Repository**: https://github.com/snehasahu04/fastapi-jwt-rbac