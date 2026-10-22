import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.database import get_db
from app.schemas import RemedialAction, RemedialStatusUpdate

router = APIRouter(prefix="/remedials", tags=["Remedial Actions"])

@router.get("", response_model=List[RemedialAction])
def get_remedials(
    student_id: Optional[str] = Query(None, alias="studentId"),
    class_id: Optional[str] = Query(None, alias="classId"),
    school_id: Optional[str] = Query(None, alias="schoolId"),
    pending_only: Optional[bool] = Query(False, alias="pendingOnly")
):
    with get_db() as conn:
        if class_id:
            st_rows = conn.execute("SELECT id FROM students WHERE class_id = ?", (class_id,)).fetchall()
            student_ids = [r["id"] for r in st_rows]
            if not student_ids:
                return []
            placeholders = ",".join("?" for _ in student_ids)
            sql = f"SELECT data FROM remedial_actions WHERE student_id IN ({placeholders})"
            params = list(student_ids)
            if pending_only:
                sql += " AND status IN ('assigned', 'inProgress')"
            rows = conn.execute(sql, params).fetchall()
            return [RemedialAction.model_validate(json.loads(r["data"])) for r in rows]

        if school_id:
            st_rows = conn.execute("SELECT id FROM students WHERE school_id = ?", (school_id,)).fetchall()
            student_ids = [r["id"] for r in st_rows]
            if not student_ids:
                return []
            placeholders = ",".join("?" for _ in student_ids)
            sql = f"SELECT data FROM remedial_actions WHERE student_id IN ({placeholders})"
            params = list(student_ids)
            if pending_only:
                sql += " AND status IN ('assigned', 'inProgress')"
            rows = conn.execute(sql, params).fetchall()
            return [RemedialAction.model_validate(json.loads(r["data"])) for r in rows]

        sql = "SELECT data FROM remedial_actions WHERE 1=1"
        params = []
        if student_id:
            sql += " AND student_id = ?"
            params.append(student_id)
        if pending_only:
            sql += " AND status IN ('assigned', 'inProgress')"

        rows = conn.execute(sql, params).fetchall()
        return [RemedialAction.model_validate(json.loads(r["data"])) for r in rows]

@router.get("/{remedial_id}", response_model=RemedialAction)
def get_remedial(remedial_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT data FROM remedial_actions WHERE id = ?", (remedial_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Remedial action not found")
        return RemedialAction.model_validate(json.loads(row["data"]))

@router.post("", response_model=RemedialAction)
def add_remedial(action: RemedialAction):
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO remedial_actions (id, student_id, subject_id, topic_id, status, data) VALUES (?, ?, ?, ?, ?, ?)",
            (
                action.id,
                action.student_id,
                action.subject_id,
                action.topic_id,
                action.status,
                json.dumps(action.model_dump(by_alias=True))
            )
        )
        return action

@router.patch("/{remedial_id}/status", response_model=RemedialAction)
def update_remedial_status(remedial_id: str, body: RemedialStatusUpdate):
    with get_db() as conn:
        row = conn.execute("SELECT data FROM remedial_actions WHERE id = ?", (remedial_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Remedial action not found")
        data = json.loads(row["data"])
        data["status"] = body.status
        conn.execute(
            "UPDATE remedial_actions SET status = ?, data = ? WHERE id = ?",
            (body.status, json.dumps(data), remedial_id)
        )
        return RemedialAction.model_validate(data)
