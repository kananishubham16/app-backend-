from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

# ----------------- Auth & Users -----------------
class UserLoginRequest(BaseSchema):
    email_or_phone: str
    password: Optional[str] = "demo123"

class DemoLoginRequest(BaseSchema):
    role: str
    user_id: Optional[str] = None

class UserModel(BaseSchema):
    id: str
    name: str
    email: str
    phone: str
    role: str
    school_id: Optional[str] = None
    block_id: Optional[str] = None
    class_ids: Optional[List[str]] = None
    children_ids: Optional[List[str]] = None
    subject_ids: Optional[List[str]] = None
    avatar_initials: Optional[str] = None

# ----------------- School, Block & Class -----------------
class BlockModel(BaseSchema):
    id: str
    name: str
    district: str
    school_ids: List[str]

class SchoolModel(BaseSchema):
    id: str
    name: str
    block_id: str
    block_name: str
    address: str
    principal_id: str

class ClassModel(BaseSchema):
    id: str
    name: str
    section: str
    school_id: str
    teacher_id: Optional[str] = None
    student_ids: List[str]

# ----------------- Subject & Topics -----------------
class TopicModel(BaseSchema):
    id: str
    name: str
    subject_id: str
    learning_objectives: List[str]
    order_index: int

class SubjectModel(BaseSchema):
    id: str
    name: str
    description: str
    icon_name: str
    topics: List[TopicModel]
    applicable_class_ids: List[str]

# ----------------- Students -----------------
class StudentModel(BaseSchema):
    id: str
    name: str
    student_id: str
    class_id: str
    class_name: str
    section: str
    school_id: str
    school_name: str
    parent_id: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None

# ----------------- Assessments -----------------
class TopicScore(BaseSchema):
    topic_id: str
    topic_name: str
    total_marks: float
    obtained_marks: float

class AssessmentModel(BaseSchema):
    id: str
    student_id: str
    subject_id: str
    type: str  # 'regular', 'remedialQuiz'
    date: str
    total_marks: float
    obtained_marks: float
    topic_scores: List[TopicScore]
    notes: Optional[str] = None

# ----------------- Remedials -----------------
class RemedialAction(BaseSchema):
    id: str
    student_id: str
    subject_id: str
    topic_id: str
    topic_name: str
    activity_description: str
    has_quiz: bool = False
    assigned_date: str
    due_date: str
    status: str  # 'assigned', 'inProgress', 'completed', 'needsFollowUp'
    teacher_note: Optional[str] = None
    parent_instruction: Optional[str] = None

class RemedialStatusUpdate(BaseSchema):
    status: str

# ----------------- Quizzes -----------------
class QuizQuestion(BaseSchema):
    id: str
    class_id: str
    subject_id: str
    topic_id: str
    difficulty: str
    question_text: str
    options: List[str]
    correct_answer_index: int
    explanation: str

class QuizAnswer(BaseSchema):
    question_id: str
    selected_index: int
    is_correct: bool

class QuizAttempt(BaseSchema):
    id: str
    student_id: str
    subject_id: str
    topic_id: str
    date: str
    answers: List[QuizAnswer]
    total_questions: int
    correct_answers: int
    remedial_action_id: Optional[str] = None

# ----------------- Parent Review -----------------
class ParentReviewModel(BaseSchema):
    id: str
    student_id: str
    subject_id: str
    parent_name: str
    review_text: str
    created_at: str
    updated_at: Optional[str] = None
    is_acknowledged: bool = False
    acknowledged_by: Optional[str] = None

class ParentReviewAcknowledge(BaseSchema):
    acknowledged_by: str
