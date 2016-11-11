This program is written in Python 2.7. and uses Elasticsearch and Kibana.
Please make sure that you have them installed.
It also requires the following dependencies:
> requests
> elasticsearch
> beautifulsoup
> html2text

To install de dependencies, run this command on your terminal
> pip2.7 install <dependency name>

If packages are not found, run this on your terminal:
> export PYTHONPATH=/usr/local/lib/python2.7/site-packages

HOW TO RUN:
> 1. Open your terminal
> 2. Go to the source folder
> 3. Run Elasticsearch and Kibana on your terminal, by typing
  > elasticsearch
  > kibana
    > to see the data on Elasticsearch, type on your browser: localhost:9200
    > to see the data on Kibana, type on your browser: localhost:5601
> 4. Type:
    > ./crawler.py
    > if it doesn't work, type the command:
      > chmod +x crawler.py
      > to transform the file into a exec
> 5. Repeat the process to the script transformers.py
   > ./transformers.py
