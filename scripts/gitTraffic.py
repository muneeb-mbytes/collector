#import dependencies
import requests
import json
import os
import pandas as pd
from datetime import date,timedelta,datetime
import time
from enum import Enum

class month(Enum):
    Jan="01"
    Feb="02"
    Mar ="03"
    Apr="04"
    May="05"
    Jun="06"
    Jul="07"
    Aug="08"
    Sep="09"
    Oct="10"
    Nov="11"
    Dec="12"
    
def createFolder(folderName):
    os.system("mkdir "+folderName)

def sortDataMonthWise(folderName,data,reponame):
    filePath=folderName+"/"+reponame+".csv"
    if(os.path.exists(filePath)):
        #print("file exists")
        df = pd.read_csv(filePath,header=None)
        df.loc[len(df)]=data
        df=df.drop_duplicates(keep='last')
        os.system("rm "+filePath)
        df.to_csv(filePath, mode='a', index=False, header=False)
        #read_csv
        #appendData
        #deleteOldFile
        #toCSV

    else:
        #print("file does not exist")
        df=pd.DataFrame(columns=['Date', 'views','unique'])
        df.loc[len(df)]=data
        df.to_csv(filePath, mode='a', index=False, header=False)

def sortData(reponame):
    df = pd.read_csv("../csvOutput/"+reponame+".csv",header=None)
    index=0
    for i in df.iloc[:,0]:
        year=i[0:4]
        monthname=i[5:7]
        monthname=month(monthname).name
        folderName=monthname+year
        pathToFolder="../sortedData/" +folderName
        views=df.iloc[index,1]
        unique=df.iloc[index,2]
        data=[i,views,unique]
        #print(folderName)
        if(os.path.exists(pathToFolder)):
            flag = 1
            #print("already exists")
            sortDataMonthWise(pathToFolder,data,reponame)
        else:
            flag = 0
            #print("doesnt exist")
            createFolder(pathToFolder)
            sortDataMonthWise(pathToFolder,data,reponame)
    
        index+=1

def appendcurrDate(days,views,unique,df):
    a=[]
    a.append(str(days))
    a.append(views)
    a.append(unique)
    df.loc[len(df)]=a
    
def appendprevDate(startDay,diffDay,df):
    while(diffDay>1):
        a=[]
        startDay=startDay+timedelta(days=1)
        a.append(str(startDay))
        a.append(0)
        a.append(0)
        df.loc[len(df)]=a
        # print("prev Data")
        # print(startDay," 0   0 ")
        diffDay-=1

def appendMissingDates(reponame):
    prevDate=0;
    df=pd.read_csv(old_csv_name,header=None)
    newdf=pd.DataFrame(columns=['Date', 'views','unique'])
    currDates=[]
    for i in df.iloc[:,0]:
        currDate=datetime.strptime(i,'%Y-%m-%d').date()
        currDates.append(currDate)
    i=0
    count=0
    for i in range(len(currDates)):
        views=df.iloc[i,1]
        unique=df.iloc[i,2]
        if(count>=len(currDates)):
            break

        elif(i==0):
            appendcurrDate(currDates[i],views,unique,newdf)
            count+=1
        else:
            dayDiff=currDates[i]-currDates[i-1]
            diffDay=dayDiff.days
            if(diffDay==1):
                appendcurrDate(currDates[i],views,unique,newdf)
                count+=1

            else:
                appendprevDate(currDates[i-1],diffDay,newdf)
                appendcurrDate(currDates[i],views,unique,newdf)
    removePath="rm "+old_csv_name
    os.system(removePath)
    newdf.to_csv(old_csv_name, mode='a', index=False, header=False)
    
    
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
        zeroes.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=False)
    else:
        #update data
        zeroes.to_csv("../csvOutput/csvUpdateData/" +reponame+".csv", mode='a', index=False, header=False)
            
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
    #sortData(reponame)
    #os.system("rm ../csvOutput/*.csv")
    

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
    appendMissingDates(reponame)
    sortData(reponame)
    #os.system("rm ../csvOutput/*.csv")


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
        
        
os.system("rm ../csvOutput/csvUpdateData/*")
os.system("rm ../jsonOutput/jsonUpdateData/*")
