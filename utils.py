import re
import json
import os
import hmac
import hashlib
from datetime import datetime
from typing import List, Any
from pathlib import Path
from PyPDF2 import PdfReader

BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY_FILE = BASE_DIR / "secret.key"

# Skill list specified by the user requirements
DEFAULT_SKILLS = [
    "python", "java", "sql", "aws", "docker", "react", "ml", "ai", "api",
    "cloud", "flask", "django"
]


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def ensure_secret_key() -> bytes:
    if SECRET_KEY_FILE.exists():
        return SECRET_KEY_FILE.read_bytes()
    key = os.urandom(32)
    SECRET_KEY_FILE.write_bytes(key)
    return key


def sign_string(key: str, message: str) -> str:
    # key may be hex or raw bytes
    raw = key.encode() if isinstance(key, str) else key
    sig = hmac.new(raw, message.encode("utf-8"), hashlib.sha256).hexdigest()
    return sig


def merkle_root(items: List[Any]) -> str:
    # items: list of serializable objects -> string leaves
    leaves = [json.dumps(i, sort_keys=True) for i in items]
    if not leaves:
        return hashlib.sha256(b"").hexdigest()
    nodes = [hashlib.sha256(l.encode("utf-8")).digest() for l in leaves]
    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])
        new_nodes = []
        for i in range(0, len(nodes), 2):
            new_nodes.append(hashlib.sha256(nodes[i] + nodes[i+1]).digest())
        nodes = new_nodes
    return nodes[0].hex()


def safe_load_json(path: str, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def safe_save_json(path: str, data: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def extract_text_from_pdf(file) -> str:
    try:
        reader = PdfReader(file)
        pages = [p.extract_text() or "" for p in reader.pages]
        return "\n".join(pages)
    except Exception:
        return ""


def sanitize_text(text: str) -> str:
    if not text:
        return ""
    # Remove common PII lines
    lines = text.splitlines()
    filtered = []
    for ln in lines:
        low = ln.lower()
        if any(tag in low for tag in ["name:", "gender:", "age:", "address:"]):
            continue
        filtered.append(ln)
    out = "\n".join(filtered)
    # collapse whitespace
    out = re.sub(r"\s+", " ", out).strip()
    return out


def extract_skills(text: str, skills_list: List[str] = None) -> List[str]:
    if skills_list is None:
        skills_list = DEFAULT_SKILLS
    t = text.lower()
    found = []
    for s in skills_list:
        if s in t:
            found.append(s)
    return sorted(found)


def extract_experience_years(text: str) -> float:
    matches = re.findall(r"(\d{1,2})\s*\+?\s*(?:years|yrs|year)", text.lower())
    nums = [int(m) for m in matches] if matches else []
    if nums:
        return max(nums)
    if "senior" in text.lower():
        return 6
    if "mid" in text.lower() or "mid-level" in text.lower():
        return 3
    return 1


def extract_project_count(text: str) -> int:
    return text.lower().count("project")


def make_txt_report(record: dict, agentfacts: dict) -> str:
    parts = []
    parts.append(f"Candidate: {record.get('name')}")
    parts.append(f"Date: {now_iso()}")
    parts.append(f"Score: {record.get('total_score')}")
    parts.append("\nBreakdown:")
    for k, v in record.get('scores', {}).items():
        parts.append(f" - {k}: {v}")
    parts.append(f"Decision: {record.get('decision')}")
    parts.append("\nExplanation:")
    parts.append(record.get('reasoning', ''))
    parts.append("\nPolicy checks:")
    for k, v in agentfacts.get('policy_checks', {}).items():
        parts.append(f" - {k}: {v}")
    parts.append(f"Merkle root: {agentfacts.get('merkle_root')}")
    parts.append(f"Signature: {agentfacts.get('signature')}")
    return "\n".join(parts)
