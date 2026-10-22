from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from app.database import Base

class Block(Base):
    __tablename__ = "blocks"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    district = Column(String, nullable=False)
    school_ids = Column(JSON, default=list)

class School(Base):
    __tablename__ = "schools"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    block_id = Column(String, index=True, nullable=False)
    block_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    principal_id = Column(String, nullable=False)

class ClassRoom(Base):
    __tablename__ = "classes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    section = Column(String, nullable=False)
    school_id = Column(String, index=True, nullable=False)
    teacher_id = Column(String, nullable=True)
    student_ids = Column(JSON, default=list)

class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    student_id = Column(String, nullable=False, index=True)  # Roll / Enrollment No
    class_id = Column(String, index=True, nullable=False)
    class_name = Column(String, nullable=False)
    section = Column(String, nullable=False)
    school_id = Column(String, index=True, nullable=False)
    school_name = Column(String, nullable=False)
    parent_id = Column(String, nullable=True, index=True)
    parent_name = Column(String, nullable=True)
    parent_phone = Column(String, nullable=True)

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon_name = Column(String, nullable=False)
    topics = Column(JSON, default=list)
    applicable_class_ids = Column(JSON, default=list)

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, index=True, nullable=False)
    subject_id = Column(String, index=True, nullable=False)
    type = Column(String, nullable=False, default="regular")
    date = Column(String, nullable=False)
    total_marks = Column(Float, nullable=False)
    obtained_marks = Column(Float, nullable=False)
    topic_scores = Column(JSON, default=list)
    notes = Column(Text, nullable=True)

class RemedialAction(Base):
    __tablename__ = "remedial_actions"

    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, index=True, nullable=False)
    subject_id = Column(String, index=True, nullable=False)
    topic_id = Column(String, index=True, nullable=False)
    topic_name = Column(String, nullable=False)
    activity_description = Column(Text, nullable=False)
    has_quiz = Column(Boolean, default=False)
    assigned_date = Column(String, nullable=False)
    due_date = Column(String, nullable=False)
    status = Column(String, nullable=False, default="assigned")
    teacher_note = Column(Text, nullable=True)
    parent_instruction = Column(Text, nullable=True)

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(String, primary_key=True, index=True)
    class_id = Column(String, index=True, nullable=False)
    subject_id = Column(String, index=True, nullable=False)
    topic_id = Column(String, index=True, nullable=False)
    difficulty = Column(String, nullable=False, default="medium")
    question_text = Column(Text, nullable=False)
    options = Column(JSON, default=list)
    correct_answer_index = Column(Integer, nullable=False)
    explanation = Column(Text, nullable=False)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, index=True, nullable=False)
    subject_id = Column(String, index=True, nullable=False)
    topic_id = Column(String, index=True, nullable=False)
    date = Column(String, nullable=False)
    answers = Column(JSON, default=list)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    remedial_action_id = Column(String, nullable=True)

class ParentReview(Base):
    __tablename__ = "parent_reviews"

    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, index=True, nullable=False)
    subject_id = Column(String, index=True, nullable=False)
    parent_name = Column(String, nullable=False)
    review_text = Column(Text, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=True)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String, nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False, default="demo123")
    role = Column(String, nullable=False)
    school_id = Column(String, nullable=True)
    block_id = Column(String, nullable=True)
    class_ids = Column(JSON, nullable=True)
    children_ids = Column(JSON, nullable=True)
    subject_ids = Column(JSON, nullable=True)
    avatar_initials = Column(String, nullable=True)
