import requests
url = 'https://assets.digitalocean.com/articles/eng_python/beautiful-soup/mockturtle.html'
page = requests.get(url)
page.status_code
page.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.prettify())
soup.find_all('p')
soup.find_all('p')[2].get_text()
