const express = require('express');
const router = express.Router();
const {
  getDoubts,
  createDoubt,
  replyToDoubt,
  updateDoubtStatus,
  deleteDoubt
} = require('../controllers/doubtController');
const { verifyToken, requireRole, optionalAuth } = require('../middleware/auth');

router.get('/', optionalAuth, getDoubts);
router.post('/', createDoubt);
router.put('/:id/reply', optionalAuth, replyToDoubt);
router.put('/:id/status', optionalAuth, updateDoubtStatus);
router.delete('/:id', verifyToken, requireRole('admin'), deleteDoubt);

module.exports = router;
