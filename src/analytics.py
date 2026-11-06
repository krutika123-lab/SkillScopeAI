import pandas as pd
from .database import query_df

def role_summary(role=None):
    sql = """SELECT job_title, COUNT(*) AS job_count,
             ROUND(AVG(salary_avg_lpa),2) AS avg_salary_lpa
             FROM jobs"""
    params = ()
    if role and role != "All":
        sql += " WHERE job_title = ?"
        params = (role,)
    sql += " GROUP BY job_title ORDER BY job_count DESC"
    return query_df(sql, params)

def location_summary(role="All"):
    sql = "SELECT location, COUNT(*) AS job_count FROM jobs"
    params = ()
    if role != "All":
        sql += " WHERE job_title = ?"
        params = (role,)
    sql += " GROUP BY location ORDER BY job_count DESC"
    return query_df(sql, params)

def salary_by_role():
    return query_df("""SELECT job_title,
        ROUND(AVG(salary_min_lpa),2) AS min_avg_lpa,
        ROUND(AVG(salary_max_lpa),2) AS max_avg_lpa,
        ROUND(AVG(salary_avg_lpa),2) AS avg_lpa,
        COUNT(*) AS postings
        FROM jobs GROUP BY job_title ORDER BY avg_lpa DESC""")

def monthly_trend():
    return query_df("""SELECT substr(posted_date,1,7) AS month,
        COUNT(*) AS postings FROM jobs
        GROUP BY month ORDER BY month""")

def experience_summary():
    return query_df("""SELECT experience_level, COUNT(*) AS postings,
        ROUND(AVG(salary_avg_lpa),2) AS avg_salary_lpa
        FROM jobs GROUP BY experience_level
        ORDER BY postings DESC""")

def top_companies(role="All"):
    sql = "SELECT company, COUNT(*) AS postings FROM jobs"
    params = ()
    if role != "All":
        sql += " WHERE job_title = ?"
        params = (role,)
    sql += " GROUP BY company ORDER BY postings DESC LIMIT 12"
    return query_df(sql, params)

def filtered_jobs(role="All", location="All", level="All"):
    conditions, params = [], []
    if role != "All":
        conditions.append("job_title = ?"); params.append(role)
    if location != "All":
        conditions.append("location = ?"); params.append(location)
    if level != "All":
        conditions.append("experience_level = ?"); params.append(level)
    sql = "SELECT * FROM jobs"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY posted_date DESC"
    return query_df(sql, tuple(params))

def skill_comparison(role="All"):
    """Calculate skill counts from stored comma-separated skill values."""
    jobs = filtered_jobs(role=role)
    counts = {}
    for _, row in jobs.iterrows():
        for skill in str(row["skills"]).split(","):
            skill = skill.strip()
            if skill:
                counts[skill] = counts.get(skill, 0) + 1
    out = pd.DataFrame([{"skill": k, "job_count": v} for k,v in counts.items()])
    if out.empty:
        return out
    out["demand_percent"] = (out["job_count"] / max(len(jobs),1) * 100).round(1)
    return out.sort_values("job_count", ascending=False)
