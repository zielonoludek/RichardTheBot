import requests, json
from bs4 import BeautifulSoup

page = 1
base_url = f'https://www.wojsko-polskie.pl'
payload = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}

response = requests.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={page}', headers=payload)
assert response.status_code == requests.codes.ok

soup = BeautifulSoup(response.content, 'lxml')

for link in soup.find("ul", {"class": "newsgrid-list"}).find_all('a'):
    print(link['href'])
