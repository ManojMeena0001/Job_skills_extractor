import json
import os
from pathlib import Path

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Path to skill categories file
skill_categories_path = data_dir / "skill_categories.json"

# Default skill categories mapping
DEFAULT_SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "go", 
        "rust", "scala", "kotlin", "perl", "swift", "r (programming language)", "matlab", 
        "bash", "powershell"
    ],
    "Web Technologies": [
        "html", "css", "react", "angular", "vue.js", "django", "flask", "spring", 
        "spring boot", "express.js", "node.js", "jquery", "bootstrap", "tailwind css", 
        "laravel", "ruby on rails", "asp.net", "next.js", "gatsby"
    ],
    "Database & Storage": [
        "sql", "mysql", "postgresql", "oracle database", "mongodb", "cassandra", 
        "redis", "dynamodb", "sqlite", "mariadb", "neo4j", "elasticsearch"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "terraform", "kubernetes", "docker", "jenkins", 
        "ansible", "puppet", "chef", "vagrant", "github actions", "gitlab ci", 
        "circleci", "travis ci", "ci/cd", "continuous integration", "continuous deployment", 
        "devops", "serverless", "microservices"
    ],
    "Data Science & Analytics": [
        "machine learning", "tensorflow", "pytorch", "keras", "scikit-learn", 
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "jupyter", 
        "deep learning", "natural language processing", "computer vision", 
        "data mining", "big data", "hadoop", "apache spark", "apache kafka", "etl"
    ],
    "Business Tools": [
        "tableau", "power bi", "looker", "qlik", "excel", "powerpoint", 
        "microsoft word", "erp", "crm", "salesforce", "sap", "jira", 
        "confluence", "slack", "asana", "trello", "microsoft project"
    ],
    "Mobile Development": [
        "android", "ios", "react native", "flutter", "swift", "kotlin", "xamarin"
    ],
    "Testing & QA": [
        "junit", "selenium", "cypress", "jest", "pytest", "mocha", "chai", 
        "cucumber", "test driven development", "behavior driven development"
    ],
    "Version Control & Collaboration": [
        "git", "github", "gitlab", "bitbucket"
    ],
    "API & Integration": [
        "rest api", "graphql", "soap api", "oauth", "jwt", "single sign-on"
    ],
    "Design & UI/UX": [
        "ui/ux design", "user interface design", "user experience design", 
        "figma", "sketch", "adobe xd", "adobe photoshop", "adobe illustrator"
    ],
    "Emerging Technologies": [
        "blockchain", "internet of things", "saas", "paas", "iaas"
    ],
    "Soft Skills": [
        "communication", "teamwork", "problem solving", "leadership", "time management", 
        "critical thinking", "creativity", "decision making", "project management", 
        "presentation skills", "analytical skills", "attention to detail"
    ],
    "Project Management": [
        "agile", "scrum", "kanban", "waterfall", "pmp", "prince2"
    ],
    "Uncategorized": []  # Will hold skills that don't match any category
}

# Write default skill categories if the file doesn't exist
if not skill_categories_path.exists():
    with open(skill_categories_path, 'w') as f:
        json.dump(DEFAULT_SKILL_CATEGORIES, f, indent=4)

def load_skill_categories():
    """
    Load the skill categories from the JSON file
    
    Returns:
        dict: Mapping of categories to lists of skills
    """
    try:
        with open(skill_categories_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is invalid, use the default
        return DEFAULT_SKILL_CATEGORIES

def categorize_skills(extracted_skills):
    """
    Categorize extracted skills into predefined groups
    
    Args:
        extracted_skills (list): List of extracted skills
        
    Returns:
        dict: Dictionary with categories as keys and lists of skills as values
    """
    if not extracted_skills:
        return {}
    
    # Load skill categories
    skill_categories = load_skill_categories()
    
    # Create a reverse mapping of skills to categories
    skill_to_category = {}
    for category, skills in skill_categories.items():
        for skill in skills:
            skill_to_category[skill.lower()] = category
    
    # Categorize each skill
    categorized = {category: [] for category in skill_categories.keys()}
    
    for skill in extracted_skills:
        skill_lower = skill.lower()
        
        # Find the category for this skill
        category = skill_to_category.get(skill_lower, "Uncategorized")
        
        # Add to the appropriate category
        categorized[category].append(skill)
    
    # Remove empty categories
    categorized = {k: v for k, v in categorized.items() if v}
    
    return categorized
