import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from hiring_agent import evaluate_candidate, load_history, load_agentfacts, generate_report_txt
from utils import extract_text_from_pdf, sanitize_text, extract_skills, DEFAULT_SKILLS

# ======================== PAGE CONFIG ========================
st.set_page_config(
    page_title="Verified AI Hiring Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================== CUSTOM CSS ========================
CSS = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid='stAppViewContainer'] {
        background: #F8FAFC !important;
        color: #111827 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    [data-testid='stSidebar'] {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
    }
    
    .main {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(16, 24, 40, 0.05), 0 10px 20px rgba(16, 24, 40, 0.08);
        border: 1px solid rgba(16, 24, 40, 0.06);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 8px 12px rgba(16, 24, 40, 0.08), 0 20px 40px rgba(16, 24, 40, 0.12);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e5e7eb;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(37, 99, 235, 0.1);
    }
    
    .metric-label {
        font-size: 13px;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
        margin: 8px 0;
    }
    
    /* Score Badge */
    .score-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
    }
    
    .score-excellent {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
    }
    
    .score-good {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
    }
    
    .score-poor {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
    }
    
    /* Decision Badge */
    .decision-shortlist {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        color: #065F46;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
        margin: 12px 0;
    }
    
    .decision-reject {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        color: #7F1D1D;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
        margin: 12px 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Text Input */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 2px solid #E5E7EB !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
        transition: border 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 2px dashed #2563EB !important;
        border-radius: 12px !important;
        background: rgba(37, 99, 235, 0.03) !important;
    }
    
    /* Headers */
    h1 {
        color: #111827 !important;
        font-weight: 800 !important;
        margin-bottom: 8px !important;
    }
    
    h2 {
        color: #111827 !important;
        font-weight: 700 !important;
        margin-top: 20px !important;
        margin-bottom: 16px !important;
    }
    
    h3 {
        color: #1F2937 !important;
        font-weight: 600 !important;
        margin: 16px 0 12px 0 !important;
    }
    
    /* Sidebar Text */
    [data-testid='stSidebar'] h2,
    [data-testid='stSidebar'] h3,
    [data-testid='stSidebar'] h4 {
        color: white !important;
    }
    
    [data-testid='stSidebar'] p,
    [data-testid='stSidebar'] span {
        color: #E0E7FF !important;
    }
    
    /* Expandable Sections */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%) !important;
        border-radius: 8px !important;
        color: #111827 !important;
        font-weight: 600 !important;
    }
    
    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    /* Lists */
    ul {
        margin-left: 20px;
    }
    
    li {
        margin-bottom: 8px;
        color: #374151;
    }
    
    /* Status Indicators */
    .status-pass {
        color: #10B981;
        font-weight: 600;
    }
    
    .status-fail {
        color: #EF4444;
        font-weight: 600;
    }
    
    /* Container */
    [data-testid="stVerticalBlock"] {
        gap: 16px;
    }
    
    /* Sidebar Links */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > button {
        width: 100%;
        text-align: left;
        margin-bottom: 8px;
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > button:hover {
        background: rgba(37, 99, 235, 0.3) !important;
    }
    
    /* Muted Text */
    .muted {
        color: #6B7280 !important;
        font-size: 14px;
    }
    
    .small {
        font-size: 13px;
    }
    
    .accent {
        color: #2563EB;
        font-weight: 600;
    }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ======================== HEADER ========================
header_col1, header_col2 = st.columns([1, 4])

with header_col1:
    st.markdown(
        """
        <div style='width:60px; height:60px; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); border-radius:14px; display:flex; align-items:center; justify-content:center; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);'>
            <svg width='32' height='32' viewBox='0 0 24 24' fill='white' xmlns='http://www.w3.org/2000/svg'><path d='M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z'/></svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_col2:
    st.markdown(
        """
        <div style='padding: 8px 0;'>
            <h1 style='margin: 0; font-size: 32px;'>Verified AI Hiring Assistant</h1>
            <p style='margin: 6px 0 0 0; color: #6B7280; font-size: 15px;'>🔐 Transparent, explainable, verifiable hiring evaluation</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ======================== SIDEBAR NAVIGATION ========================
with st.sidebar:
    st.markdown("<h2>Navigation</h2>", unsafe_allow_html=True)
    
    page = st.radio(
        "Select Tab:",
        ["📋 Evaluate Candidate", "🔄 Compare Candidates", "📊 History Dashboard", "✅ Verification"],
        label_visibility="collapsed",
    )
    
    st.markdown("---")    
    st.markdown(
        """
        <div style='background: rgba(37, 99, 235, 0.1); border-radius: 10px; padding: 16px; margin-top: 16px;'>
            <h4 style='margin: 0 0 8px 0; color: #2563EB;'>ℹ️ About</h4>
            <p style='margin: 0; font-size: 13px; color: #E0E7FF;'>
                This is a verified AI hiring agent that uses cryptographic signatures and Merkle roots to prove the integrity of every evaluation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div style='background: rgba(16, 185, 129, 0.1); border-radius: 10px; padding: 16px; margin-top: 12px;'>
            <h4 style='margin: 0 0 8px 0; color: #10B981;'>🔒 Trust & Safety</h4>
            <ul style='margin: 0; padding-left: 16px; font-size: 13px; color: #E0E7FF;'>
                <li>⚠️ Name & personal data removed before scoring</li>
                <li>🔐 All decisions cryptographically signed</li>
                <li>📝 Complete activity logs maintained</li>
                <li>✅ Bias checks enforced</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================== EVALUATE CANDIDATE ========================
if page == "📋 Evaluate Candidate":
    st.markdown("<h2>📋 Evaluate Candidate</h2>", unsafe_allow_html=True)
    st.markdown(
        '<p class="muted">Upload a resume and job description to get an explainable AI evaluation with trust verification.</p>',
        unsafe_allow_html=True,
    )
    
    # Input Section
    input_card = st.container()
    with input_card:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>📑 Candidate Information</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            name = st.text_input("👤 Candidate Name", placeholder="e.g., Alex Johnson")
            years_experience = st.number_input(
                "📅 Years of Experience",
                min_value=0.0,
                max_value=50.0,
                value=0.0,
                step=0.5,
            )
        with col2:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            skills_override = st.text_input(
                "🎯 Skills (optional)",
                placeholder="e.g., python, django, sql, aws",
                help="Leave empty to auto-extract from resume"
            )
        
        st.markdown("<h3>📄 Resume</h3>", unsafe_allow_html=True)
        
        tab_upload, tab_paste = st.tabs(["📤 Upload File", "📋 Paste Text"])
        
        with tab_upload:
            resume_file = st.file_uploader(
                "Drag and drop your resume here (.txt, .pdf)",
                type=["txt", "pdf"],
                accept_multiple_files=False,
                label_visibility="collapsed"
            )
            if resume_file:
                st.success(f"✓ Uploaded: {resume_file.name}")
        
        with tab_paste:
            paste = st.text_area(
                "Or paste your resume content here:",
                height=200,
                placeholder="Paste resume text...",
                label_visibility="collapsed"
            )
        
        st.markdown("<h3>💼 Job Description</h3>", unsafe_allow_html=True)
        job_description = st.text_area(
            "Job Description",
            height=150,
            placeholder="Paste the job description...",
            label_visibility="collapsed"
        )
        
        st.markdown("<h3>🚀 Projects (optional)</h3>", unsafe_allow_html=True)
        projects = st.text_area(
            "Projects description",
            height=100,
            placeholder="Describe relevant projects...",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Evaluate Button
        col_btn1, col_btn2 = st.columns([2, 3])
        with col_btn1:
            evaluate_btn = st.button("🚀 Evaluate Candidate", use_container_width=True)
        with col_btn2:
            st.markdown(
                '<div class="muted small" style="margin-top: 12px;">🔒 <strong>Privacy:</strong> Name, gender, age, address are removed before scoring to prevent bias.</div>',
                unsafe_allow_html=True,
            )
    
    # Results Section
    if evaluate_btn:
        # Obtain resume text
        resume_text = ""
        if resume_file is not None:
            if resume_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(resume_file)
            else:
                try:
                    resume_text = resume_file.getvalue().decode("utf-8")
                except Exception:
                    resume_text = str(resume_file.getvalue())
        if paste and not resume_text:
            resume_text = paste

        if not resume_text:
            st.error("❌ Please provide a resume (upload or paste)")
        elif not job_description:
            st.error("❌ Please provide a job description")
        elif not name:
            st.error("❌ Please enter candidate name")
        else:
            with st.spinner("⏳ Processing evaluation..."):
                resume_text = sanitize_text(resume_text)

                # Extracted skills
                extracted = extract_skills(resume_text, DEFAULT_SKILLS)
                if skills_override.strip():
                    skills_text = skills_override
                else:
                    skills_text = ", ".join(extracted)

                payload = {
                    "name": name,
                    "resume_text": resume_text,
                    "skills_text": skills_text,
                    "years_experience": years_experience if years_experience > 0 else None,
                    "projects": projects,
                    "job_description": job_description,
                }

                out = evaluate_candidate(payload)
                record = out["record"]
                agentfacts = out["agentfacts"]

            st.markdown("---")
            
            # Result Card - Score Display
            result_card = st.container()
            with result_card:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                # Top row: Name and Decision
                res_col1, res_col2 = st.columns([3, 1])
                with res_col1:
                    st.markdown(f"<h2 style='margin: 0;'>{record['name']}</h2>", unsafe_allow_html=True)
                with res_col2:
                    decision_class = "decision-shortlist" if record['decision'] == "Shortlist" else "decision-reject"
                    decision_icon = "✅" if record['decision'] == "Shortlist" else "❌"
                    st.markdown(
                        f'<div class="{decision_class}" style="text-align: center;">{decision_icon} {record["decision"]}</div>',
                        unsafe_allow_html=True,
                    )
                
                st.markdown("<hr style='margin: 16px 0;'>", unsafe_allow_html=True)
                
                # Score Visualization
                score = record['total_score']
                if score >= 80:
                    score_class = "score-excellent"
                elif score >= 60:
                    score_class = "score-good"
                else:
                    score_class = "score-poor"
                
                score_col1, score_col2 = st.columns([2, 3])
                
                with score_col1:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Overall Score</div>
                            <div class="metric-value">{score:.0f}</div>
                            <div style="font-size: 13px; color: #9CA3AF;">out of 100</div>
                            <div style="margin-top: 12px;">
                                <div style="background: #E5E7EB; height: 8px; border-radius: 4px; overflow: hidden;">
                                    <div style="background: linear-gradient(90deg, {'#10B981' if score >= 80 else '#F59E0B' if score >= 60 else '#EF4444'} 0%, {'#059669' if score >= 80 else '#D97706' if score >= 60 else '#DC2626'} 100%); height: 100%; width: {min(score, 100)}%; border-radius: 4px;"></div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                with score_col2:
                    # Score Breakdown
                    br = record['scores']
                    breakdown_df = pd.DataFrame({
                        'Category': ['Skills', 'Experience', 'Projects'],
                        'Score': [int(br['skills']), int(br['experience']), int(br['projects'])],
                        'Max': [60, 25, 15]
                    })
                    
                    for idx, row in breakdown_df.iterrows():
                        pct = (row['Score'] / row['Max']) * 100
                        st.markdown(
                            f"""
                            <div style="margin-bottom: 12px;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="font-weight: 600; color: #111827;">{row['Category']}</span>
                                    <span style="color: #2563EB; font-weight: 700;">{row['Score']}/{row['Max']}</span>
                                </div>
                                <div style="background: #E5E7EB; height: 6px; border-radius: 3px; overflow: hidden;">
                                    <div style="background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%); height: 100%; width: {min(pct, 100)}%; border-radius: 3px;"></div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Explainable AI Section
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3>🧠 Explainable AI Analysis</h3>", unsafe_allow_html=True)
            
            explain_col1, explain_col2 = st.columns([1, 1])
            
            with explain_col1:
                with st.expander("💚 Strengths", expanded=True):
                    if record['strengths']:
                        for strength in record['strengths']:
                            st.markdown(f"<div style='color: #10B981; margin: 8px 0;'>✓ {strength}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='muted'>No significant strengths identified</div>", unsafe_allow_html=True)
            
            with explain_col2:
                with st.expander("⚠️ Missing Skills", expanded=True):
                    if record['missing_skills']:
                        for skill in record['missing_skills']:
                            st.markdown(f"<div style='color: #EF4444; margin: 8px 0;'>✗ {skill}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='color: #10B981; font-weight: 600;'>✓ No critical missing skills</div>", unsafe_allow_html=True)
            
            with st.expander("📊 Skill Match Details"):
                st.markdown(
                    f"""
                    <div style='background: #F9FAFB; padding: 16px; border-radius: 10px;'>
                        <div style='margin-bottom: 12px;'>
                            <span style='font-weight: 600; color: #111827;'>Matched Skills:</span>
                            <span style='color: #10B981; font-weight: 600;'>{', '.join(record['matched_skills']) if record['matched_skills'] else 'None'}</span>
                        </div>
                        <div style='margin-bottom: 12px;'>
                            <span style='font-weight: 600; color: #111827;'>Missing Skills:</span>
                            <span style='color: #EF4444; font-weight: 600;'>{', '.join(record['missing_skills']) if record['missing_skills'] else 'None'}</span>
                        </div>
                        <div>
                            <span style='font-weight: 600; color: #111827;'>Match Percentage:</span>
                            <span style='color: #2563EB; font-weight: 600;'>{record['skill_match_percent']:.1f}%</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            with st.expander("🏢 Experience & Projects"):
                st.markdown(
                    f"""
                    <div style='background: #F9FAFB; padding: 16px; border-radius: 10px;'>
                        <div style='margin-bottom: 12px;'>
                            <span style='font-weight: 600; color: #111827;'>Years of Experience:</span>
                            <span style='color: #2563EB; font-weight: 600;'>{record['years_experience']:.1f} years</span>
                        </div>
                        <div>
                            <span style='font-weight: 600; color: #111827;'>Projects Found:</span>
                            <span style='color: #2563EB; font-weight: 600;'>{record['projects']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            with st.expander("💭 Final Reasoning"):
                st.markdown(
                    f"""
                    <div style='background: #F0F9FF; padding: 16px; border-radius: 10px; border-left: 4px solid #2563EB;'>
                        {record['reasoning']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download Report
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3>📥 Download Report</h3>", unsafe_allow_html=True)
            txt = generate_report_txt(record, agentfacts)
            st.download_button(
                label="📄 Download as Text (.txt)",
                data=txt,
                file_name=f"evaluation_{record['id'][:8]}.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ======================== COMPARE CANDIDATES ========================
elif page == "🔄 Compare Candidates":
    st.markdown("<h2>🔄 Compare Candidates</h2>", unsafe_allow_html=True)
    st.markdown(
        '<p class="muted">Upload 2–5 resumes to compare scores side-by-side and identify top performers.</p>',
        unsafe_allow_html=True,
    )
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload resumes (.txt, .pdf)",
        type=["txt", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded:
        if len(uploaded) > 5:
            st.warning("⚠️ Maximum 5 resumes allowed. Only the first 5 will be evaluated.")
            uploaded = uploaded[:5]
        
        with st.spinner("⏳ Processing resumes..."):
            items = []
            for f in uploaded:
                text = ""
                if f.type == "application/pdf":
                    text = extract_text_from_pdf(f)
                else:
                    try:
                        text = f.getvalue().decode("utf-8")
                    except Exception:
                        text = str(f.getvalue())
                
                text = sanitize_text(text)
                skills_found = extract_skills(text, DEFAULT_SKILLS)
                
                payload = {
                    "name": f.name.replace(".pdf", "").replace(".txt", ""),
                    "resume_text": text,
                    "skills_text": ", ".join(skills_found),
                }
                out = evaluate_candidate(payload)
                rec = out["record"]
                items.append(rec)
            
            if items:
                st.markdown("---")
                
                # Comparison Cards
                df = pd.DataFrame(items)
                df_sorted = df.sort_values("total_score", ascending=False)
                
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("<h3>📊 Candidate Rankings</h3>", unsafe_allow_html=True)
                
                for idx, (_, row) in enumerate(df_sorted.iterrows(), 1):
                    score = row['total_score']
                    decision = row['decision']
                    
                    col1, col2, col3, col4 = st.columns([0.5, 2, 1.5, 1.5])
                    
                    with col1:
                        st.markdown(
                            f'<div style="background: #2563EB; color: white; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700;">{idx}</div>',
                            unsafe_allow_html=True,
                        )
                    
                    with col2:
                        st.markdown(f"<strong>{row['name']}</strong>", unsafe_allow_html=True)
                    
                    with col3:
                        if score >= 80:
                            st.markdown(f'<div class="score-badge score-excellent">{score:.1f}/100</div>', unsafe_allow_html=True)
                        elif score >= 60:
                            st.markdown(f'<div class="score-badge score-good">{score:.1f}/100</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="score-badge score-poor">{score:.1f}/100</div>', unsafe_allow_html=True)
                    
                    with col4:
                        if decision == "Shortlist":
                            st.markdown(f'<div class="decision-shortlist" style="text-align: center; padding: 6px 12px;">✅ {decision}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="decision-reject" style="text-align: center; padding: 6px 12px;">❌ {decision}</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Summary Stats
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("<h3>📈 Summary Statistics</h3>", unsafe_allow_html=True)
                
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Highest Score</div>
                            <div class="metric-value">{df['total_score'].max():.1f}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                with stat_col2:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Lowest Score</div>
                            <div class="metric-value">{df['total_score'].min():.1f}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                with stat_col3:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Average Score</div>
                            <div class="metric-value">{df['total_score'].mean():.1f}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                with stat_col4:
                    shortlist_count = len(df[df['decision'] == 'Shortlist'])
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Shortlisted</div>
                            <div class="metric-value">{shortlist_count}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📤 Upload multiple resumes to begin comparison")

# ======================== HISTORY DASHBOARD ========================
elif page == "📊 History Dashboard":
    st.markdown("<h2>📊 History Dashboard</h2>", unsafe_allow_html=True)
    st.markdown(
        '<p class="muted">View all past evaluations, filter by decision, and track hiring metrics.</p>',
        unsafe_allow_html=True,
    )
    
    history = load_history()
    
    if not history:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("📭 No evaluations yet. Start by evaluating a candidate!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        df = pd.DataFrame(history)
        df['date'] = df['timestamp'].apply(lambda t: datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M'))
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>🔍 Filters</h3>", unsafe_allow_html=True)
        
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            decision_filter = st.selectbox(
                "Filter by Decision:",
                ["All", "Shortlist", "Reject"],
                label_visibility="collapsed"
            )
        
        with filter_col2:
            sort_asc = st.checkbox("Sort by score (ascending)", value=False)
        
        # Apply filters
        if decision_filter != "All":
            df = df[df['decision'] == decision_filter]
        
        df = df.sort_values('total_score', ascending=sort_asc)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display Table
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<h3>📋 Evaluations ({len(df)})</h3>", unsafe_allow_html=True)
        
        # Custom table display
        for idx, (_, row) in enumerate(df.iterrows(), 1):
            score = row['total_score']
            decision = row['decision']
            
            col1, col2, col3, col4, col5 = st.columns([0.5, 2, 1.5, 1.5, 1.5])
            
            with col1:
                st.markdown(f"<div style='text-align: center; font-weight: 600; color: #6B7280;'>{idx}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<div><strong>{row['name']}</strong><br><span class='muted'>{row['date']}</span></div>", unsafe_allow_html=True)
            
            with col3:
                if score >= 80:
                    st.markdown(f'<div class="score-badge score-excellent">{score:.1f}/100</div>', unsafe_allow_html=True)
                elif score >= 60:
                    st.markdown(f'<div class="score-badge score-good">{score:.1f}/100</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="score-badge score-poor">{score:.1f}/100</div>', unsafe_allow_html=True)
            
            with col4:
                if decision == "Shortlist":
                    st.markdown(f'<div class="decision-shortlist" style="padding: 6px 12px;">✅ Shortlist</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="decision-reject" style="padding: 6px 12px;">❌ Reject</div>', unsafe_allow_html=True)
            
            with col5:
                st.write(f"Skills: {(row['skill_match_percent']):.0f}%")
            
            st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Statistics
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>📊 Statistics</h3>", unsafe_allow_html=True)
        
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Total Evaluated</div>
                    <div class="metric-value">{len(df)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with stats_col2:
            shortlist_count = len(df[df['decision'] == 'Shortlist'])
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Shortlisted</div>
                    <div class="metric-value" style="color: #10B981;">{shortlist_count}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with stats_col3:
            reject_count = len(df[df['decision'] == 'Reject'])
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Rejected</div>
                    <div class="metric-value" style="color: #EF4444;">{reject_count}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with stats_col4:
            avg_score = df['total_score'].mean()
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Average Score</div>
                    <div class="metric-value">{avg_score:.1f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

# ======================== VERIFICATION ========================
elif page == "✅ Verification":
    st.markdown("<h2>✅ Verification & Trust</h2>", unsafe_allow_html=True)
    st.markdown(
        '<p class="muted">View agent signatures, merkle root, policy checks, and audit logs to verify the integrity of all decisions.</p>',
        unsafe_allow_html=True,
    )
    
    agentfacts = load_agentfacts()
    
    if not agentfacts:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("⏳ No agentfacts yet. Perform an evaluation first to generate verification data.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Verification Status Banner
        all_checks_pass = all(
            agentfacts.get('policy_checks', {}).get(check) == 'pass'
            for check in ['bias_check', 'data_sanitization', 'scoring_integrity']
        )
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if all_checks_pass:
            st.markdown(
                """
                <div style='background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); border: 2px solid #10B981; border-radius: 12px; padding: 20px; text-align: center;'>
                    <h3 style='margin: 0; color: #065F46;'>✅ All Verification Checks Passed</h3>
                    <p style='margin: 8px 0 0 0; color: #047857;'>This agent's output has been verified and is trustworthy.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style='background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%); border: 2px solid #EF4444; border-radius: 12px; padding: 20px; text-align: center;'>
                    <h3 style='margin: 0; color: #7F1D1D;'>⚠️ Verification Failed</h3>
                    <p style='margin: 8px 0 0 0; color: #991B1B;'>Some policy checks did not pass. Review below.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Policy Checks
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>🛡️ Policy Checks</h3>", unsafe_allow_html=True)
        
        policies = agentfacts.get('policy_checks', {})
        
        policy_col1, policy_col2, policy_col3 = st.columns(3)
        
        policy_details = {
            'bias_check': {
                'label': 'Bias Check',
                'description': 'Name, gender, age, address removed before scoring',
                'icon': '⚠️'
            },
            'data_sanitization': {
                'label': 'Data Sanitization',
                'description': 'Resume text cleaned and normalized',
                'icon': '🧹'
            },
            'scoring_integrity': {
                'label': 'Scoring Integrity',
                'description': 'Deterministic algorithm, no random bias',
                'icon': '⚙️'
            }
        }
        
        with policy_col1:
            status = policies.get('bias_check', 'unknown')
            status_class = 'status-pass' if status == 'pass' else 'status-fail'
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">⚠️ {policy_details['bias_check']['label']}</div>
                    <div style="font-size: 14px; color: #6B7280; margin: 8px 0;">{policy_details['bias_check']['description']}</div>
                    <div class="{status_class}" style="font-size: 14px; margin-top: 8px;">{'✓ PASS' if status == 'pass' else '✗ FAIL'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with policy_col2:
            status = policies.get('data_sanitization', 'unknown')
            status_class = 'status-pass' if status == 'pass' else 'status-fail'
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">🧹 {policy_details['data_sanitization']['label']}</div>
                    <div style="font-size: 14px; color: #6B7280; margin: 8px 0;">{policy_details['data_sanitization']['description']}</div>
                    <div class="{status_class}" style="font-size: 14px; margin-top: 8px;">{'✓ PASS' if status == 'pass' else '✗ FAIL'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with policy_col3:
            status = policies.get('scoring_integrity', 'unknown')
            status_class = 'status-pass' if status == 'pass' else 'status-fail'
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">⚙️ {policy_details['scoring_integrity']['label']}</div>
                    <div style="font-size: 14px; color: #6B7280; margin: 8px 0;">{policy_details['scoring_integrity']['description']}</div>
                    <div class="{status_class}" style="font-size: 14px; margin-top: 8px;">{'✓ PASS' if status == 'pass' else '✗ FAIL'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Cryptographic Signatures
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>🔐 Cryptographic Signatures</h3>", unsafe_allow_html=True)
        
        with st.expander("📜 Merkle Root (Hash Chain)", expanded=True):
            merkle_root = agentfacts.get('merkle_root', 'N/A')
            st.code(merkle_root, language="text")
            st.markdown(
                '<p class="muted">This is a SHA256 hash of all evaluation records. Any change to history will change this value.</p>',
                unsafe_allow_html=True,
            )
        
        with st.expander("✍️ HMAC Signature"):
            signature = agentfacts.get('signature', 'N/A')
            st.code(signature, language="text")
            st.markdown(
                '<p class="muted">This is an HMAC-SHA256 signature of the Merkle root, proving it has not been tampered with.</p>',
                unsafe_allow_html=True,
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Activity Logs
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>📋 Activity Logs (Latest 20)</h3>", unsafe_allow_html=True)
        
        logs = agentfacts.get('logs', [])
        if logs:
            for log in logs[-20:][::-1]:
                ts = log.get('ts', 'N/A')
                action = log.get('action', 'unknown')
                details = log.get('details', {})
                
                action_icon = {
                    'evaluate': '📊',
                    'policy_check': '✅',
                    'score_calculated': '🧮',
                    'decide': '⚖️',
                    'history_updated': '💾'
                }.get(action, '📝')
                
                st.markdown(
                    f"""
                    <div style='background: #F9FAFB; border-radius: 8px; padding: 12px; margin-bottom: 8px; border-left: 4px solid #2563EB;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <span style='font-weight: 600; color: #111827;'>{action_icon} {action.replace('_', ' ').title()}</span>
                                <br>
                                <span class='muted'>{ts}</span>
                            </div>
                            <div style='font-size: 12px; color: #6B7280;'>{str(details)[:50]}...</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown('<p class="muted">No activity logs yet.</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

