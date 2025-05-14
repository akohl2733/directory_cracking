from bs4 import BeautifulSoup
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_name(text):
    # split into tokens
    tokens = text.split()
    
    # skip email/phone-looking stuff, look for two consecutive capitalized words
    for i in range(len(tokens) - 1):
        if tokens[i][0].isupper() and tokens[i+1][0].isupper():
            return f"{tokens[i]} {tokens[i+1]}"
    return "Unknown"

def remove_names(text):
    # Process the text with spaCy NLP
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            text = text.replace(ent.text, "")
    
    return text