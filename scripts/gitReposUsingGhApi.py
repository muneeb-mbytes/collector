import requests
import json
import os
import pandas as pd
from datetime import date,timedelta

def zeroesToEmptyFile(reponame):
    
    
def removeTimestamp(df):
    #get DateValues
    a=[]
    for i in df.iloc[:,0]:
        a.append(i)
    #remove timestamp
    j=0
    for i in a:
        s=i[0:10]
        a[j]=s
        j+=1;
    #save without Timestamp in df
    for i in range(len(df.iloc[:,0])):
        df.iloc[i:,0]=a[i]
        
def updateData(reponame):
    #update data
    print("Project Name:",reponame)
    stri = 'gh api repos/' +username+ '/' +reponame+ '/traffic/views --method GET > ../jsonOutput/jsonUpdateData/' +reponame+ '.json'
    os.system(stri)
    
    #create json and csv files
    f = open('../jsonOutput/jsonUpdateData/' +reponame+ '.json')
    JsonData = json.load(f)
    df = pd.DataFrame(JsonData['views'])
    df.to_csv("../csvOutput/csvUpdateData/" +reponame+".csv", mode='a', index=False, header=False)
    f.close()
    
    #csv to dictionary
    csv_name="../csvOutput/csvUpdateData/"+reponame+".csv"
    old_csv_name = "../csvOutput/"+reponame+".csv"
    if(os.stat(old_csv_name).st_size == 0):
        print("emptyfile -",reponame)
        #get 14 days dates
        a=[]
        today=date.today()
        for i in range(15,0,-1):
            b=[]
            newdate=str(today-timedelta(i))
            b.append(newdate)
            b.append(0)
            b.append(0)
            a.append(b)
        zeroes=pd.DataFrame(columns=['Date', 'views','unique'])
        for i in range(len(a)):
            zeroes.loc[len(zeroes)]=a[i]
        removePath="rm "+old_csv_name
        os.system(removePath)   
        zeroes.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=True)
    else:
        data = pd.read_csv(csv_name,header=None)
        oldData = pd.read_csv(old_csv_name,header=None)
        newdata=pd.merge(oldData,data)
        newCleanData=newdata.drop_duplicates(keep='last')
        removeTimestamp(newCleanData)
        removePath="rm "+old_csv_name
        os.system(removePath)
        newCleanData.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=False)
    
    os.system("rm ../csvOutput/csvUpdateData/*")
    os.system("rm ../jsonOutput/jsonUpdateData/*")


def freshData(reponame):
    #print("inside fresh")
    # Create the json files for the traffic data
    print("Project Name:",reponame)
    stri = 'gh api repos/' +username+ '/' +reponame+ '/traffic/views --method GET > ../jsonOutput/' +reponame+ '.json'
    os.system(stri)

# Create csv files from the JSON files
    f = open('../jsonOutput/' +reponame+ '.json')
    JsonData = json.load(f)
    df = pd.DataFrame(JsonData['views'])
    df.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=False)
    f.close()

#username = input("Enter the github username:")
username = 'muneeb-mbytes'
path = '/home/axyrai/tools/collector/csvOutput/'
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

for i in range(0,len(repoNames)):
    path_to_csv = f'{path}{repoNames[i]}.csv'
    #print(path_to_csv)
    reponame=repoNames[i]
    if(os.path.exists(path_to_csv)):
       #print(repoNames[i]);
       updateData(reponame);
    else: 
       #print(repoNames[i]);
       freshData(reponame);

