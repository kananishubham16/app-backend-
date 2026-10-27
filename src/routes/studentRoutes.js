const express = require('express');
const router = express.Router();
const {
  getStudents,
  getStudentById,
  createStudent,
  updateStudent,
  deleteStudent,
  bulkImportStudents
} = require('../controllers/studentController');
const { optionalAuth } = require('../middleware/auth');

router.get('/', optionalAuth, getStudents);
router.get('/:id', optionalAuth, getStudentById);
router.post('/', optionalAuth, createStudent);
router.put('/:id', optionalAuth, updateStudent);
router.delete('/:id', optionalAuth, deleteStudent);
router.post('/bulk', optionalAuth, bulkImportStudents);

module.exports = router;
