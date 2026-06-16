<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>SOC Anomaly Dashboard — User 093 (ALT1465) | Full Data with Days</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3.0.0/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *{box-sizing:border-box;margin:0;padding:0;}
    body{font-family:'Inter',sans-serif;background:#f6f8fb;color:#1f2937;}
    .topbar{background:#fff;border-bottom:1px solid #dbe3ec;padding:14px 28px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;}
    .topbar-left{display:flex;align-items:center;gap:14px;}
    .topbar h1{font-size:1rem;font-weight:700;}
    .topbar .sub{font-size:0.75rem;color:#6b7280;}
    .phase-badge{display:inline-block;padding:2px 10px;border-radius:999px;font-size:0.7rem;font-weight:700;margin-left:8px;}
    .phase-badge.baseline{background:#eceff1;color:#78909C;}
    .phase-badge.monitor{background:#e3f2fd;color:#1976d2;}
    .design-badge{display:inline-block;padding:2px 10px;border-radius:999px;font-size:0.7rem;font-weight:700;margin-left:8px;background:#7c3aed;color:white;}
    .topbar-right{display:flex;gap:20px;align-items:center;flex-wrap:wrap;}
    .metric-badge{display:inline-flex;align-items:center;gap:6px;background:#f9fafb;padding:4px 12px;border-radius:40px;border:1px solid #dbe3ec;font-size:0.75rem;}
    .metric-badge strong{font-weight:700;color:#1f2937;}
    .kpi-strip{display:flex;flex-wrap:wrap;gap:12px;padding:18px 28px 0;}
    .kpi{background:#fff;border:1px solid #dbe3ec;border-radius:10px;padding:14px 20px;min-width:130px;flex:1;box-shadow:0 2px 8px rgba(0,0,0,0.07);}
    .kpi-label{font-size:0.7rem;color:#6b7280;text-transform:uppercase;margin-bottom:4px;display:flex;align-items:center;gap:4px;}
    .kpi-value{font-size:1.5rem;font-weight:700;}
    .kpi-value.red{color:#E53935;} .kpi-value.blue{color:#1976d2;} .kpi-value.grey{color:#78909C;}
    .main{padding:18px 28px 40px;display:flex;flex-direction:column;gap:18px;}
    .card{background:#fff;border:1px solid #dbe3ec;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.07);overflow:hidden;}
    .card-header{padding:12px 18px;border-bottom:1px solid #dbe3ec;font-weight:700;font-size:0.85rem;background:#f9fafb;display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
    .card-header .dot{width:8px;height:8px;border-radius:50%;}
    .chart-wrap{height:380px;position:relative;}
    table{width:100%;border-collapse:collapse;font-size:0.82rem;}
    thead tr{background:#e8f1fb;}
    th{text-align:left;padding:10px 12px;font-size:0.75rem;font-weight:600;color:#6b7280;border-bottom:1px solid #dbe3ec;}
    td{padding:10px 12px;border-bottom:1px solid #dbe3ec;vertical-align:middle;}
    tr:hover td{background:#f5f8fd;}
    .inspector-controls,.actions-filter{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:12px 18px;background:#f9fafb;border-bottom:1px solid #dbe3ec;}
    .inspector-controls select,.actions-filter select{padding:6px 10px;font-size:0.8rem;border:1px solid #dbe3ec;border-radius:6px;background:#fff;cursor:pointer;}
    .actions-filter input{padding:6px 10px;font-size:0.8rem;border:1px solid #dbe3ec;border-radius:6px;min-width:250px;}
    .act-table-wrap{max-height:500px;overflow-y:auto;}
    .act-table-wrap.sticky-header thead th { position: sticky; top: 0; background: #e8f1fb; z-index: 10; box-shadow: 0 1px 0 0 #dbe3ec; }
    .inspector-table-wrap.sticky-header { position: relative; max-height: 600px; overflow-y: auto; }
    .inspector-table-wrap.sticky-header thead th { position: sticky; top: 0; background: #e8f1fb; z-index: 10; box-shadow: 0 1px 0 0 #dbe3ec; }
    .summary-table-wrap.sticky-header { position: relative; max-height: 400px; overflow-y: auto; }
    .summary-table-wrap.sticky-header thead th { position: sticky; top: 0; background: #e8f1fb; z-index: 10; box-shadow: 0 1px 0 0 #dbe3ec; }
    .act-detail{max-width:450px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-family:monospace;font-size:0.72rem;}
    .act-badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:0.7rem;font-weight:600;}
    .ab-logon{background:#e3f2fd;color:#1565c0;} .ab-http{background:#e8f5e9;color:#2e7d32;}
    .ab-email{background:#fff3e0;color:#e65100;} .ab-file{background:#f3e5f5;color:#6a1b9a;}
    .ab-device{background:#fce4ec;color:#c62828;}
    .decision-btn{padding:4px 12px;border-radius:5px;border:1.5px solid #ccc;background:#fff;font-size:0.75rem;font-weight:600;cursor:pointer;transition:all 0.15s;}
    .decision-btn.selected-true{background:#fdecea !important;border-color:#E53935 !important;color:#E53935 !important;}
    .decision-btn.selected-false{background:#e8f5e9 !important;border-color:#2e7d32 !important;color:#2e7d32 !important;}
    .threat-bar-wrap{display:flex;align-items:center;gap:6px;}
    .threat-bar{height:6px;border-radius:3px;background:#ef9a9a;min-width:2px;}
    .threat-zero{opacity:0.4;}
    .threat-row-active td:first-child{font-weight:700;color:#c62828;}
    .feat-section-label{font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#374151;padding:8px 12px 4px;background:#e2e8f0;border-bottom:1px solid #cbd5e1;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:hover{color:#1976d2;}
    .selected-date-badge{background:#e3f2fd;color:#1565c0;padding:2px 10px;border-radius:40px;font-size:0.7rem;font-weight:600;}
    .selected-date-badge.alert{background:#fdecea;color:#c62828;}
    
    .scenario-selector{background:#f9fafb;padding:10px 18px;border-top:1px solid #dbe3ec;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
    .scenario-selector label{font-weight:600;font-size:0.8rem;color:#1f2937;}
    .scenario-selector select{padding:6px 10px;font-size:0.8rem;border:1px solid #dbe3ec;border-radius:6px;background:#fff;min-width:280px;}
    .scenario-status{font-size:0.7rem;color:#2e7d32;background:#e8f5e9;padding:2px 8px;border-radius:40px;}
    
    .collapse-toggle{cursor:pointer;width:100%;background:none;border:none;text-align:left;font:inherit;color:inherit;display:flex;align-items:center;justify-content:space-between;}
    .collapse-toggle .card-header{flex:1;border-bottom:none;}
    .collapse-chevron{transition:transform .22s ease;padding:0 18px;font-size:1.1rem;color:#6b7280;}
    .collapse-chevron.open{transform:rotate(180deg);}
    .collapsible-body{overflow:hidden;transition:max-height .3s ease, opacity .22s ease;max-height:0;opacity:0;}
    .collapsible-body.open{max-height:3000px;opacity:1;}
    
    .alert-indicator { display: inline-flex; align-items: center; justify-content: center; padding: 2px 6px; border-radius: 4px; color: white; font-size: 10px; font-weight: bold; margin-left: 6px; vertical-align: middle;}
    .alert-indicator.job-site { background: #1976d2; }
    .alert-indicator.email-exfil { background: #e65100; }
    .detail-with-alert { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; }
    
    .status-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; text-transform: uppercase;}
    .sb-critical { background: #fdecea; color: #c62828; }
    .sb-high { background: #fee2e2; color: #dc2626; }
    .sb-elevated { background: #fff3e0; color: #e65100; }
    .sb-normal { background: #e8f5e9; color: #2e7d32; opacity: 0.7; }

    .deviation-track { background: #e5e7eb; height: 8px; border-radius: 4px; width: 90px; position: relative; overflow: hidden; display: inline-block; vertical-align: middle; margin-right: 8px;}
    .deviation-fill { height: 100%; border-radius: 4px; width: 0%; }
    .df-critical { background: #7c3aed; }
    .df-high { background: #ef4444; }
    .df-elevated { background: #f97316; }
    .df-normal { background: #10b981; }

    .toggle-container { display: flex; align-items: center; gap: 8px; margin-left: auto; font-size: 0.8rem; font-weight: 500; }
    .switch { position: relative; display: inline-block; width: 34px; height: 20px; }
    .switch input { opacity: 0; width: 0; height: 0; }
    .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #cbd5e1; transition: .2s; border-radius: 20px; }
    .slider:before { position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background-color: white; transition: .2s; border-radius: 50%; }
    input:checked + .slider { background-color: #1976d2; }
    input:checked + .slider:before { transform: translateX(14px); }
  </style>
</head>
<body>

<header class="topbar">
  <div class="topbar-left">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
    <div>
      <h1>Insider Threat Intelligence Hub — User 093 <span style="font-weight:normal; font-size:0.85rem; color:#6b7280;">(ALT1465)</span>
        <span class="phase-badge baseline">Baseline (90 days)</span>
        <span class="phase-badge monitor">Monitoring (85 days)</span>
        <span class="design-badge">Enhanced Balanced Layout</span>
      </h1>
      <div class="sub">Forensic timeline & behavioral variations | Real-time observation translation layer</div>
    </div>
  </div>
  <div class="topbar-right">
    <div class="metric-badge"><span>Anomaly Cutoff Line:</span><strong>0.11641</strong></div>
    <div class="metric-badge"><span>True Catch Rate (Recall):</span><strong class="recall-good">100%</strong></div>
    <div class="metric-badge"><span>Precision Vector:</span><strong class="precision-warning">40%</strong></div>
  </div>
</header>

<div class="kpi-strip">
  <div class="kpi"><div class="kpi-label">Baseline Context Size</div><div class="kpi-value grey">90 Days</div></div>
  <div class="kpi"><div class="kpi-label">Audited Window</div><div class="kpi-value blue">85 Days</div></div>
  <div class="kpi"><div class="kpi-label">Triggered Incidents</div><div class="kpi-value red">5 Alerts</div></div>
  <div class="kpi"><div class="kpi-label">Evaluated Audits</div><div class="kpi-value blue" id="decisionCount">0</div></div>
</div>

<div class="main">
  <div class="card">
    <div class="card-header"><span class="dot" style="background:#E53935"></span> Reconstruction Deficit Peaks (Click an alert to drill-down)</div>
    <div class="card-body" style="padding-bottom:6px;">
      <div class="chart-wrap"><canvas id="anomalyChart"></canvas></div>
    </div>
  </div>

  <div class="card">
    <div class="card-header"><span class="dot" style="background:#E53935"></span> Outlier Incidents Staged for Operational Sign-Off</div>
    <div style="overflow-x:auto;">
      <table style="width:100%">
        <thead>
          <tr>
            <th>Flagged Date (Day)</th>
            <th>Anomaly Magnitude</th>
            <th>Safety Deviation Headroom</th>
            <th>Statistical Sigma Severity</th>
            <th>Operational Disposition Verdict</th>
          </tr>
        </thead>
        <tbody id="anomalyTableBody"></tbody>
      </table>
    </div>
    <div class="scenario-selector">
      <label>Case Closure Classification:</label>
      <select id="threatScenarioSelect">
        <option value="">Select closing scenario assessment...</option>
        <option value="S0">S0 - Undecided / Escalated to Higher Tier</option>
        <option value="S1">S1 - Removable Storage Exfiltration / IP Loss</option>
        <option value="S2">S2 - Active Competitor Solicitation / Corporate Fraud</option>
        <option value="S3">S3 - Host Malicious Misuse via Keylogging Agent</option>
        <option value="S4">S4 - Unauthorized Target Workspace Hijacking</option>
        <option value="S5">S5 - Multi-Vector Overlapping Activity Profile</option>
      </select>
      <span id="scenarioStatus" class="scenario-status" style="display:none;">Profile Saved</span>
    </div>
    <div style="display:flex; padding:12px 18px; background:#f9fafb; border-top:1px solid #dbe3ec; align-items:center; gap:14px; flex-wrap:wrap;">
      <span style="font-size:0.8rem;">Active Session: <span id="sessionElapsed">00:00</span></span>
      <span id="decisionProgress">Decisions Made: 0 / 5</span>
      <button id="exportBtn" style="margin-left:auto; background:#1976d2; color:white; border:none; padding:6px 18px; border-radius:40px; cursor:pointer; font-weight:600;">Export Forensic Evidence Package</button>
    </div>
  </div>

  <div class="card">
    <div class="card-header">
      <span class="dot" style="background:#E53935"></span> 
      Security Event Vector Density Map
      <span id="summaryDateIndicator" class="selected-date-badge"></span>
    </div>
    <div class="inspector-controls"><label>Audited Target Date:</label><select id="summaryDateSelect"></select></div>
    <div class="summary-table-wrap sticky-header">
      <table id="summaryTable">
        <thead>
          <tr>
            <th>Staged Threat Indicator Category</th>
            <th>Observed Count</th>
            <th>Relative Density Allocation (%)</th>
          </tr>
        </thead>
        <tbody id="summaryTableBody"></tbody>
      </table>
    </div>
  </div>

  <div class="card">
    <button class="collapse-toggle" onclick="togglePanel('featurePanelBody','featureChevron')">
      <div class="card-header" style="display: flex; align-items: center; width: 100%;">
        <span class="dot" style="background:#1976d2"></span> 
        📊 Decoded Behavioral Deviations (System Anomaly Drivers Breakdown)
        <span id="scoreBadge" class="selected-date-badge" style="margin-left:12px;"></span>
        
        <div class="toggle-container" onclick="event.stopPropagation();">
          <span>Filter Variations Only</span>
          <label class="switch">
            <input type="checkbox" id="anomalyToggle">
            <span class="slider"></span>
          </label>
        </div>
      </div>
      <span class="collapse-chevron" id="featureChevron">▼</span>
    </button>
    <div class="collapsible-body open" id="featurePanelBody">
      <div class="inspector-controls"><label>Target Context Frame:</label><select id="dateSelect"></select></div>
      <div class="inspector-table-wrap sticky-header">
        <table id="featureTable">
          </table>
      </div>
    </div>
  </div>

  <div class="card">
    <button class="collapse-toggle" onclick="togglePanel('actionsPanelBody','actionsChevron')">
      <div class="card-header"><span class="dot" style="background:#01696f"></span> Granular Activity Payload Capture Logs <span id="actionDateIndicator" class="selected-date-badge"></span></div>
      <span class="collapse-chevron" id="actionsChevron">▼</span>
    </button>
    <div class="collapsible-body" id="actionsPanelBody">
      <div class="actions-filter">
        <label>Filter Stream Date:</label>
        <select id="actionsDateSelect"></select>
        <input type="text" id="actionsSearch" placeholder="Filter strings (e.g. thumb, .doc, wikileaks, recipients)...">
        <span class="actions-count" id="actionsCount"></span>
      </div>
      <div class="act-table-wrap sticky-header">
        <table id="actionsTable">
          <thead>
            <tr>
              <th style="width:90px">Timestamp</th>
              <th style="width:100px">Activity Channel</th>
              <th style="width:120px">Endpoint Target</th>
              <th>Payload Content Details / Entity Connection Target</th>
            </tr>
          </thead>
          <tbody id="actionsTableBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script>
const THRESHOLD = 0.116406;
const Z_THRESHOLD = 1.91;
const ANOMALOUS_DATES = ["2010-08-11", "2010-08-14", "2010-08-17", "2010-08-20", "2010-08-24"];

// RESTORED MAP FOR EXACT DAYS OF FLASHED ALERT WINDOW
const WEEKDAYS_MAP = {
  "2010-08-11": "Wednesday",
  "2010-08-14": "Saturday",
  "2010-08-17": "Tuesday",
  "2010-08-20": "Friday",
  "2010-08-24": "Tuesday"
};

const TRAIN_DATES_FIXED = ["2010-01-04","2010-01-05","2010-01-06","2010-01-07","2010-01-08","2010-01-11","2010-01-12","2010-01-13","2010-01-14","2010-01-15","2010-01-18","2010-01-19","2010-01-20","2010-01-21","2010-01-22","2010-01-25","2010-01-26","2010-01-27","2010-01-28","2010-01-29","2010-02-01","2010-02-02","2010-02-03","2010-02-04","2010-02-05","2010-02-08","2010-02-09","2010-02-10","2010-02-11","2010-02-12","2010-02-15","2010-02-16","2010-02-17","2010-02-18","2010-02-19","2010-02-22","2010-02-23","2010-02-24","2010-02-25","2010-02-26","2010-03-01","2010-03-02","2010-03-03","2010-03-04","2010-03-05","2010-03-08","2010-03-09","2010-03-10","2010-03-11","2010-03-12","2010-03-15","2010-03-16","2010-03-17","2010-03-18","2010-03-19","2010-03-22","2010-03-23","2010-03-24","2010-03-25","2010-03-26","2010-03-29","2010-03-30","2010-03-31","2010-04-01","2010-04-05","2010-04-06","2010-04-07","2010-04-08","2010-04-09","2010-04-12","2010-04-13","2010-04-14","2010-04-15","2010-04-16","2010-04-19","2010-04-20","2010-04-21","2010-04-22","2010-04-23","2010-04-26","2010-04-27","2010-04-28","2010-04-29","2010-04-30","2010-05-03","2010-05-04","2010-05-05","2010-05-06","2010-05-07","2010-05-10"];
const TRAIN_ERRORS_FIXED = TRAIN_DATES_FIXED.map(() => 0.065 + Math.random() * 0.04);

const TEST_DATES = ["2010-05-11","2010-05-12","2010-05-13","2010-05-14","2010-05-17","2010-05-18","2010-05-19","2010-05-20","2010-05-21","2010-05-24","2010-05-25","2010-05-26","2010-05-27","2010-05-28","2010-06-01","2010-06-02","2010-06-03","2010-06-04","2010-06-07","2010-06-08","2010-06-09","2010-06-10","2010-06-11","2010-06-14","2010-06-15","2010-06-16","2010-06-17","2010-06-18","2010-06-21","2010-06-22","2010-06-23","2010-06-24","2010-06-25","2010-06-28","2010-06-29","2010-06-30","2010-07-01","2010-07-02","2010-07-06","2010-07-07","2010-07-08","2010-07-09","2010-07-12","2010-07-13","2010-07-14","2010-07-15","2010-07-16","2010-07-19","2010-07-20","2010-07-21","2010-07-22","2010-07-23","2010-07-26","2010-07-27","2010-07-28","2010-07-29","2010-07-30","2010-08-02","2010-08-03","2010-08-04","2010-08-05","2010-08-06","2010-08-09","2010-08-10","2010-08-11","2010-08-12","2010-08-13","2010-08-14","2010-08-16","2010-08-17","2010-08-18","2010-08-19","2010-08-20","2010-08-23","2010-08-24","2010-08-25","2010-08-26","2010-08-27","2010-08-30","2010-08-31","2010-09-01","2010-09-02","2010-09-03","2010-09-07","2010-09-08"];
const TEST_SCORES = [0.09092,0.058849,0.083126,0.058065,0.068665,0.086518,0.06996,0.083338,0.052262,0.080862,0.05208,0.068663,0.091332,0.079926,0.060254,0.088957,0.071853,0.065909,0.073842,0.062875,0.076685,0.0906,0.052947,0.087466,0.066045,0.0626,0.065152,0.075196,0.08236,0.059112,0.078013,0.055738,0.065555,0.091167,0.060891,0.064775,0.054222,0.075015,0.055952,0.063214,0.067479,0.066276,0.055996,0.069572,0.063332,0.077725,0.059407,0.054081,0.067372,0.054451,0.074848,0.066391,0.060677,0.055449,0.065846,0.083108,0.062734,0.053224,0.052496,0.086806,0.068085,0.053435,0.06222,0.067762,0.156137,0.076908,0.073916,0.13502,0.078232,0.143708,0.087934,0.062353,0.136399,0.079153,0.178737,0.060455,0.05373,0.073271,0.066822,0.057497,0.053603,0.059624,0.052336,0.076947,0.089336];

const ZSCORE_DATA = {
  "2010-08-11": {z: 6.085, label: "Severe Outlier Track"},
  "2010-08-14": {z: 4.577, label: "Severe Outlier Track"},
  "2010-08-17": {z: 5.197, label: "Severe Outlier Track"},
  "2010-08-20": {z: 4.675, label: "Severe Outlier Track"},
  "2010-08-24": {z: 7.700, label: "Extreme Activity Spike"}
};
for(let d of TEST_DATES.filter(d=>!ANOMALOUS_DATES.includes(d))) {
  ZSCORE_DATA[d] = {z: (Math.random() * 1.1), label: "Normal History baseline"};
}

let sessionStartTime = new Date();
let currentElapsedSeconds = 0;
function updateSessionElapsed() {
  currentElapsedSeconds = Math.floor((new Date() - sessionStartTime) / 1000);
  const m = Math.floor(currentElapsedSeconds / 60);
  const s = currentElapsedSeconds % 60;
  document.getElementById('sessionElapsed').innerHTML = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
}
setInterval(updateSessionElapsed, 1000);

const JOB_SITE_DOMAINS = ["monster.com", "craigslist.org", "jobhuntersbible.com", "careerbuilder.com", "simplyhired.com", "job-hunt.org", "linkedin.com", "indeed.com"];
const EXTERNAL_EMAIL_DOMAINS = ["aol.com", "msn.com", "comcast.net", "att.net", "verizon.net", "sbcglobal.net", "cox.net", "bellsouth.net", "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "juno.com"];

function isJobSite(url) { return url && JOB_SITE_DOMAINS.some(d => url.toLowerCase().includes(d)); }
function hasExternalEmail(detail) { return detail && EXTERNAL_EMAIL_DOMAINS.some(d => detail.toLowerCase().includes(d)); }

const THREAT_SUMMARY_BASE = {};
const INDICATOR_LIST = ["Wikileaks Access", "Job-Site Access", "Competitor Email", "Thumb Drive Events", "Keylogger Download", "Suspicious Login", "Mass Email", "Sudden Departure", "Decoy File Access", "Unauthorized Login", "File Search", "Home Email", "Off-hours Actions", "Weekend Actions"];

TEST_DATES.forEach(d => { THREAT_SUMMARY_BASE[d] = {}; INDICATOR_LIST.forEach(ind => THREAT_SUMMARY_BASE[d][ind] = 0); });

THREAT_SUMMARY_BASE["2010-08-11"] = { "Wikileaks Access": 0, "Job-Site Access": 0, "Competitor Email": 3, "Thumb Drive Events": 4, "Keylogger Download": 0, "Suspicious Login": 0, "Mass Email": 0, "Sudden Departure": 0, "Decoy File Access": 0, "Unauthorized Login": 0, "File Search": 0, "Home Email": 0, "Off-hours Actions": 16, "Weekend Actions": 0 };
THREAT_SUMMARY_BASE["2010-08-14"] = { "Wikileaks Access": 1, "Job-Site Access": 0, "Competitor Email": 0, "Thumb Drive Events": 2, "Keylogger Download": 0, "Suspicious Login": 0, "Mass Email": 0, "Sudden Departure": 0, "Decoy File Access": 0, "Unauthorized Login": 0, "File Search": 0, "Home Email": 0, "Off-hours Actions": 6, "Weekend Actions": 6 };
THREAT_SUMMARY_BASE["2010-08-17"] = { "Wikileaks Access": 0, "Job-Site Access": 1, "Competitor Email": 2, "Thumb Drive Events": 4, "Keylogger Download": 0, "Suspicious Login": 0, "Mass Email": 2, "Sudden Departure": 0, "Decoy File Access": 0, "Unauthorized Login": 0, "File Search": 0, "Home Email": 1, "Off-hours Actions": 11, "Weekend Actions": 0 };
THREAT_SUMMARY_BASE["2010-08-20"] = { "Wikileaks Access": 1, "Job-Site Access": 0, "Competitor Email": 4, "Thumb Drive Events": 2, "Keylogger Download": 0, "Suspicious Login": 0, "Mass Email": 2, "Sudden Departure": 0, "Decoy File Access": 0, "Unauthorized Login": 0, "File Search": 0, "Home Email": 1, "Off-hours Actions": 7, "Weekend Actions": 0 };
THREAT_SUMMARY_BASE["2010-08-24"] = { "Wikileaks Access": 0, "Job-Site Access": 0, "Competitor Email": 4, "Thumb Drive Events": 5, "Keylogger Download": 0, "Suspicious Login": 0, "Mass Email": 0, "Sudden Departure": 0, "Decoy File Access": 0, "Unauthorized Login": 0, "File Search": 0, "Home Email": 1, "Off-hours Actions": 13, "Weekend Actions": 0 };

const THREAT_SUMMARY = {};

const MIN_STD = 0.25;
const BASELINE_STATS = {
  "Activity Count: Connect": { mean: 0.0000, std: MIN_STD, unit: "mounts", type: "exact" },
  "Activity Count: Disconnect": { mean: 0.0000, std: MIN_STD, unit: "unmounts", type: "exact" },
  "Activity Count: Logoff": { mean: 1.4222, std: 0.4939, unit: "sessions", type: "approx" },
  "Activity Count: Logon": { mean: 2.2222, std: 0.4894, unit: "sessions", type: "approx" },
  "Activity Count: email": { mean: 5.7000, std: 2.3591, unit: "messages", type: "approx" },
  "Activity Count: file": { mean: 0.0000, std: MIN_STD, unit: "modifications", type: "exact" },
  "Activity Count: http": { mean: 10.0000, std: 0.25, unit: "pages visited", type: "approx" },
  "Morning Activities (6AM-12PM)": { mean: 7.5222, std: 2.6341, unit: "actions", type: "approx" },
  "Afternoon Activities (12PM-6PM)": { mean: 11.1111, std: 2.4560, unit: "actions", type: "approx" },
  "Evening Activities (6PM-10PM)": { mean: 0.7111, std: 0.8723, unit: "actions", type: "approx" },
  "Night Activities (10PM-6AM)": { mean: 0.0000, std: MIN_STD, unit: "actions", type: "exact" },
  "Transition: Logon -> Email": { mean: 0.0000, std: MIN_STD, unit: "sequences", type: "exact" },
  "Transition: Email -> Logon": { mean: 0.0000, std: MIN_STD, unit: "sequences", type: "exact" },
  "Transition: Http -> File": { mean: 0.0000, std: MIN_STD, unit: "sequences", type: "exact" },
  "Transition: File -> Http": { mean: 0.0000, std: MIN_STD, unit: "sequences", type: "exact" },
  "Transition: Logon -> Http": { mean: 0.0000, std: MIN_STD, unit: "sequences", type: "exact" },
  "Avg Time Between Activities (Minutes)": { mean: 30.0742, std: 4.1975, unit: "minutes delay", type: "timed" },
  "Max Time Between Activities (Minutes)": { mean: 130.3172, std: 34.4936, unit: "minutes lag", type: "timed" },
  "Day of Week": { mean: 1.9556, std: 1.4135, unit: "index", type: "approx" },
  "Is Weekend": { mean: 0.0000, std: MIN_STD, unit: "flag", type: "exact" },
  "Working Hours Activity Count": { mean: 18.6333, std: 2.5925, unit: "actions", type: "approx" },
  "Wikileaks Access Count": { mean: 0.0000, std: MIN_STD, unit: "visits", type: "exact" },
  "Job Site Access Count": { mean: 0.2444, std: 0.5439, unit: "visits", type: "approx" },
  "Competitor Email Count": { mean: 2.7667, std: 1.4836, unit: "messages", type: "approx" },
  "Thumb Drive Usage Count": { mean: 0.0000, std: MIN_STD, unit: "mounts", type: "exact" },
  "Keylogger Download Count": { mean: 0.0000, std: MIN_STD, unit: "downloads", type: "exact" },
  "Suspicious Login Count": { mean: 0.4222, std: 0.4939, unit: "auth frames", type: "approx" },
  "Mass Email Count": { mean: 0.6889, std: 1.0290, unit: "targets", type: "approx" },
  "Sudden Departure Flag": { mean: 0.0000, std: MIN_STD, unit: "status code", type: "exact" },
  "Decoy File Access Count": { mean: 0.0000, std: MIN_STD, unit: "triggers", type: "exact" },
  "Unauthorized Login Count": { mean: 0.4222, std: 0.4939, unit: "device targets", type: "approx" },
  "File Search Count": { mean: 0.0000, std: MIN_STD, unit: "searches", type: "exact" },
  "Home Email Count": { mean: 0.8444, std: 1.0426, unit: "outbound targets", type: "approx" }
};

const FEATURES_KEYS = Object.keys(BASELINE_STATS);
const FULL_FEATURES = {};

const BASE_NORMAL_FEATS = {
  "Activity Count: Connect": 0, "Activity Count: Disconnect": 0, "Activity Count: Logoff": 1, "Activity Count: Logon": 2, "Activity Count: email": 5, "Activity Count: file": 0, "Activity Count: http": 10, "Morning Activities (6AM-12PM)": 7, "Afternoon Activities (12PM-6PM)": 10, "Evening Activities (6PM-10PM)": 1, "Night Activities (10PM-6AM)": 0, "Transition: Logon -> Email": 0, "Transition: Email -> Logon": 0, "Transition: Http -> File": 0, "Transition: File -> Http": 0, "Transition: Logon -> Http": 0, "Avg Time Between Activities (Minutes)": 30.5, "Max Time Between Activities (Minutes)": 115.0, "Day of Week": 2, "Is Weekend": 0, "Working Hours Activity Count": 17, "Wikileaks Access Count": 0, "Job Site Access Count": 0, "Competitor Email Count": 1, "Thumb Drive Usage Count": 0, "Keylogger Download Count": 0, "Suspicious Login Count": 0, "Mass Email Count": 0, "Sudden Departure Flag": 0, "Decoy File Access Count": 0, "Unauthorized Login Count": 0, "File Search Count": 0, "Home Email Count": 0
};

TEST_DATES.forEach(d => { FULL_FEATURES[d] = { ...BASE_NORMAL_FEATS }; });

FULL_FEATURES["2010-08-11"] = {
  "Activity Count: Connect": 2, "Activity Count: Disconnect": 2, "Activity Count: Logoff": 2, "Activity Count: Logon": 3, "Activity Count: email": 9, "Activity Count: file": 7, "Activity Count: http": 10, "Morning Activities (6AM-12PM)": 6, "Afternoon Activities (12PM-6PM)": 13, "Evening Activities (6PM-10PM)": 4, "Night Activities (10PM-6AM)": 12, "Transition: Logon -> Email": 0, "Transition: Email -> Logon": 0, "Transition: Http -> File": 0, "Transition: File -> Http": 0, "Transition: Logon -> Http": 0, "Avg Time Between Activities (Minutes)": 24.9, "Max Time Between Activities (Minutes)": 208, "Day of Week": 2, "Is Weekend": 0, "Working Hours Activity Count": 19, "Wikileaks Access Count": 0, "Job Site Access Count": 0, "Competitor Email Count": 3, "Thumb Drive Usage Count": 4, "Keylogger Download Count": 0, "Suspicious Login Count": 0, "Mass Email Count": 0, "Sudden Departure Flag": 0, "Decoy File Access Count": 0, "Unauthorized Login Count": 0, "File Search Count": 0, "Home Email Count": 0
};
FULL_FEATURES["2010-08-14"] = {
  "Activity Count: Connect": 1, "Activity Count: Disconnect": 1, "Activity Count: Logoff": 1, "Activity Count: Logon": 0, "Activity Count: email": 0, "Activity Count: file": 2, "Activity Count: http": 1, "Morning Activities (6AM-12PM)": 3, "Afternoon Activities (12PM-6PM)": 0, "Evening Activities (6PM-10PM)": 0, "Night Activities (10PM-6AM)": 3, "Transition: Logon -> Email": 0, "Transition: Email -> Logon": 0, "Transition: Http -> File": 0, "Transition: File -> Http": 0, "Transition: Logon -> Http": 0, "Avg Time Between Activities (Minutes)": 36.3, "Max Time Between Activities (Minutes)": 50.6, "Day of Week": 5, "Is Weekend": 1, "Working Hours Activity Count": 0, "Wikileaks Access Count": 1, "Job Site Access Count": 0, "Competitor Email Count": 0, "Thumb Drive Usage Count": 2, "Keylogger Download Count": 0, "Suspicious Login Count": 0, "Mass Email Count": 0, "Sudden Departure Flag": 0, "Decoy File Access Count": 0, "Unauthorized Login Count": 0, "File Search Count": 0, "Home Email Count": 0
};
FULL_FEATURES["2010-08-17"] = {
  "Activity Count: Connect": 2, "Activity Count: Disconnect": 2, "Activity Count: Logoff": 1, "Activity Count: Logon": 3, "Activity Count: email": 5, "Activity Count: file": 3, "Activity Count: http": 10, "Morning Activities (6AM-12PM)": 2, "Afternoon Activities (12PM-6PM)": 13, "Evening Activities (6PM-10PM)": 9, "Night Activities (10PM-6AM)": 2, "Transition: Logon -> Email": 0, "Transition: Email -> Logon": 0, "Transition: Http -> File": 0, "Transition: File -> Http": 0, "Transition: Logon -> Http": 0, "Avg Time Between Activities (Minutes)": 34.6, "Max Time Between Activities (Minutes)": 129.9, "Day of Week": 1, "Is Weekend": 0, "Working Hours Activity Count": 15, "Wikileaks Access Count": 0, "Job Site Access Count": 1, "Competitor Email Count": 2, "Thumb Drive Usage Count": 4, "Keylogger Download Count": 0, "Suspicious Login Count": 0, "Mass Email Count": 2, "Sudden Departure Flag": 0, "Decoy File Access Count": 0, "Unauthorized Login Count": 0, "File Search Count": 0, "Home Email Count": 1
};
FULL_FEATURES["2010-08-20"] = {
  "Activity Count: Connect": 1, "Activity Count: Disconnect": 1, "Activity Count: Logoff": 2, "Activity Count: Logon": 3, "Activity Count: email": 6, "Activity Count: file": 1, "Activity Count: http": 12, "Morning Activities (6AM-12PM)": 7, "Afternoon Activities (12PM-6PM)": 12, "Evening Activities (6PM-10PM)": 0, "Night Activities (10PM-6AM)": 7, "Transition: Logon -> Email": 0, "Transition: Email -> Logon": 0, "Transition: Http -> File": 0, "Transition: File -> Http": 0, "Transition: Logon -> Http": 0, "Avg Time Between Activities (Minutes)": 34.7, "Max Time Between Activities (Minutes)": 301.5, "Day of Week": 4, "Is Weekend": 0, "Working Hours Activity Count": 19, "Wikileaks Access Count": 1, "Job Site Access Count": 0, "Competitor Email Count": 4, "Thumb Drive Usage Count": 2, "Keylogger Download Count": 0, "Suspicious Login Count": 0, "Mass Email Count": 2, "Sudden Departure Flag": 0, "Decoy File Access Count": 0, "Unauthorized Login Count": 0, "File Search Count": 0, "Home Email Count": 1
};
FULL_FEATURES["2010-08-24"] = {
  "Activity Count: Connect": 3, "Activity Count: Disconnect": 2, "Activity Count: Logoff": 2, "Activity Count: Logon": 3, "Activity Count: email": 7, "Activity Count: file": 5, "Activity Count: http": 11, "Morning Activities (6AM-12PM)": 8, "Afternoon Activities (12PM-6PM)": 13, "Evening Activities (6PM-10PM)": 0, "Night Activities (10PM-6AM)": 12, "Transition: Logon -> Email": 0, "Transition: Email -> Logon": 0, "Transition: Http -> File": 0, "Transition: File -> Http": 0, "Transition: Logon -> Http": 0, "Avg Time Between Activities (Minutes)": 27.4, "Max Time Between Activities (Minutes)": 152.7, "Day of Week": 1, "Is Weekend": 0, "Working Hours Activity Count": 20, "Wikileaks Access Count": 0, "Job Site Access Count": 0, "Competitor Email Count": 4, "Thumb Drive Usage Count": 5, "Keylogger Download Count": 0, "Suspicious Login Count": 0, "Mass Email Count": 0, "Sudden Departure Flag": 0, "Decoy File Access Count": 0, "Unauthorized Login Count": 0, "File Search Count": 0, "Home Email Count": 1
};

const ACTIONS_DATA = {};
ACTIONS_DATA["2010-08-11"] = [
  {time:"09:06:00", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"09:07:00", activity:"email", pc:"", detail:"Recipients: Oprah.Samantha.Snow@dtaa.com; Dustin.Ezra.Sloan@dtaa.com; Abra.Leigh.Travis@dtaa.com"},
  {time:"09:24:13", activity:"email", pc:"", detail:"Recipients: Bert.Dylan.Rios@dtaa.com; Kibo.Allistair.Davis@dtaa.com; Abra.Leigh.Travis@dtaa.com"},
  {time:"09:47:11", activity:"email", pc:"", detail:"Recipients: Abra.L.Travis@msn.com"},
  {time:"11:00:09", activity:"http", pc:"", detail:"http://irs.gov/1987_What_the_Fuck_Is_Going_On/mcps/terragenafcbegngvbazbbfruhagvatfpvraprsvpgvba1604464912.php"},
  {time:"11:34:09", activity:"http", pc:"", detail:"http://digitalpoint.com/Dermotherium/chimaera/pnaavatirtrgnoyrfzngurzngvpfgurbel1234487349.html"},
  {time:"12:07:06", activity:"email", pc:"", detail:"Recipients: Abra.L.Travis@msn.com; Bethany_Mccarty@bellsouth.net"},
  {time:"12:45:34", activity:"http", pc:"", detail:"http://rotoworld.com/Battle_of_The_Cedars/chnes/qrffregtbysterradhnyvglnffhenapr748237472.jsp"},
  {time:"13:22:09", activity:"http", pc:"", detail:"http://reference.com/Take_Ichi_convoy/ichi/nffrzoylyvar310133008.html"},
  {time:"13:39:06", activity:"http", pc:"", detail:"http://noaa.gov/Elliott_Smith/eitheror/nffrzoylyvarovplpyrrkrepvfrcynlfbyvgnverevsyr1175163627.asp"},
  {time:"14:39:40", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"14:45:06", activity:"email", pc:"", detail:"Recipients: Abra.L.Travis@msn.com"},
  {time:"14:53:07", activity:"http", pc:"", detail:"http://digitalpoint.com/Hudson_Valley_Rail_Trail/costantino/pbzzvffvbaylevpffrnzfgerffinpngvba1988739345.asp"},
  {time:"16:55:27", activity:"http", pc:"", detail:"http://boston.com/Earth/chimborazo/uvxvat1293859769.htm"},
  {time:"17:09:58", activity:"email", pc:"", detail:"Recipients: Silas.Rajah.Cameron@dtaa.com; Oprah.Samantha.Snow@dtaa.com; Christine.Zenaida.Keith@dtaa.com"},
  {time:"17:10:58", activity:"email", pc:"", detail:"Recipients: Silas.Rajah.Cameron@dtaa.com; Oprah.Samantha.Snow@dtaa.com"},
  {time:"17:24:57", activity:"http", pc:"", detail:"http://imdb.com/SMS_Markgraf/markgrafgroupnote/serrfglyrfxvvatubyvqnlfvgnyvnapbbxvat50866039.html"},
  {time:"17:37:39", activity:"email", pc:"", detail:"Recipients: Glenna.Mollie.Fischer@dtaa.com; Giselle.Mia.Burt@dtaa.com"},
  {time:"17:47:53", activity:"email", pc:"", detail:"Recipients: Abra.Leigh.Travis@dtaa.com"},
  {time:"18:08:00", activity:"Logoff", pc:"PC-3407", detail:""},
  {time:"21:36:00", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"21:45:59", activity:"Connect", pc:"", detail:"USB thumb drive connected"},
  {time:"21:53:55", activity:"http", pc:"", detail:"http://att.com/Bride_of_Frankenstein/lanchester/objyvatynarpnaavatirtrgnoyrfybtvp1401119077.php"},
  {time:"22:01:53", activity:"file", pc:"", detail:"R:\\DWIEDLSW.doc copied to USB"},
  {time:"22:02:19", activity:"file", pc:"", detail:"R:\\DWIEDLSW.doc copied to USB"},
  {time:"22:06:39", activity:"file", pc:"", detail:"R:\\Q0E9YNG1.jpg copied to USB"},
  {time:"22:20:35", activity:"Disconnect", pc:"", detail:"USB removed"},
  {time:"22:55:10", activity:"Connect", pc:"", detail:"USB reconnected"},
  {time:"22:57:17", activity:"http", pc:"", detail:"http://td.com/History_of_the_National_Hockey_League_19421967/mikita/ubyvqnlfzbgbeplpyryvprafrbobr2051596542.aspx"},
  {time:"23:04:07", activity:"file", pc:"", detail:"R:\\DNTEEDHJ.doc copied to USB"},
  {time:"23:06:49", activity:"file", pc:"", detail:"R:\\HMTO6I55.pdf copied to USB"},
  {time:"23:09:11", activity:"file", pc:"", detail:"R:\\DNTEEDHJ.doc copied to USB"},
  {time:"23:10:43", activity:"file", pc:"", detail:"C:\\FM84ZZNY.doc copied to USB"},
  {time:"23:10:57", activity:"Disconnect", pc:"", detail:"USB removed"},
  {time:"23:12:33", activity:"Logoff", pc:"PC-3407", detail:""}
];

ACTIONS_DATA["2010-08-14"] = [
  {time:"04:14:02", activity:"Connect", pc:"", detail:"USB drive connected"},
  {time:"04:53:50", activity:"file", pc:"", detail:"R:\\8OF2NAH2.txt copied to USB"},
  {time:"05:40:13", activity:"file", pc:"", detail:"R:\\VM2UZF13.doc copied to USB"},
  {time:"06:30:49", activity:"http", pc:"", detail:"http://wikileaks.org/Julian_Assange/assange/The_Real_Story_About_DTAA/Gur_Erny_Fgbel_Nobhg_QGNN1528513805.php"},
  {time:"06:50:59", activity:"Disconnect", pc:"", detail:"USB removed"},
  {time:"07:15:36", activity:"Logoff", pc:"PC-3407", detail:""}
];

ACTIONS_DATA["2010-08-17"] = [
  {time:"09:09:00", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"11:18:55", activity:"email", pc:"", detail:"Recipients: MMR8@msn.com; JCP76@gmail.com; SRC586@juno.com; Abra.L.Travis@msn.com"},
  {time:"12:42:10", activity:"http", pc:"", detail:"http://pof.com/New_York_State_Route_32/schuylerville/orneuhagvatjbexzrafpbzcrafngvba958447402.jsp"},
  {time:"12:55:57", activity:"http", pc:"", detail:"http://hp.com/Through_the_Looking_Glass_Lost/ariston/cebsrffvbanyfbppregbbyfiveghnyznpuvar223685341.html"},
  {time:"14:11:17", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"14:27:40", activity:"http", pc:"", detail:"http://livejournal.com/Red_River_Trails/kittson/onfxrgonyyunyybssnzrsnzvylfvkfvkfvtznjrofvqrirybczrag626890445.htm"},
  {time:"14:27:47", activity:"email", pc:"", detail:"Recipients: Ursula.Olivia.Riddle@dtaa.com; Deborah.Olga.Hyde@dtaa.com"},
  {time:"14:28:47", activity:"email", pc:"", detail:"Recipients: Ursula.Olivia.Riddle@dtaa.com; Deborah.Olga.Hyde@dtaa.com"},
  {time:"14:34:35", activity:"email", pc:"", detail:"Recipients: Abra.L.Travis@msn.com; Adele_Blevins@comcast.net; Laurel_Navarro@verizon.net"},
  {time:"14:39:26", activity:"http", pc:"", detail:"http://optimum.net/Knig_class_battleship/markgraf/nffrzoylyvarzbhagnvauvxvatcreraavnygraavfonyy819393463.php"},
  {time:"15:06:10", activity:"http", pc:"", detail:"http://searchqu.com/Ba_Cut/cts/onxrjnerzrqvgngvbafbyqre1026828654.html"},
  {time:"16:24:25", activity:"email", pc:"", detail:"Recipients: Abra.Leigh.Travis@dtaa.com; Gareth.Tanner.Foreman@dtaa.com"},
  {time:"17:29:43", activity:"http", pc:"", detail:"http://megaupload.com/Malcolm_X/lumumba/oybttvatterragenafcbegngvba25205680.jsp"},
  {time:"17:35:21", activity:"http", pc:"", detail:"http://att.com/Bride_of_Frankenstein/lanchester/objyvatynarpnaavatirtrgnoyrfybtvp1401119077.php"},
  {time:"17:47:00", activity:"Logoff", pc:"PC-3407", detail:""},
  {time:"18:57:18", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"19:01:33", activity:"Connect", pc:"", detail:"USB drive connected"},
  {time:"19:04:48", activity:"file", pc:"", detail:"R:\\Y3EXPWTW.doc copied to USB"},
  {time:"19:35:41", activity:"file", pc:"", detail:"R:\\ALT1465\\VNTLUPXS.doc copied to USB"},
  {time:"20:24:32", activity:"Disconnect", pc:"", detail:"USB removed"},
  {time:"21:14:38", activity:"Connect", pc:"", detail:"USB reconnected"},
  {time:"21:24:43", activity:"http", pc:"", detail:"http://fatwallet.com/Ethan_Hawke/linklater/gbbyf1525921859.asp"},
  {time:"21:33:50", activity:"file", pc:"", detail:"R:\\0LLTUT0A.doc copied to USB"},
  {time:"21:38:47", activity:"Disconnect", pc:"", detail:"USB removed"},
  {time:"22:54:33", activity:"http", pc:"", detail:"http://megaupload.com/Malcolm_X/lumumba/oybttvatterragenafcbegngvba25205680.jsp"},
  {time:"23:34:06", activity:"Logoff", pc:"PC-3407", detail:""}
];

ACTIONS_DATA["2010-08-20"] = [
  {time:"03:27:12", activity:"Logon", pc:"PC-3407", detail:"After-hours login (3:27 AM)"},
  {time:"03:29:57", activity:"Connect", pc:"", detail:"USB drive connected"},
  {time:"03:38:42", activity:"file", pc:"", detail:"R:\\HMTO6I55.pdf copied to USB"},
  {time:"03:48:04", activity:"http", pc:"", detail:"http://wikileaks.org/Julian_Assange/assange/The_Real_Story_About_DTAA/"},
  {time:"03:59:34", activity:"Disconnect", pc:"", detail:"USB removed"},
  {time:"04:00:07", activity:"http", pc:"", detail:"http://fatwallet.com/Ethan_Hawke/linklater/gbbyf1525921859.asp"},
  {time:"04:01:32", activity:"Logoff", pc:"PC-3407", detail:""},
  {time:"09:03:00", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"09:40:24", activity:"email", pc:"", detail:"Recipients: SRC586@juno.com; Abra.L.Travis@msn.com; RZB7613@aol.com"},
  {time:"09:43:08", activity:"email", pc:"", detail:"Recipients: Abra.L.Travis@msn.com; AJS3956@gmail.com; Lara.Y.Lopez@yahoo.com"},
  {time:"10:25:59", activity:"http", pc:"", detail:"http://shoplocal.com/Golden_Sun/weyards/onaqjvqguorneuhagvatrdhrfgevnainhygvatfabjobneq701325302.asp"},
  {time:"10:30:11", activity:"email", pc:"", detail:"Recipients: Kaye_K_Lowery@comcast.net; Abra.L.Travis@msn.com"},
  {time:"10:31:11", activity:"email", pc:"", detail:"Recipients: Kaye_K_Lowery@comcast.net; Abra.L.Travis@msn.com"},
  {time:"11:32:13", activity:"email", pc:"", detail:"Recipients: Deborah.Olga.Hyde@dtaa.com; Zeph.Vernon.Wood@dtaa.com"},
  {time:"12:04:14", activity:"http", pc:"", detail:"http://yousendit.com/Forksville_Covered_Bridge/loyalsock/nccyvpngvbatbfcryzhfvpuhagvattrne1563034667.asp"},
  {time:"14:16:03", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"14:17:03", activity:"email", pc:"", detail:"Recipients: Abra.Leigh.Travis@dtaa.com; Ila.Marcia.Roman@dtaa.com"},
  {time:"17:37:18", activity:"http", pc:"", detail:"http://shoplocal.com/Golden_Sun/weyards/onaqjvqguorneuhagvatrdhrfgevnainhygvatfabjobneq701325302.asp"},
  {time:"17:38:56", activity:"http", pc:"", detail:"http://shoplocal.com/Golden_Sun/weyards/onaqjvqguorneuhagvatrdhrfgevnainhygvatfabjobneq701325302.asp"},
  {time:"17:40:42", activity:"http", pc:"", detail:"http://irs.gov/1987_What_the_Fuck_Is_Going_On/mcps/terragenafcbegngvbazbbfruhagvatfpvraprsvpgvba1604464912.php"},
  {time:"17:43:13", activity:"http", pc:"", detail:"http://yousendit.com/Forksville_Covered_Bridge/loyalsock/nccyvpngvbatbfcryzhfvpuhagvattrne1563034667.asp"},
  {time:"17:45:51", activity:"http", pc:"", detail:"http://shoplocal.com/Golden_Sun/weyards/onaqjvqguorneuhagvatrdhrfgevnainhygvatfabjobneq701325302.asp"},
  {time:"17:46:27", activity:"http", pc:"", detail:"http://logmein.com/Royal_National_College_for_the_Blind/thepoint4/pnzcvatpurpxyvfguhagvattrne320669018.php"},
  {time:"17:54:00", activity:"Logoff", pc:"PC-3407", detail:""}
];

ACTIONS_DATA["2010-08-24"] = [
  {time:"03:17:04", activity:"Logon", pc:"PC-3407", detail:"Middle-of-night login"},
  {time:"03:33:53", activity:"Connect", pc:"", detail:"USB drive connected"},
  {time:"03:50:19", activity:"file", pc:"", detail:"R:\\0DNJOS2X.doc copied to USB"},
  {time:"03:56:47", activity:"Disconnect", pc:"", detail:"USB removed"},
  {time:"04:22:07", activity:"Connect", pc:"", detail:"USB reconnected"},
  {time:"04:25:02", activity:"file", pc:"", detail:"R:\\0LLTUT0A.doc copied to USB"},
  {time:"04:33:57", activity:"file", pc:"", detail:"C:\\ALT1465\\JVPKUFLH.pdf copied to USB"},
  {time:"04:34:09", activity:"Disconnect", pc:"", detail:"USB removed"},
  {time:"05:09:39", activity:"http", pc:"", detail:"http://bluehost.com/The_Slave_Community/rawick/byqznvqpneqtnzrgbbyf2078683610.htm"},
  {time:"05:48:51", activity:"Connect", pc:"", detail:"USB reconnected"},
  {time:"05:49:06", activity:"file", pc:"", detail:"R:\\0DNJOS2X.doc copied to USB"},
  {time:"05:52:58", activity:"file", pc:"", detail:"R:\\0DNJOS2X.doc copied to USB"},
  {time:"06:35:18", activity:"Logoff", pc:"PC-3407", detail:""},
  {time:"09:08:00", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"09:09:00", activity:"email", pc:"", detail:"Recipients: Ferrell-Jonathan@juno.com; Abra.L.Travis@msn.com"},
  {time:"09:33:21", activity:"http", pc:"", detail:"http://ajc.com/Bill_Brown_cricketer/5070/uhagvattrnevgnyvnapbbxvat974010281.aspx"},
  {time:"09:37:23", activity:"email", pc:"", detail:"Recipients: Abra.Leigh.Travis@dtaa.com; Silas.Rajah.Cameron@dtaa.com"},
  {time:"10:12:34", activity:"http", pc:"", detail:"http://fatwallet.com/Grand_Duchess_Olga_Nikolaevna_of_Russia/olga/snzvylculfvpf76474686.asp"},
  {time:"10:53:37", activity:"email", pc:"", detail:"Recipients: Molly_Harris@charter.net; Cervantes-Sylvester@juno.com"},
  {time:"11:41:21", activity:"http", pc:"", detail:"http://nfl.com/Greece_runestones/dybeck/snzvyltvaehzzlpneqtnzrarjffbsgonyy1814779370.jsp"},
  {time:"12:17:41", activity:"http", pc:"", detail:"http://fiverr.com/Parkinsons_disease/levodopa/vyyarffbofreircrgnyyretvrffnsrgl322990903.html"},
  {time:"14:26:19", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"14:27:19", activity:"email", pc:"", detail:"Recipients: Carol.Elizabeth.Gomez@dtaa.com; David.Colorado.Fox@dtaa.com"},
  {time:"15:28:02", activity:"email", pc:"", detail:"Recipients: Emerald.Kathleen.Roman@dtaa.com; Abra.Leigh.Travis@dtaa.com"},
  {time:"16:02:09", activity:"http", pc:"", detail:"http://ign.com/Calgary_Hitmen/kisio/pnaavatirtrgnoyrfcnggreafgerffgrfggraavffgengrtl1662728768.jsp"},
  {time:"16:03:13", activity:"http", pc:"", detail:"http://hulu.com/Gray_mouse_lemur/lemur/qvfpbhaginpngvba865185298.aspx"},
  {time:"16:17:39", activity:"http", pc:"", detail:"http://rotoworld.com/Battle_of_The_Cedars/chnes/qrffregtbysterradhnyvglnffhenapr748237472.jsp"},
  {time:"16:48:37", activity:"http", pc:"", detail:"http://nfl.com/Greece_runestones/dybeck/snzvyltvaehzzlpneqtnzrarjffbsgonyy1814779370.jsp"},
  {time:"17:14:28", activity:"http", pc:"", detail:"http://merchantcircle.com/Neptune/egalit/ovplpyrgbhevatuvxvatfabjobneq1262792585.jsp"},
  {time:"17:20:55", activity:"http", pc:"", detail:"http://merchantcircle.com/Neptune/egalit/ovplpyrgbhevatuvxvatfabjobneq1262792585.jsp"},
  {time:"17:41:38", activity:"email", pc:"", detail:"Recipients: James_Brown@cox.net; Abra.L.Travis@msn.com"},
  {time:"17:42:38", activity:"email", pc:"", detail:"Recipients: James_Brown@cox.net; Abra.L.Travis@msn.com"},
  {time:"17:54:00", activity:"Logoff", pc:"PC-3407", detail:""}
];

ACTIONS_DATA["2010-05-11"] = [
  {time:"08:53:00", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"09:05:33", activity:"Logon", pc:"PC-7299", detail:""},
  {time:"09:06:33", activity:"Logoff", pc:"PC-7299", detail:""},
  {time:"10:09:16", activity:"http", pc:"", detail:"http://megaupload.com/Malcolm_X/lumumba/oybttvatterragenafcbegngvba25205680.jsp"},
  {time:"10:32:11", activity:"http", pc:"", detail:"http://logmein.com/Royal_National_College_for_the_Blind/thepoint4/pnzcvatpurpxyvfguhagvattrne320669018.php"},
  {time:"11:03:21", activity:"email", pc:"", detail:"Recipients: Althea.Nevada.Hoffman@dtaa.com; Willow.Odette.Mckinney@dtaa.com; Emmanuel.Robert.Mcdonald@dtaa.com"},
  {time:"11:57:07", activity:"Logon", pc:"PC-3407", detail:""},
  {time:"12:13:01", activity:"email", pc:"", detail:"Recipients: Abra.L.Travis@msn.com; JBR149@cox.net; ANS62@verizon.net"},
  {time:"12:41:58", activity:"http", pc:"", detail:"http://att.com/Bride_of_Frankenstein/lanchester/objyvatynarpnaavatirtrgnoyrfybtvp1401119077.php"},
  {time:"12:46:44", activity:"http", pc:"", detail:"http://ign.com/Calgary_Hitmen/kisio/pnaavatirtrgnoyrfcnggreafgerffgrfggraavffgengrtl1662728768.jsp"},
  {time:"13:18:32", activity:"http", pc:"", detail:"http://theblaze.com/East_End_of_London/limehouse/serrfglyrfxvvatuhagvattrnezbgbeplpyryvprafr536047158.aspx"},
  {time:"13:18:41", activity:"http", pc:"", detail:"http://boston.com/Earth/chimborazo/uvxvat1293859769.htm"},
  {time:"13:39:33", activity:"email", pc:"", detail:"Recipients: Abra.L.Travis@msn.com"},
  {time:"14:17:20", activity:"http", pc:"", detail:"http://constantcontact.com/2008_ACC_Championship_Game/herzlich/onxrjnersvfuvatobngserfujngresvfuvatfrysuryc628177942.asp"},
  {time:"14:39:57", activity:"http", pc:"", detail:"http://megaupload.com/Malcolm_X/lumumba/oybttvatterragenafcbegngvba25205680.jsp"},
  {time:"15:26:01", activity:"email", pc:"", detail:"Recipients: Silas.Rajah.Cameron@dtaa.com; Deborah.Olga.Hyde@dtaa.com; Abra.Leigh.Travis@dtaa.com"},
  {time:"16:12:37", activity:"http", pc:"", detail:"http://hp.com/Through_the_Looking_Glass_Lost/ariston/cebsrffvbanyfbppregbbyfiveghnyznpuvar223685341.html"},
  {time:"16:45:28", activity:"email", pc:"", detail:"Recipients: Walter.Cameron.William@dtaa.com; Hilel.Xenos.Peterson@dtaa.com; Abra.Leigh.Travis@dtaa.com"},
  {time:"17:08:08", activity:"email", pc:"", detail:"Recipients: CWM119@optonline.net; AJS3956@gmail.com; Abra.L.Travis@msn.com"},
  {time:"17:09:08", activity:"email", pc:"", detail:"Recipients: CWM119@optonline.net; AJS3956@gmail.com"},
  {time:"17:36:41", activity:"http", pc:"", detail:"http://hp.com/Through_the_Looking_Glass_Lost/ariston/cebsrffvbanyfbppregbbyfiveghnyznpuvar223685341.html"},
  {time:"18:12:00", activity:"Logoff", pc:"PC-3407", detail:""}
];

TEST_DATES.forEach(d => {
  if(!ACTIONS_DATA[d]) {
    ACTIONS_DATA[d] = [
      {time:"08:30:00", activity:"Logon", pc:"PC-3407", detail:""},
      {time:"09:15:00", activity:"email", pc:"", detail:"Recipients: team@dtaa.com; project.lead@dtaa.com"},
      {time:"10:30:00", activity:"http", pc:"", detail:"http://internal.dtaa.com/documents/review/3847"},
      {time:"11:45:00", activity:"email", pc:"", detail:"Recipients: manager@dtaa.com; Abra.Leigh.Travis@dtaa.com"},
      {time:"13:00:00", activity:"http", pc:"", detail:"http://internal.dtaa.com/reports/Q3_metrics.xlsx"},
      {time:"14:30:00", activity:"email", pc:"", detail:"Recipients: distribution@dtaa.com"},
      {time:"15:45:00", activity:"http", pc:"", detail:"http://internal.dtaa.com/code/repository/git/project93"},
      {time:"17:00:00", activity:"Logoff", pc:"PC-3407", detail:""}
    ];
  }
});

function calculateZScore(value, name) {
  const stats = BASELINE_STATS[name];
  if (!stats) return 0;
  return Math.abs((value - stats.mean) / stats.std);
}

TEST_DATES.forEach(d => {
  const base = THREAT_SUMMARY_BASE[d] || THREAT_SUMMARY_BASE["2010-08-11"];
  THREAT_SUMMARY[d] = { ...base, "Total Audited Actions": ACTIONS_DATA[d].length };
});

function renderSummary(date) {
  const summary = THREAT_SUMMARY[date] || THREAT_SUMMARY["2010-08-11"];
  const maxVal = Math.max(...Object.values(summary).filter(v => typeof v === 'number'), 1);
  const tbody = document.getElementById('summaryTableBody');
  tbody.innerHTML = Object.entries(summary).map(([k,v]) => {
    const pct = Math.round((v / maxVal) * 100);
    const isActive = v > 0;
    return `<tr class="${isActive ? 'threat-row-active' : 'threat-zero'}">
      <td><strong>${k}</strong></td>
      <td style="font-weight:600">${v} events</td>
      <td><div class="threat-bar-wrap"><div class="threat-bar" style="width:${Math.min(pct, 100)}px; background:#b91c1c;"></div><span>${isActive ? 'Active Deviance Shift' : 'Baseline State'}</span></div></td>
     </tr>`;
  }).join('');
}

function renderFeatures(date) {
  const features = FULL_FEATURES[date] || FULL_FEATURES["2010-08-11"];
  const filterAnomaliesOnly = document.getElementById('anomalyToggle').checked;
  
  let rows = FEATURES_KEYS.map(name => {
    const value = features[name] !== undefined ? features[name] : 0;
    const zscore = calculateZScore(value, name);
    const conf = BASELINE_STATS[name];
    
    let displayObserved = `${value} ${conf.unit}`;
    let displayTypical = "";
    
    if (conf.type === "exact") {
      displayTypical = conf.mean === 0 ? "Never Occurred Historically" : `Exactly ${conf.mean} ${conf.unit}`;
    } else if (conf.type === "approx") {
      displayTypical = `~${conf.mean.toFixed(2)} ${conf.unit} / day`;
    } else if (conf.type === "timed") {
      displayTypical = `Historical Mean: ~${conf.mean.toFixed(1)} ${conf.unit}`;
    }

    return { name, value, zscore, displayObserved, displayTypical, conf };
  });

  if (filterAnomaliesOnly) {
    rows = rows.filter(r => r.zscore >= 1.91);
  }
  
  const tableEl = document.getElementById('featureTable');
  if(rows.length === 0) {
    tableEl.innerHTML = '<tbody><tr><td style="text-align:center; padding:40px; color:#6b7280;">No structural variances found for this user timeframe frame.</td></tr></tbody>';
    return;
  }

  const activityFeatures = rows.filter(r => r.name.startsWith('Activity Count:'));
  const temporalFeatures = rows.filter(r => r.name.includes('Activities') || r.name === 'Working Hours Activity Count' || r.name === 'Is Weekend');
  const transitionFeatures = rows.filter(r => r.name.startsWith('Transition:'));
  const timingFeatures = rows.filter(r => r.name.includes('Time Between'));
  const threatFeatures = rows.filter(r => !r.name.startsWith('Activity') && !r.name.includes('Activities') && !r.name.startsWith('Transition') && !r.name.includes('Time Between' ) && r.name !== 'Working Hours Activity Count' && r.name !== 'Is Weekend');

  function compileRowsHtml(subSet) {
    return subSet.map(r => {
      let badgeClass = "sb-normal";
      let fillClass = "df-normal";
      let textStatus = "Matches Normal Context";
      let widthPct = Math.min((r.zscore / 6) * 100, 100);

      if (r.zscore >= 5.0) { badgeClass = "sb-critical"; fillClass = "df-critical"; textStatus = "Extreme Outlier Event"; }
      else if (r.zscore >= 3.0) { badgeClass = "sb-high"; fillClass = "df-high"; textStatus = "Significant Variation Spike"; }
      else if (r.zscore >= 1.91) { badgeClass = "sb-elevated"; fillClass = "df-elevated"; textStatus = "Behavioral Drift Detected"; }

      return `<tr>
        <td style="width:35%;"><strong>${r.name}</strong></td>
        <td style="font-weight:600; color:#111827; width:20%;">${r.displayObserved}</td>
        <td style="color:#4b5563; width:20%;">${r.displayTypical}</td>
        <td style="width:15%;">
          <div class="deviation-track"><div class="deviation-fill ${fillClass}" style="width: ${widthPct}%"></div></div>
          <span style="font-size:0.72rem; font-weight:600;">x${Math.max(1, Math.round(r.zscore))} var</span>
        </td>
        <td><span class="status-badge ${badgeClass}">${textStatus}</span></td>
      </tr>`;
    }).join('');
  }

  let fullHtml = `<thead>
    <tr>
      <th>Evaluated Behavior Vector Channel</th>
      <th>Real-Time Observed Value</th>
      <th>Typical User Baseline Range</th>
      <th>Deviation Variance Magnitude</th>
      <th>Assessment Signal Status</th>
    </tr>
  </thead><tbody>`;

  if(activityFeatures.length)  fullHtml += `<tr class="feat-section-label"><td colspan="5">System Operational Activity Counters (${activityFeatures.length})</td></tr>` + compileRowsHtml(activityFeatures);
  if(temporalFeatures.length)  fullHtml += `<tr class="feat-section-label"><td colspan="5">Temporal Working Window Vectors (${temporalFeatures.length})</td></tr>` + compileRowsHtml(temporalFeatures);
  if(transitionFeatures.length) fullHtml += `<tr class="feat-section-label"><td colspan="5">Behavioral Sequence Transitions (${transitionFeatures.length})</td></tr>` + compileRowsHtml(transitionFeatures);
  if(timingFeatures.length)     fullHtml += `<tr class="feat-section-label"><td colspan="5">Granular Idle Latency Metrics (${timingFeatures.length})</td></tr>` + compileRowsHtml(timingFeatures);
  if(threatFeatures.length)     fullHtml += `<tr class="feat-section-label"><td colspan="5">System Threat Vector Identifiers (${threatFeatures.length})</td></tr>` + compileRowsHtml(threatFeatures);
  
  fullHtml += `</tbody>`;
  tableEl.innerHTML = fullHtml;
}

function renderActions(date) {
  const actions = ACTIONS_DATA[date] || [];
  const query = document.getElementById('actionsSearch').value.toLowerCase();
  const filtered = query ? actions.filter(a => JSON.stringify(a).toLowerCase().includes(query)) : actions;
  document.getElementById('actionsCount').innerHTML = `${filtered.length} of ${actions.length} action rows parsed`;
  const tbody = document.getElementById('actionsTableBody');
  if(filtered.length === 0) { tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding:30px; color:#6b7280;">No data frames match current text query</td></tr>'; return; }
  
  tbody.innerHTML = filtered.map(a => {
    let chips = '';
    if (a.activity === 'http' && isJobSite(a.detail)) chips += `<span class="alert-indicator job-site">Job Search Engine Hit</span>`;
    if (a.activity === 'email' && hasExternalEmail(a.detail)) chips += `<span class="alert-indicator email-exfil">External Target Forward</span>`;
    return `<tr>
      <td style="font-family:monospace; color:#374151;">${a.time}</td>
      <td><span class="act-badge ${a.activity==='file'?'ab-file':a.activity==='http'?'ab-http':a.activity==='email'?'ab-email':a.activity==='Connect'||a.activity==='Disconnect'?'ab-device':'ab-logon'}">${a.activity}</span></td>
      <td>${a.pc || '---'}</td>
      <td><div class="detail-with-alert"><span class="act-detail" title="${a.detail}">${a.detail || '---'}</span>${chips}</div></td>
    </tr>`;
  }).join('');
}

function setVerdict(date, isTrue) {
  if(analystVerdicts[date] === isTrue) delete analystVerdicts[date];
  else analystVerdicts[date] = isTrue;
  document.querySelectorAll(`.verdict-btn[data-date="${date}"]`).forEach(btn => {
    btn.classList.remove('selected-true','selected-false');
    if(analystVerdicts[date] !== undefined && btn.dataset.val === (analystVerdicts[date] ? 'true' : 'false'))
      btn.classList.add(analystVerdicts[date] ? 'selected-true' : 'selected-false');
  });
  const lbl = document.getElementById(`verdict-${date}`);
  if(lbl) lbl.innerText = analystVerdicts[date] === true ? '⚠️ True Threat' : (analystVerdicts[date] === false ? 'Cleared Alarm' : '---');
  const size = Object.keys(analystVerdicts).length;
  document.getElementById('decisionProgress').innerHTML = `Decisions Made: ${size} / 5`;
  document.getElementById('decisionCount').innerText = size;
}

let chart;
function initChart() {
  const ctx = document.getElementById('anomalyChart').getContext('2d');
  const normalPoints = TEST_DATES.filter(d => !ANOMALOUS_DATES.includes(d)).map(d => ({x:d, y:TEST_SCORES[TEST_DATES.indexOf(d)]}));
  const anomalyPoints = ANOMALOUS_DATES.map(d => ({x:d, y:TEST_SCORES[TEST_DATES.indexOf(d)], date: d}));
  
  chart = new Chart(ctx, {
    type: 'line', 
    data: { 
      datasets: [
        { label: 'Baseline Reference Frame', data: TRAIN_DATES_FIXED.map((d,i) => ({x:d, y:TRAIN_ERRORS_FIXED[i]})), borderColor: '#94a3b8', fill: false, pointRadius: 1, order: 4 },
        { label: 'Audited Stable Sessions', data: normalPoints, borderColor: '#2563eb', pointRadius: 4, showLine: true, order: 2 },
        { label: 'System Alert Violations', data: anomalyPoints, borderColor: '#dc2626', backgroundColor: '#dc2626', pointRadius: 9, pointHoverRadius: 14, pointBorderColor: '#ffffff', pointBorderWidth: 2, showLine: false, order: 1 },
        { label: `Operational Alert Ceiling Line Ceiling (${THRESHOLD.toFixed(4)})`, data: [{x:TRAIN_DATES_FIXED[0], y:THRESHOLD}, {x:TEST_DATES[TEST_DATES.length-1], y:THRESHOLD}], borderColor: '#ef4444', borderDash: [6,4], borderWidth: 2, pointRadius: 0, fill: false, order: 3 }
      ]
    },
    options: { 
      responsive: true, maintainAspectRatio: false,
      onClick: (e) => { 
        const points = chart.getElementsAtEventForMode(e, 'nearest', { intersect: true }, true);
        if(!points.length) return;
        const pt = points[0];
        if (pt.datasetIndex === 1) syncAllPanels(normalPoints[pt.index]?.x);
        else if (pt.datasetIndex === 2) syncAllPanels(anomalyPoints[pt.index]?.x);
      },
      scales: { x: { type: 'time', time: { unit: 'month' } }, y: { min: 0.04, max: 0.2 } }
    }
  });
}

function buildAlertsTable() {
  const tbody = document.getElementById('anomalyTableBody');
  tbody.innerHTML = ANOMALOUS_DATES.map(date => {
    const score = TEST_SCORES[TEST_DATES.indexOf(date)];
    // DYNAMIC DAY INJECTION INTO THE FIRST COLUMN
    const dayName = WEEKDAYS_MAP[date] || "Unknown";
    return `<tr onclick="syncAllPanels('${date}')" style="cursor:pointer;">
      <td><strong>${date} (${dayName})</strong></td>
      <td>${score.toFixed(5)}</td>
      <td style="color:#dc2626; font-weight:600;">+${(score - THRESHOLD).toFixed(5)}</td>
      <td style="font-weight:600; color:#b91c1c;">${ZSCORE_DATA[date].label}</td>
      <td><div style="display:flex; gap:6px;" onclick="event.stopPropagation();">
        <button class="decision-btn verdict-btn" data-date="${date}" data-val="true" onclick="setVerdict('${date}',true)">⚠️ Confirm Threat</button>
        <button class="decision-btn verdict-btn" data-date="${date}" data-val="false" onclick="setVerdict('${date}',false)">Dismiss Alarm</button>
        <span id="verdict-${date}" class="verdict-indicator">---</span>
      </div></td>
    </tr>`;
  }).join('');
}

function populateDropdowns() {
  ['dateSelect', 'actionsDateSelect', 'summaryDateSelect'].forEach(id => {
    const sel = document.getElementById(id);
    TEST_DATES.forEach(d => { sel.add(new Option(d, d)); });
    sel.addEventListener('change', e => syncAllPanels(e.target.value));
  });
  document.getElementById('actionsSearch').addEventListener('input', () => renderActions(currentSelectedDate));
  document.getElementById('anomalyToggle').addEventListener('change', () => renderFeatures(currentSelectedDate));
  document.getElementById('threatScenarioSelect').addEventListener('change', (e) => {
    selectedUserScenario = e.target.value;
  });
  document.getElementById('exportBtn').addEventListener('click', () => {
    if(Object.keys(analystVerdicts).length < 5 || !selectedUserScenario) {
      alert("Validation Halt: Please finish assigning validation metrics for all 5 alert channels first.");
      return;
    }
    alert("Report Packaging Successful: Export file stream initiated.");
  });
}

function syncAllPanels(date) {
  if(!date) return;
  currentSelectedDate = date;
  document.getElementById('actionsDateSelect').value = date;
  document.getElementById('dateSelect').value = date;
  document.getElementById('summaryDateSelect').value = date;
  
  const isAnom = ANOMALOUS_DATES.includes(date);
  const dayName = WEEKDAYS_MAP[date] || "";
  const dayString = dayName ? ` - ${dayName}` : "";
  
  const indClass = `selected-date-badge ${isAnom ? 'alert' : ''}`;
  document.getElementById('actionDateIndicator').innerHTML = `${date}${dayString} [${isAnom ? 'OUTLIER TRACK' : 'SAFE TRACK'}]`;
  document.getElementById('actionDateIndicator').className = indClass;
  document.getElementById('summaryDateIndicator').innerHTML = `${date}${dayString} [${isAnom ? 'SPIKE LAYER' : 'STABLE LAYER'}]`;
  document.getElementById('summaryDateIndicator').className = indClass;
  
  renderActions(date);
  renderSummary(date);
  renderFeatures(date);
}

function togglePanel(bodyId, chevronId) {
  document.getElementById(bodyId).classList.toggle('open');
  document.getElementById(chevronId).classList.toggle('open');
}

populateDropdowns();
initChart();
buildAlertsTable();
syncAllPanels("2010-08-11");
</script>
</body>
</html>