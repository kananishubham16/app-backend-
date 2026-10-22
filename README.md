# Learning Setu - Backend REST API 🌉

> **Smart Tracking and Remedial Action System for Student Learning Gaps in Primary Schools**  
> **SFIC Hackathon 2026 • Problem ID: PS000060**

High-performance, asynchronous REST API powered by **Python 3.14**, **FastAPI**, and **SQLite (WAL Mode)**. It serves all 4 primary education stakeholders (Teachers, Principals, BRCs, and Parents).

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+ (or Python 3.14)
- `uv` (recommended) or standard `pip`

### 2. Setup Virtual Environment & Install Dependencies
```bash
cd backend
uv venv
# or python -m venv .venv

# Install dependencies
uv pip install -r requirements.txt
# or .venv\Scripts\pip install -r requirements.txt
```

### 3. Seed Database
The backend comes pre-packaged with Gujarat Gandhinagar educational block data, schools, classes, students, subjects, assessments, and quizzes.
```bash
.\.venv\Scripts\python -m app.seed
```

### 4. Run the API Server
```bash
.\.venv\Scripts\python run.py
```
Or with uvicorn:
```bash
.\.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📖 Interactive API Documentation

Once the server is running, open in your browser:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

## 🌐 API Endpoints Overview

| Module | Method | Endpoint | Description |
|---|---|---|---|
| **Auth** | `POST` | `/api/auth/login` | Authenticate with email/phone & password |
| **Auth** | `POST` | `/api/auth/demo-login` | 1-tap demo login by role (`teacher`, `principal`, `brc`, `parent`) |
| **Auth** | `GET` | `/api/auth/me` | Fetch active user profile |
| **Auth** | `POST` | `/api/auth/logout` | End session |
| **Hierarchy** | `GET` | `/api/blocks` | List educational blocks |
| **Hierarchy** | `GET` | `/api/schools` | List schools (optional `blockId` filter) |
| **Hierarchy** | `GET` | `/api/classes` | List classrooms (optional `schoolId` filter) |
| **Curriculum** | `GET` | `/api/subjects` | List subjects & topics (optional `classId` filter) |
| **Students** | `GET` | `/api/students` | Query students by `classId`, `schoolId`, `query`, or `ids` |
| **Students** | `GET` | `/api/students/{id}` | Get student profile |
| **Assessments** | `GET` | `/api/assessments` | Fetch student/class assessments |
| **Assessments** | `GET` | `/api/assessments/latest` | Latest benchmark score for student/subject |
| **Assessments** | `POST` | `/api/assessments` | Log new formative/summative assessment |
| **Remedials** | `GET` | `/api/remedials` | Fetch remedial tasks (student, class, or pending) |
| **Remedials** | `POST` | `/api/remedials` | Assign new targeted remedial action |
| **Remedials** | `PATCH` | `/api/remedials/{id}/status` | Update remedial status (`assigned`, `inProgress`, `completed`) |
| **Quizzes** | `GET` | `/api/quizzes/questions` | 5+ targeted MCQs for weak topics |
| **Quizzes** | `POST` | `/api/quizzes/attempts` | Save student quiz attempt & auto-evaluate |
| **Parent Reviews** | `GET` | `/api/reviews` | Retrieve parent home practice reviews |
| **Parent Reviews** | `POST` | `/api/reviews` | Submit parent review |
| **Parent Reviews** | `PATCH` | `/api/reviews/{id}/acknowledge` | Teacher acknowledgement of review |

---

## 🧪 Running Automated Tests
```bash
.\.venv\Scripts\python -m pytest tests
```
All 13 integration tests run in under 1 second.
