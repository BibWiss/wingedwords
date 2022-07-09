import requests
import string
#from bs4 import BeautifulSoup

base_url = 'https://de.wikipedia.org/wiki/Liste_gefl%C3%BCgelter_Worte/' 
suffix = list(string.ascii_uppercase)

for letter in suffix:
    url = base_url + letter
    page = requests.get(url)
    with open('html/input_' + letter + '.html', 'wb+') as f:
        f.write(page.content)