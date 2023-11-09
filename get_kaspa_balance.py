from flask import Flask, Response
from prometheus_client import generate_latest, CollectorRegistry, Gauge
import json
import requests
import argparse
import os
import time
import re
import logging

app = Flask(__name__)
headers = {"content-type": "application/json"}

# Set up logging
logging.basicConfig(level=logging.NOTSET)

# Check if variable exists
try:    
    print("Using following Kaspa adresses for request:", os.environ['KASPA_ADDRESS'])
except:
    print("KASPA_ADDRESS environmental variable is not defined!")
    exit()


# Format address for request and create list
kaspa_address = os.environ['KASPA_ADDRESS']
kaspa_address = list(kaspa_address.split(","))

# Validate kaspa address format
for i in kaspa_address:
   ## print(i)
   if bool(re.match(r"^kaspa:[a-z0-9]{61,63}$", i)) == True:
        continue
   else:
        print("Kaspa address format error")
        exit()
x=0
for i in kaspa_address:
    kaspa_address[x] = kaspa_address[x].replace(":","%3A")
    x=x+1

#the required first parameter of the 'get' method is the 'url':
def request_balance(current_address):
    url_address = "https://api.kaspa.org/addresses/" + current_address + "/balance"
    try:
        response = requests.get(url_address).json()
        return response
    except requests.exceptions.RequestException as e:
        logging.error("Request to Kaspa API failed: %s", e)
        return None

# Create Prometheus metrics

g_balance = Gauge ('kaspa_balance','Kaspa balance',['address'])

@app.route('/metrics')
def metrics():
    for address in kaspa_address:
        # print(address)
        new_metrics = request_balance(address)
        # Debug 
        # print(new_metrics)
        g_balance.labels(address=new_metrics["address"]).set(new_metrics["balance"]/100000000)
    return Response(generate_latest(), content_type='text/plain; version=0.0.4')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)