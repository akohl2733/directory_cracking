import requests
from bs4 import BeautifulSoup
import re
import spacy
from info_search import find_staff_blocks

nlp = spacy.load("en_core_web_sm")


def runner(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # avoid bot detection

    # Get Page
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Target keywords and patterns (case-insensitive)
    title_keywords = re.compile(r'executive|planning|space|facilities|campus|Director|asset|capital|real estate', re.IGNORECASE)
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    phone_pattern = re.compile(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")

    # find div with class holding our data
    staff_listing = find_staff_blocks(soup)

    # initialize a set to test multiples of peoples data
    tester = set()
    email_test = set()

    # loop
    for staff in staff_listing:

        # extract and clean text using spacy
        text = staff.get_text(separator=" ").strip()
        if not text:
            continue

        doc = nlp(text)

        # search for prospects name
        name = "Unknown"
        for ent in doc.ents:
            if ent.label_ == "PERSON" and " " in ent.text and len(ent.text.split()) <= 3:
                name = ent.text.strip()
                break
        
        # skip if no valid name found
        if name == "Unknown" or " " not in name:
            continue
        
        name = re.sub(r'\b(coordinator|director|manager|dr\.?|mr\.?|mrs\.?|ms\.?)\b', '', name, flags=re.IGNORECASE).strip()
        name = ' '.join([part for part in name.split() if not part.isupper()])

        if name in tester:
            continue
        tester.add(name) 

        # search for titles we are interested in
            # extract title - more flexible approach
        title = None
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Look for title before or after name
        for i, line in enumerate(lines):
            if name in line:
                # Check previous line for title
                if i > 0 and title_keywords.search(lines[i-1]):
                    title = lines[i-1]
                # Check next line for title
                elif i < len(lines)-1 and title_keywords.search(lines[i+1]):
                    title = lines[i+1]
                break
        
        # Fallback: search entire text for title-like patterns
        if not title:
            for line in lines:
                if title_keywords.search(line) and len(line) < 100:  # limit length to avoid false positives
                    title = line
                    break

        # skip if no relevant title found
        if not title or len(title) > 100:
            continue

          

        # search for emails and phone numbers
        email_match = email_pattern.search(text)
        email = email_match.group() if email_match else "Not found"
        if email in email_test:
            continue
        email_test.add(email) 

        phone_match = phone_pattern.search(text)
        phone = phone_match.group() if phone_match else "Not found"

        if phone == "Not found" or email == "Not found":
            continue

        # # print results
        print(f"Name: {name}")
        print(f"Title: {title if title else 'Not found'}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print("-" * 40)