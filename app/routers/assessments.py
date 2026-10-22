import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.database import get_db
from app.schemas import AssessmentModel

router = APIRouter(prefix="/assessments", tags=["Assessments"])

@router.get("", response_model=List[AssessmentModel])
def get_assessments(
    student_id: Optional[str] = Query(None, alias="studentId"),
    subject_id: Optional[str] = Query(None, alias="subjectId"),
    class_id: Optional[str] = Query(None, alias="classId"),
    type: Optional[str] = Query(None)
):
    with get_db() as conn:
        if class_id:
            # Find students in this class
            st_rows = conn.execute("SELECT id FROM students WHERE class_id = ?", (class_id,)).fetchall()
            student_ids = [r["id"] for r in st_rows]
            if not student_ids:
                return []
            placeholders = ",".join("?" for _ in student_ids)
            sql = f"SELECT data FROM assessments WHERE student_id IN ({placeholders})"
            params = list(student_ids)
            if subject_id:
                sql += " AND subject_id = ?"
                params.append(subject_id)
            if type:
                sql += " AND type = ?"
                params.append(type)
            sql += " ORDER BY date DESC"
            rows = conn.execute(sql, params).fetchall()
            return [AssessmentModel.model_validate(json.loads(r["data"])) for r in rows]

        sql = "SELECT data FROM assessments WHERE 1=1"
        params = []
        if student_id:
            sql += " AND student_id = ?"
            params.append(student_id)
        if subject_id:
            sql += " AND subject_id = ?"
            params.append(subject_id)
        if type:
            sql += " AND type = ?"
            params.append(type)

        sql += " ORDER BY date DESC"
        rows = conn.execute(sql, params).fetchall()
        return [AssessmentModel.model_validate(json.loads(r["data"])) for r in rows]

@router.get("/latest", response_model=Optional[AssessmentModel])
def get_latest_assessment(
    student_id: str = Query(..., alias="studentId"),
    subject_id: str = Query(..., alias="subjectId"),
    type: Optional[str] = Query(None)
):
    with get_db() as conn:
        sql = "SELECT data FROM assessments WHERE student_id = ? AND subject_id = ?"
        params = [student_id, subject_id]
        if type:
            sql += " AND type = ?"
            params.append(type)
        sql += " ORDER BY date DESC LIMIT 1"
        row = conn.execute(sql, params).fetchone()
        if not row:
            return None
        return AssessmentModel.model_validate(json.loads(row["data"]))

@router.get("/{assessment_id}", response_model=AssessmentModel)
def get_assessment(assessment_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT data FROM assessments WHERE id = ?", (assessment_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Assessment not found")
        return AssessmentModel.model_validate(json.loads(row["data"]))

@router.post("", response_model=AssessmentModel)
def add_assessment(assessment: AssessmentModel):
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO assessments (id, student_id, subject_id, type, date, data) VALUES (?, ?, ?, ?, ?, ?)",
            (
                assessment.id,
                assessment.student_id,
                assessment.subject_id,
                assessment.type,
                assessment.date,
                json.dumps(assessment.model_dump(by_alias=True))
            )
        )
        return assessment
