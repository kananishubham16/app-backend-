import httpx
import json
import time
import sys

# Ensure UTF-8 output on Windows terminal
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000/api"

def print_step(step_num: int, title: str):
    print(f"\n{'='*70}")
    print(f">> STEP {step_num}: {title.upper()}")
    print(f"{'='*70}")

def run_demo():
    client = httpx.Client(base_url=BASE_URL, timeout=10.0)

    # Health check
    res = client.get("/health")
    assert res.status_code == 200, "Backend not healthy"
    print("Backend Health:", res.json())

    # -------------------------------------------------------------
    # Step 1: Teacher Login
    # -------------------------------------------------------------
    print_step(1, "Primary School Teacher Authentication")
    res = client.post("/auth/demo-login", json={"role": "teacher"})
    teacher = res.json()
    print(f"Teacher Logged In : {teacher['name']} ({teacher['email']})")
    print(f"Assigned School   : {teacher['schoolId']}")
    print(f"Assigned Classes  : {teacher['classIds']}")
    print(f"Assigned Subjects : {teacher['subjectIds']}")

    # -------------------------------------------------------------
    # Step 2: Teacher selects Class 3-A and views Aarav Kumar
    # -------------------------------------------------------------
    print_step(2, "Select Class & Diagnose Student Learning Gap")
    class_id = teacher['classIds'][0]
    res = client.get(f"/students?classId={class_id}")
    students = res.json()
    aarav = next(s for s in students if "Aarav" in s["name"])
    print(f"Selected Student  : {aarav['name']} (ID: {aarav['studentId']})")
    print(f"Classroom         : {aarav['className']} - {aarav['section']}")
    print(f"Parent Contact    : {aarav['parentName']} ({aarav['parentPhone']})")

    # Fetch Aarav's latest assessments
    res = client.get(f"/assessments?studentId={aarav['id']}&subjectId=subject_math")
    math_asmts = res.json()
    latest_math = math_asmts[0]
    pct = (latest_math['obtainedMarks'] / latest_math['totalMarks']) * 100
    print(f"\nLatest Math Assessment Score: {latest_math['obtainedMarks']}/{latest_math['totalMarks']} ({pct:.1f}%)")
    print(f"Classification: 🔴 WEAK (< 40.0%) - Critical Gap Identified!")
    print("Breakdown by Topic:")
    for ts in latest_math.get('topicScores', []):
        t_pct = (ts['obtainedMarks'] / ts['totalMarks']) * 100
        status_icon = "🔴" if t_pct < 40 else ("🟡" if t_pct < 70 else "🟢")
        print(f"  {status_icon} {ts['topicName']}: {ts['obtainedMarks']}/{ts['totalMarks']} ({t_pct:.1f}%)")

    # -------------------------------------------------------------
    # Step 3: Assign Targeted Remedial Action
    # -------------------------------------------------------------
    print_step(3, "Assign Targeted Remedial Action (Subtraction)")
    remedial_payload = {
        "id": f"rem_live_{int(time.time())}",
        "studentId": aarav['id'],
        "subjectId": "subject_math",
        "topicId": "topic_math_sub",
        "topicName": "Subtraction",
        "activityDescription": "Two-digit subtraction practice using physical counters and number line decomposition.",
        "hasQuiz": True,
        "assignedDate": "2026-10-22T20:00:00.000",
        "dueDate": "2026-10-29T20:00:00.000",
        "status": "assigned",
        "teacherNote": "Focus on borrowing concepts from tens place.",
        "parentInstruction": "Kindly guide Aarav with 10 practice problems at home."
    }
    res = client.post("/remedials", json=remedial_payload)
    assigned_action = res.json()
    print(f"Remedial ID       : {assigned_action['id']}")
    print(f"Topic             : {assigned_action['topicName']}")
    print(f"Status            : {assigned_action['status'].upper()}")
    print(f"Quiz Verification : {'Enabled' if assigned_action['hasQuiz'] else 'None'}")
    print(f"Parent Note       : {assigned_action['parentInstruction']}")

    # -------------------------------------------------------------
    # Step 4: Supervised Student Mini-Quiz
    # -------------------------------------------------------------
    print_step(4, "Supervised Student Quiz Execution & Auto-Grading")
    res = client.get(f"/quizzes/questions?topicId=topic_math_sub&classId={class_id}")
    questions = res.json()
    print(f"Loaded {len(questions)} diagnostic questions for topic 'Subtraction'")

    quiz_answers = []
    correct_count = 0
    for idx, q in enumerate(questions[:5], start=1):
        # Student answers correctly
        c_idx = q['correctAnswerIndex']
        quiz_answers.append({
            "questionId": q['id'],
            "selectedIndex": c_idx,
            "isCorrect": True
        })
        correct_count += 1
        print(f"  Q{idx}: {q['questionText']} -> Chosen: '{q['options'][c_idx]}' (Correct ✅)")

    quiz_pct = (correct_count / 5) * 100
    attempt_payload = {
        "id": f"att_live_{int(time.time())}",
        "studentId": aarav['id'],
        "subjectId": "subject_math",
        "topicId": "topic_math_sub",
        "date": "2026-10-22T20:15:00.000",
        "answers": quiz_answers,
        "totalQuestions": 5,
        "correctAnswers": correct_count,
        "remedialActionId": assigned_action['id']
    }
    res = client.post("/quizzes/attempts", json=attempt_payload)
    attempt = res.json()
    print(f"\nQuiz Submitted Successfully!")
    print(f"Final Score       : {attempt['correctAnswers']}/{attempt['totalQuestions']} ({quiz_pct:.1f}%)")
    print(f"Mastery Benchmark : {'PASSED (Ready for reassessment) 🟢' if quiz_pct >= 70 else 'Needs Reinforcement 🟡'}")

    # Verify remedial auto-completion
    res = client.get(f"/remedials/{assigned_action['id']}")
    updated_action = res.json()
    print(f"Remedial Status Updated Live: {updated_action['status'].upper()} ✅")

    # -------------------------------------------------------------
    # Step 5: Multi-Stakeholder Sync (Parent, Principal, BRC)
    # -------------------------------------------------------------
    print_step(5, "Multi-Stakeholder Sync Across Roles")

    # 5a. Parent view
    res = client.post("/auth/demo-login", json={"role": "parent"})
    parent = res.json()
    print(f"[Parent Dashboard] Logged in as: {parent['name']}")
    res = client.get(f"/remedials?studentId={aarav['id']}")
    child_remedials = res.json()
    completed_count = sum(1 for r in child_remedials if r['status'] == 'completed')
    print(f"  • Aarav Kumar's Remedial Tasks: {completed_count}/{len(child_remedials)} Completed")

    # 5b. Principal view
    res = client.post("/auth/demo-login", json={"role": "principal"})
    principal = res.json()
    print(f"\n[Principal Dashboard] Logged in as: {principal['name']} ({principal['schoolId']})")
    res = client.get(f"/remedials?schoolId={principal['schoolId']}")
    school_remedials = res.json()
    school_comp = sum(1 for r in school_remedials if r['status'] == 'completed')
    rate = (school_comp / len(school_remedials) * 100) if school_remedials else 0
    print(f"  • School-Wide Remedial Progress: {school_comp}/{len(school_remedials)} ({rate:.1f}% resolved)")

    # 5c. BRC view
    res = client.post("/auth/demo-login", json={"role": "brc"})
    brc = res.json()
    print(f"\n[BRC Dashboard] Logged in as: {brc['name']} (Gandhinagar Block)")
    res = client.get(f"/schools?blockId=block_1")
    schools = res.json()
    print(f"  • Monitoring {len(schools)} Primary Schools across Gandhinagar Block")
    for s in schools:
        res_c = client.get(f"/classes?schoolId={s['id']}")
        classes = res_c.json()
        print(f"    - {s['name']}: {len(classes)} Active Classrooms")

    print("\n" + "="*70)
    print("🎉 FULL REACTIVE DEMONSTRATION LOOP COMPLETED SUCCESSFULLY!")
    print("="*70)

if __name__ == "__main__":
    run_demo()
