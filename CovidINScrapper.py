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
import sys

#
# Input
save2json = False
plot2show = True

#
# Development print statemnts
debug = False


#
# India: state-wide COVID19 information pulled on current date-time (yyyymmdd-HHMMSS)
print('')
print(' >> Logging onto Ministry of Health and Foreign Affairs Website...')
url = 'https://www.mohfw.gov.in/'
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

#
# StateCOVID19 data on current date-time (YYYYMMDD-hhmmss)
print(' >> Pulling current COVID19-INDIA State-wide data...')
current_dt = time.strftime("%Y%m%d-%H%M%S")
current_d = time.strftime("%Y%m%d")
sdtable = soup.find_all('table')[0]
df = pd.read_html(str(sdtable))
stateCOVID19_df = df[0]

#
# Drop last few lines with total cases information...
stateCOVID19_df.drop(stateCOVID19_df[33:].index, inplace=True)

#
# Clean data & Change datatypes of the # columns
colnames = stateCOVID19_df.columns
coltypes = stateCOVID19_df.dtypes
if (debug): print(colnames)
if (debug): print(coltypes)
stateCOVID19_df[colnames[2]].replace(r"\*", "", regex=True, inplace=True)
stateCOVID19_df[colnames[2]] = stateCOVID19_df[colnames[2]].apply(pd.to_numeric)
stateCOVID19_df[colnames[3]] = stateCOVID19_df[colnames[3]].apply(pd.to_numeric)
stateCOVID19_df[colnames[4]] = stateCOVID19_df[colnames[4]].apply(pd.to_numeric)
if (debug): print(coltypes)


#
# Count no. of states & UT together in our dataset
nstatesuts = stateCOVID19_df[stateCOVID19_df.columns[1]].nunique()
print(' >> [Updated] COVID19-INDIA State-wide data')
ntotcases   = stateCOVID19_df[colnames[2]].sum()
nrecoveries = stateCOVID19_df[colnames[3]].sum()
ndeadths    = stateCOVID19_df[colnames[4]].sum()


#
# Create a normalized (aginst total cases in the country) state-wide data
nstateCOVID19_df = stateCOVID19_df.copy()
nstateCOVID19_df[colnames[2]] = nstateCOVID19_df[colnames[2]]/1000
nstateCOVID19_df[colnames[3]] = nstateCOVID19_df[colnames[3]]/1000
nstateCOVID19_df[colnames[4]] = nstateCOVID19_df[colnames[4]]/1000
if (debug): print(nstateCOVID19_df)

#
# Print out summary of the case data
print ('    -- Summary of COVID19 situation in INDIA (date: '+current_d[6:8]+'-'+current_d[4:6]+'-'+current_d[:4]+')')
print ('        1. # Cases:',ntotcases)
print ('        2. # Recovered:',nrecoveries)
print ('        3. # Deaths:',ndeadths)


if (save2json):
    print(' >> Saving into json file ...')
    stateCOVID19_json = stateCOVID19_df.to_json(r'stateCOVID19_'+current_d+'.json',orient='records')
    print (' Saved data as: stateCOVID19_'+current_dt+'.json')


# Plot State-wide da(ta
if (plot2show):
    print(' >> Plotting ...')
    nstateCOVID19_df.plot(kind='bar', x=colnames[1], y=colnames[2:])
    plt.ylabel('# Cases/Cured/Deaths in the country (x1000)')
    plt.show()