#!/usr/bin/env python

from typing_extensions import Annotated
from concurrent.futures import ThreadPoolExecutor, as_completed
from yaspin import yaspin
import questionary as q
import typer
import mpv 
import requests

from animeworld import Anime
import color as c
import colorify as cc


app = typer.Typer()
anime = Anime()

@app.command()
def search(anime_name: str):
	"""
	Search an Anime in Animeworld.tv
	"""

	anime_list = anime.search(anime_name)
	anime_list_option = [];

	for anime_url in anime_list:
		name = anime_url.replace('/play/', '').replace('-', ' ')[:-6]
		anime_list_option.append(name)

	select = q.select('Select an Anime: ', choices = anime_list_option).ask()
	
	# DEBUG:
	# print(anime_list[anime_list_option.index(select)])

	play(anime_list[anime_list_option.index(select)])

@app.command()
def play(url: Annotated[str, typer.Option()]):
	"""
	Play an Anime from Animeworld.tv with mpv
	"""
	anime_data = anime.anime_page(url);
	
	def validate(ep):
		if len(ep) > 0:
			try:
				ep = int(ep)
				if ep <= anime_data['eps_n'] and ep > 0:
					return True
				else:
					return "Please enter a correct value"
			except Exception as err:
				return "Please enter a correct value"
		
		return "Please enter a value"
	
	ep = q.text(
			'Select an Episode to start: [1 ... ' + str(anime_data['eps_n']) + ']',
			default = '1',
			validate = validate,
		).ask()

	play_id(int(ep) - 1);
	

def play_id(ep_index):
	while True:
		print('\n' + c.BOLD + c.CGREEN2 + '=> episode: ' + str(ep_index + 1) + c.RESET)
		print('=> url: ' + anime.BASE_API_URL + anime.anime_data['eps_id'][ep_index]);
		
		player = mpv.MPV(
			input_default_bindings=True,
			input_vo_keyboard=True,
			osc=True,
			ytdl=True
		)
		player['vo'] = 'gpu';
		player.fullscreen = False;
		
		@player.property_observer('time-pos')
		def time_observer(_name, value):
			if value != None:
				# print('Now playing at ' + str(value) + 's', end='\r')
				cc.progress_bar(value, anime.anime_data['eps_durata']);

		try:
			player.play(anime.BASE_API_URL + anime.anime_data['eps_id'][ep_index]);
			player.wait_for_playback();
		except Exception as err:
			print('\n=> ERROR: esercuzione interrotta');
			print(err);

		player.terminate();
		del player;

		print('')
		ep_index += 1;
		if ep_index >= anime.anime_data['eps_n']:
			print(c.BOLD + c.CGREEN2 + '=> fine serie' + c.RESET);
			break;
		
		retry = q.confirm('Next Episode: ').ask()

		if not(retry):
			break;

@app.command()
def ascii():
	"""
	Print Ascii font from font.txt
	"""
	cc.ascii_font();

@app.command()
def download(name: Annotated[str, typer.Option()] = None, multi_thread: Annotated[bool, typer.Option()] = False):
	"""
	Download an Anime from Animeworld.tv
	"""
	anime_list = []
	if name == None:
		while len(anime_list) == 0:
			name = q.text(
				'Insert the name of the Anime',
				validate = lambda text: True if len(text) > 0 else 'Error: insert something',
			).ask()
		
			anime_list = anime.search(name);
			if len(anime_list) == 0:
				print('=> Error: Anime not found')
	
	else:
		anime_list = anime.search(name);
		if len(anime_list) == 0:
			print('=> Error: Anime not found')
			return 0;
		
	
	anime_list_option = [];
	for anime_url in anime_list:
		name = anime_url.replace('/play/', '').replace('-', ' ')[:-6]
		anime_list_option.append(name)

	select = q.select('Select an Anime: ', choices = anime_list_option).ask()
	anime.anime_page(anime_list[anime_list_option.index(select)]);
	
	def validate(text):
		if len(text) > 0:
			if ' ' in text:
				text = text.replace(' ', '');
			
			if '-' in text:
				text = text.split('-')
				try:
					text[0] = int(text[0])
					text[1] = int(text[1])
					if text[0] >= 1 and text[1] <= anime.anime_data['eps_n']:
						return True
				except:
					return "Please enter correct a value"
		return "Please enter a value"


	ep_range = q.text(
		'Select range of Episode to download: [1-' + str(anime.anime_data['eps_n']) + ']',
		default = '1-' + str(anime.anime_data['eps_n']),
		validate = validate,
	).ask()
	
	ep_range = list(map(int, ep_range.split('-')))
	ep_range[0] = ep_range[0] - 1
	# ep_range[1] = ep_range[1] - 1
	range_ep_id = anime.anime_data['eps_id'][ep_range[0]:ep_range[1]]
	
	# DEBUG:
	# print(ep_id_dowload)

	if multi_thread:
		multithread_download(range_ep_id)
	else:	
		singlethread_download(range_ep_id)
	
	print('\n=> finish')


def singlethread_download(range_ep_id):
	with yaspin(text="Loading", color="yellow") as sp:
		for id in range_ep_id:
			source = anime.video_page(id)
			anime.dowload_anime(source)
			sp.write('=> ep ' + source.split('/')[-1] +  ' download complete')

	
def multithread_download(range_ep_id):
	futures = []
	
	with yaspin(text="Downloading", color="yellow") as sp:
		with ThreadPoolExecutor(max_workers=4) as executor:
			try:
				for id in range_ep_id:
					source = anime.video_page(id)
					future = executor.submit(anime.dowload_anime, source)
					futures.append(future)
				
				count = len(futures)
				while count != 0:
					for f in futures:
						if f.done():
							count -= 1
							sp.write('=> ep ' + str(len(futures) - count) + ' download complete')

			except KeyboardInterrupt:
				executor._threads.clear()

	
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
	if ctx.invoked_subcommand != None:
		return 0

	ascii();
	
	anime_list = []
	name = ''

	while len(anime_list) == 0:
		name = q.text(
				'Insert the name of the Anime',
				validate = lambda text: True if len(text) > 0 else 'Error: insert something',
			).ask()
		
		anime_list = anime.search(name);
		if len(anime_list) == 0:
			print('=> Error: Anime not found')
	
	search(name)

	

if __name__ == '__main__':
	try:
		app()
	except KeyboardInterrupt:
		print("=> Cancelled by user")
	except ValueError as err:
		print('=> Errore:', err);
	except AttributeError:
		pass
	except Exception as err:
		print('=> Errore:', type(err).__name__, err);




