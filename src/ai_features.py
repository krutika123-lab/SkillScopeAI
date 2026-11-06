import os
import json
from dotenv import load_dotenv

load_dotenv()

def _client():
    """Create the API client only when a key is configured."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    from openai import OpenAI
    return OpenAI(api_key=key)

def ai_is_configured():
    return bool(os.getenv("OPENAI_API_KEY"))

def _ask(system_prompt, user_prompt):
    client = _client()
    if client is None:
        return ("AI is not configured. Copy .env.example to .env, add your API key, "
                "then restart Streamlit. The analytics dashboard works without AI.")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content or "The AI returned an empty response."
    except Exception as exc:
        return f"AI request failed: {exc}"

def analyze_job_description(description):
    system = """You are a careful job-description information extractor.
Return valid JSON only, with keys: job_title, technical_skills (array),
professional_skills (array), responsibilities (array), experience_requirement,
education_requirement, short_summary. Do not invent missing facts. Use
'Not specified' when the text does not provide an answer."""
    return _ask(system, description)

def explain_analytics(metrics_text):
    system = """You are a data analytics explainer. Explain only the supplied
metrics. Do not invent percentages, counts, salaries, companies or trends.
Mention that findings describe the supplied dataset, not the entire job market."""
    return _ask(system, metrics_text)

def ask_about_data(question, metrics_text):
    system = """You are SkillScope AI, a job-market analytics assistant.
Answer using only the provided dataset summary. If the answer is not present,
say what information is missing. Never invent statistics or claim the dataset
represents every job in the market."""
    prompt = f"DATA SUMMARY:\n{metrics_text}\n\nUSER QUESTION:\n{question}"
    return _ask(system, prompt)

def career_skill_gap(target_role, user_skills, demand_text):
    system = """You are a career skills explainer. Compare the user's self-reported
skills with the supplied job-posting skill-demand summary. Do not judge actual
competence or predict hiring outcomes. Distinguish observed demand from advice."""
    prompt = (f"Target role: {target_role}\nUser-reported skills: {user_skills}\n"
              f"Observed job-posting skill demand:\n{demand_text}\n"
              "Identify skills already listed, frequently demanded skills not listed, "
              "and a sensible learning order. State that this is dataset-based guidance.")
    return _ask(system, prompt)
