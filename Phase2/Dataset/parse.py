import pandas as pd
import json
import csv
import os
import math

# Setting the maximum to -1 will process all the entries
MAX_NUMBER_ENTRIES = -1

# Initialize variables
dict_data = []
json_data = []

# Create output directory if it doesn't exist
def validate_directories():
  print('Creating required directories')
  directory = os.path.join(os.path.dirname(__file__), 'output')
  if not os.path.exists(directory):
      os.makedirs(directory)
  if not os.path.exists(os.path.join(directory, 'csv')):
      os.makedirs(os.path.join(directory, 'csv'))
  if not os.path.exists(os.path.join(directory, 'json')):
      os.makedirs(os.path.join(directory, 'json'))
  print('Directories created successfully')

# Load the pickle data to an object
def load_data():
  print('Loading binary data')
  matches = pd.read_pickle('./league_of_legends_match_data_v2.pickle')
  print('Binary data loaded successfully')
  return matches

# Get the data in usable formats
def process_data(matches):
  print('Processing Data')
  for _, row in matches.iterrows():
      if (MAX_NUMBER_ENTRIES > 0 and len(json_data) >= MAX_NUMBER_ENTRIES):
        continue
      json_data.append(row.to_json())
      dict_data.append(row.to_dict())
  print('Data Processed Successfully')

# Get Games CSV Format
def get_games(matches):
  games = []
  for match in matches:
    clone = match.copy()
    clone['statusCode'] = clone['status.status_code'] if not math.isnan(clone['status.status_code']) else None
    clone['statusMessage'] = clone['status.message'] if not math.isnan(clone['status.message']) else None
    del clone['status.status_code']
    del clone['status.message']
    del clone['participantIdentities']
    del clone['participants']
    del clone['teams']
    games.append(clone)
  return games

# Get Teams CSV Format
def get_teams(matches):
  teams = []
  for match in matches:
    for team in match['teams']:
      index = len(teams)
      clone = team.copy()
      del clone['bans']
      teams.append(clone)
      teams[index]['gameId'] = match['gameId']
  return teams

# Get Bans CSV Format
def get_bans(matches):
  bans = []
  for match in matches:
    for team in match['teams']:
      for ban in team['bans']:
        index = len(bans)
        bans.append(ban)
        bans[index]['gameId'] = match['gameId']
        bans[index]['teamId'] = team['teamId']
        bans[index]['banId'] = index
  return bans

# Get Participants CSV Format
def get_participants(matches):
  participants = []
  for match in matches:
    for participant in match['participants']:
      index = len(participants)
      clone = participant.copy()
      try:
        del clone['stats']
        del clone['timeline']
      except:
        continue
      participants.append(clone)
      participants[index]['gameId'] = match['gameId']
  return participants

# Get Stats CSV Format
def get_stats(matches):
  stats = []
  for match in matches:
    for participant in match['participants']:
      try:
        participant['stats'].copy()
      except KeyError:
        continue
      index = len(stats)
      clone = participant['stats'].copy()
      stats.append(clone)
      stats[index]['gameId'] = match['gameId']
  return stats

# Get Timelines CSV Format
def get_timelines(matches):
  timelines = []
  for match in matches:
    for participant in match['participants']:
      index = len(timelines)
      tl = participant['timeline'].copy()
      timelines.append(tl)
      timelines[index]['gameId'] = match['gameId']
  return timelines

# Write CSV File
def write_csv_file(path, values):
  print('Saving ' + path)
  try:
    with open(path, 'w', newline='') as outfile:
      keys = values[0].keys()
      writer = csv.DictWriter(outfile, keys, extrasaction='ignore')
      writer.writeheader()
      writer.writerows(values)
  except KeyError:
    print('ERROR occurred while saving ' + path)
    return
  print('Saved ' + path + ' successfully')

# Save the data to CSV files for PostGres
def save_csv_files(matches):
  write_csv_file('./output/csv/games.csv', get_games(matches))
  write_csv_file('./output/csv/teams.csv', get_teams(matches))
  write_csv_file('./output/csv/bans.csv', get_bans(matches))
  write_csv_file('./output/csv/participants.csv', get_participants(matches))
  write_csv_file('./output/csv/stats.csv', get_stats(matches))
  write_csv_file('./output/csv/timelines.csv', get_timelines(matches))

# Save the data to a JSON file for MongoDB
def save_json_file(matches):     
  name = './output/json/matches.json'
  print('Saving ' + name)
  with open(name, 'w') as outfile:
    json_file = json.loads('[' + ','.join(matches) + ']')
    json.dump(json_file, outfile)
  print('Saved ' + name + ' successfully')

# Load the data
validate_directories()
process_data(load_data())

# Save the files
save_csv_files(dict_data)
save_json_file(json_data)