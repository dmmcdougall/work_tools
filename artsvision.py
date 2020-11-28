from bs4 import BeautifulSoup
from requests import Session

# the below prints the contens of the log in page
# source = requests.get('https://artsvision.net/main.asp').text
#
# soup = BeautifulSoup(source, 'lxml')
#
# print(soup.prettify())

# this works at printing the conents of the log in page
with Session() as s:
    site = s.get('https://artsvision.net/main.asp')
    print(site.content)

