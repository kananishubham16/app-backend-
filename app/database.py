import sqlite3
import json
import os
from contextlib import contextmanager

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "learning_setu.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS blocks (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            district TEXT NOT NULL,
            data JSON NOT NULL
        );

        CREATE TABLE IF NOT EXISTS schools (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            block_id TEXT NOT NULL,
            data JSON NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_schools_block ON schools(block_id);

        CREATE TABLE IF NOT EXISTS classes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            section TEXT NOT NULL,
            school_id TEXT NOT NULL,
            teacher_id TEXT,
            data JSON NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_classes_school ON classes(school_id);

        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL,
            class_id TEXT NOT NULL,
            school_id TEXT NOT NULL,
            parent_id TEXT,
            data JSON NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_students_class ON students(class_id);
        CREATE INDEX IF NOT EXISTS idx_students_school ON students(school_id);
        CREATE INDEX IF NOT EXISTS idx_students_parent ON students(parent_id);

        CREATE TABLE IF NOT EXISTS subjects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            data JSON NOT NULL
        );

        CREATE TABLE IF NOT EXISTS assessments (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            subject_id TEXT NOT NULL,
            type TEXT NOT NULL,
            date TEXT NOT NULL,
            data JSON NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_assessments_student ON assessments(student_id);
        CREATE INDEX IF NOT EXISTS idx_assessments_subj ON assessments(student_id, subject_id);

        CREATE TABLE IF NOT EXISTS remedial_actions (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            subject_id TEXT NOT NULL,
            topic_id TEXT NOT NULL,
            status TEXT NOT NULL,
            data JSON NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_remedial_student ON remedial_actions(student_id);
        CREATE INDEX IF NOT EXISTS idx_remedial_status ON remedial_actions(status);

        CREATE TABLE IF NOT EXISTS quiz_questions (
            id TEXT PRIMARY KEY,
            class_id TEXT NOT NULL,
            subject_id TEXT NOT NULL,
            topic_id TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            data JSON NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_quiz_q_topic ON quiz_questions(topic_id);
        CREATE INDEX IF NOT EXISTS idx_quiz_q_class ON quiz_questions(class_id);

        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            topic_id TEXT NOT NULL,
            remedial_action_id TEXT,
            data JSON NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_quiz_att_student ON quiz_attempts(student_id);
        CREATE INDEX IF NOT EXISTS idx_quiz_att_topic ON quiz_attempts(student_id, topic_id);

        CREATE TABLE IF NOT EXISTS parent_reviews (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            subject_id TEXT NOT NULL,
            data JSON NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_reviews_student ON parent_reviews(student_id);

        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            role TEXT NOT NULL,
            password TEXT NOT NULL DEFAULT 'demo123',
            data JSON NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
        CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
        """)
