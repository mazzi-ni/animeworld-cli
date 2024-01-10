import animeworld as a
import color as c
import colorify as cc
import mpv

def play(anime_data, ep_index):
	base_url = 'https://www.animeworld.tv/api/episode/serverPlayerAnimeWorld?id='
	
	while True:
		print('\n' + c.BOLD + c.CGREEN2 + '=> ep: ' + str(ep_index + 1) + c.RESET)
		print('=> url: ' + base_url + anime_data['eps_id'][ep_index]);
		
		cc.hide_cursor();

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
				cc.progress_bar(value, anime_data['eps_durata']);
				

		try:
			player.play(base_url + anime_data['eps_id'][ep_index]);
			player.wait_for_playback();
		except Exception as err:
			print('\n=> ERROR: esercuzione interrotta');
			print(err);

		player.terminate();
		del player;

		print('')
		cc.show_cursor();
		ep_index += 1;
		if ep_index >= anime_data['eps_n']:
			print(c.BOLD + c.CGREEN2 + '=> fine serie' + c.RESET);
			break;
		
		retry = input(
      c.BOLD + c.CRED + "\n=> " +
      c.RESET + c.BOLD + "next ep ?? " +
      c.RESET
    );

		if 'n' in retry:
			break;


def main():

	cc.ascii_font();

	# input anime name
	anime_list = []
	while len(anime_list) == 0:
		name = ''
		while len(name) == 0:
			name = input(
				c.BOLD + c.CRED + "=> " + 
				c.RESET + c.BOLD + 'nome dell\'anime: ' +
				c.RESET
			)
	
		anime_obj = a.Anime(name);
		anime_list = anime_obj.search();

		if len(anime_list) == 0:
			print('=> ERROR: Nessun Anime trovato\n')
	
	# print list anime:
	for index, anime in enumerate(anime_list):
		anime = anime.replace('/play/', '').replace('-', ' ')[:-6]
		print(
			# '  ' +
			c.BOLD + 
			c.CYELLOW +
			'[' + str(index) + ']. ' +
			c.RESET +
			anime
		)
	print(' ')

	# input anime index
	index_anime = 0;
	while True:
		index_anime = input(
			c.BOLD + c.CRED + 
			"=> " + c.RESET + c.BOLD + 
			"select an anime [default 0]: " + c.RESET
		)
		
		if index_anime == '':
			index_anime = 0;

		try:
			index_anime = int(index_anime);
			if index_anime > len(anime_list):
				print("=> ERROR: inserisci un valore valido\n");
		
			if index_anime >= 0 and index_anime < len(anime_list):
				break;
		except:
			print("=> ERROR: inserisci un valore valido\n");
	
	# get anime page and scrape it
	anime_data = anime_obj.anime_page(anime_list[index_anime]);
	
	# DEBUG:
	# print(anime_data)

	# select start episode
	ep_index = 0;
	while True:
		ep_index = input(
      c.BOLD + c.CRED + "=> " +
      c.RESET + c.BOLD + 
			'scegli num episodio [1 ... ' + str(anime_data['eps_n']) + ']:  ' +
      c.RESET
    )

		if ep_index == '':
			ep_index = 1;

		try:
			ep_index = int(ep_index);
			
			if ep_index > anime_data['eps_n'] or ep_index <= 0:
				print("=> ERROR: inserisci un valore valido\n");
			else:
				break;

		except:
			print("=> ERROR: inserisci un valore valido\n");
	
	# ep_index -= 1;
	# play function
	play(anime_data, ep_index - 1);
	

if __name__ == '__main__':
	try:
		main();
	except KeyboardInterrupt:
		print('\n=> Interrupted');
	except Exception as err:
		print('=> ERROR:');
		print('-------------------');
		print(err);
		print('-------------------');
		print('=> ERROR: exit force\n');
	
  
