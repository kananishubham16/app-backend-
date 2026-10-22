import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.database import get_db
from app.schemas import SubjectModel

router = APIRouter(prefix="/subjects", tags=["Curriculum & Subjects"])

@router.get("", response_model=List[SubjectModel])
def get_subjects(class_id: Optional[str] = Query(None, alias="classId")):
    with get_db() as conn:
        rows = conn.execute("SELECT data FROM subjects").fetchall()
        all_subjects = [SubjectModel.model_validate(json.loads(r["data"])) for r in rows]

        if not class_id:
            return all_subjects

        # Filter subjects applicable to classId
        filtered = []
        for s in all_subjects:
            if not s.applicable_class_ids:
                filtered.append(s)
            elif class_id in s.applicable_class_ids:
                filtered.append(s)
            elif any(class_id in cid or cid in class_id for cid in s.applicable_class_ids):
                filtered.append(s)

        return filtered if filtered else all_subjects

@router.get("/{subject_id}", response_model=SubjectModel)
def get_subject(subject_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT data FROM subjects WHERE id = ?", (subject_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Subject not found")
        return SubjectModel.model_validate(json.loads(row["data"]))
