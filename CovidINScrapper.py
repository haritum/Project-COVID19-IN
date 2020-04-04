#####################################################
#
#		WebScarping Data Camp Course Details
#
#####################################################


#
# Import scrapy library
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import time


#
# India: state-wide COVID19 information pulled on current date-time (yyyymmdd-HHMMSS)
url = 'https://www.mohfw.gov.in/'
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

#
# StateCOVID19 data on current date-time (YYYYMMDD-hhmmss)
current_dt = time.strftime("%Y%m%d-%H%M%S")
current_d = time.strftime("%Y%m%d")
sdtable = soup.find_all('table')[0]
df = pd.read_html(str(sdtable))
stateCOVID19_df = df[0]
print(stateCOVID19_df.columns)
stateCOVID19_json = stateCOVID19_df.to_json(r'stateCOVID19_'+current_d+'.json',orient='records')
print (' Saved data as: stateCOVID19_'+current_dt+'.json')