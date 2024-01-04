from bs4 import BeautifulSoup
import requests
import sys

class Anime:
	BASE_URL = 'https://www.animeworld.so'

	def __init__(self, name):
		self.name = name;
		self.anime_data = {}
	
	def search(self):
		url = self.BASE_URL + '/search?keyword=' + self.name.replace(' ', '+');
		page = requests.get(url);
		soup = BeautifulSoup(page.content, 'html.parser');
		
		anime_list = []
		for link in soup.find_all('a'):
			if 'name' in str(link.get('class')):
				anime_list.append(link.get('href'));

		# last 6*3 + 6 remain because are extra
		anime_list = anime_list[:-24]
		
		# DEBUG:
		# print(anime_list);
		# print(len(anime_list));

		return anime_list;

	def anime_page(self, link):
		page = requests.get(self.BASE_URL + link);
		soup = BeautifulSoup(page.content, 'html.parser');
		
		anime_metadata = {}
		for col in soup.find_all('dl'):
			for tag, value in zip(col.find_all('dt'), col.find_all('dd')):
				t =  str(tag.string).replace('\r\n', '').replace(' ', '').replace(':','');
				v =  str(value.string).replace('\r\n', '').replace(' ', '');
				
				anime_metadata.update({t:v});
		
		# DEBUG:
		# print(anime_metadata)
		
		# TODO: take only server active !!

		episode_id = []
		for ep in soup.find_all('a'):
			if str(link) in str(ep.get('href')):
				episode_id.append(ep.get('data-id'));
		
		# DEBUG:
		print(episode_id)
		
		if int(anime_metadata['Episodi']) == 1:
			episode_id = episode_id[- int(anime_metadata['Episodi']) : ];
		else:
			episode_id = episode_id[- int(anime_metadata['Episodi']) - 1 : ];
		
		# DEBUG:
		# print(episode_id)
		# print(len(episode_id))

		self.anime_data = {
				"eps_id" : episode_id,
				"eps_n" : anime_metadata['Episodi'],
				"stagione" : anime_metadata['Stagione'],
				"data_uscita" : anime_metadata['DatadiUscita'],
				"eps_durata" : anime_metadata['Durata'],
				"Audio" : anime_metadata['Audio']
			}

		return self.anime_data;


