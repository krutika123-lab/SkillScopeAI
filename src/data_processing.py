from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "job_postings.csv"

def load_jobs():
    """Load, validate and clean the demonstration job-posting dataset."""
    df = pd.read_csv(DATA_FILE)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.drop_duplicates(subset=["job_id"]).copy()
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    for col in ["salary_min_lpa", "salary_max_lpa"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["company", "job_title", "location", "experience_level", "skills"]:
        df[col] = df[col].fillna("Not specified").astype(str).str.strip()
    df["salary_avg_lpa"] = df[["salary_min_lpa", "salary_max_lpa"]].mean(axis=1)
    df["skills_list"] = df["skills"].apply(
        lambda x: [s.strip() for s in str(x).split(",") if s.strip()]
    )
    df["month"] = df["posted_date"].dt.to_period("M").astype(str)
    return df

def skill_frequency(df):
    """Count distinct job postings that mention each skill."""
    exploded = df[["job_id", "skills_list"]].explode("skills_list")
    result = (exploded.dropna().groupby("skills_list")["job_id"]
              .nunique().sort_values(ascending=False).reset_index())
    result.columns = ["skill", "job_count"]
    result["demand_percent"] = (result["job_count"] / max(df["job_id"].nunique(), 1) * 100).round(1)
    return result

def kpi_summary(df):
    return {
        "jobs": int(df["job_id"].nunique()),
        "companies": int(df["company"].nunique()),
        "locations": int(df["location"].nunique()),
        "avg_salary": float(np.nanmean(df["salary_avg_lpa"])) if df["salary_avg_lpa"].notna().any() else 0,
        "remote_share": float((df["remote_option"] == "Remote").mean() * 100)
    }
