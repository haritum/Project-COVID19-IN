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
import seaborn as sns
import os
import sys
import folium
import webbrowser

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
stateCOVID19_df[colnames[1]].replace(r"Telengana", "Telangana", regex=True, inplace=True)
stateCOVID19_df[colnames[1]].replace(r"Odisha", "Orissa", regex=True, inplace=True)
stateCOVID19_df[colnames[2]] = stateCOVID19_df[colnames[2]].apply(pd.to_numeric)
stateCOVID19_df[colnames[3]] = stateCOVID19_df[colnames[3]].apply(pd.to_numeric)
stateCOVID19_df[colnames[4]] = stateCOVID19_df[colnames[4]].apply(pd.to_numeric)
if (debug): print(coltypes)


# print(stateCOVID19_df[colnames[1]].unique())
# sys.exit('Testing...')
#
# Count no. of states & UT together in our dataset
nstatesuts = stateCOVID19_df[stateCOVID19_df.columns[1]].nunique()
print(' >> [Updated] COVID19-INDIA State-wide data')
ntotcases   = stateCOVID19_df[colnames[2]].sum()
nrecoveries = stateCOVID19_df[colnames[3]].sum()
ndeadths    = stateCOVID19_df[colnames[4]].sum()

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
    sns.set_style('ticks')
    #
    #
    # plt.figure(figsize = (12,15))
    # plt.barh(stateCOVID19_df[colnames[1]], stateCOVID19_df[colnames[2]], 0.5, align='edge', color='deepskyblue')
    # for index, value in enumerate(stateCOVID19_df[colnames[2]]):
    #     plt.text(value, index, str(value), fontsize = 8)
    # plt.title(' Total cases in each state in India', fontsize=18)
    # plt.xlabel('# Cases in the state', fontsize=12)
    # plt.xticks(fontsize = 8)
    # plt.yticks(fontsize = 8)
    # plt.show()
    # #
    # #
    # plt.figure(figsize = (12,15))
    # plt.barh(stateCOVID19_df[colnames[1]], stateCOVID19_df[colnames[3]], 0.5, align='edge', color='green')
    # for index, value in enumerate(stateCOVID19_df[colnames[3]]):
    #     plt.text(value, index, str(value), fontsize = 8)
    # plt.title(' Total Recoveries in each state in India', fontsize=18)
    # plt.xlabel('# Recoveries in the state', fontsize=12)
    # plt.xticks(fontsize = 8)
    # plt.yticks(fontsize = 8)
    # plt.show()
    # #
    # #
    # plt.figure(figsize = (12,15))
    # plt.barh(stateCOVID19_df[colnames[1]], stateCOVID19_df[colnames[4]], 0.5, align='edge', color='red')
    # for index, value in enumerate(stateCOVID19_df[colnames[4]]):
    #     plt.text(value, index, str(value), fontsize = 8)
    # plt.title(' Total Deaths in each state in India', fontsize=18)
    # plt.xlabel('# Deaths in the state', fontsize=12)
    # plt.xticks(fontsize = 8)
    # plt.yticks(fontsize = 8)
    # plt.show()
    #
    #
    india_state_geo = os.path.join('india_states.geojson')
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('stamentoner').add_to(m)
    folium.Choropleth(geo_data=india_state_geo,
                  name='choropleth-cases',
                  data=stateCOVID19_df,
                  columns=[colnames[1],colnames[2]],
                  key_on='feature.properties.NAME_1',
                  fill_color='YlOrRd',
                  nan_fill_color='white',
                  fill_opacity=0.45,
                  line_opacity=0.5,
                  highlight=True,
                  show=True,
                  legend_name='No. of COVID19 Cases in India').add_to(m)
    # folium.Choropleth(geo_data=india_state_geo,
    #               name='choropleth-recoveries',
    #               data=stateCOVID19_df,
    #               columns=[colnames[1],colnames[3]],
    #               key_on='feature.properties.NAME_1',
    #               fill_color='BuGn',
    #               nan_fill_color='white',
    #               fill_opacity=0.45,
    #               line_opacity=0.5,
    #               highlight=True,
    #               show=False,
    #               legend_name='No. of COVID19 Recoveries in India').add_to(m)
    # folium.Choropleth(geo_data=india_state_geo,
    #               name='choropleth-deaths',
    #               data=stateCOVID19_df,
    #               columns=[colnames[1],colnames[4]],
    #               key_on='feature.properties.NAME_1',
    #               fill_color='GnBu',
    #               nan_fill_color='white',
    #               fill_opacity=0.45,
    #               line_opacity=0.5,
    #               highlight=True,
    #               show=False,
    #               legend_name='No. of COVID19 Deaths in India').add_to(m)
    folium.LayerControl().add_to(m)
    html_page = 'india_covid19-cases-recoveries-deaths.html'
    m.save(html_page)

    webbrowser.open(html_page, new=2)
