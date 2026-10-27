const express = require('express');
const router = express.Router();
const holisticController = require('../controllers/holisticController');

router.get('/:studentId', holisticController.getHolisticByStudent);
router.post('/:studentId/badge', holisticController.awardBadge);
router.put('/:studentId', holisticController.updateMetrics);

module.exports = router;
