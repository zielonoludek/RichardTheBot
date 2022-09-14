from re import template
import requests, json
from bs4 import BeautifulSoup

''' Session Initialization '''
base_url = f'https://www.wojsko-polskie.pl'
payload = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
}

''' Load Archive '''
with open("announcements_archive.json", "r") as json_file:
    archive = json.load(json_file)

template = archive["template"]
announcements = archive["announcements"]
previous, page, template["id"] = 0, announcements[-1]["page"] if len(announcements) else 1, announcements[-1]["id"] if len(announcements) else 0

with requests.Session() as s:
    while True:
        if previous == page: break
        response = s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={page}', headers=payload)
        soup = BeautifulSoup(response.content, 'lxml')
        previous = page
        page = soup.find('div', class_='pagination-wrapper').find_all('a')[-2].text

with requests.Session() as s:
    for p in range(int(page) + 1, 1, -1):
        response = s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={p}', headers=payload)
        soup = BeautifulSoup(response.content, 'lxml')

        for link in soup.find('ul', class_='newsgrid-list').find_all('a'):
            archive["announcements"].append({p, +1, link["title"], link["href"], link.find('img')['src'], link.find('div', class_='text').text})

with open("announcements_archive.json", "w") as json_file:
    json.dump(archive, json_file, indent=4)