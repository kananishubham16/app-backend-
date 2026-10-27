const express = require('express');
const router = express.Router();
const { getAdvice, createAdvice, updateAdviceStatus, deleteAdvice } = require('../controllers/adviceController');
const { verifyToken, requireRole, optionalAuth } = require('../middleware/auth');

router.get('/', optionalAuth, getAdvice);
router.post('/', optionalAuth, createAdvice);
router.put('/:id/status', optionalAuth, updateAdviceStatus);
router.delete('/:id', verifyToken, requireRole('coordinator', 'admin'), deleteAdvice);

module.exports = router;
