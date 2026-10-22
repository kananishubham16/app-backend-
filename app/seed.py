import json
import os
from app.database import init_db, get_db

def seed_database(force: bool = False):
    init_db()

    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM schools").fetchone()[0]
        if not force and count > 0:
            print("Database already contains data. Skipping seeding.")
            return

        seed_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "seed_data.json")
        if not os.path.exists(seed_file_path):
            print(f"Seed file not found at {seed_file_path}")
            return

        with open(seed_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if force:
            for table in [
                "blocks", "schools", "classes", "students", "subjects",
                "assessments", "remedial_actions", "quiz_questions",
                "quiz_attempts", "parent_reviews", "users"
            ]:
                conn.execute(f"DELETE FROM {table}")

        # 1. Blocks
        for b in data.get("blocks", []):
            conn.execute(
                "INSERT OR REPLACE INTO blocks (id, name, district, data) VALUES (?, ?, ?, ?)",
                (b["id"], b["name"], b["district"], json.dumps(b))
            )

        # 2. Schools
        for s in data.get("schools", []):
            conn.execute(
                "INSERT OR REPLACE INTO schools (id, name, block_id, data) VALUES (?, ?, ?, ?)",
                (s["id"], s["name"], s["blockId"], json.dumps(s))
            )

        # 3. Classes
        for c in data.get("classes", []):
            conn.execute(
                "INSERT OR REPLACE INTO classes (id, name, section, school_id, teacher_id, data) VALUES (?, ?, ?, ?, ?, ?)",
                (c["id"], c["name"], c["section"], c["schoolId"], c.get("teacherId"), json.dumps(c))
            )

        # 4. Students
        for st in data.get("students", []):
            conn.execute(
                "INSERT OR REPLACE INTO students (id, name, student_id, class_id, school_id, parent_id, data) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (st["id"], st["name"], st["studentId"], st["classId"], st["schoolId"], st.get("parentId"), json.dumps(st))
            )

        # 5. Subjects
        for sub in data.get("subjects", []):
            conn.execute(
                "INSERT OR REPLACE INTO subjects (id, name, data) VALUES (?, ?, ?)",
                (sub["id"], sub["name"], json.dumps(sub))
            )

        # 6. Assessments
        for a in data.get("assessments", []):
            conn.execute(
                "INSERT OR REPLACE INTO assessments (id, student_id, subject_id, type, date, data) VALUES (?, ?, ?, ?, ?, ?)",
                (a["id"], a["studentId"], a["subjectId"], a.get("type", "regular"), a["date"], json.dumps(a))
            )

        # 7. Remedial Actions
        for r in data.get("remedialActions", []):
            conn.execute(
                "INSERT OR REPLACE INTO remedial_actions (id, student_id, subject_id, topic_id, status, data) VALUES (?, ?, ?, ?, ?, ?)",
                (r["id"], r["studentId"], r["subjectId"], r["topicId"], r.get("status", "assigned"), json.dumps(r))
            )

        # 8. Quiz Questions
        for q in data.get("quizQuestions", []):
            conn.execute(
                "INSERT OR REPLACE INTO quiz_questions (id, class_id, subject_id, topic_id, difficulty, data) VALUES (?, ?, ?, ?, ?, ?)",
                (q["id"], q["classId"], q["subjectId"], q["topicId"], q.get("difficulty", "medium"), json.dumps(q))
            )

        # 9. Quiz Attempts
        for qa in data.get("quizAttempts", []):
            conn.execute(
                "INSERT OR REPLACE INTO quiz_attempts (id, student_id, topic_id, remedial_action_id, data) VALUES (?, ?, ?, ?, ?)",
                (qa["id"], qa["studentId"], qa["topicId"], qa.get("remedialActionId"), json.dumps(qa))
            )

        # 10. Demo Users
        for u in data.get("demoUsers", []):
            conn.execute(
                "INSERT OR REPLACE INTO users (id, email, phone, role, password, data) VALUES (?, ?, ?, ?, ?, ?)",
                (u["id"], u["email"].lower(), u["phone"], u["role"], "demo123", json.dumps(u))
            )

        print("Database initialized and successfully seeded with SFIC 2026 data!")

if __name__ == "__main__":
    seed_database(force=True)
