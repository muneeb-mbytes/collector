# Prerequisites
brew install python  
python3 --version  


curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py  
python3 get-pip.py  
pip3 --version  

pip3 install json2csv  
pip3 install pandas  
pip3 install requests  
pip3 install ghapi  

# Run the following   
python3 gitReposUsingGhApi.py  
 
# Commit using the below command  
git add .  
git commit -m "Updating the traffic views for all repos"  
git push origin main  
