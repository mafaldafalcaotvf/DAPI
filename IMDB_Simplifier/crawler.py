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

"""crawl.py: Crawls IMDB and stores data back in Elasticsearch."""

__author__ = "Mafalda Falcao"

# --- Imports ---

import requests
import re
import json
import sys

from datetime import datetime
from elasticsearch import Elasticsearch

# --- Global Stuff ---

count = 10

fetchedTitles = set()
fetchedNames  = set()

# --- Fetch and Store ---

def fetchAndStoreName(res):
    print("Fetching resource " + res)
    r2 = requests.get('http://imdb.wemakesites.net/api/' + res)

    if r2.status_code == 200:
        js = json.loads(r2.content)
        js['crawltimestamp'] = datetime.today()
        es.index(index='names', doc_type='name', id=res, body=js)
    else:
        print("Failed to fetch specific resource " + res)

def fetchAndStoreTitle(res):
    print("Fetching resource " + res)
    r2 = requests.get('http://imdb.wemakesites.net/api/' + res)

    if r2.status_code == 200:
        js = json.loads(r2.content)
        js['crawltimestamp'] = datetime.today()
        es.index(index='titles', doc_type='title', id=res, body=js)
    else:
        print("Failed to fetch specific resource " + res)

# --- Process Command Line Arguments ---

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='names', ignore=400)
es.indices.create(index='titles', ignore=400)

if (len(sys.argv) > 2):
    print("USAGE: crawler.py <count>")
elif (len(sys.argv) == 2):
    count = int(sys.argv[1])

print("Starting the crawling process (" + str(count) + " fetches)...")

# --- Entrypoint Fetch ---

for x in range(0, count):
    r = requests.get('http://www.imdb.com/random/title')
    if r.status_code == 200:
        m = re.search('<link rel=\"canonical\" href=\"http://www.imdb.com/title/(.*?)/\" />', r.content)
        res = m.group(1)

        linkedNames  = set(re.findall("/name/(nm[0-9]+?)/", r.content))
        linkedTitles = set(re.findall("/title/(tt[0-9]+?)/", r.content))

        print("Got resource " + res + " which is linked to " + str(len(linkedNames)) + " unique names and " + str(len(linkedTitles)) + " unique titles")

        fetchAndStoreTitle(res)

        for title in linkedTitles:
            if title not in fetchedTitles:
                fetchedTitles.add(title)
                fetchAndStoreTitle(title)

        for name in linkedNames:
            if name not in fetchedNames:
                fetchedNames.add(name)
                fetchAndStoreName(name)
    else:
        print("Failed to query random resource")
