#import dependencies
import requests
import json
import os
import pandas as pd
from datetime import date,timedelta
import time

def zeroesToEmptyFile(reponame,flag):
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
     
            
    if(flag==0):
        #fresh data
        if(os.path.exists(old_csv_name)):
            removePath="rm "+old_csv_name
            os.system(removePath)  
        zeroes.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=True)
    else:
        #update data
        zeroes.to_csv("../csvOutput/csvUpdateData/" +reponame+".csv", mode='a', index=False, header=True)
            
def removeTimestamp(df):
    a=[]
    for i in df.iloc[:,0]:
        a.append(i)
    j=0
    for i in a:
        s=i[0:10]
        a[j]=s
        j+=1;
    for i in range(len(df.iloc[:,0])):
        df.iloc[i:,0]=a[i]
    return df

def getapi(reponame):
    api_link='gh api repos/' +username+ '/' +reponame+ '/traffic/views --method GET > ../jsonOutput/jsonUpdateData/' +reponame+ '.json'
    os.system(api_link)
    
def new_csv(reponame):
    f = open('../jsonOutput/jsonUpdateData/' +reponame+ '.json')
    JsonData = json.load(f)
    df = pd.DataFrame(JsonData['views'])
    df.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=False)
    f.close()
    
def update_csv(reponame):
    f = open('../jsonOutput/jsonUpdateData/' +reponame+ '.json')
    JsonData = json.load(f)
    df = pd.DataFrame(JsonData['views'])
    df.to_csv("../csvOutput/csvUpdateData/" +reponame+".csv", mode='a', index=False, header=False)
    f.close()

def merge_csv(reponame):
    
    data = pd.read_csv(csv_name,header=None)
    oldData = pd.read_csv(old_csv_name,header=None)
    newdata=pd.merge(oldData,data)
    newCleanData=newdata.drop_duplicates(keep='last')
    removePath="rm "+old_csv_name
    os.system(removePath)
    newCleanData.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=False)
    



def freshData(reponame):
    flag=0
    getapi(reponame)
    new_csv(reponame)
    #time.sleep(10)
    if(os.stat(old_csv_name).st_size == 0):
        print("empty file",reponame)
        zeroesToEmptyFile(reponame,flag)
    df=pd.read_csv(old_csv_name,header=None)
    df=removeTimestamp(df)
    df.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=False)

def updateData(reponame):
    flag=1
    getapi(reponame)
    update_csv(reponame)
    if(os.stat(csv_name).st_size == 0):
        print("empty file",reponame)
        zeroesToEmptyFile(reponame,flag)
    #time.sleep(10)
    df=pd.read_csv(old_csv_name,header=None)
    df=removeTimestamp(df) 
    removePath="rm "+csv_name
    os.system(removePath)
    df.to_csv("../csvOutput/csvUpdateData/" +reponame+".csv", mode='a', index=False, header=False)
    #print("removed timestamp")
    merge_csv(reponame)


username = 'muneeb-mbytes'
path = '/home/axyrai/tools/collector/csvOutput/'
request = requests.get('https://api.github.com/users/'+username+'/repos?per_page=1000')
JsonData = request.json()

repoNames = []
for i in range(0,len(JsonData)):
	if (JsonData[i]['name'] == '.github'):
		continue
	if (JsonData[i]['name'] == 'mbits-mirafra.github.io'):
		continue
	repoNames.append(JsonData[i]['name'])

for i in range(0,len(repoNames)):
    path_to_csv = f'{path}{repoNames[i]}.csv'
    reponame=repoNames[i]
    csv_name="../csvOutput/csvUpdateData/"+reponame+".csv"
    old_csv_name = "../csvOutput/"+reponame+".csv"
    if(os.path.exists(path_to_csv)):
        print("updating ",reponame)
        updateData(reponame);
    else: 
        print("fetching ",reponame)
        freshData(reponame);
        
        
#os.system("rm ../csvOutput/csvUpdateData/*")
os.system("rm ../jsonOutput/jsonUpdateData/*")
