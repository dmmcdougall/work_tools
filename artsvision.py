from bs4 import BeautifulSoup
import requests

source = requests.get('https://artsvision.net/main.asp').text

soup = BeautifulSoup(source, 'lxml')

print(soup.prettify())