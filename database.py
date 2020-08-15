from bs4 import BeautifulSoup
import threading
import urllib
from tqdm import tqdm 
import json
import sys
from math import sqrt
from joblib import Parallel, delayed

def get_whisky_characteristics(url = r'https://www.thewhiskyexchange.com/p/55556/macallan-rare-cask-2020-release', return_data=False):
	try:
		req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
		con = urllib.request.urlopen( req )
		soup = BeautifulSoup(con,'html.parser')

		flavors = soup.find_all('li', attrs={'class':'flavour-profile__item flavour-profile__item--style'})
		d = {}
		d['Url'] = url.split("/")[-1]

		d['Style'] = {}
		for flavor in flavors: 
			d['Style'][flavor.contents[3].text] = int(flavor.contents[1]['data-part'])

		d['Characteristics'] = []
		characteristics = soup.find_all('li', attrs={'class': 'flavour-profile__item flavour-profile__item--character'})

		for character in characteristics: 
			d['Characteristics'].append(character.contents[3].text.lstrip().rstrip())

		facts = soup.find_all('li', attrs={'class': 'product-facts__item'})
		for fact in facts:
			d[fact.contents[3].text] = fact.contents[5].text

		price = soup.find_all('p', attrs={'class': 'product-action__unit-price'})
		price = float(price[0].contents[0].split(' per litre')[0][2:])*1.12*0.7
		d['Price per 70cl, USD'] = float('%.2f' %price)

		if 'Age' in d.keys():
			d['Age, yrs'] = int(d['Age'].split(' Year')[0])
			d['Age Statement'] = 'True'
			del(d['Age'])
		else:
			d['Age Statement'] = 'False'

		header = soup.find_all('header', attrs={'class': 'product-main__header'})
		d['Name'] = header[0].contents[1].text[1:-1]
		d['Type'] = header[0].contents[3].contents[1].text
		d['Proof'] = float(header[0].contents[5].text.split("/ ")[-1][:-2])*2.

		if return_data: 
			return d
	except:
		#db.append("None")
		return 'None'

def get_whisky_exchange_urls():
	base = r'https://www.thewhiskyexchange.com'

	urls = [r'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky',
			r'https://www.thewhiskyexchange.com/c/304/blended-scotch-whisky',
			r'https://www.thewhiskyexchange.com/c/309/blended-malt-scotch-whisky',
			r'https://www.thewhiskyexchange.com/c/310/grain-scotch-whisky',
			r'https://www.thewhiskyexchange.com/c/33/american-whiskey',
			r'https://www.thewhiskyexchange.com/c/34/canadian-whisky',
			r'https://www.thewhiskyexchange.com/c/317/indian-whisky',
			r'https://www.thewhiskyexchange.com/c/35/japanese-whisky',
			r'https://www.thewhiskyexchange.com/c/493/english-whisky',
			r'https://www.thewhiskyexchange.com/c/32/irish-whiskey',
			r'https://www.thewhiskyexchange.com/c/540/taiwanese-whisky',
			r'https://www.thewhiskyexchange.com/c/305/world-whisky'		
			]

	whisky_urls = []
	image_urls = []

	for url in urls:
		req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
		con = urllib.request.urlopen( req )
		soup = BeautifulSoup(con,'html.parser')
		n_items = int(soup.find_all('ul', attrs={'class':'sort-type'})[0].contents[1].text.split('(')[-1].split(')')[0])
		n_pages = np.ceil(n_items / 200.).astype('int')

		for n in tqdm(range(1,n_pages+1)):
			new_url = url + '?pg={}&psize=200'
			req = urllib.request.Request(new_url.format(n), headers={'User-Agent' : "Magic Browser"}) 
			con = urllib.request.urlopen( req )
			soup = BeautifulSoup(con,'html.parser')

			items = soup.find_all('div', attrs={'class':'item'})
			page_urls = [base + item.contents[1]['href'] for item in items]

			for item in items:
				try:
					img_url = item.contents[1].contents[1].contents[1]['data-original']
				except:
					img_url = 'N/A'
				image_urls.append(img_url)
			
			whisky_urls.extend(page_urls)
		
	return whisky_urls, image_urls

def create_database(urls = None):
	if not isinstance(urls, list):
		urls, image_urls = get_whisky_exchange_urls()

	db = Parallel(n_jobs=8)(delayed(get_whisky_characteristics)(i, True) for i in tqdm(urls))

	db = [i for i in db if i != 'None']
	db = [i for i in db if len(i['Style'].keys())]

	with open('whisky-database.json', 'w') as f:
		json.dump(db, f)
	
	return db

def load_database():
	with open("./database/whisky-database.json", "r") as f:
		db = json.load(f)
	return db

def prepare_database(db):
	data = []
	styles = ['Body', 'Richness', 'Smoke', 'Sweetness']
	categorical_variables = ['Country', 'Region', 'Cask Type', 'Price per 70cl, USD', 'Proof', 'Age, yrs', 'Colouring']
	all_flavors = []
	for entry in db:
		all_flavors.extend(entry['Characteristics'])
		for style in styles:
			if not style in entry['Style'].keys():
				entry['Style'][style] = 0

	unique_flavors = sorted(np.unique(all_flavors))
	flavor_dict = dict(zip(unique_flavors, range(len(unique_flavors))))

	categorical_data = []
	for entry in db:
		row = []
		cat = []
		row.extend(list(entry['Style'].values()))
		#row.extend([entry['Proof']])

		characteristics = np.array([0] * len(flavor_dict))
		for char in entry["Characteristics"]:
			characteristics[flavor_dict[char]] = 1

		row.extend(characteristics.tolist())
		data.append(row)

		cat = [entry[i] if i in entry else 'N/A' for i in categorical_variables]
		categorical_data.append(cat)


	return np.vstack(data), dict(zip(categorical_variables, np.vstack(categorical_data).T))

