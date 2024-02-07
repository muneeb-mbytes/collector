import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def trafficPlot(repoPath,reponame,folderName):
    #reponame="apb_avip"
    df = pd.read_csv(repoPath,header=None)
    plt.figure(figsize=(50,25))
    plt.rcParams.update({'font.size': 26})
    plt.plot(df[0], df[1],label='Views')
    plt.plot(df[0],df[2],label='UniqueViews')
    for i, txt in enumerate(df[1]):
        plt.text(df.iloc[i,0], df.iloc[i,1], f"({df.iloc[i,1]})", fontsize=26)
    for i, txt in enumerate(df[2]):
        plt.text(df.iloc[i,0], df.iloc[i,2], f"({df.iloc[i,2]})", fontsize=26)
    plt.xlabel('Date')
    plt.ylabel('Views')
    plt.title(reponame)
    plt.legend()
    try:
        os.system("mkdir ../Graphs/"+folderName)
    except:
        print("graphfolder already exists")
    plt.savefig("../Graphs/"+folderName+"/"+reponame+".png")
    
if len(sys.argv)==3:
    reponame=sys.argv[2]
    folderName=sys.argv[1]
    folderPath="../sortedData/"+folderName
    repoPath=folderPath+"/"+reponame+".csv"
    if(os.path.exists(folderPath)) :
        if(os.path.exists(repoPath)) :
            trafficPlot(repoPath,reponame,folderName)
        else:
            print("Data for this repo does not exists")
    else:
        print("Data for this timeframe does not exists")
        
else :
    print("invalid arguments")
        


