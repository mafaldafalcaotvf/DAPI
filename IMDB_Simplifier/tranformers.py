#!/usr/bin/python2.7
#
# This program requires two dependencies:
#
# > pip2.7 install requests
# > pip2.7 install elasticsearch
#
# If packages are not found, run this:
#
# > export PYTHONPATH=/usr/local/lib/python2.7/site-packages

import re
import json
#import requests
import urllib2
import html2text
from datetime import datetime
from elasticsearch import Elasticsearch
from BeautifulSoup import BeautifulSoup

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='richtitles', ignore=400)
es.indices.create(index='richnames', ignore=400)

# --- Title Transformers --- #

def transformDuration(jsonContent):
    t = 0
    duration = jsonContent['data']['duration']

    if duration is None or type(duration) is int:
        print('Found None on duration')
        return

    try:
        t = datetime.strptime(duration, '%Hh %Mmin').time()
        jsonContent['data']['duration'] = t.hour * 60 + t.minute
    except ValueError:
        try:
            t = datetime.strptime(duration, '%Mmin').time()
            jsonContent['data']['duration'] = t.minute
        except:
            try:
                t = datetime.strptime(duration, '%Hh').time()
                jsonContent['data']['duration'] = t.hour * 60
            except:
                print("Unrecognized duration format: " + duration)

# --- Name Transformers --- #

def transformYear(jsonContent):
    for film in jsonContent['data']['filmography']:
        year = film['year']

        if year is None:
            print('Found None on year')
        else:
            try:
                if not year.isdigit():
                    ym = re.search("([0-9]+)", year)
                    year = int(ym.group(1))
            except:
                print("Unrecognized year format: " + year)
                year = None

        film['year'] = year

def transformBio(id, jsonContent):
    bio = jsonContent['data']['description']

    #req = requests.get('http://www.imdb.com/name/' + id + '/bio?ref=nm_ov_bio_sm')
    soup = BeautifulSoup(urllib2.urlopen('http://www.imdb.com/name/' + id + '/bio?ref=nm_ov_bio_sm').read())

    text = soup.find('div', {'class' : 'soda odd'})
    #print(text)
    txt = text.get_text(text)
    bio = txt
    #bio = html2text.html2text()



def transformInfo(jsonContent):
    for film in jsonContent['data']['filmography']:
        info = film['info']

        if info is None:
            print('Found None on info')
            return

        try:
            inf = re.search("/(tt[0-9]+)/", info)
            info = inf.group(1)
            film['info'] = info
        except:
            print("Unrecognized info format: " + info)

# --- Fetching Functions --- #

def fetchAndTransformTitles(docId):
    jsonContent = es.get(index='titles', doc_type='title', id=docId)['_source']

    print('Enriching title ' + docId)

    transformDuration(jsonContent)

    es.index(index='richtitles', doc_type='title', id=docId, body=jsonContent)

def fetchAndTransformNames(docId):
    jsonContent = es.get(index='names', doc_type='name', id=docId)['_source']

    print('Enriching name ' + docId)

    transformYear(jsonContent)
    transformInfo(jsonContent)
    transformBio(docId, jsonContent)

    es.index(index='richnames', doc_type='name', id=docId, body=jsonContent)

# Obter todos os documentos

def transformTitles():
    hits = es.search(index='titles', doc_type='title')
    res = es.search(index='titles', doc_type='title', filter_path=['hits.hits._id', 'hits.hits._type'], size=hits['hits']['total'])

    for x in res['hits']['hits']:
        id = x['_id']
        jsonContent = fetchAndTransformTitles(id)

def transformNames():
    hits = es.search(index='names', doc_type='name')
    res = es.search(index='names', doc_type='name', filter_path=['hits.hits._id', 'hits.hits._type'], size=hits['hits']['total'])

    for x in res['hits']['hits']:
        id = x['_id']
        jsonContent = fetchAndTransformNames(id)


transformNames()
