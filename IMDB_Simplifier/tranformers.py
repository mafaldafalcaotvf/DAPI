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
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='richtitles', ignore=400)
es.indices.create(index='richnames', ignore=400)

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

def transformYear(jsonContent):
    for film in jsonContent['data']['filmography']:
        year = film['year']

        if year is None:
            print('Found None on year')
            return

        try:
            if year.isdigit():
                film['year'] = year
            else:
                ym = re.search("([0-9]+)", year)
                year = ym.group(1)
                film = year
                #print("No digit")
        except:
            print("Unrecognized year format: " + year)


# def transformInfo(jsonContent)

# Fetching Functions

def fetchAndTransformTitles(docId):
    jsonContent = es.get(index='titles', doc_type='title', id=docId)['_source']

    print('Enriching title ' + docId)

    transformDuration(jsonContent)

    es.index(index='richtitles', doc_type='title', id=docId, body=jsonContent)

def fetchAndTransformNames(docId):
    jsonContent = es.get(index='names', doc_type='name', id=docId)['_source']

    print('Enriching title ' + docId)

    transformYear(jsonContent)
    #transformInfo(jsonContent)

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
#doc = json.loads('{ "data": {"year": "2007x"} }')
#transformYear(doc)
#print(doc)
