const HolisticEvaluation = require('../models/HolisticEvaluation');

// Preset templates for fallback lookups
const BADGE_TEMPLATES = {
  high_effort: {
    title: 'High Effort & Grit',
    titleGu: 'ખંત અને સાતત્યપૂર્ણ પ્રયાસ',
    iconName: 'track_changes_outlined',
    category: 'effort'
  },
  curious_mind: {
    title: 'Curious Questioner',
    titleGu: 'જિજ્ઞાસુ વિદ્યાર્થી',
    iconName: 'lightbulb_outline',
    category: 'curiosity'
  },
  team_player: {
    title: 'Team Player & Empathy',
    titleGu: 'સહકાર અને ટીમવર્ક',
    iconName: 'handshake_outlined',
    category: 'teamwork'
  },
  creative_thinker: {
    title: 'Creative Thinker',
    titleGu: 'સર્જનાત્મક વિચારસરણી',
    iconName: 'palette_outlined',
    category: 'creativity'
  },
  active_sport: {
    title: 'Energetic & Well-being',
    titleGu: 'ઉત્સાહી અને શારીરિક સુદ્રઢતા',
    iconName: 'sports_volleyball_outlined',
    category: 'cocurricular'
  }
};

/**
 * Get or seed student's 360 Holistic Evaluation
 * GET /api/v1/holistic/:studentId
 */
exports.getHolisticByStudent = async (req, res, next) => {
  try {
    const { studentId } = req.params;
    let evaluation = await HolisticEvaluation.findOne({ studentId });

    if (!evaluation) {
      // Create seed evaluation for the student
      evaluation = await HolisticEvaluation.create({
        studentId,
        practiceGrit: 82.0,
        learningConsistency: 85.0,
        engagementCuriosity: 78.0,
        teamworkEmpathy: 84.0,
        coCurricular: 80.0,
        teacherNotes: 'Demonstrates active participation and sincere effort in daily classroom tasks.',
        strengths: ['Regular attendance', 'Helpful peer collaboration'],
        growthAreas: ['Oral presentation confidence'],
        badges: [
          {
            id: `b_${Date.now()}_1`,
            badgeKey: 'curious_mind',
            title: 'Curious Questioner',
            titleGu: 'જિજ્ઞાસુ વિદ્યાર્થી',
            iconName: 'lightbulb_outline',
            awardedBy: 'Class Teacher',
            awardedAt: new Date(Date.now() - 3 * 86400000),
            note: 'Asked thoughtful questions during science reading.'
          }
        ]
      });
    }

    res.status(200).json({
      success: true,
      data: evaluation
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Award 1-tap Micro Shout-out Badge (Supports single badgeKey or multiple badgeKeys)
 * POST /api/v1/holistic/:studentId/badge
 */
exports.awardBadge = async (req, res, next) => {
  try {
    const { studentId } = req.params;
    const { badgeKey, badgeKeys, title, titleGu, iconName, awardedBy, note } = req.body;

    const keysToAward = Array.isArray(badgeKeys) && badgeKeys.length > 0
      ? badgeKeys
      : (badgeKey ? [badgeKey] : []);

    if (keysToAward.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'badgeKey or badgeKeys array is required'
      });
    }

    let evaluation = await HolisticEvaluation.findOne({ studentId });
    if (!evaluation) {
      evaluation = new HolisticEvaluation({ studentId });
    }

    const createdBadges = [];
    keysToAward.forEach((key, index) => {
      const template = BADGE_TEMPLATES[key] || {};
      const newBadge = {
        id: `b_${Date.now()}_${index}`,
        badgeKey: key,
        title: (keysToAward.length === 1 && title) ? title : (template.title || 'Positive Shout-Out'),
        titleGu: (keysToAward.length === 1 && titleGu) ? titleGu : (template.titleGu || 'સકારાત્મક પ્રોત્સાહન'),
        iconName: (keysToAward.length === 1 && iconName) ? iconName : (template.iconName || 'star'),
        awardedBy: awardedBy || 'Teacher',
        awardedAt: new Date(Date.now() + index * 10),
        note: note || 'Recognized for excellent positive attitude in class.'
      };

      createdBadges.push(newBadge);
      evaluation.badges.unshift(newBadge);

      // Reinforce trait score according to badge type
      if (key === 'high_effort') {
        evaluation.practiceGrit = Math.min(100, evaluation.practiceGrit + 3.0);
      } else if (key === 'curious_mind') {
        evaluation.engagementCuriosity = Math.min(100, evaluation.engagementCuriosity + 4.0);
      } else if (key === 'team_player') {
        evaluation.teamworkEmpathy = Math.min(100, evaluation.teamworkEmpathy + 4.0);
      } else if (key === 'creative_thinker') {
        evaluation.engagementCuriosity = Math.min(100, evaluation.engagementCuriosity + 3.0);
        evaluation.coCurricular = Math.min(100, evaluation.coCurricular + 3.0);
      } else if (key === 'active_sport') {
        evaluation.coCurricular = Math.min(100, evaluation.coCurricular + 5.0);
      }
    });

    if (note) {
      evaluation.teacherNotes = note;
    }

    await evaluation.save();

    res.status(200).json({
      success: true,
      message: `${keysToAward.length} badge(s) successfully awarded!`,
      data: evaluation,
      awardedBadges: createdBadges
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Update holistic metrics (e.g. from automated jobs or teacher notes)
 * PUT /api/v1/holistic/:studentId
 */
exports.updateMetrics = async (req, res, next) => {
  try {
    const { studentId } = req.params;
    const {
      practiceGrit,
      learningConsistency,
      engagementCuriosity,
      teamworkEmpathy,
      coCurricular,
      teacherNotes,
      strengths,
      growthAreas
    } = req.body;

    let evaluation = await HolisticEvaluation.findOne({ studentId });
    if (!evaluation) {
      evaluation = new HolisticEvaluation({ studentId });
    }

    if (practiceGrit !== undefined) evaluation.practiceGrit = Number(practiceGrit);
    if (learningConsistency !== undefined) evaluation.learningConsistency = Number(learningConsistency);
    if (engagementCuriosity !== undefined) evaluation.engagementCuriosity = Number(engagementCuriosity);
    if (teamworkEmpathy !== undefined) evaluation.teamworkEmpathy = Number(teamworkEmpathy);
    if (coCurricular !== undefined) evaluation.coCurricular = Number(coCurricular);
    if (teacherNotes !== undefined) evaluation.teacherNotes = teacherNotes;
    if (strengths !== undefined) evaluation.strengths = strengths;
    if (growthAreas !== undefined) evaluation.growthAreas = growthAreas;

    await evaluation.save();

    res.status(200).json({
      success: true,
      message: 'Holistic evaluation updated successfully',
      data: evaluation
    });
  } catch (error) {
    next(error);
  }
};
