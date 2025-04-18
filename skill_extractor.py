import json
import os
import re
import spacy
from pathlib import Path
from fuzzywuzzy import fuzz, process

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Check if skill dictionary exists, if not create it
skill_dict_path = data_dir / "skill_dictionary.json"

# Default technical skill dictionary
DEFAULT_SKILL_DICT = {
    # Programming Languages
    "python": "python",
    "java": "java",
    "javascript": "javascript",
    "typescript": "typescript",
    "c++": "c++",
    "c#": "c#",
    "ruby": "ruby",
    "php": "php",
    "go": "go",
    "rust": "rust",
    "scala": "scala",
    "kotlin": "kotlin",
    "perl": "perl",
    "swift": "swift",
    "r": "r (programming language)",
    "matlab": "matlab",
    "bash": "bash",
    "powershell": "powershell",
    "html": "html",
    "css": "css",
    "xml": "xml",
    "json": "json",
    "yaml": "yaml",
    
    # Databases
    "sql": "sql",
    "mysql": "mysql",
    "postgresql": "postgresql",
    "postgres": "postgresql",
    "oracle": "oracle database",
    "mongodb": "mongodb",
    "cassandra": "cassandra",
    "redis": "redis",
    "dynamodb": "dynamodb",
    "sqlite": "sqlite",
    "mariadb": "mariadb",
    "neo4j": "neo4j",
    "elasticsearch": "elasticsearch",
    
    # Cloud & Infrastructure
    "aws": "aws",
    "amazon web services": "aws",
    "azure": "azure",
    "microsoft azure": "azure",
    "gcp": "gcp",
    "google cloud": "gcp",
    "terraform": "terraform",
    "kubernetes": "kubernetes",
    "k8s": "kubernetes",
    "docker": "docker",
    "jenkins": "jenkins",
    "ansible": "ansible",
    "puppet": "puppet",
    "chef": "chef",
    "vagrant": "vagrant",
    "github actions": "github actions",
    "gitlab ci": "gitlab ci",
    "circleci": "circleci",
    "travis ci": "travis ci",
    
    # Data Science & ML
    "machine learning": "machine learning",
    "ml": "machine learning",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "keras": "keras",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "pandas": "pandas",
    "numpy": "numpy",
    "scipy": "scipy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "jupyter": "jupyter",
    "deep learning": "deep learning",
    "nlp": "natural language processing",
    "natural language processing": "natural language processing",
    "computer vision": "computer vision",
    "data mining": "data mining",
    
    # BI & Analytics
    "tableau": "tableau",
    "power bi": "power bi",
    "looker": "looker",
    "qlik": "qlik",
    "excel": "excel",
    "powerpoint": "powerpoint",
    "word": "microsoft word",
    
    # Web Frameworks & Libraries
    "react": "react",
    "angular": "angular",
    "vue": "vue.js",
    "django": "django",
    "flask": "flask",
    "spring": "spring",
    "spring boot": "spring boot",
    "express": "express.js",
    "node": "node.js",
    "nodejs": "node.js",
    "jquery": "jquery",
    "bootstrap": "bootstrap",
    "tailwind": "tailwind css",
    "laravel": "laravel",
    "rails": "ruby on rails",
    "asp.net": "asp.net",
    "next.js": "next.js",
    "gatsby": "gatsby",
    
    # Mobile
    "android": "android",
    "ios": "ios",
    "react native": "react native",
    "flutter": "flutter",
    "swift": "swift",
    "kotlin": "kotlin",
    "xamarin": "xamarin",
    
    # DevOps & Tools
    "git": "git",
    "github": "github",
    "gitlab": "gitlab",
    "bitbucket": "bitbucket",
    "jira": "jira",
    "confluence": "confluence",
    "slack": "slack",
    "agile": "agile",
    "scrum": "scrum",
    "kanban": "kanban",
    "ci/cd": "ci/cd",
    "continuous integration": "continuous integration",
    "continuous deployment": "continuous deployment",
    "devops": "devops",
    
    # Testing
    "junit": "junit",
    "selenium": "selenium",
    "cypress": "cypress",
    "jest": "jest",
    "pytest": "pytest",
    "mocha": "mocha",
    "chai": "chai",
    "cucumber": "cucumber",
    "tdd": "test driven development",
    "test driven development": "test driven development",
    "bdd": "behavior driven development",
    "behavior driven development": "behavior driven development",
    
    # Soft Skills
    "communication": "communication",
    "teamwork": "teamwork",
    "problem solving": "problem solving",
    "leadership": "leadership",
    "time management": "time management",
    "critical thinking": "critical thinking",
    "creativity": "creativity",
    "decision making": "decision making",
    "project management": "project management",
    "presentation": "presentation skills",
    "analytical skills": "analytical skills",
    "attention to detail": "attention to detail",
    
    # Project Management
    "agile": "agile",
    "scrum": "scrum",
    "kanban": "kanban",
    "waterfall": "waterfall",
    "pmp": "pmp",
    "prince2": "prince2",
    "jira": "jira",
    "asana": "asana",
    "trello": "trello",
    "ms project": "microsoft project",
    "microsoft project": "microsoft project",
    
    # Other common tech
    "rest api": "rest api",
    "graphql": "graphql",
    "soap": "soap api",
    "microservices": "microservices",
    "serverless": "serverless",
    "saas": "saas",
    "paas": "paas",
    "iaas": "iaas",
    "oauth": "oauth",
    "jwt": "jwt",
    "sso": "single sign-on",
    "single sign-on": "single sign-on",
    "blockchain": "blockchain",
    "iot": "internet of things",
    "internet of things": "internet of things",
    "big data": "big data",
    "hadoop": "hadoop",
    "spark": "apache spark",
    "kafka": "apache kafka",
    "etl": "etl",
    "erp": "erp",
    "crm": "crm",
    "salesforce": "salesforce",
    "sap": "sap",
    "ui/ux": "ui/ux design",
    "user interface": "user interface design",
    "user experience": "user experience design",
    "figma": "figma",
    "sketch": "sketch",
    "adobe xd": "adobe xd",
    "photoshop": "adobe photoshop",
    "illustrator": "adobe illustrator",
}

# Write default skill dictionary if it doesn't exist
if not skill_dict_path.exists():
    with open(skill_dict_path, 'w') as f:
        json.dump(DEFAULT_SKILL_DICT, f, indent=4)

def load_skill_dictionary():
    """
    Load the skill dictionary from the JSON file
    
    Returns:
        dict: Skill dictionary mapping lowercase skill names to canonical names
    """
    try:
        with open(skill_dict_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is invalid, use the default
        return DEFAULT_SKILL_DICT

def extract_skills(text):
    """
    Extract technical skills from job description text
    
    Args:
        text (str): Preprocessed job description text
        
    Returns:
        list: List of extracted skills
    """
    if not text:
        return []
    
    # Load skill dictionary
    skill_dict = load_skill_dictionary()
    skill_keywords = list(skill_dict.keys())
    
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract skills using exact and fuzzy matching
    extracted_skills = set()
    
    # Direct matching for multi-word skills
    for skill in skill_keywords:
        if len(skill.split()) > 1:  # Check for multi-word skills
            if skill.lower() in text.lower():
                extracted_skills.add(skill_dict[skill])
    
    # Matching for single-word skills and fuzzy matching
    for token in doc:
        token_text = token.text.lower()
        
        # Direct match for single words
        if token_text in skill_dict:
            extracted_skills.add(skill_dict[token_text])
        
        # Check for compound terms (e.g., "machine learning")
        if token.i < len(doc) - 1:
            bigram = f"{token.text} {doc[token.i + 1].text}".lower()
            if bigram in skill_dict:
                extracted_skills.add(skill_dict[bigram])
        
        if token.i < len(doc) - 2:
            trigram = f"{token.text} {doc[token.i + 1].text} {doc[token.i + 2].text}".lower()
            if trigram in skill_dict:
                extracted_skills.add(skill_dict[trigram])
    
    # Fuzzy matching for skills
    # Get all n-grams of 1-3 words from the text
    words = text.lower().split()
    all_ngrams = []
    
    # Add single words
    all_ngrams.extend(words)
    
    # Add bigrams
    for i in range(len(words) - 1):
        all_ngrams.append(f"{words[i]} {words[i+1]}")
    
    # Add trigrams
    for i in range(len(words) - 2):
        all_ngrams.append(f"{words[i]} {words[i+1]} {words[i+2]}")
    
    # Perform fuzzy matching
    for ngram in all_ngrams:
        # Skip very short terms which might cause false positives
        if len(ngram) < 3:
            continue
            
        # Find closest matches with a high similarity score
        matches = process.extractBests(
            ngram, 
            skill_keywords, 
            score_cutoff=90,  # Only consider matches with high similarity
            limit=1
        )
        
        for match, score in matches:
            extracted_skills.add(skill_dict[match])
    
    return list(extracted_skills)
