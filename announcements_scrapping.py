import requests, json
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

''' Session Initialization '''
base_url = 'https://www.wojsko-polskie.pl'
payload = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
}
try:
    response = requests.get(base_url, headers=payload)
    http_encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(response.content, is_html=True)
    encoding = html_encoding or http_encoding
    print("-> Connection Succeded")
except:
    print("-> Connection Failed")

''' Load Archive & varables assignment '''
with open("announcements_archive.json", "r") as json_file:
    archive = json.load(json_file)
previous, page, id = 0, archive['announcements'] if len(archive['announcements']) else 1, archive['announcements'][-1] if len(archive['announcements']) else 1

''' Pages check '''
with requests.Session() as s:
    while previous != page:
        response = s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={page}', headers=payload)
        soup = BeautifulSoup(response.content, 'lxml', from_encoding=encoding)
        previous = page
        page = int(soup.find('div', class_='pagination-wrapper').find_all('a')[-2].text)

''' Scrap missing annoucements '''
try:
    with requests.Session() as s:
        for p in range(page, 0, -1):
            response = s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={p}', headers=payload)
            soup = BeautifulSoup(response.content, 'lxml', from_encoding=encoding)

            for link in soup.find('ul', class_='newsgrid-list').find_all('a'):
                archive['announcements'].append({"page": p, "id": id, "title": link["title"], "href": base_url+link["href"], "img": base_url+link.find('img')['src'].replace('\n', ''), "content": link.find('div', class_='text').text.strip().replace('\n', '')})
                id+=1
    print("-> Page scrapped succesfully")

    ''' Save data to json '''
    try:
        with open("announcements_archive.json", "w", encoding='utf8') as json_file:
            json.dump(archive, json_file, indent=4, ensure_ascii=False)
        print("-> Data saved to json succesfully")
    except:
        print("-> During saving data to json, the program encountered a problem")

except:
    print("-> During scrapping, the program encountered a problem")
