#!/usr/bin/python

# Import Modules
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

# Import Credentials
from credentials.keys import *

# Set Client Credentials
base_url = 'https://api.genius.com/search'
headers = {'Authorization': 'Bearer ' + client_token}

