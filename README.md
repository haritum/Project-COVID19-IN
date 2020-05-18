# Project-WebScraping-Covid19-INDIA
In this repository, I keep track of files created as a part of **[Project to automatically pull COVID19 data from mohfw.gov.in](https://www.mohfw.gov.in/)**.

- Ministry of Health and Foreign Welfare (mohfw) hasn't created an API for COVID19 as of now.
- This small python script is used to pull the up-to-date Covid19 scenario in India (from mohfw.gov.in) and save the data as **stateCOVID19_yyyymmdd.json** file.
- We limit ourself to access state-wide COVID19 information about:

	1. Serial number of the State/UT
	2. State/UT Name
	3. Total no. of confirmed cases
	4. Total Cured/Discharged/Migrated cases
	5. Total Deaths

- Let's now use this up-to-date Covid19 data and create a informative visualizations of the Pandemic scence in India. 
	- [x] Bar plot of state-wide info. on # Cases, # Recoveries, # Deaths
	- [x] Choropleth Map of the # Cases
	- [x] Choropleth Map of the # Recoveries
	- [x] Choropleth Map of the # Deaths
