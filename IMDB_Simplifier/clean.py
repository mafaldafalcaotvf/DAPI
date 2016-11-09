#!/usr/bin/python2.7

"""crawl.py: Cleans Elasticsearch Indexes."""

__author__ = "Mafalda Falcao"

# --- Imports ---

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

es.indices.delete(index='names', ignore=404)
es.indices.delete(index='titles', ignore=404)
es.indices.delete(index='richtitles', ignore=404)
es.indices.delete(index='richnames', ignore=404)

es.indices.create(index='names')
es.indices.create(index='titles')
es.indices.create(index='richtitles')
es.indices.create(index='richnames')
