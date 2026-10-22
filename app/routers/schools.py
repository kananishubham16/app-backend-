import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.database import get_db
from app.schemas import BlockModel, SchoolModel, ClassModel

router = APIRouter(tags=["Schools & Hierarchy"])

# ----------------- Blocks -----------------
@router.get("/blocks", response_model=List[BlockModel])
def get_blocks():
    with get_db() as conn:
        rows = conn.execute("SELECT data FROM blocks").fetchall()
        return [BlockModel.model_validate(json.loads(r["data"])) for r in rows]

@router.get("/blocks/{block_id}", response_model=BlockModel)
def get_block(block_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT data FROM blocks WHERE id = ?", (block_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Block not found")
        return BlockModel.model_validate(json.loads(row["data"]))

# ----------------- Schools -----------------
@router.get("/schools", response_model=List[SchoolModel])
def get_schools(block_id: Optional[str] = Query(None, alias="blockId")):
    with get_db() as conn:
        if block_id:
            rows = conn.execute("SELECT data FROM schools WHERE block_id = ?", (block_id,)).fetchall()
        else:
            rows = conn.execute("SELECT data FROM schools").fetchall()
        return [SchoolModel.model_validate(json.loads(r["data"])) for r in rows]

@router.get("/schools/{school_id}", response_model=SchoolModel)
def get_school(school_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT data FROM schools WHERE id = ?", (school_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="School not found")
        return SchoolModel.model_validate(json.loads(row["data"]))

# ----------------- Classes -----------------
@router.get("/classes", response_model=List[ClassModel])
def get_classes(
    school_id: Optional[str] = Query(None, alias="schoolId"),
    teacher_id: Optional[str] = Query(None, alias="teacherId")
):
    with get_db() as conn:
        if school_id and teacher_id:
            rows = conn.execute(
                "SELECT data FROM classes WHERE school_id = ? AND teacher_id = ?",
                (school_id, teacher_id)
            ).fetchall()
        elif school_id:
            rows = conn.execute("SELECT data FROM classes WHERE school_id = ?", (school_id,)).fetchall()
        elif teacher_id:
            rows = conn.execute("SELECT data FROM classes WHERE teacher_id = ?", (teacher_id,)).fetchall()
        else:
            rows = conn.execute("SELECT data FROM classes").fetchall()
        return [ClassModel.model_validate(json.loads(r["data"])) for r in rows]

@router.get("/classes/{class_id}", response_model=ClassModel)
def get_class(class_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT data FROM classes WHERE id = ?", (class_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Class not found")
        return ClassModel.model_validate(json.loads(row["data"]))
