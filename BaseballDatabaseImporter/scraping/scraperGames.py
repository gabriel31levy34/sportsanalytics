import requests
from bs4 import BeautifulSoup
import random
import re
import pandas as pd
from datetime import datetime
import glob
import csv

"""
CSC 353 Final Project 

Author: Dominic Flocco, Henry Howell, Gabe Levy, Izzy Moody 

Web scraper that scrapes game result data from baseball-reference.com
for all MLB games played from 2015 to 2021. 

"""

def scrapeScores():
    """
    Uses beautiful soup package to scrape baseball-reference.com for game result 
    data into pandas dataframe. Writes data into csv file that is saved in directory. 

    Returns: 
        None
    """
  
    column_names = ["date", "home_team", "away_team", "home_score", "away_score"]
    df = pd.DataFrame(columns=column_names)
    for i in range(2015, 2022):
        url = 'https://www.baseball-reference.com/leagues/majors/' + str(i) + '-schedule.shtml'
        reqs = requests.get(url)
        data = BeautifulSoup(reqs.content, features='html.parser')
        schedule = data.find('div',{'class': 'section_content'})
        days = schedule.find_all('div')
        for day in days:
            date = day.find('h3').getText()
            index = date.index(" ")
            date = date[index+1:]
            date_time = datetime.strptime(date, '%B %d, %Y')
            date_time = str(date_time)[:10]
            games = day.find_all('p', {'class': 'game'})
           
            for game in games:
                gameInfo = {}
                gameInfo['date'] = date_time
                teams = game.find_all('a')[:2]
                away_team = teams[0].getText()
                home_team = teams[1].getText()
                gameInfo['home_team'] = home_team
                gameInfo['away_team'] = away_team
                away_score = game.getText()[game.getText().rfind(')')-1]
                home_score = game.getText()[game.getText().index('(')+1]
                gameInfo['home_score'] = home_score
                gameInfo['away_score'] = away_score
                df = df.append(gameInfo, ignore_index=True)
            
    df.to_csv("data/game_results.csv", index=False)
    return None
    
def main():
    
    scrapeScores()

if __name__ == "__main__":
    main()