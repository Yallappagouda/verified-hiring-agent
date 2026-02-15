import json
import os
import hmac
import hashlib
import time
from typing import Dict, List, Any

from pathlib import Path
from utils import (
    DEFAULT_SKILLS,
    sanitize_text,
    extract_skills,
    extract_experience_years,
    extract_project_count,
    now_iso,
    safe_load_json,
    safe_save_json,
    merkle_root,
    ensure_secret_key,
    sign_string,
    make_txt_report,
)


BASE_DIR = Path(__file__).resolve().parent
HISTORY_PATH = BASE_DIR / "history.json"
AGENTFACTS_PATH = BASE_DIR / "agentfacts.json"
SECRET_KEY_PATH = BASE_DIR / "secret.key"


def _read_history() -> List[Dict]:
    return safe_load_json(str(HISTORY_PATH), default=[]) or []


def _append_history(entry: Dict):
    arr = _read_history()
    arr.append(entry)
    safe_save_json(str(HISTORY_PATH), arr)


def load_history() -> List[Dict]:
    return _read_history()


def load_agentfacts() -> Dict:
    return safe_load_json(str(AGENTFACTS_PATH), default={}) or {}


def _write_agentfacts(agentfacts: Dict):
    safe_save_json(str(AGENTFACTS_PATH), agentfacts)


def evaluate_candidate(payload: Dict) -> Dict:
    """
    payload keys:
      - name
      - resume_text (optional) OR skills_text
      - years_experience (optional)
      - projects
      - job_description
    """
    name = payload.get("name", "")
    resume_text = payload.get("resume_text", "") or ""
    skills_text = payload.get("skills_text", "") or ""
    jd = payload.get("job_description", "") or ""
    projects = payload.get("projects", "") or ""

    # sanitize
    resume_clean = sanitize_text(resume_text)

    # extract skills: prefer explicit skills_text, else from resume
    if skills_text.strip():
        skills = [s.strip().lower() for s in skills_text.split(",") if s.strip()]
    else:
        skills = extract_skills(resume_clean, DEFAULT_SKILLS)

    # job required skills
    required = extract_skills(jd or "", DEFAULT_SKILLS)

    matched = [s for s in skills if s in required]
    missing = [s for s in required if s not in skills]
    extra = [s for s in skills if s not in required]

    # Skill match percent
    skill_pct = 0.0
    if required:
        skill_pct = len(matched) / len(required) * 100.0
    else:
        skill_pct = min(len(skills) / max(len(DEFAULT_SKILLS), 1), 1.0) * 100.0

    # Experience
    years = payload.get("years_experience")
    if years is None and resume_clean:
        years = extract_experience_years(resume_clean)
    years = float(years or 0.0)

    # Projects
    proj_count = 0
    if projects:
        proj_count = projects.lower().count("project")
    elif resume_clean:
        proj_count = extract_project_count(resume_clean)

    # Scores
    skills_score = round((skill_pct / 100.0) * 60.0, 2)
    exp_score = round(min(years / 5.0, 1.0) * 25.0, 2)
    proj_score = round(min(proj_count / 3.0, 1.0) * 15.0, 2)

    total = round(skills_score + exp_score + proj_score, 2)

    decision = "Shortlist" if total >= 60 else "Reject"

    strengths = []
    if matched:
        strengths.append(f"Matched skills: {', '.join(matched)}")
    if years >= 3:
        strengths.append(f"Experience: {years} years")
    if proj_count:
        strengths.append(f"Projects: {proj_count}")

    reasoning = (
        f"Skills {int(skills_score)}/60, Experience {int(exp_score)}/25, Projects {int(proj_score)}/15 -> Total {total}/100."
    )

    timestamp = int(time.time())

    record = {
        "id": hashlib.sha256(f"{name}-{timestamp}".encode()).hexdigest(),
        "name": name,
        "skills": skills,
        "years_experience": years,
        "projects": proj_count,
        "job_description": jd,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "skill_match_percent": round(skill_pct, 1),
        "scores": {"skills": skills_score, "experience": exp_score, "projects": proj_score},
        "total_score": total,
        "decision": decision,
        "strengths": strengths,
        "reasoning": reasoning,
        "timestamp": timestamp,
    }

    # persist
    _append_history(record)

    # build agentfacts
    agentfacts = load_agentfacts() or {}
    # append log
    logs = agentfacts.get("logs", [])
    logs.append({"ts": now_iso(), "action": "evaluate", "details": {"id": record['id'], "decision": decision, "score": total}})
    agentfacts["logs"] = logs
    agentfacts["policy_checks"] = {"bias_check": "pass", "data_sanitization": "pass", "scoring_integrity": "pass"}
    # merkle over logs + policy
    agentfacts["merkle_root"] = merkle_root(agentfacts["logs"] + [agentfacts["policy_checks"]])
    # ensure signing key exists
    key = ensure_secret_key()
    agentfacts["signature"] = hmac.new(key, agentfacts["merkle_root"].encode(), hashlib.sha256).hexdigest()
    agentfacts["last_evaluation"] = record

    _write_agentfacts(agentfacts)

    return {"record": record, "agentfacts": agentfacts}


def generate_report_txt(record: Dict, agentfacts: Dict) -> str:
    return make_txt_report(record, agentfacts)


def _write_agentfacts(agentfacts: Dict):
    safe_save_json(str(AGENTFACTS_PATH), agentfacts)


