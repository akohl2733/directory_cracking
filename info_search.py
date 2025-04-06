def find_staff_blocks(soup):

    staff_blocks = []

    # Common class names
    possible_classes = [ 'staff-card', 
        'staff-member', 'staff-profile', 'staff-item',
        'team-member', 'team-card', 'team-profile',
        'profile', 'profile-card', 'profile-item',
        'person', 'person-card', 'person-item',
        'employee', 'employee-card', 'employee-profile',
        'member', 'member-card', 'member-profile',
        'faculty', 'faculty-card', 'faculty-member',
        'directory-item', 'directory-entry',
        'staff', 'staffinfo', 'staff-info', 'staff-details',
        'bio', 'bio-card', 'bio-info',
        'content', 'content-block', 'content-item'
    ]

    possible_ids = [
        'staff', 'staff-list', 'staff-directory',
        'team', 'team-list', 'team-directory',
        'faculty', 'faculty-list', 'faculty-directory',
        'people', 'people-list', 'people-directory',
        'directory', 'staff-container'
    ]
    
    # check if common class names exist
    for class_name in possible_classes:
        blocks = soup.find_all("div", class_=class_name)
        if blocks:
            staff_blocks.extend(blocks)

    for ids in possible_ids:
        container = soup.find(id=ids)
        if container:
            staff_blocks.append(container)
        
    # check if table structure exists
    for table in soup.find_all('table'):
        text = table.get_text().lower()
        if any(keyword in text for keyword in ['@', 'email', 'phone', 'title', 'director', 'manager', 'staff', 'office', 'department']):
            staff_blocks.append(table)

    jobs = ['director', '.edu', 'campus', 
            'facilities', 'staff', 'space',
            'real estate', 'provost', 'cfo',
            'executive', 'capital', 'facility']

    # Fallback: look for divs with likely keywords
    fallback_blocks = []
    for div in soup.find_all("div"):
        text = div.get_text().lower()
        if any(keyword in text for keyword in jobs):
            fallback_blocks.append(div)
    if fallback_blocks:
        staff_blocks.extend(fallback_blocks)

    seen = set()
    unique_blocks = []
    for block in staff_blocks:
        block_id = id(block)
        if block_id not in seen:
            seen.add(block_id)
            unique_blocks.append(block)

    return staff_blocks