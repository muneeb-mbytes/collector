import requests
import json
import os
import pandas as pd

#username = input("Enter the github username:")
username = 'mbits-mirafra'
request = requests.get('https://api.github.com/users/'+username+'/repos?per_page=1000')
JsonData = request.json()

# Store various repo names into an array
repoNames = []
for i in range(0,len(JsonData)):
	if (JsonData[i]['name'] == '.github'):
		continue
	if (JsonData[i]['name'] == 'mbits-mirafra.github.io'):
		continue
	#print("Project Number:",i+1)
	repoNames.append(JsonData[i]['name'])
	#print("Project Name:",JsonData[i]['name'])
	#print("Project URL:",JsonData[i]['svn_url'],"\n")

# Create the json files for the traffic data
for i in range(0,len(repoNames)):
	print("Project Name:",repoNames[i])
	stri = 'gh api repos/' +username+ '/' +repoNames[i]+ '/traffic/views --method GET > ../jsonOutput/' +repoNames[i]+ '.json'
	os.system(stri)

# Create csv files from the JSON files
for i in range(0,len(repoNames)):
	f = open('../jsonOutput/' +repoNames[i]+ '.json')
	JsonData = json.load(f)
	df = pd.DataFrame(JsonData['views'])
	df.to_csv("../csvOutput/" +repoNames[i]+".csv", mode='a', index=False, header=False)
	f.close()


## # Get the query for traffic for each repo
## request = requests.get('https://api.github.com/users/'+username+'/axi4_avip/traffic/views')
## JsonData = request.json()
## print(JsonData)
## 
## #for i in range(0,len(JsonData)):
## #	print("Display",JsonData['views'])


