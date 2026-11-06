# SkillScope AI

AI-powered job-market intelligence and career analytics dashboard.

## Features
- Job market KPIs and interactive dashboard
- Skill demand and salary analysis
- Location, experience and company analysis
- Searchable job explorer and CSV downloads
- Generative AI job-description analyzer
- Natural-language questions grounded in calculated dataset summaries
- Career skill-gap comparison

## Technology
Python, Pandas, NumPy, SQLite/SQL, Streamlit, Plotly and an optional OpenAI-compatible API integration.

## Dataset note
`data/job_postings.csv` contains 700 **synthetic demonstration records** generated for learning and testing. Company names are used as sample labels; records are not actual job vacancies. Do not describe the figures as live market statistics. Replace the data with licensed/public data or a permitted API before making real-world claims.

## Run in VS Code (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```
The dashboard and analytics work without an AI key. To enable AI, open `.env`, add your API key to `OPENAI_API_KEY`, save, and restart Streamlit. Keep `.env` private and never commit it.

## Database
The app creates `data/skillscope.db` and refreshes the `jobs` table from the cleaned CSV at startup. SQL queries are in `src/analytics.py` and `src/database.py`.

## NumPy and Pandas
`src/data_processing.py` uses Pandas for loading, cleaning, date parsing, deduplication and skill-list preparation. NumPy is used for numerical summaries such as mean salary. Analytics functions use SQL for grouped counts and salary summaries.

## AI use
1. Extract skills and requirements from pasted job descriptions.
2. Explain metrics calculated by Python/SQL.
3. Answer natural-language questions using a limited calculated summary.
4. Explain a comparison between user-reported skills and observed role demand.

The AI does not calculate official job-market statistics, predict hiring outcomes or train an ML model. Validate outputs before relying on them.

## Suggested next steps
- Add a real, permitted job-postings source.
- Add data provenance and collection timestamps.
- Add tests for data cleaning and skill extraction.
- Add authentication only if the project needs multiple users.
- Consider PostgreSQL for a hosted deployment.
