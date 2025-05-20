import requests
from bs4 import BeautifulSoup
import re
import spacy
from .info_search import find_staff_blocks
from .cleaning import extract_name, remove_names

nlp = spacy.load("en_core_web_sm")

def runner(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # avoid bot detection

    # Get Page
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Fetched HTML preview: ", response.text[:500])

    # Target keywords and patterns (case-insensitive)
    title_keywords = re.compile(r'executive|planning|space|facilities|campus|Director|asset|capital|real estate', re.IGNORECASE)
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    phone_pattern = re.compile(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")

    # find div with class holding our data
    staff_listing = find_staff_blocks(soup)

    # initialize a set to test multiples of peoples data
    tester = set()
    res = []
    email_test = set()

    # loop through each block found by find_staff_blocks()
    for staff in staff_listing:
        # extract and clean text
        text = staff.get_text(separator=" ").strip()
        if not text:
            continue

        # split into non-empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # chunk lines into groups of 3–5 (heuristic for "one person")
        people_chunks = []
        chunk = []
        for line in lines:
            # print(line, "\n")
            chunk.append(line)
            if len(chunk) >= 4:
                people_chunks.append(chunk)
                chunk = []
        if chunk:  # add leftovers
            people_chunks.append(chunk)

        # process each chunk as one person
        for person_lines in people_chunks:
            person_text = ' '.join(person_lines)
            # print(person_text, "\n")
            doc = nlp(person_text)

            # Extract name
            name = "Unknown"
            for ent in doc.ents:
                # print("0000000000000000")
                if ent.label_ == "PERSON" and " " in ent.text and len(ent.text.split()) <= 3:
                    name = ent.text.strip()
                    # print(name, "\n-------------")
                    break
            
            #fallback
            if name == "Unknown":
                name = extract_name(person_text)

            # Clean and validate name
            if name == "Unknown" or " " not in name:
                continue
            name = re.sub(r'\b(coordinator|director|manager|dr\.?|mr\.?|mrs\.?|ms\.?)\b', '', name, flags=re.IGNORECASE).strip()
            name = ' '.join([part for part in name.split() if not part.isupper()])
            if name in tester:
                continue
            tester.add(name)

            # Extract title
            title = None
            for line in person_lines:
                if title_keywords.search(line):
                    title = line
                    title = re.sub(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', "", title)
                    title = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "", title)
                    title = re.sub(r'telephone[-:\s]?', "", title, flags=re.IGNORECASE)
                    title = remove_names(title)
                    title = title.strip()
                    break
            if not title:
                continue

            # Extract email and phone
            email_match = email_pattern.search(person_text)
            phone_match = phone_pattern.search(person_text)

            email = email_match.group() if email_match else "Not found"
            phone = phone_match.group() if phone_match else "Not found"

            # Skip if invalid or duplicate
            if email in email_test or email == "Not found" or phone == "Not found":
                continue
            email_test.add(email)

            # Output
            # print(f"Name: {name}")
            # print(f"Title: {title}")
            # print(f"Email: {email}")
            # print(f"Phone: {phone}")
            # print("-" * 40)

            res.append({
                "name": name,
                "title": title,
                "email": email,
                "phone": phone})
            
    return res