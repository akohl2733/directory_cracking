def find_staff_blocks(soup):

    # Try common class names
    possible_classes = ['content', 'staff-card', 'profile', 'team-member', 'staff-info']
    for class_name in possible_classes:
        blocks = soup.find_all("div", class_=class_name)
        if blocks:
            return blocks

    # Fallback: look for divs with likely keywords
    fallback_blocks = []
    for div in soup.find_all("div"):
        text = div.get_text().lower()
        if any(keyword in text for keyword in ['director', '@', 'campus', 'facilities', 'staff', 'space']):
            fallback_blocks.append(div)

    return fallback_blocks