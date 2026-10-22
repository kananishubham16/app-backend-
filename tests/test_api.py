import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
from app.seed import seed_database

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    init_db()
    seed_database(force=True)

client = TestClient(app)

def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_auth_demo_login():
    for role in ["teacher", "principal", "brc", "parent"]:
        res = client.post("/api/auth/demo-login", json={"role": role})
        assert res.status_code == 200
        data = res.json()
        assert data["role"] == role
        assert "name" in data
        assert "id" in data

def test_auth_login():
    res = client.post("/api/auth/login", json={"emailOrPhone": "teacher@demo.com", "password": "demo123"})
    assert res.status_code == 200
    assert res.json()["email"] == "teacher@demo.com"

def test_get_blocks():
    res = client.get("/api/blocks")
    assert res.status_code == 200
    blocks = res.json()
    assert len(blocks) >= 1
    assert blocks[0]["id"] == "block_1"

def test_get_schools():
    res = client.get("/api/schools?blockId=block_1")
    assert res.status_code == 200
    schools = res.json()
    assert len(schools) == 3

def test_get_classes():
    res = client.get("/api/classes?schoolId=school_1")
    assert res.status_code == 200
    classes = res.json()
    assert len(classes) == 2

def test_get_students():
    res = client.get("/api/students?classId=class_3a_s1")
    assert res.status_code == 200
    students = res.json()
    assert len(students) >= 5

def test_get_student_search():
    res = client.get("/api/students?query=Aarav")
    assert res.status_code == 200
    students = res.json()
    assert len(students) >= 1
    assert "Aarav" in students[0]["name"]

def test_get_subjects():
    res = client.get("/api/subjects")
    assert res.status_code == 200
    subjects = res.json()
    assert len(subjects) == 4

def test_get_assessments():
    res = client.get("/api/assessments?studentId=student_1")
    assert res.status_code == 200
    assessments = res.json()
    assert len(assessments) >= 1

def test_remedial_flow():
    # 1. Fetch remedials
    res = client.get("/api/remedials?studentId=student_1")
    assert res.status_code == 200
    remedials = res.json()
    assert len(remedials) >= 1
    first_id = remedials[0]["id"]

    # 2. Update status
    res = client.patch(f"/api/remedials/{first_id}/status", json={"status": "inProgress"})
    assert res.status_code == 200
    assert res.json()["status"] == "inProgress"

def test_quiz_questions_and_attempts():
    # 1. Fetch questions for subtraction
    res = client.get("/api/quizzes/questions?topicId=topic_math_sub")
    assert res.status_code == 200
    questions = res.json()
    assert len(questions) >= 5

    # 2. Submit quiz attempt
    attempt_payload = {
        "id": "test_attempt_001",
        "studentId": "student_1",
        "subjectId": "subject_math",
        "topicId": "topic_math_sub",
        "date": "2026-10-22T10:00:00.000",
        "answers": [
            {"questionId": questions[0]["id"], "selectedIndex": questions[0]["correctAnswerIndex"], "isCorrect": True}
        ],
        "totalQuestions": 5,
        "correctAnswers": 5,
        "remedialActionId": None
    }
    res = client.post("/api/quizzes/attempts", json=attempt_payload)
    assert res.status_code == 200
    assert res.json()["id"] == "test_attempt_001"

def test_parent_reviews():
    review_payload = {
        "id": "rev_001",
        "studentId": "student_1",
        "subjectId": "subject_math",
        "parentName": "Suresh Kumar",
        "reviewText": "Aarav is practicing subtraction at home.",
        "createdAt": "2026-10-22T12:00:00.000",
        "isAcknowledged": False
    }
    res = client.post("/api/reviews", json=review_payload)
    assert res.status_code == 200

    # Acknowledge review
    res = client.patch("/api/reviews/rev_001/acknowledge", json={"acknowledgedBy": "Anita Sharma"})
    assert res.status_code == 200
    assert res.json()["isAcknowledged"] is True
