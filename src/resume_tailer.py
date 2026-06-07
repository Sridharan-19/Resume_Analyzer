"""
Resume tailoring engine for specific job roles.
Intelligently customizes resume based on job description and target role.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import os
import logging

log = logging.getLogger(__name__)

# Role-specific keyword priorities
ROLE_KEYWORDS = {
    "Data Scientist": [
        "machine learning", "statistical analysis", "data analysis", "pandas", "numpy",
        "scikit-learn", "experimentation", "a/b testing", "metrics", "insights",
        "sql", "python", "tableau", "power bi", "big data", "hadoop", "spark"
    ],
    "Gen AI Engineer": [
        "generative ai", "llm", "large language model", "gpt", "claude", "gemini",
        "rag", "retrieval augmented generation", "prompt engineering", "langchain",
        "transformers", "hugging face", "embedding", "vector database", "agentic ai",
        "openai api", "fine-tuning", "lora", "semantic search"
    ],
    "AIML Engineer": [
        "artificial intelligence", "machine learning", "deep learning", "neural networks",
        "pytorch", "tensorflow", "computer vision", "nlp", "transformer", "yolo",
        "cnn", "rnn", "gan", "reinforcement learning", "model deployment", "mlops"
    ],
    "ML Engineer": [
        "machine learning", "model development", "feature engineering", "model training",
        "scikit-learn", "xgboost", "random forest", "classification", "regression",
        "clustering", "recommendation systems", "time series forecasting", "ensemble methods",
        "model evaluation", "cross-validation", "hyperparameter tuning"
    ],
}

# Highlight sections from resume that are most relevant
ROLE_HIGHLIGHT_SECTIONS = {
    "Data Scientist": [
        "Cross-Selling & White Space Analysis",
        "Credit Risk Analytics",
        "Demand Forecasting",
        "Product Recommendation System"
    ],
    "Gen AI Engineer": [
        "Medical Records Review Management",
        "Agentic AI",
        "Multilingual RAG Chatbot"
    ],
    "AIML Engineer": [
        "Computer Vision",
        "Deep Learning",
        "Medical NER pipelines",
        "Document Classification"
    ],
    "ML Engineer": [
        "Demand Forecasting",
        "Machine Learning",
        "Recommendation System",
        "Predictive models"
    ],
}


def _extract_top_keywords(text, top_n=10):
    """Extract top keywords from job description using TF-IDF."""
    try:
        vec = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=3000,
            lowercase=True
        )
        X = vec.fit_transform([text])
        features = vec.get_feature_names_out()
        idf_scores = vec.idf_
        
        pairs = list(zip(features, idf_scores))
        pairs.sort(key=lambda x: -x[1])
        return [p[0] for p in pairs[:top_n]]
    except Exception as e:
        log.warning(f"Error extracting keywords: {e}")
        return []


def _extract_job_role(job_title: str) -> str:
    """Infer the role category from job title."""
    title_lower = job_title.lower()
    
    if "gen" in title_lower and "ai" in title_lower:
        return "Gen AI Engineer"
    elif "generative" in title_lower or "llm" in title_lower:
        return "Gen AI Engineer"
    elif "aiml" in title_lower or "ai/ml" in title_lower:
        return "AIML Engineer"
    elif ("ml" in title_lower or "machine learning" in title_lower) and "engineer" in title_lower:
        return "ML Engineer"
    elif "data scientist" in title_lower:
        return "Data Scientist"
    else:
        return "ML Engineer"  # Default


def _get_relevant_skills(resume_text: str, role: str) -> list:
    """Extract skills from resume relevant to the role."""
    role_skills = ROLE_KEYWORDS.get(role, [])
    found_skills = []
    
    resume_lower = resume_text.lower()
    for skill in role_skills:
        if skill.lower() in resume_lower:
            found_skills.append(skill)
    
    return found_skills[:15]  # Top 15 relevant skills


def tailor_resume_for_job(resume_path, job):
    """
    Create a tailored resume for a specific job posting.
    
    Args:
        resume_path: Path to base resume file
        job: Job dictionary with title, description, etc.
    
    Returns:
        Path to tailored resume file
    """
    with open(resume_path, 'r', encoding='utf-8') as f:
        resume = f.read()
    
    job_title = job.get('title', 'Unknown')
    jd = job.get('description', '')
    company = job.get('company', 'Company')
    
    # Infer role type
    role_type = _extract_job_role(job_title)
    
    # Extract keywords from job description
    jd_keywords = _extract_top_keywords(jd, top_n=12)
    
    # Get role-specific keywords that are missing from resume
    role_keywords = ROLE_KEYWORDS.get(role_type, [])
    missing_keywords = [k for k in role_keywords if k.lower() not in resume.lower()][:8]
    
    # Get relevant skills from resume for this role
    relevant_skills = _get_relevant_skills(resume, role_type)
    
    # Create tailored resume
    tailored = resume
    
    # Add role-specific tailoring section
    tailoring_section = f"\n\n{'='*80}\nTAILORED FOR: {job_title} at {company}\n{'='*80}\n"
    tailoring_section += f"\nROLE TYPE: {role_type}\n\n"
    
    # Add matching skills section
    if relevant_skills:
        tailoring_section += f"RELEVANT SKILLS FOR THIS ROLE:\n"
        tailoring_section += f"{', '.join(relevant_skills)}\n\n"
    
    # Add key requirements matched
    tailoring_section += f"KEY REQUIREMENTS MATCHED:\n"
    matched_jd_keywords = [k for k in jd_keywords if k.lower() in resume.lower()]
    if matched_jd_keywords:
        tailoring_section += f"✓ {', '.join(matched_jd_keywords[:8])}\n\n"
    
    # Add missing keywords to highlight
    if missing_keywords:
        tailoring_section += f"ADDITIONAL EXPERTISE:\n"
        tailoring_section += f"Proficient in: {', '.join(missing_keywords)}\n\n"
    
    # Add role-specific accomplishment
    role_highlights = ROLE_HIGHLIGHT_SECTIONS.get(role_type, [])
    if role_highlights:
        tailoring_section += f"KEY PROJECT EXPERIENCE FOR THIS ROLE:\n"
        for highlight in role_highlights[:3]:
            tailoring_section += f"• {highlight}\n"
        tailoring_section += "\n"
    
    tailored += tailoring_section
    
    # Write to outputs
    out_dir = os.path.join(os.path.dirname(resume_path), 'tailored')
    os.makedirs(out_dir, exist_ok=True)
    
    # Create filename
    safe_title = job_title.replace(' ', '_').replace('/', '_')[:30]
    safe_company = company.replace(' ', '_')[:20]
    out_filename = f"tailored_{safe_company}_{safe_title}.txt"
    out_path = os.path.join(out_dir, out_filename)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(tailored)
    
    log.info(f"Tailored resume created: {out_path} (Role: {role_type})")
    return out_path

