from bs4 import BeautifulSoup
from requests import Session

# the below prints the contens of the log in page
# source = requests.get('https://artsvision.net/main.asp').text
#
# soup = BeautifulSoup(source, 'lxml')
#
# print(soup.prettify())

# this works at printing the conents of the log in page
# with Session() as s:
#     site = s.get('https://artsvision.net/main.asp')
#     print(site.content)

# no work
with Session() as s:
    login_data = {"username": USER, "password": PASSWORD}
    s.post("https://artsvision.net/epcor.asp", login_data)
    home_page = s.get("https://artsvision.net/main.asp")
    print(home_page.content)