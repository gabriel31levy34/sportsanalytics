import mysql.connector
import os
import csv
import datetime
import pandas as pd
import glob
import numpy as np

"""
CSC 353 Final Project 

Author: Dominic Flocco, Henry Howell, Gabe Levy, Izzy Moody 

Imports data stored in csv files from scraping into mySQL database. Populates
the database by connecting to DBMS, reading in data and executing sql statements 
to import data into Baseball database 

"""
teamMap = {"Arizona D'Backs": "ARI", "Atlanta Braves": "ATL", "Baltimore Orioles": "BAL", 
"Boston Red Sox": "BOS", "Chicago White Sox": "CWS", "Chicago Cubs": "CHC","Cincinnati Reds": "CIN",
"Cleveland Indians": "CLE", "Colorado Rockies": "COL", "Detroit Tigers": "DET", "Houston Astros": "HOU",
"Kansas City Royals": "KC", "LA Angels of Anaheim": "LAA", "Los Angeles Dodgers":"LA", "Miami Marlins":"MIA", 
"Milwaukee Brewers": "MIL", "Minnesota Twins": "MIN", "New York Mets": "NYM", "New York Yankees": "NYY", 
"Oakland Athletics": "OAK", "Los Angeles Angels": "LAA", "Philadelphia Phillies": "PHI", "Pittsburgh Pirates": 
"PIT", "San Diego Padres": "SD", "San Francisco Giants": "SF", "Seattle Mariners": "SEA", "St. Louis Cardinals": 
"STL", "Tampa Bay Rays": "TB", "Texas Rangers": "TEX", "Toronto Blue Jays": "TOR", "Washington Nationals":"WAS"}

pd.set_option('use_inf_as_na',True)

def insertPlayers(cursor, last_name, first_name, position, bats, throws, height, weight, debut, birthdate):
    """
    Inserts a player into Players table of mySQL database from player_info.csv file. 
    """
    insert_str = """INSERT INTO Players 
    (last_name, first_name, position, bats, throws, height, weight, debut, birthdate)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    try:
        cursor.execute(
    insert_str,
    (last_name, first_name, position, bats, throws, height, weight, debut, birthdate))
    except mysql.connector.IntegrityError:
        pass
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        exit(1)


def insertGames(cursor, date_game, home_team_ID, away_team_ID, home_score, away_score):
    """
    Inserts game result into Game table in my SQL database from game_results.csv file.

    """
    insert_str = """INSERT INTO Game 
    (date_game, home_team, away_team, home_score, away_score)
    VALUES (%s, %s, %s, %s, %s)"""

    try:
        cursor.execute(
    insert_str,
    (date_game, home_team_ID, away_team_ID, home_score, away_score))
    except mysql.connector.IntegrityError:
        pass
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        exit(1)
        

def insertPitcherStats(cursor, player_name, player_id, season, G, IP, PA, AB, H, Single, Double, Triple, HR, 
    K, BB, HBP, K_percent,BB_percent, BAA, SLG, OBP, OPS, ER, R, SV, BS, W, L, ERA, xBA, xSLG, wOBA, xwOBA, 
    xOBP, xISO, exit_velocity_avg, launch_angle_avg, sweet_spot_percent, barrel_batted_rate, Pitches, four_seam_percent, 
    four_seam_avg_speed, four_seam_avg_spin, slider_percent, slider_avg_mph, slider_avg_spin, changeup_percent, changeup_avg_mph, 
    changeup_avg_spin, curveball_percent, curveball_avg_mph, curveball_avg_spin, sinker_percent, sinker_avg_mph, sinker_avg_spin, 
    cutter_percent, cutter_avg_mph, cutter_avg_spin, splitter_percent, splitter_avg_mph, splitter_avg_spin, knuckle_percent, 
    knuckle_avg_mph, knuckle_avg_spin):
    """
    Inserts pitcher season stats into PitcherSeasonStats in mySQL database from savant_data csv files. 
    See statistits definitions at bottom of webpage for information on parameters.
    """
    
    insert_str = """INSERT INTO PitcherSeasonStats 
    (player_id, season, G, IP, PA, AB, H, 1B, 2B, 3B, HR, K, BB, HBP, K_percent, BB_percent, BAA, SLG, OBP, OPS, ER, R,
    SV, BS, W, L, ERA, xBA, xSLG, wOBA, xwOBA, xOBP, xISO, exit_velocity_avg, launch_angle_avg, sweet_spot_percent, 
    barrel_rate, Pitches, four_seam_percent, four_seam_avg_speed, four_seam_avg_spin, slider_percent, slider_avg_speed, 
    slider_avg_spin, changeup_percent, changeup_avg_speed, changeup_avg_spin, curveball_percent, curveball_avg_speed, 
    curveball_avg_spin, sinker_percent, sinker_avg_speed, sinker_avg_spin, cutter_percent, cutter_avg_speed, cutter_avg_spin, 
    splitter_percent, splitter_avg_speed, splitter_avg_spin, knuckle_percent, knuckle_avg_speed, knuckle_avg_spin) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s)"""

    try:
        cursor.execute(
    insert_str,
    (player_id, season, G, IP, PA, AB, H, Single, Double, Triple, HR, K, BB, HBP, K_percent, BB_percent, BAA, SLG, 
        OBP, OPS, ER, R, SV, BS, W, L, ERA, xBA, xSLG, wOBA, xwOBA, xOBP, xISO, exit_velocity_avg, launch_angle_avg, 
        sweet_spot_percent, barrel_batted_rate, Pitches, four_seam_percent, four_seam_avg_speed, four_seam_avg_spin, 
        slider_percent, slider_avg_mph, slider_avg_spin, changeup_percent, changeup_avg_mph, changeup_avg_spin, 
        curveball_percent, curveball_avg_mph, curveball_avg_spin, sinker_percent, sinker_avg_mph, sinker_avg_spin, 
        cutter_percent, cutter_avg_mph, cutter_avg_spin, splitter_percent, splitter_avg_mph, splitter_avg_spin, 
        knuckle_percent, knuckle_avg_mph, knuckle_avg_spin))
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        print(player_name)
        exit(1)


def insertHitterStats(cursor, player_name, player_id, season, G, PA, AB, H, Single, Double, Triple, HR, K, BB, 
    K_percent, BB_percent, Average, SLG, OBP, OPS, RBI, SB, CS, HBP, R, SB_percent, xBA, xSLG, wOBA, xwOBA, 
    xOBP, xISO, wOBACON, xwOBACON, BACON, xBACON, batted_balls, exit_velocity_avg, launch_angle_avg, sweet_spot_percent, 
    barrel_batted_rate, groundballs_percent, flyballs_percent, linedrives_percent, popups_percent, whiff_percent, sprint_speed):
    """
    Inserts batter season stats into PitcherSeasonStats in mySQL database from savant_data csv files. 
    See statistits definitions at bottom of webpage for information on parameters.
    """
    insert_str = """INSERT INTO BatterSeasonStats  
    (player_id, season, G, PA, AB, H, 1B, 2B, 3B, HR, K, BB, K_percent, BB_percent, Average, SLG, OBP, OPS, RBI, 
    SB, CS, HBP, R, SB_percent, xBA, xSLG, wOBA, xwOBA, xOBP, xISO, wOBACON, xwOBACON, BACON, xBACON, batted_balls, 
    exit_velocity_avg, launch_angle_avg, sweet_spot_percent, barrel_rate, groundballs_percent, flyballs_percent, 
    linedrives_percent, popups_percent, whiff_percent, sprint_speed) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    try:
        cursor.execute(
    insert_str,
    (player_id, season, G, PA, AB, H, Single, Double, Triple, HR, K, BB, K_percent, BB_percent, Average, SLG, OBP, 
    OPS, RBI, SB, CS, HBP, R, SB_percent, xBA, xSLG, wOBA, xwOBA, xOBP, xISO, wOBACON, xwOBACON, BACON, xBACON, 
    batted_balls, exit_velocity_avg, launch_angle_avg, sweet_spot_percent, barrel_batted_rate, groundballs_percent, 
    flyballs_percent, linedrives_percent, popups_percent, whiff_percent, sprint_speed))
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        print(player_name)
        exit(1)


def insertPitcherPlaysInGame(cursor, player_id, game_id, team, days_rest,IP,H,R,ER,BB,SO,HR,HBP,earned_run_avg,
    batters_faced,pitches,strikes_total,strikes_looking,strikes_swinging,inplay_gb_total,inplay_fb_total,inplay_ld,
    inplay_pu,inplay_unk,inherited_runners,inherited_score,SB,CS,pickoffs,AB,doubles,triples,IBB,GIDP,SF,
    ROE,leverage_index_avg,wpa_def,cwpa_def,re24_def):
    """
    Inserts pitcher game data from scraped game level baseball reference data. See statistits definitions at bottom of webpage 
    for information on parameters.
    """
    insert_str = """INSERT INTO PitcherPlaysIn
    (player_id, game_id, team, days_rest,IP,H,R,ER,BB,SO,HR,HBP,ERA,BF,pitches,strikes_total,strikes_looking,
    strikes_swinging,inplay_gb_total,inplay_fb_total,inplay_ld,inplay_pu,inplay_unk,inherited_runners,inherited_score,
    SB,CS,pickoffs,AB,2B,3B,IBB,GIDP,SF,ROE,leverage_index_avg,wpa_def,cwpa_def,re24_def) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    try:
        cursor.execute(
    insert_str,
    (player_id, game_id, team, days_rest,IP,H,R,ER,BB,SO,HR,HBP,earned_run_avg,batters_faced,pitches,strikes_total,
    strikes_looking,strikes_swinging,inplay_gb_total,inplay_fb_total,inplay_ld,inplay_pu,inplay_unk,inherited_runners,
    inherited_score,SB,CS,pickoffs,AB,doubles,triples,IBB,GIDP,SF,ROE,leverage_index_avg,wpa_def,cwpa_def,re24_def))
    except mysql.connector.IntegrityError:
        pass
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        exit(1)


def insertHitterPlaysInGame(cursor, player_id, game_id, team, PA,AB,R,H,doubles,triples,HR,RBI,BB,IBB,SO,HBP,SH,SF,
    ROE,GIDP,SB,CS,batting_avg,onbase_perc,slugging_perc,onbase_plus_slugging,batting_order_position,leverage_index_avg,
    wpa_bat,cli_avg,cwpa_bat,re24_bat,pos_game):
    """
    Inserts batter game data from scraped game level baseball reference data. See statistits definitions at bottom of webpage 
    for information on parameters.
    """
    insert_str = """INSERT INTO BatterPlaysIn 
    (player_id,game_id,team,PA,AB,R,H,2B,3B,HR,RBI,BB,IBB,SO,HBP,SH,SF,ROE,GIDP,SB,CS,batting_avg,onbase_perc,slugging_perc,
    onbase_plus_slugging,batting_order_position,leverage_index_avg,wpa_bat,cli_avg,cwpa_bat,re24_bat,pos_game) 
    VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s)"""
    
    try:
        cursor.execute(
    insert_str,
    (player_id,game_id,team,PA,AB,R,H,doubles,triples,HR,RBI,BB,IBB,SO,HBP,SH,SF,ROE,GIDP,SB,CS,batting_avg,onbase_perc,slugging_perc,
    onbase_plus_slugging,batting_order_position,leverage_index_avg,wpa_bat,cli_avg,cwpa_bat,re24_bat,pos_game))
    except mysql.connector.IntegrityError:
        pass
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        exit(1)


# This converts the date obtained from the XML files into a SQL date string. 
def convertDate(date):
    day = date[6:]+ " "
    month = date[4:6]+ " "
    year = date[:4] 
    
    return datetime.datetime.strptime(month + day + year, '%m %d %Y').strftime('%Y-%m-%d')

# Reads in pitcher season level data into dataframe
pitcherSeasonStats = {}
pitcherSeasonStatsFiles = glob.glob("data/savant_data/pitcher_stats/*")
for file in pitcherSeasonStatsFiles:
    year = file[-8:-4]
    df = pd.read_csv(file)
    pitcherSeasonStats[year] = df.replace({np.nan: 0, 'inf': 0, np.inf: 0, 'nan':0})
# Reads in batter season level data into dataframe
hitterSeasonStatsFiles = glob.glob("data/savant_data/hitter_stats_NEW/*")
hitterSeasonStats = {}
for file in hitterSeasonStatsFiles:
    year = file[-8:-4]
    df = pd.read_csv(file)
    hitterSeasonStats[year] = df.replace({np.nan: 0, 'inf': None, np.inf: 0, 'nan': 0})

# Reads in game results level data into dataframe
gameResults = pd.read_csv("data/game_results.csv")

# Reads in player info data into dataframe
playerInfo = pd.read_csv("data/player_info.csv")
playerInfo.replace({np.nan: None, 'inf': None, np.inf: None, 'nan': None}, inplace=True)

# Reads hitter game log data into and stores in hitterGameLog dictionary
hitterGameLogFiles = glob.glob("data/bsb_reference_data/batter_gamelogs/*")
hitterGameLogs = {}
for file in hitterGameLogFiles:
    split = file.split("/")[-1].split("_")
    first_name = split[0]
    last_name = split[1]
    df = pd.read_csv(file)
    hitterGameLogs[(first_name, last_name)] = df.replace({np.nan: 0, 'inf': 0, np.inf: 0, 'nan':0})

# Reads pitcher game log data into and stores in hitterGameLog dictionary
pitcherGameLogFiles = glob.glob("data/bsb_reference_data/pitcher_gamelogs/*")
pitcherGameLogs = {}
for file in pitcherGameLogFiles:
    split = file.split("/")[-1].split("_")
    first_name = split[0]
    last_name = split[1]
    df = pd.read_csv(file)
    pitcherGameLogs[(first_name, last_name)] = df.replace({np.nan: 0, 'inf': 0, np.inf: 0, 'nan':0})

# Reads SQL schema string 
with open("sql/BaseballSchema.sql", "r") as in_file:
    schema_string = in_file.read()

# Connect to MySQL
connection = mysql.connector.connect(
    user='root',
    password='123456',
    host='localhost')


cursor = connection.cursor()

databaseName = "Baseball"
# Run the contents of 'BaseballSchema.sql', creating a schema (deleting previous incarnations)
try:
    results = cursor.execute(schema_string, multi=True)
    for cur in results:
        if cur.with_rows:
            cur.fetchall()
    connection.commit()
except mysql.connector.Error as error_descriptor:
    if error_descriptor.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table already exists: {}".format(error_descriptor))
        exit(1)
    else:
        print("Failed creating schema: {}".format(error_descriptor))
        exit(1)

cursor.close()

# Connect to MySQL
connection = mysql.connector.connect(
    user='root',
    password='ControlWhatYouCan',
    host='localhost')

cursor = connection.cursor()

# Specifies which database to populate after schema is executed in mySQL server
try:
    cursor.execute("USE {}".format(databaseName))

except mysql.connector.Error as error_descriptor:
    print("Failed using database: {}".format(error_descriptor))
    exit(1)

# Populate game results table and store auto incremented game id
gameIDs = []
gameDict = {}
home_teams = []
away_teams = []
for i, row in gameResults.iterrows():
    home_team = teamMap[row['home_team']]
    home_teams.append(home_team)
    away_team = teamMap[row['away_team']]
    away_teams.append(away_team)
    home_score = str(row['home_score'])
    away_score = str(row['away_score'])
    game_date = row['date']
    insertGames(cursor, game_date, home_team, away_team, home_score, away_score)
    game_id = cursor.lastrowid
    gameIDs.append(game_id)
    gameDict[(game_date, home_team, away_team, home_score, away_score)] = game_id
gameResults['id'] = gameIDs
gameResults['home_team'] = home_teams
gameResults['away_team'] = away_teams


# battersSeen = {}
# for year in hitterSeasonStats:
#     df = hitterSeasonStats[year]
    
#     for i, r in df.iterrows():
#         first_name = r[' first_name'].strip()
#         last_name = r['last_name'].strip()
#         # Insert Player if not in DB and store auto incremented player_id
#         if (first_name,last_name) not in battersSeen:
            
#             try:
#                 playerData = playerInfo.loc[(playerInfo['first_name'] == first_name) & (playerInfo['last_name'] == last_name)]
#             except KeyError:
#                 continue

#             for i, row in playerData.iterrows():
#                 position = row['position'].replace("\"", "")
#                 insertPlayers(cursor, last_name, first_name, position, row['bats'], row['throws'], row['height'], 
#                     row['weight'], row['debut'], row['dob'])
#             player_id = cursor.lastrowid
#             battersSeen[(first_name, last_name)] = player_id
#             if first_name == "Shohei" and last_name == "Ohtani":

#                 shohei = player_id
#         else:
            
#             player_id = battersSeen[(first_name, last_name)]
#         # Insert Batter season stats
#         insertHitterStats(cursor, last_name, player_id, year, r['b_game'], r['b_ab'], r['b_total_pa'], r['b_total_hits'], 
#                         r['b_single'], r['b_double'], r['b_triple'], r['b_home_run'], r['b_strikeout'], r['b_walk'], 
#                         r['b_k_percent'], r['b_bb_percent'],r['batting_avg'],r['slg_percent'],r['on_base_percent'],
#                         r['on_base_plus_slg'],r['b_rbi'],r['r_total_stolen_base'], r['r_total_caught_stealing'],['b_hit_by_pitch'],r['r_run'],
#                         r['r_stolen_base_pct'],r['xba'],r['xslg'],r['woba'],r['xwoba'],r['xobp'],r['xiso'],r['wobacon'],r['xwobacon'],r['bacon'],
#                         r['xbacon'],r['batted_ball'],r['exit_velocity_avg'],r['launch_angle_avg'],r['sweet_spot_percent'],r['barrel_batted_rate'],
#                         r['groundballs_percent'],r['flyballs_percent'],r['linedrives_percent'],r['popups_percent'],r['whiff_speed'],r['sprint_speed'])
#         # Get player game log  
#         playerGameLog = hitterGameLogs[(first_name, last_name)]
#         for i, game in playerGameLog.iterrows():

#             outcome = game['game_result'].split(",")[1]
#             if game['cwpa_bat']: 
#                 cwpa = game['cwpa_bat'].replace("%", "")
#             else:
#                 cwpa = None
#             team = game['team_ID']
#             opponent = game['opp_ID']
#             team_score = game['game_result'].split("-")[0][-1]
#             opp_score = game['game_result'].split("-")[1][0]
#             date = game['date_game']
#             home_tup = (date, team, opponent, team_score, opp_score)
#             away_tup = (date, opponent, team, opp_score, team_score)
#             if  home_tup in gameDict:
#                 gameID = gameDict[home_tup]
#             elif away_tup in gameDict:
#                 gameID = gameDict[away_tup]
            
#             # Insert player game log
#             insertHitterPlaysInGame(cursor, player_id, gameID, team, game['PA'],game['AB'],game['R'],
#                                 game['H'],game['2B'],game['3B'],game['HR'],game['RBI'],game['BB'],
#                                 game['IBB'],game['SO'],game['HBP'],game['SH'],game['SF'],game['ROE'],
#                                 game['GIDP'],game['SB'],game['CS'],game['batting_avg'],game['onbase_perc'],
#                                 game['slugging_perc'],game['onbase_plus_slugging'],game['batting_order_position'],
#                                 game['leverage_index_avg'],game['wpa_bat'],game['cli_avg'],cwpa,
#                                 game['re24_bat'],game['pos_game'])
# pitchersSeen = {}
# for year in pitcherSeasonStats:
#     df = pitcherSeasonStats[year]
    
#     for i, r in df.iterrows():
#         first_name = r[' first_name'].strip()
#         last_name = r['last_name'].strip()
#         # Insert Player if not in DB and store auto incremented player_id
#         if (first_name,last_name) not in pitchersSeen:
            
#             try:
#                 playerData = playerInfo.loc[(playerInfo['first_name'] == first_name) & (playerInfo['last_name'] == last_name)]
#             except KeyError:
#                 continue

#             for i, row in playerData.iterrows():
#                 position = row['position'].replace("\"", "")
#                 insertPlayers(cursor, last_name, first_name, position, row['bats'], row['throws'], row['height'], 
#                     row['weight'], row['debut'], row['dob'])
#             player_id = cursor.lastrowid
#             pitchersSeen[(first_name, last_name)] = player_id
#             if first_name == "Shohei" and last_name == "Ohtani":
#                 player_id = shohei
#         else:
            
#             player_id = pitchersSeen[(first_name, last_name)]

#         # Insert Pitcher Season Stats
#         insertPitcherStats(cursor, last_name, player_id, year, r['p_game'], r['p_formatted_ip'], r['p_total_pa'], r['p_ab'], r['p_total_hits'], r['p_single'], r['p_double'], r['p_triple'],
#                         r['p_home_run'], r['p_strikeout'], r['p_walk'], r['p_hit_by_pitch'],r['p_k_percent'], r['p_bb_percent'], r['batting_avg'], r['slg_percent'], r['on_base_percent'],
#                         r['on_base_plus_slg'], r['p_earned_run'], r['p_run'], r['p_save'], r['p_blown_save'], r['p_win'], r['p_loss'], r['p_era'], r['p_opp_batting_avg'], 
#                         r['xslg'], r['woba'], r['xwoba'], r['xobp'], r['xiso'], r['exit_velocity_avg'], r['launch_angle_avg'], r['sweet_spot_percent'], r['barrel_batted_rate'], 
#                         r['n'], r['n_ff_formatted'], r['ff_avg_speed'], r['ff_avg_spin'], r['n_sl_formatted'], r['sl_avg_speed'], r['sl_avg_spin'], r['n_ch_formatted'], r['ch_avg_speed'],
#                         r['ch_avg_spin'], r['n_cukc_formatted'], r['cu_avg_speed'], r['cu_avg_spin'], r['n_sift_formatted'], r['si_avg_speed'], r['n_fc_formatted'], r['fc_avg_speed'],
#                         r['fs_avg_speed'], r['fs_avg_speed'], r['n_fs_formatted'], r['fs_avg_speed'], r['fs_avg_spin'], r['n_kn_formatted'], r['kn_avg_speed'], r['kn_avg_spin'])
#         # Get pitcher game log
#         playerGameLog = pitcherGameLogs[(first_name, last_name)]
#         for i, game in playerGameLog.iterrows():

#             outcome = game['game_result'].split(",")[1]
#             if game['cwpa_def']: 
#                 cwpa = game['cwpa_def'].replace("%", "")
#             else:
#                 cwpa = None
#             team = game['team_ID']
#             opponent = game['opp_ID']
#             team_score = game['game_result'].split("-")[0][-1]
#             opp_score = game['game_result'].split("-")[1][0]
#             date = game['date_game']
#             # Get game_id
#             if (date, team, opponent, team_score, opp_score) in gameDict:
#                 game_id = gameDict[(date, team, opponent, team_score, opp_score)]
#             elif (date, opponent, team, opp_score, team_score) in gameDict:
#                 game_id = gameDict[(date, opponent, team, opp_score, team_score)]
#             if game['earned_run_avg'] == '---':
#                 era = None
#             else: 
#                 era = game['earned_run_avg']
#             # Insert pitcher gamelog
#             insertPitcherPlaysInGame(cursor, player_id, game_id, team, game['days_rest'],game['IP'],game['H'],game['R'],game['ER'],game['BB'],game['SO'],game['HR'],game['HBP'],
#                                 era,game['batters_faced'],game['pitches'],game['strikes_total'],game['strikes_looking'],game['strikes_swinging'],game['inplay_gb_total'],
#                                 game['inplay_fb_total'],game['inplay_ld'],game['inplay_pu'],game['inplay_unk'],game['inherited_runners'],game['inherited_score'],game['SB'],game['CS'],
#                                 game['pickoffs'],game['AB'],game['2B'],game['3B'],game['IBB'],game['GIDP'],game['SF'],game['ROE'],game['leverage_index_avg'],game['wpa_def'],cwpa,
#                                 game['re24_def'])

        
connection.commit()
cursor.close()
connection.close()