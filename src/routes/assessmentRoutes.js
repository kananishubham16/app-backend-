const express = require('express');
const router = express.Router();
const { getAssessments, getLatestAssessment, addAssessment } = require('../controllers/assessmentController');

router.get('/latest', getLatestAssessment);
router.get('/', getAssessments);
router.post('/', addAssessment);

module.exports = router;
