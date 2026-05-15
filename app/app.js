const express = require('express');
const app = express();

app.use(express.json());
app.use(express.static('public'));

let logs = [];
let automationEnabled = false;

const SCENARIO = {
  name: "Filmavond",
  actions: [
    "Verlichting dimmen naar 20%",
    "TV aanzetten — Netflix",
    "Thermostaat → 21°C",
    "Voordeur vergrendelen",
  ]
};

function runScenario(trigger = "manueel") {
  const time = new Date().toLocaleTimeString('nl-BE', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });

  SCENARIO.actions.forEach(action => {
    logs.push({ time, trigger, action });
  });

  if (logs.length > 30) {
    logs = logs.slice(-30);
  }

  console.log(`[${time}] ${trigger} → ${SCENARIO.name}`);
}

// Automatisatie elke 30 seconden
setInterval(() => {
  if (automationEnabled) {
    runScenario("automatisch");
  }
}, 30000);

app.get('/scenario', (req, res) => {
  res.json(SCENARIO);
});

app.get('/logs', (req, res) => {
  res.json(logs.slice().reverse());
});

app.post('/trigger', (req, res) => {
  runScenario("manueel");
  res.json({ status: "ok" });
});

app.post('/automation/toggle', (req, res) => {
  automationEnabled = !automationEnabled;
  res.json({ enabled: automationEnabled });
});

app.get('/automation/status', (req, res) => {
  res.json({ enabled: automationEnabled });
});

app.listen(5000, () => {
  console.log('Server running on port 5000');
});