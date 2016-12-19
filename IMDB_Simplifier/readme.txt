This program is written in Python 2.7. and uses Elasticsearch and Kibana.
Please make sure that you have them installed.
It also requires the following dependencies on Python:

> requests
> elasticsearch
> beautifulsoup
> html2text

To install de dependencies, run this command on your terminal:
> pip2.7 install <dependency name>

If the packages are not found, run this on your terminal:
> export PYTHONPATH=/usr/local/lib/python2.7/site-packages

HOW TO RUN:
> 1. Open your terminal
> 2. Go to the source folder
> 3. Run Elasticsearch and Kibana on your terminal, by running:
  > elasticsearch
  > kibana
    > to see the data on Elasticsearch, point your to browser: localhost:9200
    > to see the data on Kibana, point your to browser: localhost:5601
> 4. Run:
    > ./crawler.py
    > make sure the scripts have executable permissions (eg, chmod +x crawler.py)
> 5. Run:
   > ./transformers.py
> 6. If you would like to clean all the data injected on Elasticsearch, run on your terminal:
   > ./cleaner.py
