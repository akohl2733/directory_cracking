import requests
from bs4 import BeautifulSoup
import re
import pymysql
import spacy


def runner(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # avoid bot detection
    nlp = spacy.load("en_core_web_sm")

    # Get Page
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Target keywords (case-insensitive)
    title_keywords = re.compile(r'executive|planning|space|facilities|campus|Director', re.IGNORECASE)

    # target typical email patterns
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    # target typical phone number patterns
    phone_pattern = re.compile(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")

    # Ensure connection management with 'with' statements
    # db_connection = pymysql.connect(
    #     host="localhost",  # usually 'localhost' or the host of your MySQL server
    #     user="root",  # your MySQL username
    #     password="root",  # your MySQL password
    #     database="he_leads"  # the name of the database you created
    # )
    # cursor = db_connection.cursor()

    staff_listing = soup.find_all("div", class_='content')


    for staff in staff_listing:

        text = staff.get_text(separator=" ").strip()

        doc = nlp(text)

        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        name = names[0] if names else "Unknown"

        title = None
        for line in text.split("\n"):
            if title_keywords.search(line):
                title = line.strip()
                break

        email_match = email_pattern.search(text)
        email = email_match.group() if email_match else "Not found"

        phone_match = phone_pattern.search(text)
        phone = phone_match.group() if phone_match else "Not found"


        print(f"Name: {name}")
        print(f"Title: {title if title else 'Not found'}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print("-" * 40)