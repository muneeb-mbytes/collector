# Python program to read
# json file

import pandas as pd
import json

# Opening JSON file
f = open('temp.json')

# returns JSON object as 
# a dictionary
JsonData = json.load(f)

# Iterating through the json
# list
for i in JsonData['views']:
	print(i)

# Convert JSON data to a pandas DataFrame
df = pd.DataFrame(JsonData['views'])

# Writing DataFrame to a CSV file
# timestamp, total views, unique visitors
df.to_csv("output.csv", mode='w', index=False, header=False)

print("Data appended successfully")

# Closing file
f.close()
 
