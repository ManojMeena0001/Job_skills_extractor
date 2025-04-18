import re
import spacy
import os

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If the model is not installed, download and load it
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Clean and preprocess job description text for analysis
    
    Args:
        text (str): Raw job description text
        
    Returns:
        str: Cleaned and preprocessed text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S*@\S*\s?', '', text)
    
    # Replace multiple whitespaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Process with spaCy
    doc = nlp(text)
    
    # Collect tokens, excluding punctuation and specific stop words
    # Keep some stop words that might be part of technical terms (e.g., "of" in "Internet of Things")
    keep_tokens = []
    excluded_stop_words = {'a', 'an', 'the', 'is', 'was', 'were', 'be', 'been', 'being'}
    
    for token in doc:
        if (not token.is_punct and                     # Skip punctuation
            not token.is_space and                     # Skip whitespace
            not (token.is_stop and token.text in excluded_stop_words) and  # Skip only certain stopwords
            not token.like_num):                       # Skip numbers
            keep_tokens.append(token.text)
    
    # Join tokens back into text
    processed_text = ' '.join(keep_tokens)
    
    return processed_text
