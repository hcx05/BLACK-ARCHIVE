// LEDGER — internal case-index API for OCPA Region 4 / RELAY node
// nosemgrep
const express = require('express');
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Case index (IDOR vulnerability). Records 1-4 are dependent/candidate
// cases; record 5 is an internal service account, not a case record.
const cases = {
  1: { id: 1, name: "Eli Okafor", colony: "Eridanus II", status: "Case Closed - Deceased (medical, age 6)",
       case_ref: "OCPA-R4-11902", transfer_ref: "SPINDLE-7-0119" },
  2: { id: 2, name: "Talia Wren", colony: "Madrigal", status: "Case Closed - Deceased (medical, age 6)",
       case_ref: "OCPA-R4-11944", transfer_ref: "SPINDLE-7-0142" },
  3: { id: 3, name: "Dominic Farrow", colony: "Skopje", status: "Case Closed - Deceased (medical, age 6)",
       case_ref: "OCPA-R4-11887", transfer_ref: "SPINDLE-7-0087" },
  4: { id: 4, name: "Priya Anand", colony: "Eridanus II", status: "Active - standard dependent case",
       case_ref: "OCPA-R4-12210", transfer_ref: null },
  5: { id: 5, type: "system", service: "ledger-cairn-sync", api_key: "sk-relay-7f2a9c1e4b8d3f6a",
       internal_notes: "Automated nightly sync between LEDGER case index and CAIRN long-term archive. Do not disable - legal hold pending." },
};

// IDOR: No authorization check - any case ID accessible
app.get('/api/cases/:id', (req, res) => {
  const record = cases[req.params.id];
  if (record) {
    res.json(record);
  } else {
    res.status(404).json({ error: "Case not found" });
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
    name: "LEDGER Case Index API",
    version: "1.0.0",
    endpoints: ["/api/cases", "/api/cases/:id", "/api/health"]
  });
});

app.listen(3000, '0.0.0.0', () => {
  console.log('LEDGER API listening on port 3000');
});
