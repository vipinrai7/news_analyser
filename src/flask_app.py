from flask import Flask, g, jsonify, render_template
from flask_bootstrap import Bootstrap 
import requests
import os
import json
import base64

URL_SOURCES = 'https://newsapi.org/v1/sources'
URL_HEADLINE = 'https://newsapi.org/v1/articles'
API_KEY = 'f3db3605619e43639d45d2806bcee853'

def create_app():
	app = Flask(__name__)
	Bootstrap(app)
	return app


def retreive_json_data():
	file = open('sources.json','r')
	json_data = json.loads(file.read())
	data = []
	for items in json_data['sources']:
		category = items['category']
		name = items['name']
		desc = items['description']
		logo = items['urlsToLogos']['small']
		url = 'https://icons.better-idea.org/icon?url='+items['url']+'&size=50..100..100'
		ids = items['id']
		part = dict(category=category, name=name, url=url , desc=desc,ids=ids)
		data.append(part)
	return data


app = create_app()


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/sources')
def sources():
	if not os.path.exists('sources.json'):
		response = requests.get(URL_SOURCES,data=dict(apiKey=API_KEY))
		with open('sources.json','w') as links:
			m=response.json()
			json.dump(m,links)
			links.close()
	datas=retreive_json_data()
	return render_template('sources.html',data=datas)

@app.route('/results/<ids>')
def results(ids):
	response = requests.get(URL_HEADLINE, params=dict(apiKey=API_KEY,source=ids))
	mx = response.json()

	headlines = []
	for items in mx['articles']:
		article = {}
		article['description'] = items['description']
		article['author'] = items['author']
		article['url'] = base64.b64encode(items['url'])
		article['title'] = items['title']
		article['time'] = items['publishedAt']
		article['image'] = items['urlToImage']
		headlines.append(article)

	return render_template('results.html', headlines=headlines)

@app.route('/analytics/<url>')
def analytics(url):
	url_decoded = base64.b64decode(url)
	apikey = '81a99dfe-78eb-4420-ab19-2831f0887673'
	api_url = 'https://api.havenondemand.com/1/api/sync/analyzesentiment/v2'
	data = dict(apikey=apikey,url=url_decoded)
	response = requests.get(api_url, params=data)
	json_data = response.json()
	
	stats=dict(json_data['sentiment_analysis'][0])

	return render_template('analytics.html', data=stats, url=url_decoded)

if __name__ == '__main__':
	app.run()