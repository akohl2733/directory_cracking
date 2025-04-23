from test import runner
from db import insert_rec, test_connection



# url for Jacksonville State's capital planning and facilities department
# link = "https://www.jsu.edu/physicalplant/staff.html"
# link = "https://space.virginia.edu/"
# link = "https://lsu.edu/pdc/about/staff.php"
# link = "https://facilities.lehigh.edu/capital-projects-and-planning/planning-design-construction"

if __name__ == "__main__":
    data = runner(link)

    for person in data:
        insert_rec(person)
        print(f"Inserted: {person['name']}")
        
test_connection()  # Optional log





# create way for it to search through table more efficiently
# find ways to reduce excess after the title (see JSU and Louis B Gilliam at UVA)
# remove phone numbers and the emails from Dusty and other guys page