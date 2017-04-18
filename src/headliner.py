import requests
from pprint import pprint

URL_HEADLINE = 'https://newsapi.org/v1/articles'
data = {'apiKey': 'f3db3605619e43639d45d2806bcee853','source':'al-jazeera-english'}

response = requests.get(URL_HEADLINE, params=data)
mx = response.json()

headlines = []
for items in mx['articles']:
	article = {}
	article['description'] = items['description']
	article['author'] = items['author']
	article['url'] = items['url']
	article['title'] = items['title']
	article['time'] = items['publishedAt']
	article['image'] = items['urlToImage']
	headlines.append(article)

pprint(headlines)

