def getapi(reponame):
    api_link='gh api repos/' +username+ '/' +reponame+ '/traffic/views --method GET > ../jsonOutput/jsonUpdateData/' +reponame+ '.json'
    os.system(api_link)
    
def new_csv(reponame):
    f = open('../jsonOutput/jsonUpdateData' +reponame+ '.json')
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
    csv_name="../csvOutput/csvUpdateData/"+reponame+".csv"
    old_csv_name = "../csvOutput/"+reponame+".csv"
    data = pd.read_csv(csv_name,header=None)
    oldData = pd.read_csv(old_csv_name,header=None)
    newdata=pd.merge(oldData,data)
    newCleanData=newdata.drop_duplicates(keep='last')
    removePath="rm "+old_csv_name
    os.system(removePath)
    newCleanData.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=False)
