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
=======
# 🚀 SkillScope AI – Job Market Intelligence & Career Analytics Platform

**SkillScope AI** is an interactive, AI-powered Data Analytics platform designed to analyze job market trends, identify in-demand technical skills, explore salary patterns, and help individuals understand career skill gaps.

The platform combines **Python, NumPy, Pandas, SQL, Streamlit, Plotly, and Generative AI** to transform job posting data into meaningful insights and career recommendations.

It provides an interactive dashboard where users can explore job opportunities, analyze industry requirements, compare salaries, and understand which skills are valuable for different career roles.

---

## 📌 Project Overview

In today's competitive job market, students and job seekers often find it difficult to understand which technical skills are in demand, what companies expect from candidates, and how salary trends vary across different roles and experience levels.

SkillScope AI addresses this problem through data analytics and Generative AI.

The platform processes job posting datasets and presents useful insights through interactive charts, visualizations, filters, and AI-assisted analysis.

### 🎯 Project Objectives

- Analyze job market trends using structured datasets.
- Identify the most demanded technical and professional skills.
- Understand salary distributions across different job roles.
- Compare job opportunities across locations and experience levels.
- Analyze job descriptions and extract important requirements using Generative AI.
- Compare existing skills with market demand to identify skill gaps.
- Provide data-driven career insights through an interactive dashboard.

---

## ✨ Key Features

### 1. 📊 Interactive Analytics Dashboard

Provides an overview of the job market through interactive visualizations and key performance indicators.

Features include:
- Total job postings.
- Number of companies.
- Number of job locations.
- Average salary.
- Remote job percentage.
- Job distribution by experience level.
- Monthly job posting trends.
- Most demanded technical skills.

### 2. 💻 Skill Demand Analysis

Analyzes the frequency of different technical skills appearing in job postings.

Features include:
- Identification of popular technical skills.
- Skill demand comparison.
- Job posting counts for individual skills.
- Skill demand percentage.
- Interactive bar charts and treemap visualizations.

### 3. 💰 Salary & Location Analytics

Provides insights into salary patterns and geographical job distribution.

Features include:
- Average salary comparison across job roles.
- Salary distribution by experience.
- Job opportunities across locations.
- Comparison of salary ranges.
- Location-based job market analysis.

### 4. 🔎 Job Explorer

Allows users to explore and filter job posting records.

Features include:
- Search by company name.
- Search by job title.
- Search by skills and descriptions.
- Filter by job role.
- Filter by location.
- Filter by experience level.
- Download filtered job records as CSV.

### 5. 🤖 AI Job Description Analyzer

Uses Generative AI to interpret job descriptions and extract important information.

Purpose:
- Identify technical skills.
- Identify soft skills.
- Extract job responsibilities.
- Understand experience requirements.
- Identify important job-related keywords.
- Summarize employer expectations.

### 6. 💬 Ask Your Data

Provides a natural-language interface for understanding job market data.

Users can ask questions such as:

- Which technical skills are most demanded for Business Analyst jobs?
- How is Python relevant in today's job market?
- What is the relationship between salary and experience?
- Which skills should a fresher learn to become a Data Analyst?
- What are the major hiring trends in the available dataset?

Generative AI uses calculated dataset summaries to produce understandable explanations and insights.

### 7. 🎯 Career Skill Gap Analysis

Helps users compare their current skills with the skills required for a selected job role.

Features include:
- Enter existing technical skills.
- Select a target job role.
- Compare skills with observed job market demand.
- Identify missing skills.
- Prioritize skills to learn.
- Generate career-oriented learning recommendations.

---

## 🧠 How Generative AI Is Used

Generative AI is integrated into SkillScope AI to make the analytics platform more interactive and useful.

Instead of only displaying charts and numerical results, the AI features help interpret information and generate human-readable explanations.

| AI Feature | Purpose |
|---|---|
| Ask Your Data | Answers natural-language questions using calculated dataset summaries. |
| AI Job Analyzer | Extracts skills, responsibilities and requirements from job descriptions. |
| Career Skill Gap | Compares candidate skills with job market demand and generates learning recommendations. |

### AI Workflow

1. Job posting data is loaded from CSV files.
2. Python and Pandas clean and process the data.
3. NumPy supports numerical operations.
4. SQL supports structured data storage and querying.
5. Analytics functions calculate job market metrics.
6. Relevant summaries are passed to the Generative AI component.
7. The AI generates explanations and recommendations.
8. Results are presented through the Streamlit dashboard.

**Important:** The project supports a demonstration mode with sample responses when live API access is unavailable. Live Generative AI responses require a configured API key and applicable API access.

---

## 🛠️ Technologies Used

| Technology | Application |
|---|---|
| Python | Core programming and application logic |
| NumPy | Numerical computations |
| Pandas | Data cleaning, processing and analysis |
| SQL / SQLite | Structured data storage and queries |
| Streamlit | Interactive dashboard development |
| Plotly | Interactive charts and visualizations |
| OpenAI API | Generative AI integration |
| CSV | Dataset storage and input |
| Git & GitHub | Version control and project management |
| VS Code | Development environment |

---

## 📂 Project Structure

```text
SkillScope_AI/
│
├── app.py
│
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── job_postings.csv
│
├── src/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── database.py
│   ├── analytics.py
│   └── ai_features.py
│
└── database/
    └── SQLite database (if configured)
```

### File Descriptions

- `app.py` – Main Streamlit application and dashboard.
- `data_processing.py` – Loads, cleans and processes job posting data.
- `database.py` – Handles SQLite database initialization and operations.
- `analytics.py` – Performs analytical calculations and skill comparisons.
- `ai_features.py` – Implements Generative AI functionality.
- `job_postings.csv` – Dataset containing job posting information.
- `requirements.txt` – Python project dependencies.
- `.env.example` – Template for environment variables.
- `.gitignore` – Prevents sensitive and unnecessary files from being uploaded.

---

## ⚙️ Installation & Setup

Follow these steps to run SkillScope AI locally.

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/SkillScope_AI.git
```

### Step 2: Navigate to the project directory

```bash
cd SkillScope_AI
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Configure environment variables

Create a `.env` file in the root project directory.

Copy the contents of `.env.example` and configure your own API key if you want to use live Generative AI features.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

Do not upload your `.env` file or API key to GitHub.

### Step 6: Run the application

```bash
python -m streamlit run app.py
```

### Step 7: Open the dashboard

Open your browser and visit:

```text
http://localhost:8501
```

The SkillScope AI dashboard should now be available locally.

---

## 📈 Dashboard Modules

| Module | Functionality |
|---|---|
| Overview | Job market summary and KPIs |
| Skill Demand | Technical skill demand analysis |
| Salary & Locations | Salary and geographical comparisons |
| Job Explorer | Search and filter job records |
| AI Job Analyzer | Job description analysis |
| Ask Your Data | Natural-language data insights |
| Career Skill Gap | Skill comparison and career recommendations |

---

## 🔐 Data & Security

- API credentials are stored in environment variables.
- Sensitive configuration files are excluded through `.gitignore`.
- AI features should use only the relevant data required for analysis.
- The AI component receives calculated dataset summaries rather than unrestricted database access.

**Dataset Note:** The included job posting dataset is synthetic demonstration data. The analytical results are intended for project demonstration and learning purposes and should not be interpreted as verified live job market statistics.

---

## 🚀 Future Enhancements

Potential improvements for future versions include:

- Integration with verified real-time job market data sources.
- Automated job data collection through permitted APIs.
- Advanced company-wise skill demand comparison.
- More detailed salary trend analysis.
- Interactive skill demand heatmaps.
- Downloadable AI-generated career reports.
- Personalized career learning roadmaps.
- Cloud deployment and application hosting.
- User authentication and personalized dashboards.
- Scheduled data refresh and automated reporting.

---

## 🎓 Learning Outcomes

Through this project, the following concepts are demonstrated:

- Python programming and modular development.
- Data cleaning and preprocessing.
- Numerical analysis using NumPy.
- Data manipulation using Pandas.
- SQL and relational database concepts.
- Exploratory Data Analysis (EDA).
- Data visualization and dashboard development.
- Generative AI integration.
- Natural-language interaction with analytical data.
- API integration and environment configuration.
- Git and GitHub project management.

---

## 👩‍💻 Project Information

**Project Name:** SkillScope AI

**Project Domain:** Data Analytics and Generative AI

**Project Type:** Interactive Job Market Intelligence Platform

**Primary Language:** Python

**Dashboard Framework:** Streamlit

**AI Integration:** OpenAI API (optional live mode)

**Database:** SQLite

---

## ⭐ Acknowledgement

SkillScope AI is developed as a learning and portfolio project to explore the practical application of Data Analytics and Generative AI in career and job market intelligence.

If you find this project interesting, consider giving the repository a ⭐.

---

**SkillScope AI – Turning Job Market Data into Career Intelligence.**
>>>>>>> 8752fffd6c295de6fa5dc18ba3a93a7d50ca644e
