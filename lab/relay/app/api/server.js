// LEDGER — internal case-index API for OCPA Region 4 / RELAY node
// nosemgrep
const express = require('express');
const app = express();
const { cases, str } = require('./content.js');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// IDOR: No authorization check - any case ID accessible
app.get('/api/cases/:id', (req, res) => {
  const record = cases[req.params.id];
  if (record) {
    res.json(record);
  } else {
    res.status(404).json({ error: str.case_not_found });
  }
});

// List all cases (information disclosure)
app.get('/api/cases', (req, res) => {
  res.json(Object.values(cases));
});

// Health check exposes internal info
app.get('/api/health', (req, res) => {
  res.json({
    status: "ok",
    hostname: require('os').hostname(),
    platform: process.platform,
    arch: process.arch,
    uptime: process.uptime(),
    env: process.env.NODE_ENV || "development",
    internal_services: {
      archive_fileshare: "cairn.internal:445"
    }
  });
});

app.get('/', (req, res) => {
  res.json({
    name: str.api_name,
    version: "1.0.0",
    endpoints: ["/api/cases", "/api/cases/:id", "/api/health"]
  });
});

app.listen(3000, '0.0.0.0', () => {
  console.log('LEDGER API listening on port 3000');
});
