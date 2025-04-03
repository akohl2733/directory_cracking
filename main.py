from bs4 import BeautifulSoup
from test import runner


# url for Jacksonville State's capital planning and facilities department
link = "https://www.jsu.edu/physicalplant/staff.html"

runner(link)


# create it so it only prints out values that have acceptable titles
# allow it to search through html - not handicapped to specified class tags we are using
# remove phone numbers and the emails from Dusty and other guys page