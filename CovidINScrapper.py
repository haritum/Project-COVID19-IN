#####################################################
#
#		WebScarping Data Camp Course Details
#
#####################################################


#
# Import scrapy library
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import matplotlib.pyplot as plt

#
# Input
save2json = True
plot2show = False


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
stateCOVID19_df.drop(stateCOVID19_df.tail(2).index, inplace=True)
#print(stateCOVID19_df.columns)
#print(stateCOVID19_df.dtypes)
stateCOVID19_df['Total Confirmed cases (Including 65 foreign Nationals)'].replace(r"\*", "", regex=True, inplace=True)
stateCOVID19_df['Total Confirmed cases (Including 65 foreign Nationals)'] = stateCOVID19_df['Total Confirmed cases (Including 65 foreign Nationals)'].apply(pd.to_numeric)
stateCOVID19_df['Cured/Discharged/Migrated'] = stateCOVID19_df['Cured/Discharged/Migrated'].apply(pd.to_numeric)
stateCOVID19_df['Death'] = stateCOVID19_df['Death'].apply(pd.to_numeric)
print(stateCOVID19_df.dtypes)

if (save2json):
    stateCOVID19_json = stateCOVID19_df.to_json(r'stateCOVID19_'+current_d+'.json',orient='records')
    print (' Saved data as: stateCOVID19_'+current_dt+'.json')


# Plot State-wide da(ta
if (plot2show):
    stateCOVID19_df.plot(kind='bar', x='Name of State / UT', y=['Total Confirmed cases (Including 65 foreign Nationals)','Cured/Discharged/Migrated','Death'])
    plt.show()