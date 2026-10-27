const express = require('express');
const router = express.Router();
const {
  getSchools,
  getSchoolById,
  addSchool,
  getInspections,
  addInspection,
  getTrainings,
  addTraining,
  getDirectives,
  addDirective,
  updateDirective
} = require('../controllers/brcController');

// Schools
router.get('/schools', getSchools);
router.get('/schools/:id', getSchoolById);
router.post('/schools', addSchool);

// Inspections
router.get('/inspections', getInspections);
router.post('/inspections', addInspection);

// Trainings
router.get('/trainings', getTrainings);
router.post('/trainings', addTraining);

// Directives
router.get('/directives', getDirectives);
router.post('/directives', addDirective);
router.put('/directives/:id', updateDirective);

module.exports = router;
