import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.database import get_db
from app.schemas import StudentModel

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("", response_model=List[StudentModel])
def get_students(
    class_id: Optional[str] = Query(None, alias="classId"),
    school_id: Optional[str] = Query(None, alias="schoolId"),
    parent_id: Optional[str] = Query(None, alias="parentId"),
    ids: Optional[str] = Query(None, description="Comma-separated student IDs"),
    query: Optional[str] = Query(None, description="Search by name or roll number")
):
    with get_db() as conn:
        if ids:
            id_list = [i.strip() for i in ids.split(",") if i.strip()]
            if not id_list:
                return []
            placeholders = ",".join("?" for _ in id_list)
            rows = conn.execute(
                f"SELECT data FROM students WHERE id IN ({placeholders})", id_list
            ).fetchall()
            return [StudentModel.model_validate(json.loads(r["data"])) for r in rows]

        sql = "SELECT data FROM students WHERE 1=1"
        params = []

        if class_id:
            sql += " AND class_id = ?"
            params.append(class_id)
        if school_id:
            sql += " AND school_id = ?"
            params.append(school_id)
        if parent_id:
            sql += " AND parent_id = ?"
            params.append(parent_id)

        rows = conn.execute(sql, params).fetchall()
        students = [StudentModel.model_validate(json.loads(r["data"])) for r in rows]

        if query:
            q = query.strip().lower()
            students = [
                s for s in students
                if q in s.name.lower() or q in s.student_id.lower()
            ]

        return students

@router.get("/{student_id}", response_model=StudentModel)
def get_student(student_id: str):
    with get_db() as conn:
        row = conn.execute(
            "SELECT data FROM students WHERE id = ? OR student_id = ?",
            (student_id, student_id)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Student not found")
        return StudentModel.model_validate(json.loads(row["data"]))

@router.post("", response_model=StudentModel)
def create_student(student: StudentModel):
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO students (id, name, student_id, class_id, school_id, parent_id, data) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                student.id,
                student.name,
                student.student_id,
                student.class_id,
                student.school_id,
                student.parent_id,
                json.dumps(student.model_dump(by_alias=True))
            )
        )
        return student
