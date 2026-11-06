from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "skillscope.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def initialize_database(df):
    """Create the jobs table and load the cleaned data."""
    with get_connection() as conn:
        df_to_save = df.drop(columns=["skills_list"], errors="ignore").copy()
        df_to_save["posted_date"] = df_to_save["posted_date"].astype(str)
        df_to_save.to_sql("jobs", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_role ON jobs(job_title)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location)")
        conn.commit()

def query_df(sql, params=()):
    with get_connection() as conn:
        return pd.read_sql_query(sql, conn, params=params)

def get_filter_options():
    return {
        "roles": query_df("SELECT DISTINCT job_title FROM jobs ORDER BY job_title")["job_title"].tolist(),
        "locations": query_df("SELECT DISTINCT location FROM jobs ORDER BY location")["location"].tolist(),
        "levels": query_df("SELECT DISTINCT experience_level FROM jobs ORDER BY experience_level")["experience_level"].tolist()
    }
