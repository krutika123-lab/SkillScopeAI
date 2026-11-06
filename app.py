import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_processing import load_jobs
from src.database import initialize_database
from src.analytics import filtered_jobs, skill_comparison
from src.ai_features import (
    ai_is_configured,
    analyze_job_description,
    ask_about_data,
    career_skill_gap,
)

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="SkillScope AI",
    page_icon="📊",
    layout="wide",
)

# Theme selector. Light mode is the default for comfortable readability.
dark_mode = st.sidebar.toggle("🌙 Dark mode", value=False)
plotly_template = "plotly_dark" if dark_mode else "plotly_white"

if dark_mode:
    theme = {
        "page": "#101827", "sidebar": "#172337", "surface": "#1d2b40",
        "surface2": "#24364f", "text": "#f3f6fc", "muted": "#c0ccdc",
        "border": "#354963", "hero1": "#183b66", "hero2": "#49347d",
        "hero3": "#14616a", "accent": "#38bdf8",
    }
else:
    theme = {
        "page": "#f4f7fb", "sidebar": "#ffffff", "surface": "#ffffff",
        "surface2": "#edf3fa", "text": "#172033", "muted": "#526178",
        "border": "#d9e2ef", "hero1": "#dceafe", "hero2": "#eee7ff",
        "hero3": "#d9f5f1", "accent": "#2563eb",
    }

# ---------------------------------------------------------
# Custom dashboard styling
# ---------------------------------------------------------
st.markdown(
    f"""
    <style>
    :root {{
        --page: {theme['page']};
        --sidebar: {theme['sidebar']};
        --surface: {theme['surface']};
        --text: {theme['text']};
        --muted: {theme['muted']};
        --border: {theme['border']};
    }}
    .stApp {{ background: var(--page); color: var(--text); }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stSidebar"] {{
        background: var(--sidebar);
        border-right: 1px solid var(--border);
    }}
    [data-testid="stSidebar"] * {{ color: var(--text); }}
    .stApp p, .stApp label, .stApp li,
    .stApp [data-testid="stMarkdownContainer"] {{ color: var(--text); }}
    .stApp [data-testid="stCaptionContainer"] {{ color: var(--muted) !important; }}
    h1, h2, h3, h4, h5, h6 {{ color: var(--text) !important; }}
    [data-testid="stWidgetLabel"] p {{ color: var(--text) !important; font-weight: 600; }}
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div {{
        background: var(--surface) !important;
        border-color: var(--border) !important;
    }}
    input, textarea {{ color: var(--text) !important; }}
    .hero {{
        padding: 1.7rem 1.9rem;
        border-radius: 20px;
        background: linear-gradient(115deg, {theme['hero1']}, {theme['hero2']}, {theme['hero3']});
        border: 1px solid var(--border);
        margin: .4rem 0 1.35rem 0;
        box-shadow: 0 10px 30px rgba(30, 64, 110, .10);
    }}
    .hero h1 {{ color: {'#ffffff' if dark_mode else '#14213d'} !important; margin: 0; font-size: 2.35rem; font-weight: 800; }}
    .hero p {{ color: {'#e5efff' if dark_mode else '#344765'} !important; margin: .45rem 0 0; font-size: 1.02rem; }}
    .section-kicker {{
        color: {'#e5efff' if dark_mode else '#344765'};
        font-size: .76rem; font-weight: 800; letter-spacing: .12em;
        margin-bottom: .3rem;
    }}
    .kpi {{
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 16px; padding: 17px 18px; min-height: 112px;
        box-shadow: 0 5px 18px rgba(30, 50, 80, .06);
    }}
    .kpi-label {{ color: var(--muted) !important; font-size: .78rem; font-weight: 700; letter-spacing: .06em; }}
    .kpi-value {{ color: var(--text) !important; font-size: 1.75rem; font-weight: 800; margin-top: .35rem; }}
    div.stButton > button, div.stDownloadButton > button {{
        border-radius: 10px; font-weight: 650; border: 1px solid var(--border);
    }}
    div.stButton > button[kind="primary"] {{ background: #2563eb; color: white; border: none; }}
    [data-testid="stDataFrame"] {{ border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
    hr {{ border-color: var(--border); }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------
@st.cache_data
def get_data():
    return load_jobs()


df = get_data()

# Create/update the SQLite table from the cleaned CSV data.
initialize_database(df)


# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------
st.sidebar.title("📊 SkillScope AI")
st.sidebar.caption("Job Market Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Skill Demand",
        "Salary & Locations",
        "Job Explorer",
        "AI Job Analyzer",
        "Ask Your Data",
        "Career Skill Gap",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Dataset: 700 synthetic demonstration job postings")
st.sidebar.caption("AI features require an API key. Analytics works without one.")


# ---------------------------------------------------------
# Main page heading
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="section-kicker">JOB MARKET INTELLIGENCE PLATFORM</div>
        <h1>SkillScope AI</h1>
        <p>Turn job-market data into career intelligence.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Filter options
# ---------------------------------------------------------
options = {
    "roles": ["All"] + sorted(df["job_title"].dropna().unique().tolist()),
    "locations": ["All"] + sorted(df["location"].dropna().unique().tolist()),
    "levels": ["All"] + sorted(df["experience_level"].dropna().unique().tolist()),
}


# ---------------------------------------------------------
# Global filters
# ---------------------------------------------------------
if page in [
    "Overview",
    "Skill Demand",
    "Salary & Locations",
    "Job Explorer",
]:
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        selected_role = st.selectbox(
            "Job role",
            options["roles"],
            key="global_role",
        )

    with filter_col2:
        selected_location = st.selectbox(
            "Location",
            options["locations"],
            key="global_location",
        )

    with filter_col3:
        selected_level = st.selectbox(
            "Experience level",
            options["levels"],
            key="global_level",
        )

    view = filtered_jobs(
        selected_role,
        selected_location,
        selected_level,
    )

else:
    selected_role = "All"
    selected_location = "All"
    selected_level = "All"
    view = df.copy()


# IMPORTANT:
# SQLite returns dates as strings. Convert them to Pandas datetime
# values before using .dt or sorting by date.
if "posted_date" in view.columns:
    view["posted_date"] = pd.to_datetime(
        view["posted_date"],
        errors="coerce",
    )


# ---------------------------------------------------------
# PAGE 1: OVERVIEW
# ---------------------------------------------------------
if page == "Overview":

    k = {
        "jobs": len(view),
        "companies": view["company"].nunique(),
        "locations": view["location"].nunique(),
        "avg_salary": (
            view["salary_avg_lpa"].mean()
            if len(view) and view["salary_avg_lpa"].notna().any()
            else 0
        ),
        "remote_share": (
            view["remote_option"].eq("Remote").mean() * 100
            if len(view)
            else 0
        ),
    }

    cols = st.columns(5)

    cards = [
        ("JOB POSTINGS", f"{k['jobs']:,}"),
        ("COMPANIES", f"{k['companies']:,}"),
        ("LOCATIONS", f"{k['locations']:,}"),
        ("AVG. SALARY", f"₹{k['avg_salary']:.1f} LPA"),
        ("REMOTE JOBS", f"{k['remote_share']:.1f}%"),
    ]

    for col, (label, value) in zip(cols, cards):
        col.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    left, right = st.columns(2)

    with left:
        st.subheader("Most demanded skills")

        sk = skill_comparison(selected_role)

        if not sk.empty:
            fig = px.bar(
                sk.head(10).sort_values("job_count"),
                x="job_count",
                y="skill",
                orientation="h",
                color="job_count",
                color_continuous_scale="Teal",
            )

            fig.update_layout(
                template=plotly_template,
                height=390,
                coloraxis_showscale=False,
            )

            st.plotly_chart(fig, width="stretch")

        else:
            st.info("No skill data is available for this selection.")

    with right:
        st.subheader("Job postings by experience")

        exp = (
            view.groupby("experience_level", as_index=False)
            .size()
            .rename(columns={"size": "postings"})
        )

        if not exp.empty:
            fig = px.pie(
                exp,
                names="experience_level",
                values="postings",
                hole=0.55,
            )

            fig.update_layout(
                template=plotly_template,
                height=390,
            )

            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No experience-level data is available.")

    # Monthly hiring trend
    st.subheader("Hiring trend by month")

    trend_data = view.dropna(subset=["posted_date"]).copy()

    if not trend_data.empty:
        trend_data["month"] = (
            trend_data["posted_date"]
            .dt.to_period("M")
            .astype(str)
        )

        trend = (
            trend_data.groupby("month", as_index=False)
            .size()
            .rename(columns={"size": "postings"})
        )

        fig = px.line(
            trend,
            x="month",
            y="postings",
            markers=True,
        )

        fig.update_layout(
            template=plotly_template,
            height=320,
            xaxis_title="Month",
            yaxis_title="Number of postings",
        )

        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No valid posting dates are available for the hiring trend.")

    # Latest job records
    st.subheader("Latest job records")

    latest_columns = [
        "company",
        "job_title",
        "location",
        "experience_level",
        "salary_min_lpa",
        "salary_max_lpa",
        "posted_date",
    ]

    latest_jobs = (
        view[latest_columns]
        .sort_values("posted_date", ascending=False)
        .head(15)
    )

    st.dataframe(
        latest_jobs,
        width="stretch",
        hide_index=True,
    )


# ---------------------------------------------------------
# PAGE 2: SKILL DEMAND
# ---------------------------------------------------------
elif page == "Skill Demand":

    st.subheader("Technical skill demand analysis")

    st.caption(
        "Demand percentage = postings mentioning the skill "
        "÷ filtered postings × 100."
    )

    sk = skill_comparison(selected_role)

    if sk.empty:
        st.info("No records match the selected filters.")

    else:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                sk.head(20),
                x="skill",
                y="job_count",
                color="demand_percent",
                color_continuous_scale="Teal",
                title="Number of postings by skill",
            )

            fig.update_layout(
                template=plotly_template,
                xaxis_tickangle=-35,
            )

            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.treemap(
                sk.head(20),
                path=["skill"],
                values="job_count",
                color="demand_percent",
                color_continuous_scale="Viridis",
                title="Skill demand distribution",
            )

            fig.update_layout(template=plotly_template)

            st.plotly_chart(fig, width="stretch")

        st.dataframe(
            sk,
            width="stretch",
            hide_index=True,
        )

        st.download_button(
            "Download skill analysis CSV",
            sk.to_csv(index=False),
            "skill_demand.csv",
            "text/csv",
        )


# ---------------------------------------------------------
# PAGE 3: SALARY AND LOCATIONS
# ---------------------------------------------------------
elif page == "Salary & Locations":

    st.subheader("Salary and geographic analysis")

    left, right = st.columns(2)

    with left:
        salary = (
            view.groupby("job_title", as_index=False)["salary_avg_lpa"]
            .mean()
            .sort_values("salary_avg_lpa", ascending=False)
        )

        if not salary.empty:
            fig = px.bar(
                salary,
                x="job_title",
                y="salary_avg_lpa",
                title="Average salary by role",
                color="salary_avg_lpa",
            )

            fig.update_layout(
                template=plotly_template,
                xaxis_tickangle=-35,
                yaxis_title="Average salary (LPA)",
            )

            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No salary data is available.")

    with right:
        loc = (
            view.groupby("location", as_index=False)
            .size()
            .rename(columns={"size": "postings"})
            .sort_values("postings", ascending=False)
        )

        if not loc.empty:
            fig = px.bar(
                loc,
                x="postings",
                y="location",
                orientation="h",
                title="Job postings by location",
            )

            fig.update_layout(template=plotly_template)

            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No location data is available.")

    st.subheader("Salary details")

    if not view.empty:
        salary_table = (
            view.groupby("job_title")
            .agg(
                postings=("job_id", "count"),
                min_salary=("salary_min_lpa", "mean"),
                max_salary=("salary_max_lpa", "mean"),
                average_salary=("salary_avg_lpa", "mean"),
            )
            .round(2)
            .reset_index()
        )

        st.dataframe(
            salary_table,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No records match the selected filters.")


# ---------------------------------------------------------
# PAGE 4: JOB EXPLORER
# ---------------------------------------------------------
elif page == "Job Explorer":

    st.subheader("Explore job postings")

    search = st.text_input(
        "Search company, title, skills or description"
    )

    if search:
        mask = (
            view.astype(str)
            .apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    na=False,
                    regex=False,
                )
            )
            .any(axis=1)
        )

        view = view[mask]

    st.write(f"**{len(view):,}** matching records")

    explorer_columns = [
        "job_id",
        "company",
        "job_title",
        "location",
        "experience_level",
        "employment_type",
        "salary_min_lpa",
        "salary_max_lpa",
        "skills",
        "posted_date",
    ]

    explorer_data = view[explorer_columns].sort_values(
        "posted_date",
        ascending=False,
    )

    st.dataframe(
        explorer_data,
        width="stretch",
        hide_index=True,
    )

    st.download_button(
        "Download filtered jobs",
        view.to_csv(index=False),
        "filtered_jobs.csv",
        "text/csv",
    )


# ---------------------------------------------------------
# PAGE 5: AI JOB ANALYZER
# ---------------------------------------------------------
elif page == "AI Job Analyzer":

    st.subheader("AI Job Description Analyzer")

    st.write(
        "Paste a job description. Generative AI will extract "
        "skills, responsibilities and requirements."
    )

    description = st.text_area(
        "Job description",
        height=230,
        placeholder="Paste the complete job description here...",
    )

    if st.button("Analyze with Generative AI", type="primary"):

        if len(description.strip()) < 40:
            st.warning("Please enter a longer job description.")

        else:
            with st.spinner("Analyzing job description..."):
                result = analyze_job_description(description)

            st.markdown(result)

    if not ai_is_configured():
        st.info(
            "Add OPENAI_API_KEY to your .env file to enable this feature."
        )


# ---------------------------------------------------------
# PAGE 6: ASK YOUR DATA
# ---------------------------------------------------------
elif page == "Ask Your Data":

    st.subheader("Ask your job-market data")

    st.write(
        "Ask a question in normal language. The AI receives a "
        "calculated dataset summary, not unrestricted database access."
    )

    role = st.selectbox(
        "Focus on job role",
        options["roles"],
        key="ask_role",
    )

    sample = filtered_jobs(role=role)
    sk = skill_comparison(role)

    average_salary = (
        sample["salary_avg_lpa"].mean()
        if not sample.empty
        else 0
    )

    metrics = (
        f"Filtered posting count: {len(sample)}\n"
        f"Roles: {sample['job_title'].value_counts().to_dict()}\n"
        f"Experience distribution: "
        f"{sample['experience_level'].value_counts().to_dict()}\n"
        f"Location distribution: "
        f"{sample['location'].value_counts().head(10).to_dict()}\n"
        f"Average salary LPA: {average_salary:.2f}\n"
        f"Top skills (skill, job_count, demand_percent): "
        f"{sk.head(20).to_dict('records')}"
    )

    question = st.text_input(
        "Your question",
        placeholder="Which skills are most common for Data Analyst jobs?",
    )

    if st.button("Ask SkillScope AI", type="primary"):

        if question.strip():

            with st.spinner("Preparing a data-backed answer..."):
                answer = ask_about_data(question, metrics)

            st.markdown(answer)

        else:
            st.warning("Enter a question first.")

    with st.expander("See the data context provided to AI"):
        st.code(metrics)


# ---------------------------------------------------------
# PAGE 7: CAREER SKILL GAP
# ---------------------------------------------------------
elif page == "Career Skill Gap":

    st.subheader("Career Skill Gap Assistant")

    st.write(
        "Compare skills you report having with skills found "
        "in job postings for a selected role."
    )

    role = st.selectbox(
        "Target job role",
        options["roles"],
        key="gap_role",
    )

    user_skills = st.text_input(
        "Your current skills (comma-separated)",
        placeholder="Python, Excel, SQL",
    )

    sk = skill_comparison(role)

    if st.button("Analyze my skill gap", type="primary"):

        if not user_skills.strip():
            st.warning("Enter at least one skill.")

        elif sk.empty:
            st.warning("No job postings available for this role.")

        else:
            demand = sk.head(25).to_string(index=False)

            with st.spinner(
                "Comparing your skills with job-market demand..."
            ):
                result = career_skill_gap(
                    role,
                    user_skills,
                    demand,
                )

            st.markdown(result)

    if not sk.empty:
        st.subheader("Observed skill demand for this role")

        st.dataframe(
            sk.head(15),
            width="stretch",
            hide_index=True,
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "SkillScope AI | Demonstration dataset contains synthetic "
    "records. It is not a live measure of the complete job market."
)
