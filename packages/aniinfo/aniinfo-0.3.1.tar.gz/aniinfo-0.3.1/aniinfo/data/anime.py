import requests, json
from . import readConfig

config = readConfig.config_read()

url = 'https://graphql.anilist.co'

ANIME_SEARCH_QUERY = """
query($id: Int, $page: Int, $per_page: Int, $search: String) {
	Page(page: $page, perPage: $per_page) {
		media(id: $id, search: $search, type: ANIME, sort: POPULARITY_DESC) {
			id
			title {
				romaji
				english
				native
			}
			episodes
			studios {
				nodes {
					name
				}
			}
			season
			status
			seasonYear
			format
			genres
		}
		pageInfo {
			total
			currentPage
			lastPage
			hasNextPage
			perPage
		}
	}
}
"""

CHARACTER_SEARCH_QUERY = """
query($per_page: Int, $page: Int, $search: String) {
	Page(page: $page, perPage: $per_page) {
		characters(search: $search) {
			id
			name {
				first
				full
				native
				last
			}
			age
			gender
			dateOfBirth {
				year
				month
				day
			}
		}
		pageInfo {
			total
			currentPage
			lastPage
			hasNextPage
			perPage
		}
	}
}
"""

MANGA_SEARCH_QUERY = """
query($id: Int, $page: Int, $per_page: Int, $search: String) {
	Page(page: $page, perPage: $per_page) {
		media(id: $id, search: $search, type: MANGA, sort: POPULARITY_DESC) {
			id
			title {
				romaji
				english
				native
			}
			chapters
			status
			genres
			characters(sort: FAVOURITES_DESC) {
				edges {
					node {
						name {
							first
							full
							native
							last
						}
						id
					}
					role
				}
			}
			volumes
		}
		pageInfo {
			total
			currentPage
			lastPage
			hasNextPage
			perPage
		}
	}
}
"""

def search_anime(name, page=1, perPage=config['per_page']):

	variables = {
		'search': name,
		'page': page,
		'per_page': perPage
	}

	response = json.loads(requests.post(url, json={'query': ANIME_SEARCH_QUERY, 'variables': variables}).text)

	media = response['data']['Page']['media']
	total = response['data']['Page']['pageInfo']['total']

	for i in range(perPage):
		try:
			anime = media[i]
		except: break #prevent index out of range
		Name = anime['title'][config['title_language']]
		EpisodeCount = anime['episodes']
		Genre = ', '.join(anime['genres'])
		season = f"{anime['season'] if anime['season']==None else anime['season'].lower()} {anime['seasonYear']}"
		studio = anime['studios']['nodes'][0]['name']
		status = anime['status'].lower()

		print(f'\033[33m{Name}')
		if config['anime_show_episode']: print(f'  \033[35mEpisode : \033[39m{EpisodeCount}')
		if config['anime_show_season'] : print(f'  \033[35mSeason  : \033[39m{season}')
		if config['anime_show_studio'] : print(f'  \033[35mStudio  : \033[39m{studio}')
		if config['anime_show_status'] : print(f'  \033[35mStatus  : \033[39m{status}')
		if config['anime_show_genres'] : print(f'  \033[35mGenres  : \033[39m{Genre}')
		print('')
	
	print(f"page {response['data']['Page']['pageInfo']['currentPage']} of {response['data']['Page']['pageInfo']['lastPage']}")






def search_manga(name, page=1, perPage=config['per_page']):

	variables = {
		'search': name,
		'page': page,
		'per_page': perPage
	}

	response = requests.post(url, json={'query': MANGA_SEARCH_QUERY, 'variables': variables})
	response = json.loads(response.text)

	media = response['data']['Page']['media']
	total = response['data']['Page']['pageInfo']['total']

	for i in range(perPage):
		try: manga = media[i]
		except: break #prevent index out of range
		Name = manga['title'][config['title_language']]
		chapters = manga['chapters']
		volumes = manga['volumes']
		Genre = ', '.join(manga['genres'])
		status = manga['status'].lower()


		print(f'\033[33m{Name}')
		if config['manga_show_chapter']: print(f'  \033[35mChapters : \033[39m{chapters}')
		if config['manga_show_volume'] : print(f'  \033[35mVolumes  : \033[39m{volumes}')
		if config['manga_show_status'] : print(f'  \033[35mStatus   : \033[39m{status}')
		if config['manga_show_genres'] : print(f'  \033[35mGenres   : \033[39m{Genre}')
		print('')

	print(f"page {response['data']['Page']['pageInfo']['currentPage']} of {response['data']['Page']['pageInfo']['lastPage']}")

def search_char(name, page=1, perPage=config['per_page']):

	variables = {
		'search': name,
		'page': page,
		'per_page': perPage
	}

	response = requests.post(url, json={'query': CHARACTER_SEARCH_QUERY, 'variables': variables})
	response = json.loads(response.text)

	charList = response['data']['Page']['characters']
	total = response['data']['Page']['pageInfo']['total']

	for i in range(perPage):
		try: char = charList[i]
		except: break #prevent index out of range
		Name = char['name']['full']
		age = char['age']
		gender = char['gender']
		birthdate = f"{char['dateOfBirth']['day']}/{char['dateOfBirth']['month']}/{char['dateOfBirth']['year']}"
		
		
		print(f'\033[33m{Name}')
		if config['char_show_age']      : print(f'  \033[35mAge         : \033[39m{age}')
		if config['char_show_gender']   : print(f'  \033[35mGender      : \033[39m{gender}')
		if config['char_show_birthdate']: print(f'  \033[35mBirthdate   : \033[39m{birthdate}')
		print('')

	print(f"page {response['data']['Page']['pageInfo']['currentPage']} of {response['data']['Page']['pageInfo']['lastPage']}")
