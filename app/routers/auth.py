import json
from fastapi import APIRouter, HTTPException, Query
from app.database import get_db
from app.schemas import UserModel, UserLoginRequest, DemoLoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=UserModel)
def login(req: UserLoginRequest):
    query = req.email_or_phone.strip().lower()
    clean_phone = "".join(req.email_or_phone.split())

    with get_db() as conn:
        # Match email or phone
        rows = conn.execute("SELECT data FROM users").fetchall()
        for row in rows:
            u = json.loads(row["data"])
            u_email = u.get("email", "").lower()
            u_phone = "".join(u.get("phone", "").split())
            if u_email == query or u_phone == clean_phone:
                return UserModel.model_validate(u)

    raise HTTPException(status_code=401, detail="Invalid email or password")

@router.post("/demo-login", response_model=UserModel)
def demo_login(req: DemoLoginRequest):
    with get_db() as conn:
        if req.user_id:
            row = conn.execute("SELECT data FROM users WHERE id = ?", (req.user_id,)).fetchone()
            if row:
                return UserModel.model_validate(json.loads(row["data"]))

        # Match by role
        row = conn.execute("SELECT data FROM users WHERE role = ? LIMIT 1", (req.role,)).fetchone()
        if row:
            return UserModel.model_validate(json.loads(row["data"]))

    raise HTTPException(status_code=404, detail=f"No demo user found for role '{req.role}'")

@router.get("/me", response_model=UserModel)
def get_current_user(user_id: str = Query(..., alias="userId")):
    with get_db() as conn:
        row = conn.execute("SELECT data FROM users WHERE id = ?", (user_id,)).fetchone()
        if row:
            return UserModel.model_validate(json.loads(row["data"]))
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}
