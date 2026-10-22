import json
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from app.database import get_db
from app.schemas import ParentReviewModel, ParentReviewAcknowledge

router = APIRouter(prefix="/reviews", tags=["Parent Feedback & Reviews"])

@router.get("", response_model=List[ParentReviewModel])
def get_reviews(
    student_id: Optional[str] = Query(None, alias="studentId"),
    subject_id: Optional[str] = Query(None, alias="subjectId")
):
    with get_db() as conn:
        sql = "SELECT data FROM parent_reviews WHERE 1=1"
        params = []
        if student_id:
            sql += " AND student_id = ?"
            params.append(student_id)
        if subject_id:
            sql += " AND subject_id = ?"
            params.append(subject_id)
        rows = conn.execute(sql, params).fetchall()
        return [ParentReviewModel.model_validate(json.loads(r["data"])) for r in rows]

@router.post("", response_model=ParentReviewModel)
def add_review(review: ParentReviewModel):
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO parent_reviews (id, student_id, subject_id, data) VALUES (?, ?, ?, ?)",
            (
                review.id,
                review.student_id,
                review.subject_id,
                json.dumps(review.model_dump(by_alias=True))
            )
        )
        return review

@router.patch("/{review_id}/acknowledge", response_model=ParentReviewModel)
def acknowledge_review(review_id: str, body: ParentReviewAcknowledge):
    with get_db() as conn:
        row = conn.execute("SELECT data FROM parent_reviews WHERE id = ?", (review_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Review not found")
        data = json.loads(row["data"])
        data["isAcknowledged"] = True
        data["acknowledgedBy"] = body.acknowledged_by
        data["updatedAt"] = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "UPDATE parent_reviews SET data = ? WHERE id = ?",
            (json.dumps(data), review_id)
        )
        return ParentReviewModel.model_validate(data)
