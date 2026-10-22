from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.config import settings
from app.database import init_db
from app.seed import seed_database
from app.routers import (
    auth,
    schools,
    subjects,
    students,
    assessments,
    remedials,
    quizzes,
    reviews,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_database(force=False)
    yield

app = FastAPI(
    title="Learning Setu REST API",
    description="""
# Learning Setu (લર્નિંગ સેતુ) 🌉
### Smart Tracking and Remedial Action System for Student Learning Gaps in Primary Schools
**SFIC Hackathon 2026 • Problem ID: PS000060**

This backend services all 4 primary education stakeholders:
- 👨‍🏫 **Primary School Teachers**: Diagnostic logging, class assessments, remedial actions, quiz verification.
- 🏫 **School Principals**: School-wide mastery analytics, class & subject comparative performance.
- 🌐 **Block Resource Coordinators (BRC)**: Multi-school block analytics, coverage tracking, targeted school support.
- 👨‍👩‍👧 **Parents**: Linked child diagnostics, home practice instructions, direct quiz launch.
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Enable CORS for Flutter apps (Web, Android Emulator, iOS, Desktop)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "mode": "production-ready"
    }

# Mount API Routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(schools.router, prefix=settings.API_PREFIX)
app.include_router(subjects.router, prefix=settings.API_PREFIX)
app.include_router(students.router, prefix=settings.API_PREFIX)
app.include_router(assessments.router, prefix=settings.API_PREFIX)
app.include_router(remedials.router, prefix=settings.API_PREFIX)
app.include_router(quizzes.router, prefix=settings.API_PREFIX)
app.include_router(reviews.router, prefix=settings.API_PREFIX)
