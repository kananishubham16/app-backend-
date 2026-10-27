const mongoose = require('mongoose');

const characterBadgeSchema = new mongoose.Schema({
  id: { type: String, required: true },
  badgeKey: { type: String, required: true },
  title: { type: String, required: true },
  titleGu: { type: String, required: true },
  iconName: { type: String, required: true },
  awardedBy: { type: String, required: true },
  awardedAt: { type: Date, default: Date.now },
  note: { type: String, default: '' }
});

const holisticEvaluationSchema = new mongoose.Schema(
  {
    studentId: {
      type: String,
      required: true,
      unique: true,
      trim: true
    },
    practiceGrit: {
      type: Number,
      default: 75.0,
      min: 0,
      max: 100
    },
    learningConsistency: {
      type: Number,
      default: 80.0,
      min: 0,
      max: 100
    },
    engagementCuriosity: {
      type: Number,
      default: 75.0,
      min: 0,
      max: 100
    },
    teamworkEmpathy: {
      type: Number,
      default: 80.0,
      min: 0,
      max: 100
    },
    coCurricular: {
      type: Number,
      default: 75.0,
      min: 0,
      max: 100
    },
    badges: [characterBadgeSchema],
    teacherNotes: {
      type: String,
      default: ''
    },
    strengths: [{ type: String }],
    growthAreas: [{ type: String }]
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true }
  }
);

holisticEvaluationSchema.virtual('compositeScore').get(function () {
  const score =
    this.practiceGrit * 0.25 +
    this.learningConsistency * 0.25 +
    this.engagementCuriosity * 0.2 +
    this.teamworkEmpathy * 0.15 +
    this.coCurricular * 0.15;
  return Math.min(100, Math.max(0, Math.round(score * 10) / 10));
});

module.exports = mongoose.model('HolisticEvaluation', holisticEvaluationSchema);
