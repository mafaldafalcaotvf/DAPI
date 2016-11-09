#!/usr/bin/python2.7

"""crawl.py: Cleans Elasticsearch Indexes."""

__author__ = "Mafalda Falcao"

# --- Imports ---

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

es.indices.delete(index='names', ignore=400)
es.indices.delete(index='titles', ignore=400)

es.indices.create(index='names')
es.indices.create(index='titles')
