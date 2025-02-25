import re
from bs4 import BeautifulSoup
from os import path, makedirs
import requests

class Anime:
    BASE_URL = "https://www.animeworld.so"
    BASE_API_URL = "https://www.animeworld.so/api/episode/serverPlayerAnimeWorld?id="

    def __init__(self):
        self.name = ""
        self.anime_data = {}
        self.session = requests.session()

    def get_cookie(self, url):
        page = self.session.get(url)

        cookie_match = re.search(r'SecurityAW-E4=[a-f0-9]{32}', str(page.content));
        if cookie_match:
            self.session.cookies.set("SecurityAW-E4", cookie_match.group().split('=')[1])
            return cookie_match.group();

        return "";

    def get_soup(self, url):
        cookie = self.get_cookie(url);
        
        page = self.session.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup;

    def search(self, name):
        url = self.BASE_URL + "/search?keyword=" + name.replace(" ", "+")

        if name == "ongoing":
            url = self.BASE_URL + "/" + name
        
        soup = self.get_soup(url);
        if soup == None:
            return;
        
        anime_list = []
        for link in soup.find_all("a"):
            if "name" in str(link.get("class")):
                anime_list.append(link.get("href"))

        # last 6*3 + 6 remain because are that anime in the bottom
        anime_list = anime_list[:-24]
        self.name = name
        # DEBUG:
        # print(anime_list);
        # print(len(anime_list));

        return anime_list

    def anime_page(self, link):
        url = link
        if not (self.BASE_URL in link):
            url = self.BASE_URL + link
        
        soup = self.get_soup(url);
        if soup == None:
            return;

        anime_metadata = {}
        for col in soup.find_all("dl"):
            for tag, value in zip(col.find_all("dt"), col.find_all("dd")):
                t = (
                    str(tag.string)
                    .replace("\r\n", "")
                    .replace(" ", "")
                    .replace(":", "")
                )
                v = str(value.string).replace("\r\n", "").replace(" ", "")

                anime_metadata.update({t: v})

        # DEBUG:
        # print(bool(anime_metadata))

        # TODO: sistemare le ridondanze in questo codice ↓

        eps = []
        for div in soup.find_all("div"):
            if "server active" in str(div):
                eps = div.find_all("a")

        episode_id = []
        for e in eps:
            episode_id.append(e.get("data-id"))

        # DEBUG:
        # print(episode_id)
        # print(len(episode_id))

        if not (bool(anime_metadata)):
            raise ValueError("url not correct")

        # convert anime duration in int
        if "he" in anime_metadata["Durata"] and "min" in anime_metadata["Durata"]:
            h_and_min = anime_metadata["Durata"].split("he", 1)
            try:
                min = int(h_and_min[1].replace("min", ""))
                h = int(h_and_min[0])
                anime_metadata["Durata"] = h * 60 + min
            except:
                anime_metadata["Durata"] = 0

        elif "min/ep" in anime_metadata["Durata"]:
            anime_metadata["Durata"] = anime_metadata["Durata"].replace("min/ep", "")
            try:
                anime_metadata["Durata"] = int(anime_metadata["Durata"])
            except:
                anime_metadata["Durata"] = 0

        else:
            anime_metadata["Durata"] = 0

        self.anime_data = {
            "eps_id": episode_id,
            "eps_n": len(episode_id),  # anime_metadata['Episodi'],
            "stagione": anime_metadata["Stagione"],
            "data_uscita": anime_metadata["DatadiUscita"],
            "eps_durata": anime_metadata["Durata"],
            "Audio": anime_metadata["Audio"],
        }

        # DEBUG:
        # print(self.anime_data);

        return self.anime_data

    def video_page(self, id):
        url = self.BASE_API_URL + id

        soup = self.get_soup(url);
        source = soup.find("source").get("src")

        if source == None:
            print("=> Err id non valido")
            return "nope"

        return source

    def original_video_url(self, url):
        soup = self.get_soup(url);
        video_url = soup.find('source').get('src');

        if video_url == None:
            raise ValueError("ERROR url non valido")

        return video_url


    def dowload_anime(self, link):
        home = path.expanduser("~/Videos")
        source_url = link.split("/")
        file_name = path.join(home, source_url[-2], source_url[-1])

        if not path.exists(path.dirname(file_name)):
            try:
                makedirs(path.dirname(file_name))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # DEBUG:
        # print(source_url)
        # print(file_name)

        with open(file_name, "wb") as f:
            response = requests.get(link, stream=True)
            total_length = response.headers.get("content-length")

            # DEBUG:
            # print(total_length);

            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)

                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)

