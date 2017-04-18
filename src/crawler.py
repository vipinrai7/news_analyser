import bs4
import json
import requests

URL_SOURCES = 'https://newsapi.org/v1/sources'
URL_HEADLINE = 'https://newsapi.org/v1/articles'
data = {'apiKey': 'f3db3605619e43639d45d2806bcee853'}
sources_dataset = requests.get(URL_SOURCES, params=data)
json_data = sources_dataset.json()

url_list= []
url_id=[]

for sources in json_data['sources']:
	url_list.append(str(sources['url']))
	url_id.append(str(sources['name']))

counter=0
for url in url_list :
	fname='filea'+str(counter)+'.txt'
	data = {'source':url,'apiKey': 'f3db3605619e43639d45d2806bcee853'}
	fp = open(fname,'a+')
	print "Visiting "+url+" please Wait"
	parse_data = requests.get(url)
	print str(parse_data.status_code) + "\n"
	soup_object= bs4.BeautifulSoup(parse_data.text)
	ptag=soup_object.select('p')
	for p in ptag:
		fp.write(str(p))

	counter = counter+1
