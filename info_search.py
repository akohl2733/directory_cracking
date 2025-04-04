def find_staff_blocks(soup):

    staff_blocks = []

    # Common class names
    possible_classes = ['content', 'staff-card', 
                        'profile', 'team-member', 'staff-info'
                        ]
    
    # check if common class names exist
    for class_name in possible_classes:
        blocks = soup.find_all("div", class_=class_name)
    if blocks:
        staff_blocks.extend(blocks)
        
    # check if table structure exists
    for table in soup.find_all('table'):
        text = table.get_text().lower()
        if any(keyword in text for keyword in ['@', 'email', 'phone', 'title', 'director', 'staff']):
            staff_blocks.append(table)

    # Fallback: look for divs with likely keywords
    fallback_blocks = []
    for div in soup.find_all("div"):
        text = div.get_text().lower()
        if any(keyword in text for keyword in ['director', '@', 'campus', 'facilities', 'staff', 'space']):
            fallback_blocks.append(div)
    if fallback_blocks:
        staff_blocks.extend(fallback_blocks)

    return staff_blocks