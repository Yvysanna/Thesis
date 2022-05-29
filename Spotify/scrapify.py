import requests 
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
result = requests.get("https://open.spotify.com/", headers=headers)

# href="/playlist/37i9dQZF1DXcBWIGoYBM5M"

src = result.content
soup = BeautifulSoup(src, 'lxml')

print(soup.prettify())