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

// List all cases (information disclosure) - summary only. Full records,
// including the transfer_ref anomaly and the id-5 service account, only
// come back from /api/cases/:id - that's what makes the missing
// authorization check on that endpoint an actual IDOR instead of a
// second copy of what this endpoint already hands out.
app.get('/api/cases', (req, res) => {
  const summaries = Object.values(cases).map((r) => (
    r.type === 'system' ? { id: r.id, type: r.type } : { id: r.id, name: r.name, colony: r.colony }
  ));
  res.json(summaries);
});

// Health check exposes internal info - but only that a downstream
// dependency is unwell, not its address. The hostname itself is only
// meant to come from /etc/ledger/sync.conf and the service_accounts
// table, both of which require actually landing on this host first.
app.get('/api/health', (req, res) => {
  res.json({
    status: "ok",
    hostname: require('os').hostname(),
    platform: process.platform,
    arch: process.arch,
    uptime: process.uptime(),
    env: process.env.NODE_ENV || "development",
    internal_services: {
      archive_fileshare: "degraded"
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
