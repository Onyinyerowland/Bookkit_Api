# BookIt API — FastAPI + PostgreSQL

A production-ready REST API for **BookIt**, a bookings platform where users can browse services, make bookings, and leave reviews. Admins manage users, services, and bookings.

---

## Features


- **Authentication & Authorization**
- JWT-based access + refresh tokens
- Passwords hashed using **bcrypt**
- Role-based access control (`user`, `admin`)
- `401 Unauthorized` for unauthenticated requests
- `403 Forbidden` for unauthorized access


- **Users**
- Register, login, logout, refresh
- Profile management (`/me`)


- **Services**
- Public: search & browse services
- Admin: full CRUD


- **Bookings**
- Users: create, manage, cancel their own
- Admin: view/update all bookings
- Conflict detection: prevents overlapping bookings


- **Reviews**
- Users: review completed bookings
- One review per booking
- Admin: manage reviews


- **Database**
- **PostgreSQL** (chosen for relational integrity, transactions, and scalability)
- Migrations handled with **Alembic**


- **Documentation**
- Auto-generated Swagger UI at `/docs`
- Redoc at `/redoc`


- **Production-ready**
- Structured logging
- Configurable via environment variables
- Docker & docker-compose support


---


## Why PostgreSQL?


- Strong relational integrity for bookings, services, and reviews.
- ACID guarantees ensure no double-bookings.
- Rich support for constraints (unique, foreign keys, enums).
- Widely supported, robust for production workloads.


---

## Project Structure

```

bookit-fastapi-postgres/
├── alembic/ # Migration scripts
├── app/
│ ├── main.py # FastAPI entrypoint
│ ├── Routers (auth, services, bookings, reviews, users)
│ ├── core/ # Config, security utils, logging
│ ├── db/ # Session, base class
│ ├── models/ # SQLAlchemy models
│ ├── repositories/ # DB queries
│ ├── schemas/ # Pydantic models
│ ├── services/ # Business logic
  ├── deps/ # Dependencies
│ └── utils/ # Helpers (tokens, hashing)
├── tests/ # pytest test suite
├── alembic.ini # Alembic config
├── Dockerfile # Container build
├── docker-compose.yml # DB + app orchestration
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

## API Endpoints


### Auth
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`


### Users
- `GET /me` — Get current user profile
- `PATCH /me` — Update profile


### Services
- `GET /services` — Public list with filters (`q`, `price_min`, `price_max`, `active`)
- `GET /services/{id}` — Service details
- `POST /services` (admin)
- `PATCH /services/{id}` (admin)
- `DELETE /services/{id}` (admin)


### Bookings
- `POST /bookings` — User creates booking (conflict validation)
- `GET /bookings` — User: their bookings; Admin: all (filters: `status`, `from`, `to`)
- `GET /bookings/{id}` — Owner or admin
- `PATCH /bookings/{id}` — Owner (reschedule/cancel if pending/confirmed), Admin (update status)
- `DELETE /bookings/{id}` — Owner (before start), Admin (anytime)


### Reviews
- `POST /reviews` — For completed booking, one per booking
- `GET /services/{id}/reviews`
- `PATCH /reviews/{id}` — Owner
- `DELETE /reviews/{id}` — Owner or admin

---

## Environment Variables


Create `.env`:


| Variable              | Description                     | Example |
|---------------------  |--------------------------------------------
| `DATABASE_URL`        | PostgreSQL connection string    |`postgresql://user:pass@localhost:5432/bookit` |
| `SECRET_KEY`          | Secret key for JWT signing      | `supersecret` |
| `ACCESS_TOKEN_EXPIRE` | Access token lifetime (minutes) | `15` |
| `REFRESH_TOKEN_EXPIRE`| Refresh token lifetime (days)   | `7` |
| `LOG_LEVEL`           | Logging level                   | `INFO` |


---

## Running Locally


```bash
# 1. Clone repo
$ git clone https://github.com/onyinyerowland/bookit_Api
$ cd bookit_Api


# 2. Create virtualenv
$ python -m venv venv
$ source venv/bin/activate


# 3. Install deps
$ pip install -r requirements.txt


# 4. Start Postgres (via docker-compose)
$ docker-compose up -d


# 5. Run migrations
$ alembic upgrade head


# 6. Run API
$ uvicorn app.main:app --reload
```


Visit Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)


---


## Deployment


- **Containerized** with Docker
- Deployable on **PipeOps** or any cloud provider
- Expose port 80/443 with TLS
- Example production command:


```bash
docker-compose -f docker-compose.yml up -d --build
```


**Public Base URL (example)**: `https://bookit.pipeops.app`


- API docs: `https://bookit.pipeops.app/docs`
- Redoc: `https://bookit.pipeops.app/redoc`


---


## Testing


Run unit + integration tests with pytest:


```bash
pytest -v
```


Covers:
- Auth flow (register/login/refresh/logout)
- Booking conflict logic
- Permissions (user vs admin)
- Happy/unhappy paths with status code assertions


---


## Roadmap
- Payment integration
- Email/notification service
- Admin dashboard UI (React/Next.js)
- CI/CD with GitHub Actions


---
