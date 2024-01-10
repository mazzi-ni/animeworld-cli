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

		# last 6*3 + 6 remain because are that anime in the bottom
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
		
		# TODO: sistemare le ridondanze in questo codice ↓
		
		eps = []
		for div in soup.find_all('div'):
			if 'server active' in str(div):
				eps = div.find_all('a');
		
		episode_id = []
		for e in eps:
			episode_id.append(e.get('data-id'));

		# DEBUG:
		# print(episode_id)
		# print(len(episode_id))
		
		# convert anime duration in int
		if 'he' in anime_metadata['Durata'] and 'min' in anime_metadata['Durata']:
			h_and_min = anime_metadata['Durata'].split('he', 1);
			try:
				min = int(h_and_min[1].replace('min',''));
				h = int(h_and_min[0]);
				anime_metadata['Durata'] = h * 60 + min;
			except:
				anime_metadata['Durata'] = 0;

		elif 'min/ep' in anime_metadata['Durata']:
			anime_metadata['Durata'] = anime_metadata['Durata'].replace('min/ep', '');
			try:
				anime_metadata['Durata'] = int(anime_metadata['Durata'])
			except:
				anime_metadata['Durata'] = 0;

		else:
			anime_metadata['Durata'] = 0;

		self.anime_data = {
				"eps_id" : episode_id,
				"eps_n" : len(episode_id), #anime_metadata['Episodi'],
				"stagione" : anime_metadata['Stagione'],
				"data_uscita" : anime_metadata['DatadiUscita'],
				"eps_durata" : anime_metadata['Durata'],
				"Audio" : anime_metadata['Audio']
			}

		# DEBUG:
		# print(self.anime_data);

		return self.anime_data;


