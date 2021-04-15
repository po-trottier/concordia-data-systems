import pandas as pd
import json
import os

# Create output directory if it doesn't exist
directory = os.path.join(os.path.dirname(__file__), 'output')
if not os.path.exists(directory):
    os.makedirs(directory)

# Load the pickle data to an object
matches = pd.read_pickle('./league_of_legends_match_data_v2.pickle')

# Initialize variables
data = []

# Save the JSON data to a file
def save_json_file(matches):     
  name = f'./output/matches.json'
  print('Saving ' + name)
  with open(name, 'w') as outfile:
    json.dump(matches, outfile)

def save_csv_files(matches):
  print(matches[0])

# Save the matches in group of 1000
for index, row in matches.iterrows():
    data.append(row.to_dict())
    if (len(data) > 2):
      continue

# Save the last set of matches
save_json_file(data)
save_csv_files(data)