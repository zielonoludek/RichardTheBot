import requests, json, datetime, time, math, os, animation
from bs4 import BeautifulSoup

with requests.Session() as s:
    def annoucements():
        #Clear terminal
        os.system('cls')

        #Requests Set up
        class Old_annoucement(Exception): pass
        base_url = 'https://www.wojsko-polskie.pl'
        payload = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        #Set flag
        try:
            with open("archives.json", "r", encoding='utf8') as json_file:
                archive = json.load(json_file)
                last_in_archive = {"pages": math.ceil(len(archive["announcements"])/6), "title": archive["announcements"][-1]["title"]} if archive["announcements"] else {"pages": 1}
        except:
            archive, last_in_archive = {"announcements": []}, {"pages": 1}

        #Check pages
        while True:
            try:
                next_page = int(BeautifulSoup(s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={last_in_archive["pages"]}', headers=payload).content, 'lxml').find('div', class_='pagination-wrapper').find_all('a')[-2].text)
            except: continue
            if last_in_archive["pages"] == next_page:
                del next_page
                break
            last_in_archive["pages"] = next_page

        #Scrap missing annoucements
        def scrapp_annoucement():
            #Variable
            archive_update = []

            #Start checking
            print('\n-> Looking for announcements:')
            wait_animation = animation.Wait(['-','\\','|','/'], color="blue", speed=0.1)
            wait_animation.start()

            try:
                for p in range(1, last_in_archive["pages"]+1):
                    for link in BeautifulSoup(s.get(f'{base_url}/wat/articles/list/komunikaty-dla-studentow/?strona={p}', headers=payload).content, 'lxml').find('ul', class_='newsgrid-list').find_all('a'):
                        try:
                            if last_in_archive["title"] == link["title"]: raise Old_annoucement
                        except KeyError: pass
                        wait_animation.stop()
                        to_upload = {"title": link["title"], "href": base_url+link["href"], "img": base_url+link.find('img')['src'].replace('\n', ''), "content": link.find('div', class_='text').text.strip().replace('\n', '')}
                        print(f'-> Annoucement added [{datetime.datetime.now()}]\n{json.dumps(to_upload, indent = 4, ensure_ascii=False)}\n')
                        archive_update.append(to_upload)
            except Old_annoucement: pass

            #Save to json
            if archive_update:
                archive_update.reverse()
                [archive["announcements"].append(update) for update in archive_update]
                with open("archives.json", 'r+' if os.path.isfile("archives.json") else 'w', encoding="utf-8") as json_file: json.dump(archive, json_file, indent=4, ensure_ascii=False)

                #Prepare next run
                try: last_in_archive["title"]
                except KeyError: last_in_archive["title"] = archive_update[-1]["title"]
                del archive_update

            time.sleep(5)
            wait_animation.stop()

            scrapp_annoucement()
            
        scrapp_annoucement()

annoucements()
