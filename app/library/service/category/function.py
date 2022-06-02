# tuong lai tuoi sang
# author: DinhPhu

# requet and get some meme from internet
import requests
from bs4 import BeautifulSoup

url = 'https://www.google.com/search?q=%s&source=lnms&tbm=isch'

req = requests.get(url % 'cat')
soup = BeautifulSoup(req.text, 'html.parser')

print(soup.prettify())

