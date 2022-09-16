import requests, json, datetime, time
from bs4 import BeautifulSoup

with requests.Session() as s:
    def annoucements():
        #Requests Set up
        idle_mode = False
        base_url = 'https://www.wojsko-polskie.pl'
        payload = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        assert s.get(base_url, headers=payload), "-> Connection Failed"

        #Set flag
        with open("archives.json", "r", encoding='utf8') as json_file:
            to_load = json.load(json_file)["announcements"]
            last_in_archives = {"page": to_load[0]["page"], "id": to_load[-1]["id"], "title": to_load[-1]["title"]} if to_load else {"page": 1, "id": 1, "title": ""}

        #Check pages
        while next_page := int(BeautifulSoup(s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={last_in_archives["page"]}', headers=payload).content, 'lxml').find('div', class_='pagination-wrapper').find_all('a')[-2].text):
            if last_in_archives["page"] == next_page: break
            last_in_archives["page"] = next_page

        #Scrap missing annoucements
        while True:
            for p in range(last_in_archives["page"], 0, -1):
                for link in BeautifulSoup(s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={p}', headers=payload).content, 'lxml').find('ul', class_='newsgrid-list').find_all('a'):
                    if idle_mode: time.sleep(30)
                    if last_in_archives["title"] == link["title"]: continue
                    to_upload = {"page": p, "id": last_in_archives["id"], "title": link["title"], "href": base_url+link["href"], "img": base_url+link.find('img')['src'].replace('\n', ''), "content": link.find('div', class_='text').text.strip().replace('\n', '')}
                    #Save to json
                    with open("archives.json",'r+', encoding="utf-8") as archives:
                        archives_update = json.load(archives)
                        archives_update["announcements"].append(to_upload)
                        archives.seek(0)
                        json.dump(archives_update, archives, indent=4, ensure_ascii=False)
                    last_in_archives["id"] += 1
                    print(f'-> Annoucement added [{datetime.datetime.now()}]\n{json.dumps(to_upload, indent = 4, ensure_ascii=False)}\n')   
            
            if not idle_mode:
                last_in_archives["page"] = 1
                idle_mode = True

annoucements()
