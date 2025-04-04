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

    # loop
    for staff in staff_listing:

        # extract and clean text using spacy
        text = staff.get_text(separator=" ").strip()
        if not text:
            continue
        doc = nlp(text)

        # search for prospects name
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        name = names[0].strip() if names else "Unknown"
        if " " not in name:
            continue

        # search for titles we are interested in
        title = None
        for line in text.split("\n"):
            if title_keywords.search(line):
                title = line.strip()
                break
        if title == None or len(title) > 60:  # in the case that there is no title - move on to next
            continue

        # test if name has already been found
        if name in tester:
            continue
        tester.add(name)           

        # search for emails and phone numbers
        email_match = email_pattern.search(text)
        email = email_match.group() if email_match else "Not found"

        phone_match = phone_pattern.search(text)
        phone = phone_match.group() if phone_match else "Not found"

        if phone == "Not found" or email == "Not found":
            continue

        # print results
        print(f"Name: {name}")
        print(f"Title: {title if title else 'Not found'}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print("-" * 40)