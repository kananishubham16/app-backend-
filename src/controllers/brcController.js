const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, '../data');
const schoolsFile = path.join(dataDir, 'block_schools.json');
const inspectionsFile = path.join(dataDir, 'inspections.json');
const trainingsFile = path.join(dataDir, 'trainings.json');
const directivesFile = path.join(dataDir, 'directives.json');

const readData = (filePath, fallback = []) => {
  try {
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(content);
    }
  } catch (err) {
    console.error(`Error reading ${filePath}:`, err);
  }
  return fallback;
};

const writeData = (filePath, data) => {
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
  } catch (err) {
    console.error(`Error writing ${filePath}:`, err);
  }
};

// --- Schools ---
exports.getSchools = (req, res) => {
  let schools = readData(schoolsFile);
  const { cluster } = req.query;
  if (cluster && cluster !== 'All') {
    schools = schools.filter((s) => s.cluster && s.cluster.toLowerCase() === cluster.toLowerCase());
  }
  res.status(200).json(schools);
};

exports.getSchoolById = (req, res) => {
  const { id } = req.params;
  const schools = readData(schoolsFile);
  const match = schools.find((s) => s.id === id);
  if (match) {
    res.status(200).json(match);
  } else {
    res.status(404).json({ error: 'School not found' });
  }
};

exports.addSchool = (req, res) => {
  const body = req.body;
  const schools = readData(schoolsFile);
  if (!body.id) {
    body.id = `SCH-${String(schools.length + 1).padStart(2, '0')}`;
  }
  schools.push(body);
  writeData(schoolsFile, schools);
  res.status(201).json({ success: true, school: body });
};

// --- Inspections ---
exports.getInspections = (req, res) => {
  const inspections = readData(inspectionsFile);
  res.status(200).json(inspections);
};

exports.addInspection = (req, res) => {
  const body = req.body;
  const inspections = readData(inspectionsFile);
  if (!body.id) {
    body.id = `INSP-${inspections.length + 101}`;
  }
  if (!body.date) {
    body.date = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  }
  inspections.unshift(body);
  writeData(inspectionsFile, inspections);

  // Update school's last inspection
  if (body.schoolId) {
    const schools = readData(schoolsFile);
    const sch = schools.find((s) => s.id === body.schoolId);
    if (sch) {
      sch.lastInspection = body.date;
      sch.inspectionRating = Number(body.overallRating) || sch.inspectionRating;
      writeData(schoolsFile, schools);
    }
  }

  res.status(201).json({ success: true, inspection: body });
};

// --- Trainings ---
exports.getTrainings = (req, res) => {
  const trainings = readData(trainingsFile);
  res.status(200).json(trainings);
};

exports.addTraining = (req, res) => {
  const body = req.body;
  const trainings = readData(trainingsFile);
  if (!body.id) {
    body.id = `TRG-${trainings.length + 201}`;
  }
  trainings.unshift(body);
  writeData(trainingsFile, trainings);
  res.status(201).json({ success: true, training: body });
};

exports.updateTraining = (req, res) => {
  const { id } = req.params;
  const body = req.body;
  const trainings = readData(trainingsFile);
  const idx = trainings.findIndex((t) => t.id === id);

  if (idx === -1) {
    return res.status(404).json({ error: 'Training not found' });
  }

  for (const [k, v] of Object.entries(body)) {
    trainings[idx][k] = v;
  }
  writeData(trainingsFile, trainings);
  res.status(200).json({ success: true, training: trainings[idx] });
};

// --- Directives ---
exports.getDirectives = (req, res) => {
  const directives = readData(directivesFile);
  res.status(200).json(directives);
};

exports.addDirective = (req, res) => {
  const body = req.body;
  const directives = readData(directivesFile);
  if (!body.id) {
    body.id = `DIR-${directives.length + 301}`;
  }
  if (!body.issuedDate) {
    body.issuedDate = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  }
  directives.unshift(body);
  writeData(directivesFile, directives);
  res.status(201).json({ success: true, directive: body });
};

exports.updateDirective = (req, res) => {
  const { id } = req.params;
  const body = req.body;
  const directives = readData(directivesFile);
  const idx = directives.findIndex((d) => d.id === id);

  if (idx === -1) {
    return res.status(404).json({ error: 'Directive not found' });
  }

  for (const [k, v] of Object.entries(body)) {
    directives[idx][k] = v;
  }
  writeData(directivesFile, directives);
  res.status(200).json({ success: true, directive: directives[idx] });
};
