import requests
from bs4 import BeautifulSoup, NavigableString
import random
import re
import pandas as pd
from datetime import datetime
import glob
import csv
"""
CSC 353 Final Project 

Author: Dominic Flocco, Henry Howell, Gabe Levy, Izzy Moody 

Web scraper that scrapes information from individual player pages 
on baseball-reference.com and creates a csv with each player in 
the database and their demographic and biological information

"""
def readIDs():
    """
    Reads CSV file generated from stathead.com and creates a dictionary that
    maps a players first and last name to their baseball reference id. This id is
    used to create the url to scrape. 

    Returns: 
        allIDs - dictionary that maps (firstname, lastname) to bsb reference id 

    """
    allIDs = {}
    batterIDs = {}
    pitcherIDs = {}
    urlseen = set()
    with open("data/stathead_data/stathead_batter_data.csv", 'r') as f: 
        reader = csv.DictReader(f)
        for row in reader: 
            splitFirst = row['Player'].split()
            firstname = splitFirst[0]
            if len(splitFirst) == 3:
                splitLast = splitFirst[2].split("\\")
                lastname = splitFirst[1] + " " + splitLast[0]
                id = splitLast[1]
            elif len(splitFirst) == 4:
                splitLast = splitFirst[3].split("\\")
                lastname = splitFirst[1] + " " + splitFirst[2] + " " + splitLast[0]
                id = splitLast[1]
            else:
                splitLast = splitFirst[1].split("\\")
                lastname = splitLast[0]
                id = splitLast[1]
            
            if id not in urlseen:
                batterIDs[(firstname, lastname)] = id
                allIDs[(firstname, lastname)] = id
                urlseen.add(id)
            
    with open("data/stathead_data/stathead_pitcher_data.csv", 'r') as f: 
        reader = csv.DictReader(f)
        
        for row in reader: 
            splitFirst = row['Player'].split()
            firstname = splitFirst[0]
            if len(splitFirst) == 3:
                splitLast = splitFirst[2].split("\\")
                lastname = splitFirst[1] + splitLast[0]
                id = splitLast[1]
            elif len(splitFirst) == 4:
                splitLast = splitFirst[3].split("\\")
                lastname = splitFirst[1] + splitFirst[2] + splitLast[0]
                id = splitLast[1]
            else:
                splitLast = splitFirst[1].split("\\")
                lastname = splitLast[0]
                id = splitLast[1]

            if id not in urlseen:
                pitcherIDs[(firstname, lastname)] = id
                allIDs[(firstname, lastname)] = id
                urlseen.add(id)

    return allIDs

allIDs = readIDs()

def convertName(firstname, lastname): 
    """ 
    Converts and instance of player firstname and lastname to their baseball 
    reference ID to be used in scraping. If the name is not found in curated list, 
    the id is created using the general pattern for bsb reference ids. Some players
    were not in the allIDs dictionary and had unique IDs that did not follow the detected
    pattern. In this case, their id was hardcoded in. 

    Parameters:    
        firstname - player first name 
        lastname - player last name 
    Returns: 
        id - baseball reference id 
    """

    if (firstname, lastname) in allIDs:
        id = allIDs[(firstname, lastname)]
    else: 
        num = "01"
        if lastname == "Cruz Jr.":
            return "cruzne02"
        if lastname == "Gurriel":
            return "gourryu01"
        if lastname == "Voit III":
            lastname ="voit"
        if firstname == "Tommy":
            firstname = "th"
        if lastname == "De Jesus Jr.":
            return 'dejesiv02'
        if "Jr." in lastname: 
            lastname = lastname.split()[0]
        lastname = ''.join(filter(str.isalnum, lastname))
        firstname = ''.join(filter(str.isalnum, firstname))
        lastname = lastname.lower()
        firstname = firstname.lower()
        if len(lastname) >= 5: 
            lastname = lastname[:5]
        firstname = firstname[:2]

        id =  lastname + firstname + num 
    return id

def scrapePlayerInfo(firstname, lastname):
    """
    Uses beautiful soup package to scrape baseball-reference.com for player biological
    and demographic information. 

    Parameters: 
        firstname - player first name 
        latname - player last name 

    Returns: 
        playerData - pandas dataframe with player information 
    """

    player = convertName(firstname, lastname)
    url = "https://www.baseball-reference.com/players/"+ player[0] +"/" + player + ".shtml"
   
    reqs = requests.get(url)
    data = BeautifulSoup(reqs.content, features="html.parser")
    player_info = data.find('div', {'id': 'meta'} )
    player_info_rows = list(player_info.findAll('p'))
    playerData = {}
    bodyInfo = player_info_rows[2].get_text(strip=True).split(",")
    # playerData['height'] = bodyInfo[0]
    # playerData['weight'] = bodyInfo[1][:3]
    for row in player_info_rows: 
        if not isinstance(row, NavigableString):
            value = row.get_text(strip=True)
            info = value.split(":")
            if "Position" in value: 
                playerData["position"] = info[1]
            elif "Bats" in value and "Joey" not in value: 
                playerData['bats'] = info[1].split("\n")[0]
                playerData['throws'] = info[2]
            elif "Team" in value and "National" not in value: 
                team = info[1].split("(")[0] 
                playerData['cur_team'] = team
            elif "lb" in value and "kg" in value: 
                height = value.split(",")[0]
                weight = value.split(",")[1][:3]
                playerData["height"] = height
                playerData["weight"] = weight 
            elif "Born" in value:
                try: 
                    date = info[1].split()
                    month = date[0]
                    day = date[1].split(",")[0]
                    year = date[1].split(",")[1][:4]
                    dob = datetime.strptime(year + month + day, "%Y%B%d")
                    dob = str(dob)[:10]
                except: 
                    dob = ""
                playerData['dob'] = dob
    
            elif "Debut" in value: 
                try:
                    date = info[1].split()
                    month = date[0]
                    day = date[1][:-1]
                    year = date[2][:4]
                    debut = datetime.strptime(year + month + day, "%Y%B%d")
                    debut = str(debut)[:10]
                except: 
                    debut = ""
                
                playerData['debut'] = debut
    playerData['first_name'] = firstname 
    playerData['last_name'] = lastname 
    playerData['bsbref_id'] = player   
    return playerData
        

def readHitterNames():
    """
    Reads in batter names to be scraped based on season level statistics 
    downloaded from basebal savant. 

    Returns: 
        players - dictionary that maps (firstname, lastname) to the set of 
        seasons that a player plays in
    """
    hittersSeen = set()
    files = glob.glob("data/savant_data/hitter_stats/*")
    
    players = {}
    for file in files: 
        with open(file, 'r') as f: 
            reader = csv.DictReader(f)
            for row in reader: 
                last_name = row['\ufefflast_name']
                first_name = row[' first_name'][1:]
                player_id = row['player_id']
                year = row['year']
                if player_id not in hittersSeen: 
                    players[(first_name, last_name)] = [year]
                    hittersSeen.add(player_id)
                else:
                    players[(first_name, last_name)].append(year)
    
    return players
    
def readPitcherNames():
    """
    Reads in pitcher names to be scraped based on season level statistics 
    downloaded from basebal savant. 

    Returns: 
        players - dictionary that maps (firstname, lastname) to the set of 
        seasons that a player plays in
    """
    pitchersSeen = set()
    files = glob.glob("data/savant_data/pitcher_stats/*")
    players = {}
    for file in files: 
        with open(file, 'r') as f: 
            reader = csv.DictReader(f)
            for row in reader: 
                last_name = row['\ufefflast_name']
                first_name = row[' first_name'][1:]
                player_id = row['player_id']
                year = row['year']
                if player_id not in pitchersSeen: 
                    players[(first_name, last_name)] = [year]
                    pitchersSeen.add(player_id)
                else:
                    players[(first_name, last_name)].append(year)
    players[("Ryan", "O'Rourke")] = [2015, 2016, 2019]
    return players


def main():
    
    batters = readHitterNames()
    pitchers = readPitcherNames()
    
    column_names = ['first_name', 'last_name', 'bsbref_id', "position", "bats", "throws", "height", "weight",
                    "cur_team", "dob",  "debut"]

    df = pd.DataFrame(columns=column_names)
    for player in batters: 
        player_info = scrapePlayerInfo(player[0], player[1])
        seasons = ','.join(batters[player])
        player_info['seasons'] = seasons
        df = df.append(player_info, ignore_index=True)
        if len(df)%100==0:
            print(len(df))
 
    
    df = pd.DataFrame(columns=column_names)
    for player in pitchers: 
        player_info = scrapePlayerInfo(player[0], player[1])
        seasons = ','.join(pitchers[player])
        player_info['seasons'] = seasons
        df = df.append(player_info, ignore_index=True)
        if len(df)%100==0:
            print(len(df))
    df.to_csv("data/player_info.csv")

if __name__ == "__main__":
    main()