import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.database import get_db
from app.schemas import QuizQuestion, QuizAttempt

router = APIRouter(prefix="/quizzes", tags=["Quizzes & Evaluation"])

@router.get("/questions", response_model=List[QuizQuestion])
def get_quiz_questions(
    topic_id: str = Query(..., alias="topicId"),
    class_id: Optional[str] = Query("", alias="classId"),
    subject_id: Optional[str] = Query("", alias="subjectId")
):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT data FROM quiz_questions WHERE topic_id = ?",
            (topic_id,)
        ).fetchall()
        all_questions = [QuizQuestion.model_validate(json.loads(r["data"])) for r in rows]

        if not all_questions:
            return []

        if not class_id:
            return all_questions

        # Try matching class specifically
        class_matches = [
            q for q in all_questions
            if not q.class_id or q.class_id == class_id or q.class_id in class_id or class_id in q.class_id
        ]

        if len(class_matches) >= 5:
            return class_matches

        # Combine fallback to ensure at least 5 questions if available
        combined = list(class_matches)
        for q in all_questions:
            if not any(c.id == q.id for c in combined):
                combined.append(q)

        return combined

@router.post("/attempts", response_model=QuizAttempt)
def save_quiz_attempt(attempt: QuizAttempt):
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO quiz_attempts (id, student_id, topic_id, remedial_action_id, data) VALUES (?, ?, ?, ?, ?)",
            (
                attempt.id,
                attempt.student_id,
                attempt.topic_id,
                attempt.remedial_action_id,
                json.dumps(attempt.model_dump(by_alias=True))
            )
        )
        # If this attempt was linked to a remedial action, and score >= 70%, we can optionally mark it completed!
        if attempt.remedial_action_id:
            rem_row = conn.execute("SELECT data FROM remedial_actions WHERE id = ?", (attempt.remedial_action_id,)).fetchone()
            if rem_row:
                rem_data = json.loads(rem_row["data"])
                # update status if passed
                pct = (attempt.correct_answers / attempt.total_questions * 100) if attempt.total_questions > 0 else 0
                if pct >= 70:
                    rem_data["status"] = "completed"
                    conn.execute("UPDATE remedial_actions SET status = 'completed', data = ? WHERE id = ?", (json.dumps(rem_data), attempt.remedial_action_id))

        return attempt

@router.get("/attempts", response_model=List[QuizAttempt])
def get_quiz_attempts(
    student_id: Optional[str] = Query(None, alias="studentId"),
    topic_id: Optional[str] = Query(None, alias="topicId")
):
    with get_db() as conn:
        sql = "SELECT data FROM quiz_attempts WHERE 1=1"
        params = []
        if student_id:
            sql += " AND student_id = ?"
            params.append(student_id)
        if topic_id:
            sql += " AND topic_id = ?"
            params.append(topic_id)
        rows = conn.execute(sql, params).fetchall()
        return [QuizAttempt.model_validate(json.loads(r["data"])) for r in rows]
