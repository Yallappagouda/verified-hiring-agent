# Verified AI Hiring Assistant

**A Hackathon-Ready AI Hiring Evaluation Platform with Trust & Verification**

A modern, explainable candidate evaluation system built with Python and Streamlit. This project demonstrates a production-grade hiring assistant that combines AI-driven candidate scoring with verifiable trust mechanisms (AgentFacts, Merkle roots, and cryptographic signatures).

**Mission:** Provide transparent, bias-free, and verifiable candidate evaluations with explainable reasoning for every hiring decision.

---

## 🤖 AI Agents in This Project

### 1. **Hiring Evaluation Agent** (`hiring_agent.py`)
- **Role:** Core evaluation engine that scores candidates
- **Responsibilities:**
  - Parse resumes (text extraction from .txt and .pdf)
  - Extract skills using keyword matching (12 core tech skills)
  - Extract experience level from resume patterns
  - Calculate weighted scores (Skills: 60%, Experience: 25%, Projects: 15%)
  - Generate hiring decisions (Shortlist/Reject based on >= 60 threshold)
  - Maintain evaluation history
- **Decision Logic:** Deterministic, rule-based scoring with explainable breakdowns

### 2. **Verification & Trust Agent** (integrated in `hiring_agent.py`)
- **Role:** Ensure integrity and transparency of all decisions
- **Responsibilities:**
  - Generate cryptographic signatures (HMAC-SHA256) for each evaluation
  - Compute Merkle roots over evaluation histories
  - Track policy compliance (bias check, data sanitization, scoring integrity)
  - Log all evaluation events with timestamps
  - Write immutable verification records to `agentfacts.json`
- **Trust Model:** Blockchain-style merkle chaining + HMAC signing

### 3. **Data Sanitization Agent** (in `utils.py`)
- **Role:** Ensure bias-free evaluation by removing personally identifiable information
- **Responsibilities:**
  - Strip name, age, gender, address before scoring
  - Normalize text and collapse whitespace
  - Preserve only job-relevant information
- **Bias Prevention:** Ensures decisions are based solely on skills, experience, and projects

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.20+ | Interactive web UI, responsive layout |
| **Backend** | Python 3.9+ | Core evaluation logic |
| **Data Processing** | Pandas 1.4+ | Dataframe operations, history management |
| **Visualization** | Plotly 5.0+ | Interactive charts, score breakdown |
| **PDF Parsing** | PyPDF2 3.0+ | Extract text from .pdf resumes |
| **Hashing** | hashlib (stdlib) | SHA256 for merkle & signatures |
| **Signing** | hmac (stdlib) | HMAC-SHA256 for verification |
| **Storage** | JSON (local) | history.json, agentfacts.json |
| **Environment** | Virtual Environment (.venv) | Dependency isolation |

---

## 📁 Project Structure

```
verified-hiring-agent/
│
├── app.py                      # Main Streamlit UI (4 tabs)
├── hiring_agent.py             # Evaluation logic & AgentFacts writer
├── utils.py                    # Parsing, sanitization, helpers
│
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── history.json                # Evaluation history (auto-created)
├── agentfacts.json             # Trust metadata (auto-created)
├── secret.key                  # HMAC signing key (auto-generated)
│
└── venv/                       # Virtual environment (local)
```

### **File Responsibilities**

| File | Size | Role | Key Functions |
|------|------|------|----------------|
| `app.py` | ~189 lines | Streamlit UI | 4 tabs: Evaluate, Compare, History, Verification |
| `hiring_agent.py` | ~170 lines | Evaluation engine | `evaluate_candidate()`, `load_history()`, `generate_report_txt()` |
| `utils.py` | ~145 lines | Helpers | Parsing, sanitization, signing, reporting |
| `history.json` | Dynamic | Persistent storage | Array of evaluation records |
| `agentfacts.json` | Dynamic | Verification log | Merkle root, signatures, policy checks |

---

## ✅ How This Project Follows Verified Agent Build Track Rules

This project is a complete implementation of a **Verified AI Agent** that meets all requirements of the Verified Agent Build Track for hackathons. It demonstrates transparent, trustworthy AI decision-making with cryptographic proof of integrity.

---

### 1. **Project Overview**

The **Verified AI Hiring Assistant** is an intelligent hiring evaluation agent that:
- Analyzes candidate resumes against job requirements
- Scores candidates based on **skills, experience, and project relevance only**
- Generates transparent, explainable hiring decisions (Shortlist or Reject)
- Produces **verifiable output** signed with HMAC-SHA256
- Maintains immutable activity logs and audit trails
- Prevents bias by automatically removing personal identifiers

**Core Mission:** Every hiring decision is transparent, auditable, and verifiable. No decision is made in a black box.

---

### 2. **Verified Agent Requirement**

This project implements a **fully verified agent** that produces signed proof of all outputs:

**What Gets Verified:**
- ✅ **Agent Metadata:** Version, capabilities, decision model
- ✅ **Output Signature:** HMAC-SHA256 signature over evaluation merkle root
- ✅ **Merkle Root:** Cryptographic hash chain of all evaluation records
- ✅ **Policy Attestation:** Proof that bias checks passed
- ✅ **Activity Logs:** Complete audit trail with timestamps

**Generated File: `agentfacts.json`**
```json
{
  "signature": "7f2a9c4e1b8d...",  // HMAC-SHA256 proof
  "merkle_root": "a3f8c9d2e1b5...",  // Hash of all history
  "policy_checks": {
    "bias_check": "pass",
    "data_sanitization": "pass",
    "scoring_integrity": "pass"
  },
  "logs": [...]  // Activity log
}
```

**Verification Guarantee:** Anyone can verify this agent's output using the signature. If the signature is valid, the output has NOT been tampered with, and the policy checks PASSED.

---

### 3. **Provable Activity Logs**

Every significant runtime action is logged for auditability:

**Logged Events:**
- `candidate_evaluated` — When a candidate is scored
- `policy_check_executed` — When bias checks run
- `score_calculated` — When final score is computed
- `decision_made` — When Shortlist/Reject decision is finalized
- `history_updated` — When evaluation is persisted

**Log Format:** Each entry contains:
```
{
  "ts": "2026-02-15T10:23:45Z",  // ISO timestamp
  "action": "candidate_evaluated",
  "details": {
    "candidate_id": "...",
    "score": 78.0,
    "decision": "Shortlist"
  }
}
```

**Integrity:** Logs are incorporated into the Merkle tree, so any tampering with logs changes the merkle root and invalidates the signature.

---

### 4. **Policy Checks (Trust & Safety)**

The agent enforces **bias-free scoring policies** before generating decisions:

**Policy 1: Remove Personal Identifiers (bias_check)**
- ❌ Removed: Candidate name, gender, age, address
- ✅ Preserved: Skills, experience, projects
- **Result:** Scoring cannot be influenced by personal characteristics
- **Status:** Logged as `bias_check: pass`

**Policy 2: Data Sanitization**
- Removes extra whitespace
- Normalizes text case
- Strips PII patterns
- **Result:** Clean, consistent input for evaluation
- **Status:** Logged as `data_sanitization: pass`

**Policy 3: Scoring Integrity**
- Deterministic algorithm (same input → same output)
- No randomness or ML bias
- Rule-based scoring (transparent, auditable)
- **Result:** Reproducible, fair decisions
- **Status:** Logged as `scoring_integrity: pass`

All three policies must pass before a evaluation is considered valid.

---

### 5. **Explainable AI Decisions**

Every decision includes complete reasoning, not just a score:

**What Users See:**
```
CANDIDATE: Alex Doe
FINAL SCORE: 78/100
DECISION: Shortlist ✓

SCORE BREAKDOWN:
  Skills Score: 48/60 (Matched 3 of 4 required skills)
  Experience Score: 20/25 (4 years vs 5 year target)
  Projects Score: 10/15 (2 projects mentioned)

STRENGTHS:
  • Matched skills: Python, Django, SQL
  • 4 years of relevant experience
  • Has completed project work

MISSING SKILLS:
  • AWS (required but not found)

REASONING:
  Candidate has strong core skills (Python, Django, SQL) and solid
  experience (4 years). Missing AWS is a gap but score exceeds
  shortlist threshold of 60. Recommend interviewing.
```

**Transparency Features:**
- 🔍 Step-by-step scoring shown
- 📊 Visual charts of score breakdown
- 📝 Human-readable explanation
- ✅ List of matched strengths
- ⚠️ List of missing skills
- 💭 Clear reasoning for decision

Every score is **auditable and defensible** against claims of bias.

---

### 6. **Verification Process (How to Verify This Agent)**

Anyone can verify the agent output in 5 steps:

**Step 1: Run the Agent**
```bash
streamlit run app.py
```
Upload a resume, run an evaluation. The agent generates a score and decision.

**Step 2: View Generated Files**
```bash
cat agentfacts.json       # Contains signature & merkle root
cat history.json          # Contains evaluation record
cat secret.key            # Contains HMAC key (for verification)
```

**Step 3: Check the Signature**
```
Merkle Root: a3f8c9d2e1b5c9d2e1b5c9d2e1b5c9d2...
Signature: 7f2a9c4e1b8d7f2a9c4e1b8d7f2a9c4e1b8d...
```
If both values are present, the agent produced verifiable output.

**Step 4: Verify Policy Checks**
```json
"policy_checks": {
  "bias_check": "pass",           ✓ No personal identifiers used
  "data_sanitization": "pass",    ✓ Input was cleaned
  "scoring_integrity": "pass"     ✓ Deterministic algorithm used
}
```
All three must show `pass` for agent to be trustworthy.

**Step 5: Audit the Activity Log**
```
- 2026-02-15T10:23:45Z: evaluate — Alex Doe evaluated
- 2026-02-15T10:23:46Z: policy_check — bias_check passed
- 2026-02-15T10:23:47Z: policy_check — sanitization passed
- 2026-02-15T10:23:48Z: score_calculated — Score: 78.0
- 2026-02-15T10:23:49Z: decide — Decision: Shortlist
```
Complete chronological record proves the agent followed all policies.

---

### 7. **Deliverables Included**

This project provides all artifacts required by the Verified Agent Build Track:

**Code Artifacts:**
- ✅ `app.py` — Interactive agent interface (189 lines)
- ✅ `hiring_agent.py` — Core evaluation logic (170 lines)
- ✅ `utils.py` — Helpers & cryptographic signing (145 lines)
- ✅ `requirements.txt` — All dependencies listed

**Verification Artifacts:**
- ✅ `agentfacts.json` — Signed agent output with merkle root
- ✅ `history.json` — Immutable evaluation records
- ✅ `secret.key` — HMAC key for signature verification

**Documentation:**
- ✅ `README.md` — Complete setup and usage instructions
- ✅ Verification tab in UI — Check signature & policy status
- ✅ Activity logs — Accessible via "Verification" tab

**Validation:**
- ✅ Signature verification implemented
- ✅ Merkle root computation included
- ✅ Policy checks logged and enforced
- ✅ Activity trail maintained

---

### 8. **Hackathon Alignment**

**Why This Project Exemplifies Verified Agents:**

1. **Trustworthiness:** Signature proves output hasn't been tampered with
2. **Transparency:** Every decision includes full reasoning
3. **Accountability:** Complete activity logs for audit
4. **Fairness:** Automated bias detection and policy enforcement
5. **Auditability:** Merkle root chain proves history integrity
6. **Reproducibility:** Deterministic algorithm, no black-box ML

**Judges Can Verify By:**
- Running `streamlit run app.py`
- Uploading a test resume
- Checking `agentfacts.json` for signature
- Reviewing activity logs in "Verification" tab
- Confirming all policy checks pass

**Production Readiness:**
- ~500 lines of production-quality code
- Zero external dependencies for cryptography (uses Python stdlib)
- Handles edge cases (PDF parsing, skill extraction)
- Clean, modular architecture

This project proves that AI agents CAN be transparent, verifiable, and trustworthy while remaining practical and user-friendly.

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.9 or higher
- pip (Python package manager)
- 5 MB disk space for dependencies

### **Step 1: Clone or Download the Project**
```bash
cd d:\Agent_Hackthoan\verified-hiring-agent
```

### **Step 2: Create a Virtual Environment**

**Windows PowerShell:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed streamlit-1.20+ pandas-1.4+ plotly-5.0+ PyPDF2-3.0+ numpy-1.22+
```

### **Step 4: Run the Application**
```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://[YOUR_IP]:8501
```

Open `http://localhost:8501` in your browser.

---

## 🎯 Features & Functionality

### **1️⃣ Evaluate Candidate (`app.py` - Tab 1)**

**Input:**
- Candidate Name
- Resume file (.txt or .pdf) OR paste resume text
- Job Description
- Optional skills override (comma-separated)
- Years of Experience (auto-extracted or manual)
- Projects description

**Process:**
1. Parse resume (PDF→text extraction, text→sanitization)
2. Extract skills using keyword matching (12 core tech skills: python, java, sql, aws, docker, react, ml, ai, api, cloud, flask, django)
3. Extract experience level from patterns
4. Match candidate skills vs. job requirements
5. Calculate weighted scores:
   - **Skills:** (matched skills / required skills) × 60
   - **Experience:** min(years / 5) × 25
   - **Projects:** min(projects / 3) × 15
6. Generate decision (Shortlist ≥ 60, Reject < 60)

**Output:**
- Score breakdown chart (visual progress bar)
- Explainable AI panel:
  - Final score (e.g., 78/100)
  - Strengths (what they match well)
  - Missing skills (gaps)
  - Experience evaluation
  - Final reasoning
- Download report (.txt)

**Example Output:**
```
Candidate: Alex Doe
Score: 78/100
Decision: Shortlist

Breakdown:
- Skills: 48/60 (80% match)
- Experience: 20/25 (4 years)
- Projects: 10/15 (2 projects)

Reasoning: Skills 48/60, Experience 20/25, Projects 10/15 → Total 78/100.
```

---

### **2️⃣ Compare Candidates (`app.py` - Tab 2)**

**Input:**
- Upload 2–5 resumes (.txt or .pdf files)

**Process:**
1. Batch evaluate all uploaded resumes
2. Extract skills automatically for each
3. Score each candidate using same engine
4. Sort by score (highest first)

**Output:**
- Comparison table:
  ```
  | Candidate | Score | Decision   |
  |-----------|-------|-----------|
  | Alice.pdf | 85.0  | Shortlist |
  | Bob.pdf   | 72.0  | Shortlist |
  | Carol.pdf | 45.0  | Reject    |
  ```

**Use Case:** Hiring managers can quickly rank candidates and identify top performers.

---

### **3️⃣ History Dashboard (`app.py` - Tab 3)**

**Features:**
- View all past evaluations
- Filter by decision (All / Shortlist / Reject)
- Sort by score (descending)
- Timestamp for each evaluation
- Persistent across sessions (stored in `history.json`)

**Example Table:**
```
| Name  | Score | Decision  | Date               |
|-------|-------|-----------|-------------------|
| Alex  | 78.0  | Shortlist | 2026-02-15 10:23  |
| Carol | 45.0  | Reject    | 2026-02-15 10:15  |
```

---

### **4️⃣ Verification Tab (`app.py` - Tab 4)**

**Trust Guarantees:**
- **Merkle Root:** Cryptographic hash of entire evaluation history
  - If any past evaluation is tampered, Merkle root changes
  - Provides integrity proof across all records
- **HMAC Signature:** Authenticates the Merkle root
  - Signed with secret key generated at first run
  - Proves evaluations haven't been altered
- **Policy Checks:**
  - ✅ `bias_check: pass` — PII removed before scoring
  - ✅ `data_sanitization: pass` — Text cleaned
  - ✅ `scoring_integrity: pass` — Deterministic algorithm
- **Activity Logs:** Timestamped record of all evaluations
  - Latest 20 logs displayed
  - Format: `[TIMESTAMP] action — {details}`

**Example Verification Output:**
```
Merkle root: a3f8c9d2e1b5...
Signature: 7f2a9c4e1b8d...

Policy checks:
- bias_check: pass
- data_sanitization: pass
- scoring_integrity: pass

Activity logs:
- 2026-02-15T10:23:45Z: evaluate — {id: abc123, decision: Shortlist, score: 78}
- 2026-02-15T10:15:30Z: evaluate — {id: def456, decision: Reject, score: 45}
```

---

## 🔍 Scoring Algorithm (Detailed)

### **Skill Matching (60 points)**
```python
Skill List: python, java, sql, aws, docker, react, ml, ai, api, cloud, flask, django

For each candidate:
  1. Extract skills from resume (keyword matching)
  2. Extract required skills from job description
  3. Calculate match percentage = (matched / required) × 100
  4. Skill Score = (match % / 100) × 60
  
Example:
  Candidate skills: [python, django, sql]
  Required skills: [python, django, sql, aws]
  Matched: 3/4 = 75%
  Skill Score: 0.75 × 60 = 45/60
```

### **Experience Scoring (25 points)**
```python
Target: 5 years
  1. Extract years from resume (e.g., "5 years experience")
  2. Calculate percentage = min(years / 5, 100%)
  3. Experience Score = percentage × 25

Example:
  Years extracted: 4
  Percentage: min(4/5, 1.0) = 0.8 = 80%
  Experience Score: 0.8 × 25 = 20/25
```

### **Projects Scoring (15 points)**
```python
Target: 3 projects
  1. Count word "project" in resume/projects field
  2. Calculate percentage = min(count / 3, 100%)
  3. Projects Score = percentage × 15

Example:
  Projects count: 2
  Percentage: min(2/3, 1.0) = 0.67 = 67%
  Projects Score: 0.67 × 15 = 10/15
```

### **Total Score & Decision**
```python
Total = Skill Score + Experience Score + Projects Score
Decision = "Shortlist" if Total >= 60 else "Reject"

Example: 45 + 20 + 10 = 75/100 → Shortlist
```

---

## 🔐 Trust & Verification Mechanisms

### **1. Bias Prevention**
```python
# Sanitization removes:
- Name: [stripped from scoring]
- Gender: [not considered]
- Age/DOB: [not considered]
- Address: [not considered]

# Preserves:
- Skills
- Experience
- Projects
- Technical keywords
```

### **2. Cryptographic Verification**
```
Evaluation Record
    ↓ (JSON serialized)
SHA256 Hash (Leaf Node)
    ↓ (Multiple leaves)
Merkle Tree
    ↓ (Root computed)
Merkle Root (Unique for all history)
    ↓ (HMAC signed)
HMAC Signature (Proves authenticity)
    ↓
Stored in agentfacts.json (Immutable proof)
```

**Why This Matters:**
- ✅ Proves no evaluations were deleted or modified
- ✅ Detects tampering immediately
- ✅ Provides audit trail for compliance

### **3. Deterministic Scoring**
- Same resume with same job description always produces same score
- No randomness or machine learning bias
- Fully reproducible and auditable
- Decision logic is rule-based (no black-box ML)

---

## 📊 Data & Storage

### **history.json**
Stores all evaluations. Grows with each assessment.

```json
[
  {
    "id": "abc123def456...",
    "name": "Alex Doe",
    "skills": ["python", "django", "sql"],
    "years_experience": 4.0,
    "projects": 2,
    "matched_skills": ["python", "django", "sql"],
    "missing_skills": ["aws"],
    "extra_skills": [],
    "skill_match_percent": 75.0,
    "scores": {
      "skills": 45.0,
      "experience": 20.0,
      "projects": 10.0
    },
    "total_score": 75.0,
    "decision": "Shortlist",
    "strengths": ["Matched skills: python, django, sql", "Experience: 4 years"],
    "reasoning": "Skills 45/60, Experience 20/25, Projects 10/15 → Total 75/100.",
    "timestamp": 1707969825
  }
]
```

### **agentfacts.json**
Trust & verification metadata.

```json
{
  "logs": [
    {"ts": "2026-02-15T10:23:45Z", "action": "evaluate", "details": {"id": "abc123...", "decision": "Shortlist", "score": 75.0}}
  ],
  "policy_checks": {
    "bias_check": "pass",
    "data_sanitization": "pass",
    "scoring_integrity": "pass"
  },
  "merkle_root": "a3f8c9d2e1b5...",
  "signature": "7f2a9c4e1b8d...",
  "last_evaluation": { ... }
}
```

---

## 🎓 Hackathon Submission Highlights

### **Innovation**
- ✅ **Explainable AI:** Every score has clear reasoning users can understand
- ✅ **Verifiable Decisions:** Cryptographic proof of integrity
- ✅ **Bias-Free Evaluation:** Automatic PII removal before scoring
- ✅ **Multi-Resume Support:** Compare up to 5 candidates side-by-side

### **Production Features**
- ✅ **Resume Parsing:** Handles both .txt and .pdf formats
- ✅ **History Management:** Persistent evaluation records
- ✅ **Downloadable Reports:** Export results as .txt files
- ✅ **Responsive UI:** Light theme, clean design, accessible layout

### **Trust & Security**
- ✅ **Merkle Root Verification:** Detect any tampering
- ✅ **HMAC Signatures:** Authenticate all outputs
- ✅ **Policy Compliance:** Automated bias checks
- ✅ **Audit Trail:** Complete activity log with timestamps

---

## 📖 Usage Guide

### **Scenario 1: Evaluate a Single Candidate**
1. Go to **"Evaluate Candidate"** tab
2. Enter candidate name
3. Upload resume (PDF) or paste text
4. Enter job description
5. Click **"Evaluate Candidate"**
6. Review score breakdown and explainable AI panel
7. Download report if needed

### **Scenario 2: Compare Multiple Candidates**
1. Go to **"Compare Candidates"** tab
2. Upload 2–5 resumes
3. System auto-evaluates all
4. View comparison table (sorted by score)
5. Identify top candidates

### **Scenario 3: Check Evaluation History**
1. Go to **"History Dashboard"** tab
2. Filter by decision (Shortlist/Reject/All)
3. Sort by score
4. View dates and scores
5. Copy data for reports

### **Scenario 4: Verify Integrity**
1. Go to **"Verification"** tab
2. Review Merkle root
3. Check policy compliance status
4. View activity logs
5. Confirm no tampering

---

## 🛠️ Requirements & Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥1.20 | Web framework |
| `pandas` | ≥1.4 | Data manipulation |
| `plotly` | ≥5.0 | Interactive charts |
| `numpy` | ≥1.22 | Numerical computing |
| `PyPDF2` | ≥3.0 | PDF text extraction |
| `Python` | ≥3.9 | Runtime |

**Install all:**
```bash
pip install -r requirements.txt
```

---

## 🚨 Important Notes

### **Limitations**
- Keyword-based skill matching (not NLP)
- Local JSON storage (not production database)
- Single-machine deployment (no distributed signing)
- No user authentication
- HMAC signing (not asymmetric cryptography for production)

### **For Production Deployment**
- Replace JSON with PostgreSQL/MongoDB
- Integrate with LDAP/OAuth for authentication
- Use asymmetric cryptography (RSA/Ed25519)
- Deploy behind load balancer (gunicorn + nginx)
- Add SSL/TLS certificates
- Implement rate limiting & logging
- Use cloud storage (AWS S3, Azure Blob) for reports

### **Future Enhancements**
- [ ] NLP-based skill extraction (spaCy, transformers)
- [ ] Machine learning resume scoring (gradient boosting)
- [ ] Multi-language support
- [ ] Resume ATS parsing (LinkedIn format)
- [ ] Job description enrichment (auto-extract requirements)
- [ ] Team collaboration (shared evaluations)
- [ ] Mobile app (React Native)

---

## 📞 Support & Questions

For questions or issues:
1. Check `README.md` (this file)
2. Review `history.json` for past evaluations
3. Check `agentfacts.json` for verification details
4. Run `streamlit run app.py` with fresh data if stuck

---

## 📝 Example Walkthrough

### **Step 1: Start the app**
```bash
streamlit run app.py
```

### **Step 2: Evaluate a candidate**
- Name: "John Smith"
- Resume: "5 years Python, Django, SQL. 3 projects: E-commerce, CRM, API."
- Job Description: "Looking for Python, Django, SQL, AWS developer"
- Years: 5

### **Step 3: Results**
```
Score: 75.0 / 100
Decision: Shortlist

Breakdown:
- Skills: 45/60 (3 of 4 matched: python, django, sql)
- Experience: 25/25 (5 years ≥ target)
- Projects: 5/15 (1 project mentioned)

Strengths:
- Matched skills: python, django, sql
- Experience: 5 years

Missing skills: aws

Reasoning: Skills 45/60, Experience 25/25, Projects 5/15 → Total 75/100.
Decision: Shortlist ✓
```

### **Step 4: Download & Share**
- Click "Download report (.txt)"
- Share with hiring team
- Archive in system

### **Step 5: Verify Integrity**
- Go to Verification tab
- See Merkle root & signature
- Confirm all policy checks pass ✓
- Trust the evaluation

---

## 🏆 Hackathon Summary

**Project Name:** Verified AI Hiring Assistant

**Core Achievement:** Explainable, verifiable, bias-free hiring evaluation with cryptographic proof of integrity.

**Key Differentiators:**
1. Transparency: Every score has clear reasoning
2. Trust: Merkle root + HMAC verification
3. Fairness: Automated bias detection
4. Accessibility: Simple, clean UI

**Tech Stack:** Python, Streamlit, Pandas, Plotly, PyPDF2

**Agents:** 3 (Evaluation, Verification, Sanitization)

**Lines of Code:** ~500 lines (production quality)

**Deployment:** Streamlit (`streamlit run app.py`)

---


🌍 Live Deployment

This application is deployed using Streamlit Community Cloud.

🔗 Access the App:

👉 https://verified-hiring-agentgitgitpush-uoriginmain-evhtrec52egzlzurta.streamlit.app/

☁️ Deployment Platform:

Streamlit Community Cloud

Python 3.9+

Automatic dependency installation via requirements.txt

📌 Note:

Evaluation history (history.json) and verification metadata (agentfacts.json) are stored temporarily in the cloud environment and reset on redeploy due to ephemeral storage. Verification functionality remains fully operational.

**Made for Hackathon • Built with ❤️ • Verified with 🔐**
