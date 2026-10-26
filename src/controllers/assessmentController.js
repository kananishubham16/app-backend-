const Student = require('../models/Student');

const SUBJECT_ID_MAP = {
  'subject_math': 'Mathematics',
  'subject_eng': 'English',
  'subject_guj': 'Gujarati',
  'subject_hindi': 'Hindi',
  'subject_evs': 'EVS (Environmental Studies)',
  'Mathematics': 'Mathematics',
  'English': 'English',
  'Gujarati': 'Gujarati',
  'Hindi': 'Hindi',
  'EVS': 'EVS (Environmental Studies)',
  'EVS (Environmental Studies)': 'EVS (Environmental Studies)'
};

const SUBJECT_TO_ID = {
  'Mathematics': 'subject_math',
  'English': 'subject_eng',
  'Gujarati': 'subject_guj',
  'Hindi': 'subject_hindi',
  'EVS (Environmental Studies)': 'subject_evs',
  'EVS': 'subject_evs'
};

const extractAssessmentsFromStudent = (student, filterSubjectId) => {
  const assessments = [];
  if (!student.subjects) return assessments;

  const subjectsObj = student.subjects instanceof Map
    ? Object.fromEntries(student.subjects)
    : (student.subjects.toObject ? student.subjects.toObject() : student.subjects);

  for (const [subjName, subjData] of Object.entries(subjectsObj)) {
    const canonicalId = SUBJECT_TO_ID[subjName] || subjName.toLowerCase().replace(/[^a-z0-9]/g, '_');
    if (filterSubjectId && filterSubjectId !== canonicalId && filterSubjectId !== subjName) {
      continue;
    }

    const topicsObj = subjData.topics instanceof Map
      ? Object.fromEntries(subjData.topics)
      : (subjData.topics || {});

    const topicScores = Object.entries(topicsObj).map(([tName, score], idx) => ({
      topicId: `topic_${canonicalId}_${idx + 1}`,
      topicName: tName,
      totalMarks: 100,
      obtainedMarks: Number(score) || 0
    }));

    assessments.push({
      id: `asmt_${student.studentId}_${canonicalId}`,
      studentId: student.studentId,
      subjectId: canonicalId,
      subjectName: subjName,
      type: 'regular',
      date: student.updatedAt ? new Date(student.updatedAt).toISOString() : new Date().toISOString(),
      totalMarks: subjData.total || 100,
      obtainedMarks: subjData.marks || 0,
      topicScores,
      notes: student.remarks || 'Regular classroom diagnostic assessment.'
    });
  }

  return assessments;
};

// @desc    Get assessments by studentId, subjectId, or classId
// @route   GET /api/v1/assessments
exports.getAssessments = async (req, res, next) => {
  try {
    const { studentId, subjectId, classId } = req.query;
    const query = {};

    if (studentId) {
      query.studentId = studentId;
    }
    if (classId) {
      query.class = classId;
    }

    const students = await Student.find(query);
    let allAssessments = [];

    for (const student of students) {
      const studentAsmts = extractAssessmentsFromStudent(student, subjectId);
      allAssessments.push(...studentAsmts);
    }

    // Support both direct list response for Flutter and wrapped response
    if (req.query.format === 'wrapped') {
      return res.status(200).json({
        success: true,
        count: allAssessments.length,
        data: allAssessments
      });
    }

    res.status(200).json(allAssessments);
  } catch (err) {
    next(err);
  }
};

// @desc    Get latest assessment for a student and subject
// @route   GET /api/v1/assessments/latest
exports.getLatestAssessment = async (req, res, next) => {
  try {
    const { studentId, subjectId } = req.query;
    if (!studentId || !subjectId) {
      return res.status(400).json({ success: false, message: 'studentId and subjectId are required' });
    }

    const student = await Student.findOne({ studentId });
    if (!student) {
      return res.status(404).json({ success: false, message: 'Student not found' });
    }

    const assessments = extractAssessmentsFromStudent(student, subjectId);
    if (assessments.length === 0) {
      return res.status(404).json(null);
    }

    res.status(200).json(assessments[0]);
  } catch (err) {
    next(err);
  }
};

// @desc    Add or update assessment marks
// @route   POST /api/v1/assessments
exports.addAssessment = async (req, res, next) => {
  try {
    const { studentId, subjectId, obtainedMarks, topicScores, notes } = req.body;
    const student = await Student.findOne({ studentId });
    if (!student) {
      return res.status(404).json({ success: false, message: 'Student not found' });
    }

    const realSubjectName = SUBJECT_ID_MAP[subjectId] || subjectId;
    const currentSubjects = student.subjects instanceof Map
      ? Object.fromEntries(student.subjects)
      : (student.subjects ? student.subjects.toObject() : {});

    const topicsMap = {};
    if (Array.isArray(topicScores)) {
      topicScores.forEach((ts) => {
        topicsMap[ts.topicName] = ts.obtainedMarks;
      });
    }

    currentSubjects[realSubjectName] = {
      total: 100,
      marks: Math.round(Number(obtainedMarks) || 0),
      topics: topicsMap
    };

    if (notes) {
      student.remarks = notes;
    }

    student.subjects = currentSubjects;
    await student.save();

    const createdAsmt = extractAssessmentsFromStudent(student, subjectId)[0] || {
      id: `asmt_${student.studentId}_${subjectId}`,
      studentId,
      subjectId,
      type: 'regular',
      date: new Date().toISOString(),
      totalMarks: 100,
      obtainedMarks: Number(obtainedMarks) || 0,
      topicScores: topicScores || [],
      notes
    };

    res.status(201).json(createdAsmt);
  } catch (err) {
    next(err);
  }
};
