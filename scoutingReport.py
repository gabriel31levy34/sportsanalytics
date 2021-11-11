#Authors: Gabriel Levy and Ben Yokoyama

import requests
from bs4 import BeautifulSoup
import random

def scrape(school,site,team):
    #url = "https://www.sports-reference.com/cbb/schools/davidson/2020.html"
    url = "https://www.sports-reference.com/cbb/schools/" + school + "/2021.html"
    reqs = requests.get(url)
    data = BeautifulSoup(reqs.content, features="html.parser")
    
    #url_schedule = "https://www.sports-reference.com/cbb/schools/davidson/2020-schedule.html"
    url_schedule = "https://www.sports-reference.com/cbb/schools/"+school+"/2021-schedule.html"
    reqs_schedule = requests.get(url_schedule)
    data_schedule = BeautifulSoup(reqs_schedule.content, features="html.parser")
    
    player_stats = []
    team_opponent_stats = []
    schedule_stats = []
    
    #[name,mins,pts,rebs,asts,stls,blks,orebs,FG%,FGA,3P%,3PA,2P%,2PA,FT%,FTA]
    per_game_stat_index = [0,3,24,18,19,20,21,16,6,5,12,11,9,8,15,14]

    #[pts/g,FG%,2P%,3P%,FT%]
    #added later: 3PM/g, 3PA/g, streak, home record, away, neutral, win margin, loss margin, overall record
    team_stat_index = [22,4,7,10,13]
    
    #[site,result,team score,opp score,overall wins, overall losses,streak]
    schedule_stat_index = [3,6,7,8,10,11,12]
    
    team_stats = data.find('table',{'id': 'schools_per_game'})
    team_stats_line = team_stats.find("tbody")
    team_stats_rows = team_stats_line.find_all('tr')
    
    count1 = 0
    for row in team_stats_rows:
        current_stat = []
        for f in team_stat_index:
            if (count1 == 1) or (count1 == 3):
                current_stat.append(row.select('td')[f].get_text(strip=True))
            else:
                current_stat.append(float(row.select('td')[f].get_text(strip=True)))
        
        count1 += 1
        team_opponent_stats.append(current_stat)
    
    team_opponent_stats[0][1] = str(round(float(team_opponent_stats[0][1])*100,1))+"%"
    team_opponent_stats[0][2] = str(round(float(team_opponent_stats[0][2])*100,1))+"%"
    team_opponent_stats[0][3] = str(round(float(team_opponent_stats[0][3])*100,1))+"%"
    team_opponent_stats[0][4] = str(round(float(team_opponent_stats[0][4])*100,1))+"%"
        
    team_opponent_stats[0].append(round(float(team_stats_rows[0].select('td')[8].get_text(strip=True)),1))
    team_opponent_stats[0].append(round(float(team_stats_rows[0].select('td')[9].get_text(strip=True)),1))
    
    team_opponent_stats[2].append(round(float(team_stats_rows[2].select('td')[8].get_text(strip=True)),1))
    team_opponent_stats[2].append(round(float(team_stats_rows[2].select('td')[9].get_text(strip=True)),1))
    
    
    per_game = data.find('table', {'id': 'per_game'})
    per_game_players = per_game.find("tbody")
    per_game_rows = per_game_players.find_all('tr')
    
    
    for row in per_game_rows:
        count2 = 1
        current_player = []
        for f in per_game_stat_index:
            if (count2 == 1) or (row.select('td')[f].get_text(strip=True) == ''):
                current_player.append(row.select('td')[f].get_text(strip=True))
            else:
                current_player.append(float(row.select('td')[f].get_text(strip=True)))
            count2 += 1
        player_stats.append(current_player)
        
    scheduling_stats = data_schedule.find('table',{'id': 'schedule'})
    schedule_stats_game = scheduling_stats.find("tbody")
    schedule_stats_rows = schedule_stats_game.find_all('tr')
        
    for row in schedule_stats_rows:
        count3 = 0

        current_game = []
        if len(row.select('td')) > 0:
            if(row.select('td')[6].get_text(strip=True)!=''):
                for f in schedule_stat_index:
                    if (count3 == 7) or (count3 == 8):
                        current_game.append(float(row.select('td')[f].get_text(strip=True)))
                    else:
                        current_game.append(row.select('td')[f].get_text(strip=True))
                    count3 += 1
                schedule_stats.append(current_game)
    
    home_record = [0,0]
    away_record = [0,0]
    neutral_record = [0,0]
    avg_win = 0
    avg_loss = 0
    for row in schedule_stats:
        if row[0] == 'N':
            if row[1] =='W':
                neutral_record[0] += 1
            elif row[1] == 'L':
                neutral_record[1] += 1
        elif row[0] == '':
            if row[1] =='W':
                home_record[0] += 1
            elif row[1] == 'L':
                home_record[1] += 1
        elif row[0] == '@':
            if row[1] =='W':
                away_record[0] += 1
            elif row[1] == 'L':
                away_record[1] += 1
        
        if row[1] == 'W':
            avg_win += (float(row[2]) - float(row[3]))
        elif row[1] == 'L':
            avg_loss += (float(row[3]) - float(row[2]))
    
    avg_win = avg_win/(home_record[0]+away_record[0]+neutral_record[0])
    avg_loss = avg_loss/(home_record[1]+away_record[1]+neutral_record[1])
    streak = ''
    if int(schedule_stats[-1][-1][-1]) >= 3:
        streak = schedule_stats[-1][-1]
    
    team_opponent_stats[0].append(streak)
    team_opponent_stats[0].append(str(home_record[0]) + '-' + str(home_record[1]))
    team_opponent_stats[0].append(str(away_record[0]) + '-' + str(away_record[1]))
    team_opponent_stats[0].append(str(neutral_record[0]) + '-' + str(neutral_record[1]))
    team_opponent_stats[0].append(str(round(avg_win,1)))
    team_opponent_stats[0].append(str(round(avg_loss,1)))
    team_opponent_stats[0].append(str(schedule_stats[-1][-3]) + '-' + str(schedule_stats[-1][-2]))
    
    
    for i in range(len(team_opponent_stats)):
        for j in range(len(team_opponent_stats[i])):
            team_opponent_stats[i][j] = str(team_opponent_stats[i][j])
    
    top_players = find_relevant_players(player_stats)
    
    if team == 1:
        return print_team_report1(team_opponent_stats, school, top_players, site)
    else:
        return print_team_report2(team_opponent_stats, school, top_players, site)
    
    
def find_relevant_players(player_stats):
    
    
    indices = [2,3,4,5,6]
    leaders = []
    
    #pts,reb,ast,stl,blk
    for i in indices:
        current = []
        if i == 2:
            for k in range(3):
                max_name = ''
                max_num = 0
                player_fg = 0.0
                
                for j in range(len(player_stats)):
                    if player_stats[j][0] not in current:
                        if player_stats[j][i] > max_num:
                            max_num = player_stats[j][i]
                            max_name = player_stats[j][0]
                            player_fg = player_stats[j][8]
                current.append(max_name)
                current.append(max_num)
                current.append(str(round(float(player_fg)*100,1))+"%")
            
        else:
            max_name = ''
            max_num = 0
            for j in range(len(player_stats)):
                if player_stats[j][i] > max_num:
                    max_num = player_stats[j][i]
                    max_name = player_stats[j][0]
            current.append(max_name)
            current.append(max_num)
            
        leaders.append(current)
        
    return leaders

def print_team_report1(team_opponent_stats, school, top_players, site):
    
    report = ""
    team_name = ''
    school_array = school.split("-")
    for i in range(len(school_array)):
        school_array[i] = school_array[i].capitalize()
        if i != len(school_array)-1:
            team_name += school_array[i] + ' '
        else:
            team_name += school_array[i]

    
    subtitle = team_name + ":\n\n"
    report += subtitle
    
    r = random.randint(0,3)
    line_1 = ""
    
    if r==0:
        if site == 'h':
            line_1 = team_name + " has a " + team_opponent_stats[0][8] + " record on their home court"
        elif site == 'a':
            line_1 = team_name + " has a " + team_opponent_stats[0][9] + " record away from home"
        else:
            line_1 = team_name + " is " + team_opponent_stats[0][10] + " in neutral-site games"
        line_1 += " and is " + team_opponent_stats[0][13] + " overall this season. "
    elif r==1:
        if site == 'h':
            line_1 = "When playing at home, " + team_name + " has a record of " + team_opponent_stats[0][8] + ". "
        elif site == 'a':
            line_1 = "When playing on the road, " + team_name + " has a record of " + team_opponent_stats[0][9] + ". "
        else:
            line_1 = "When playing at a neutral site, " + team_name + " has a record of " + team_opponent_stats[0][10] + ". "
        line_1 += "Their total record this season is " + team_opponent_stats[0][13] + ". "
    elif r==2:
        if site == 'h':
            line_1 = "On their own floor, " + team_name + "'s win-loss record for the season is " + team_opponent_stats[0][8] + ". "
        elif site == 'a':
            line_1 = "On an opponent's floor, " + team_name + "'s win-loss record for the season is " + team_opponent_stats[0][9] + ". "
        else:
            line_1 = "On a neutral floor, " + team_name + "'s win-loss record for the season is " + team_opponent_stats[0][10] + ". "
        line_1 += "Overall, they are " + team_opponent_stats[0][13] + ". "
    else:
        if site == 'h':
            line_1 = "In games played at their own arena this season, " + team_name + " is " + team_opponent_stats[0][8] + ". "
        elif site == 'a':
            line_1 = "In games played at opposing arenas this season, " + team_name + " is " + team_opponent_stats[0][9] + ". "
        else:
            line_1 = "In games played at neutral arenas this season, " + team_name + " is " + team_opponent_stats[0][10] + ". "
        line_1 += "They have a " + team_opponent_stats[0][13] + " overall record. "
    report += line_1
    
    r = random.randint(0,3)
    if r==0:
        if int(team_opponent_stats[1][0][0:-2]) <= 100:
            line_2 = team_name + " is averaging an impressive " + team_opponent_stats[0][0] + " PPG, which ranks " + team_opponent_stats[1][0] + " in the nation. "
        elif int(team_opponent_stats[1][0][0:-2]) >= 250:
            line_2 = team_name + " is averaging a minor " + team_opponent_stats[0][0] + " PPG, which ranks " + team_opponent_stats[1][0] + " in the nation. "
        else:
            line_2 = team_name + " is averaging " + team_opponent_stats[0][0] + " PPG, which ranks " + team_opponent_stats[1][0] + " in the nation. "
        if int(team_opponent_stats[3][0][0:-2]) <= 100:
            line_2 += "Opponents are scoring a low " + team_opponent_stats[2][0] + " points on the " + team_name + " defense. "
        elif int(team_opponent_stats[3][0][0:-2]) >= 250:
            line_2 += "Opponents are scoring a high " + team_opponent_stats[2][0] + " points on the " + team_name + " defense. "
        else:
            line_2 += "Opponents are scoring " + team_opponent_stats[2][0] + " points on the " + team_name + " defense. "
    elif r==1:
        if int(team_opponent_stats[1][0][0:-2]) <= 100:
            line_2 = team_name + " excels on offense, scoring " + team_opponent_stats[0][0] + " PPG. This is good for " + team_opponent_stats[1][0] + " in the country. "
        elif int(team_opponent_stats[1][0][0:-2]) >= 250:
            line_2 = team_name + " struggles on offense, scoring " + team_opponent_stats[0][0] + " PPG. This leaves their offense at " + team_opponent_stats[1][0] + " in the country. "
        else:
            line_2 = team_name + "'s offense scores " + team_opponent_stats[0][0] + " PPG. This ranks their scoring in the middle of the pack at " + team_opponent_stats[1][0] + " in the country. "
        if int(team_opponent_stats[3][0][0:-2]) <= 100:
            line_2 += "Their stifling defense only allows " + team_opponent_stats[2][0] + " points per game. "
        elif int(team_opponent_stats[3][0][0:-2]) >= 250:
            line_2 += "Their below average defense allows " + team_opponent_stats[2][0] + " points per game. "
        else:
            line_2 += "Their defense allows " + team_opponent_stats[2][0] + " points per game. "
    elif r==2:
        if int(team_opponent_stats[1][0][0:-2]) <= 100:
            line_2 = team_name + " boasts a good offense that drops " + team_opponent_stats[0][0] + " PPG. This puts them at " + team_opponent_stats[1][0] + " in Division 1. "
        elif int(team_opponent_stats[1][0][0:-2]) >= 250:
            line_2 = team_name + " has a weak offense that only drops " + team_opponent_stats[0][0] + " PPG. This puts them at " + team_opponent_stats[1][0] + " in Divison 1. "
        else:
            line_2 = team_name + " has an average offense that drops " + team_opponent_stats[0][0] + " PPG. This puts them at " + team_opponent_stats[1][0] + " in Division 1. "
        if int(team_opponent_stats[3][0][0:-2]) <= 100:
            line_2 += "On the other side of the court, their top tier defense only yields " + team_opponent_stats[2][0] + " points per game. "
        elif int(team_opponent_stats[3][0][0:-2]) >= 250:
            line_2 += "On the other side of the court, their bottom tier defense yields " + team_opponent_stats[2][0] + " points per game. "
        else:
            line_2 += "On the other side of the court, their middle tier defense yields " + team_opponent_stats[2][0] + " points per game. "
    else:
        if int(team_opponent_stats[1][0][0:-2]) <= 100:
            line_2 = " Coming in at " + team_opponent_stats[1][0] + " in the country for scoring, " + team_name + "'s talented offense puts in " + team_opponent_stats[0][0] + " points per game. "
        elif int(team_opponent_stats[1][0][0:-2]) >= 250:
            line_2 = " Coming in at " + team_opponent_stats[1][0] + " in the country for scoring, " + team_name + "'s laboring offense puts in " + team_opponent_stats[0][0] + " points per game. "
        else:
            line_2 = " Coming in at " + team_opponent_stats[1][0] + " in the country for scoring, " + team_name + "'s mediocre offense puts in " + team_opponent_stats[0][0] + " points per game. "
        if int(team_opponent_stats[3][0][0:-2]) <= 100:
            line_2 += team_name + "'s defense is quite good, only giving up " + team_opponent_stats[2][0] + " points per game. "
        elif int(team_opponent_stats[3][0][0:-2]) >= 250:
            line_2 += team_name + "'s defense is not very good, giving up " + team_opponent_stats[2][0] + " points per game. "
        else:
            line_2 += team_name + "'s defense ranks right in the middle, giving up " + team_opponent_stats[2][0] + " points per game. "
    report += line_2
    
    r = random.randint(0,3)
    if r==0:
        line_3 = "This team shoots " + team_opponent_stats[0][1] + " from the field and " + team_opponent_stats[0][4] + " from the free throw line. "
        line_3 += "Additionally, " + team_name + " makes " + team_opponent_stats[0][5] + " threes per game on " + team_opponent_stats[0][3] + " shooting. "
    elif r==1:
        line_3 = "They are " + team_opponent_stats[0][1] + " and " + team_opponent_stats[0][3] + " from the field and the three point line, respectively. " + team_name + " makes "+ team_opponent_stats[0][5] + " threes per game. "
        line_3 += "From the free throw line, they are shooting " + team_opponent_stats[0][4] + ". "
    elif r==2:
        line_3 = team_name + " shoots " + team_opponent_stats[0][1] + " on field goals, " + team_opponent_stats[0][3] + " from three, and " + team_opponent_stats[0][4] + " from the free throw line. " 
        line_3 += "This includes " + team_opponent_stats[0][5] + " made threes per game. "
    else:
        line_3 = team_name + "'s offense combines to for a " + team_opponent_stats[0][1] + " made shot rate. This factors in their " + team_opponent_stats[0][3] + " three-point percentage while making an average of " + team_opponent_stats[0][5] + " threes per game. "
        line_3 += "After getting fouled, they shoot " + team_opponent_stats[0][4] + " from the charity stripe. "
    report += line_3
    
    line_4 = ""
    r = random.randint(0,3)
    if r==0:
        if team_opponent_stats[0][7] != '':
            streak_array = team_opponent_stats[0][7].split(' ')
            
            line_4 += team_name + " has been on a " + streak_array[1] + "-game "
            if streak_array[0] == 'W':
                line_4 += "winning streak. "
            else:
                line_4 += "losing streak. "
            report += line_4
    elif r==1:
        if team_opponent_stats[0][7] != '':
            streak_array = team_opponent_stats[0][7].split(' ')
            if streak_array[0] == 'W':
                line_4 += team_name + " has been playing well recently, winning the last " + streak_aray[1] + " games. "
            else:
                line_4 += team_name + " has had some tough sledding recently, losing the last " + streak_aray[1] + " games. "
            report += line_4
    elif r==2:
        if team_opponent_stats[0][7] != '':
            streak_array = team_opponent_stats[0][7].split(' ')
            if streak_array[0] == 'W':
                line_4 += team_name + " comes into this game having won the last " + streak_aray[1] + " games. "
            else:
                line_4 += team_name + " comes into this game having lost the last " + streak_aray[1] + " games. "
            report += line_4
    else:
        if team_opponent_stats[0][7] != '':
            streak_array = team_opponent_stats[0][7].split(' ')
            if streak_array[0] == 'W':
                line_4 += "Looking to continue what they've been doing, " + team_name + " brings a " + streak_aray[1] + "-game win streak into this game. "
            else:
                line_4 += "Looking to find a way to bounce back, " + team_name + " brings a " + streak_aray[1] + "-game losing streak into this game. "
            report += line_4
    
    r = random.randint(0,3)
    if r==0:
        line_5 = "In wins, " + team_name + " scores " + team_opponent_stats[0][11] + " more points than their opponent. "
        line_5 += "However, when they lose, they get beaten by an average of " + team_opponent_stats[0][12] + " points.\n\n"
    elif r==1:
        line_5 = "Their average win margin for the season is " + team_opponent_stats[0][11] + " points "
        line_5 += "and their average loss margin is " + team_opponent_stats[0][12] + " points.\n\n"
    elif r==2:
        line_5 = team_name + " defeats the opposition by an average of " + team_opponent_stats[0][11] + " points per win, "
        line_5 += "but they fall short by " + team_opponent_stats[0][12] + " points per loss.\n\n"
    else:
        line_5 = "The point differential when they win amounts to " + team_opponent_stats[0][11] + " points per game. "
        line_5 += "Meanwhile, it is " + team_opponent_stats[0][12] + " points when they lose.\n\n"
    report += line_5
    
    r = random.randint(0,3)
    if r==0:
        line_6 = team_name + " is led offensively by " + top_players[0][0] + ", who scores " + str(top_players[0][1]) + " points per game on " + top_players[0][2] + " shooting. "
        line_6 += top_players[0][3] + " adds a heavy scoring load with " + str(top_players[0][4]) + " PPG while shooting " + top_players[0][5] + ". "
        line_6 += team_name + " further receives help from " + top_players[0][6] + ", who shoots " + top_players[0][8] + " from the field and averages " + str(top_players[0][7]) + " PPG. "
    elif r==1:
        line_6 = top_players[0][0] + " spearheads " + team_name + "'s scoring, collecting " + str(top_players[0][1]) + " points per game while shooting " + top_players[0][2] + " from the field. "
        line_6 += "Along with " + top_players[0][0].split()[-1] + ", " + top_players[0][3] + " helps offensively, scoring " + str(top_players[0][4]) + " PPG on " + top_players[0][5] + " shooting. "
        line_6 += "One more contributor is " + top_players[0][6] + ", who gives " + team_name + " " + str(top_players[0][7]) + " PPG while shooting at a " + top_players[0][8] + " clip. "
    elif r==2:
        line_6 = team_name + "'s scoring is fueled by " + top_players[0][0] + ", aggregating " + str(top_players[0][1]) + " points per game on " + top_players[0][2] + " shooting. "
        line_6 += top_players[0][3] + " compounds " + str(top_players[0][4]) + " more points per game with a shooting percentage of " + top_players[0][5] + ". "
        line_6 += "The third leading scorer for " + team_name + " is " + top_players[0][6] + ", who drops " + str(top_players[0][7]) + " PPG and is " + top_players[0][8] + " from the field. "
    else:
        line_6 = "The leading scorer for this squad is " + top_players[0][0] + ", who  pours in " + str(top_players[0][1]) + " points per game and shoots " + top_players[0][2] + " from the field. "
        line_6 += top_players[0][3] + " brings " + str(top_players[0][4]) + " PPG to the table while shooting " + top_players[0][5] + ". "
        line_6 += top_players[0][6] + " supports " + top_players[0][0].split()[-1] + " and " + top_players[0][3].split()[-1] + " by shooting " + top_players[0][8] + " on field goals and tallying " + str(top_players[0][7]) + " points per game. "
    report += line_6
    
    r = random.randint(0,3)
    if r==0:
        if top_players[2][0] in report:
            line_7 = top_players[2][0].split()[-1] + " also facilitates the offense, collecting " + str(top_players[2][1]) + " assists per game. "
        else:
            line_7 = top_players[2][0] + " facilitates the offense, collecting " + str(top_players[2][1]) + " assists per game. "
    elif r==1:
        if top_players[2][0] in report:
            line_7 = top_players[2][0].split()[-1] + " also helps others score by dealing out " + str(top_players[2][1]) + " assists per game. "
        else:
            line_7 = top_players[2][0] + " helps others score by dealing out " + str(top_players[2][1]) + " assists per game. "
    elif r==2:
        if top_players[2][0] in report:
            line_7 = top_players[2][0].split()[-1] + " also finds open teammates and amasses " + str(top_players[2][1]) + " assists per game. "
        else:
            line_7 = top_players[2][0] + " finds open teammates and amasses " + str(top_players[2][1]) + " assists per game. "
    else:
        if top_players[2][0] in report:
            line_7 = "While also a scorer, " + top_players[2][0].split()[-1] + " leads the team in assists too, racking up assists per game. "
        else:
            line_7 = "Though not as much of a scorer, " + top_players[2][0].split() + " leads the team in assists, racking up assists per game. "
    report += line_7
    
    r = random.randint(0,3)
    if r==0:
        if top_players[1][0] in report:
            line_8 = top_players[1][0].split()[-1] + " additionally leads " + team_name + " on the glass grabbing " + str(top_players[1][1]) + " rebounds per game. "
        else:
            line_8 = top_players[1][0] + " leads " + team_name + " on the glass grabbing " + str(top_players[1][1]) + " rebounds per game. "
    elif r==1:
        if top_players[1][0] in report:
            line_8 = top_players[1][0].split()[-1] + " also crashes the boards, cleaning up " + str(top_players[1][1]) + " rebounds per game. "
        else:
            line_8 = top_players[1][0] + " crashes the boards , cleaning up " + str(top_players[1][1]) + " rebounds per game. "
    elif r==1:
        if top_players[1][0] in report:
            line_8 = "All over the court, " + top_players[1][0].split()[-1] + " also grabs " + str(top_players[1][1]) + " rebounds per game, leading the team. "
        else:
            line_8 = top_players[1][0] + " grabs " + str(top_players[1][1]) + " rebounds per game, leading the team. "
    else:
        if top_players[1][0] in report:
            line_8 = top_players[1][0].split()[-1] + " helps the team in various ways, adding " + str(top_players[1][1]) + " rebounds per game to the stat sheet. "
        else:
            line_8 = top_players[1][0] + " finds a way to help the team down low, bringing in " + str(top_players[1][1]) + " rebounds per game to lead the team. "
    report += line_8
    
    r = random.randint(0,3)
    if r==0:
        if top_players[3][0] in report:
            line_9 = team_name + "'s defense is anchored by " + top_players[3][0].split()[-1] + ", who has " + str(top_players[3][1]) + " steals per game and "
        else:
            line_9 = team_name + "'s defense is anchored by " + top_players[3][0] + ", who has " + str(top_players[3][1]) + " steals per game and "
        if top_players[4][0] in report:
            line_9 += top_players[4][0].split()[-1] + " protecting the rim with " + str(top_players[4][1]) + " blocks per game. "
        else:
            line_9 += top_players[4][0] + " protecting the rim with " + str(top_players[4][1]) + " blocks per game. "
    elif r==1:
        if top_players[3][0] in report:
            line_9 = "Defensively, " + top_players[3][0].split()[-1] + " leads " + team_name + ", swiping "  + str(top_players[3][1]) + " steals per game. "
        else:
            "Defensively, " + top_players[3][0] + " leads " + team_name + ", swiping "  + str(top_players[3][1]) + " steals per game. "
        if top_players[4][0] in report:
            line_9 += "Further helping on defense is " + top_players[4][0].split()[-1] + ", who disrupts the lane with " + str(top_players[4][1]) + " blocks per game. "
        else:
            line_9 += "Further helping on defense is " + top_players[4][0] + ", who disrupts the lane with " + str(top_players[4][1]) + " blocks per game. "
    elif r==2:
        if top_players[3][0] in report:
            line_9 = "On the defensive end, " + top_players[3][0].split()[-1] + " complements his offense with " + str(top_players[3][1]) + " steals per game. "
        else:
            "On the defensive end, the steals leader for " + team_name + " is " + top_players[3][0] + " who rounds up "  + str(top_players[3][1]) + " steals per game. "
        if top_players[4][0] in report:
            line_9 += "Defending the basket is " + top_players[4][0].split()[-1] + ", who blocks opponents' shots " + str(top_players[4][1]) + " times per game. "
        else:
            line_9 += "Defending the basket is " + top_players[4][0] + ", who blocks opponents' shots " + str(top_players[4][1]) + " times per game. "
    else:
        if top_players[3][0] in report:
            line_9 = "Not just an offensive threat, " + top_players[3][0].split()[-1] + "'s fast hands create havoc on the defensive end as he gathers " + str(top_players[3][1]) + " steals per game. "
        else:
            top_players[3][0] + "'s fast hands create havoc on the defensive end as he gathers " + str(top_players[3][1]) + " steals per game. "
        if top_players[4][0] in report:
            line_9 += top_players[4][0].split()[-1] + " carries a lot of presence near the basket, blocking " + str(top_players[4][1]) + " shots per game. "
        else:
            line_9 += top_players[4][0].split() + " carries a lot of presence near the basket, blocking " + str(top_players[4][1]) + " shots per game. "
    report += line_9
    
    return report
    

def print_team_report2(team_opponent_stats, school, top_players, site):
    report = ""
    team_name = ''
    school_array = school.split("-")

    for i in range(len(school_array)):
        school_array[i] = school_array[i].capitalize()
        if i != len(school_array)-1:
            team_name += school_array[i] + ' '
        else:
            team_name += school_array[i]

    subtitle = team_name + ":\n\n"
    report += subtitle

    line_1 = ""
    r = random.randint(0,2)
    if r==0:
        if site == 'h':
            line_1 = team_name + " is " + team_opponent_stats[0][8] + " on their home court"
        elif site == 'a':
            line_1 = team_name + " is " + team_opponent_stats[0][9] + " away from home"
        else:
            line_1 = team_name + " is " + team_opponent_stats[0][10] + " in neutral-site games"
        line_1 += " and is " + team_opponent_stats[0][13] + " overall this season. "
    elif r==1:
        if site == 'h':
            line_1 = "When defending their home court, " + team_name + " is " + team_opponent_stats[0][8]
        elif site == 'a':
            line_1 = "On the road " + team_name + " is " + team_opponent_stats[0][9]
        else:
            line_1 = "In games at neutral sites, " + team_name + " is " + team_opponent_stats[0][10]
        line_1 += " while they have accumulated a total record of " + team_opponent_stats[0][13] + " this season. "
    else:
        if site == 'h':
            line_1 = "At home " + team_name + " has a record of " + team_opponent_stats[0][8]
        elif site == 'a':
            line_1 = "When traveling, " + team_name + " has a record of " + team_opponent_stats[0][9]
        else:
            line_1 = "In neutral site games " + team_name + " has a record of " + team_opponent_stats[0][10]
        line_1 += ", and is " + team_opponent_stats[0][13] + " in all competitions. "
    report += line_1

    r = random.randint(0,2)
    if r==0:
        if int(team_opponent_stats[1][0][0:-2]) <= 100:
            line_2 = "They are ranked " + team_opponent_stats[1][0] + " in the nation with a strong "+ team_opponent_stats[0][0] + " points per game. "
        elif int(team_opponent_stats[1][0][0:-2]) >= 250:
            line_2 = "They are ranked " + team_opponent_stats[1][0] + " in the nation with a underwhelming "+ team_opponent_stats[0][0] + " points per game. "
        else:
            line_2 = "They are ranked " + team_opponent_stats[1][0] + " in the nation with "+ team_opponent_stats[0][0] + " points per game. "
        if int(team_opponent_stats[3][0][0:-2]) <= 100:
            line_2 += team_name + "'s defense is very solid, only allowing " + team_opponent_stats[2][0] + " points per game. "
        elif int(team_opponent_stats[3][0][0:-2]) >= 250:
            line_2 += team_name + "'s defense has some holes, allowing " + team_opponent_stats[2][0] + " points per game. "
        else:
            line_2 += team_name + "'s defense treads water, allowing " + team_opponent_stats[2][0] + " points per game. "
    elif r==1:
        if int(team_opponent_stats[1][0][0:-2]) <= 100:
            line_2 = "Their excellent "+ team_opponent_stats[0][0] + " points per game have earned them the " + team_opponent_stats[1][0] + " rank in the nation. "
        elif int(team_opponent_stats[1][0][0:-2]) >= 250:
            line_2 = "Their disappointing "+ team_opponent_stats[0][0] + " points per game have earned them the " + team_opponent_stats[1][0] + " rank in the nation. "
        else:
            line_2 = "Their middling "+ team_opponent_stats[0][0] + " points per game have earned them the " + team_opponent_stats[1][0] + " rank in the nation. "
        if int(team_opponent_stats[3][0][0:-2]) <= 100:
            line_2 += "On the defensive end of the floor, " + team_name + " concedes very few chances, only giving opposing teams " + team_opponent_stats[2][0] + " points per game. " 
        elif int(team_opponent_stats[3][0][0:-2]) >= 250:
            line_2 += "On the defensive end of the floor, " + team_name + " concedes many chances, giving opposing teams " + team_opponent_stats[2][0] + " points per game. "
        else:
            line_2 += "On the defensive end of the floor, " + team_name + " does fine, giving opposing teams " + team_opponent_stats[2][0] + " points per game. "
    else:
        if int(team_opponent_stats[1][0][0:-2]) <= 100:
            line_2 = "Their offense has had success this season, putting in "+ team_opponent_stats[0][0] + " points per game. This ranks " + team_opponent_stats[1][0] + " in the NCAA. "
        elif int(team_opponent_stats[1][0][0:-2]) >= 250:
            line_2 = "Their offense has been subpar this season, putting in just "+ team_opponent_stats[0][0] + " points per game. This ranks " + team_opponent_stats[1][0] + " in the NCAA. "
        else:
            line_2 = "Their offense has been decent this season, putting in "+ team_opponent_stats[0][0] + " points per game. This ranks " + team_opponent_stats[1][0] + " in the NCAA. "
        if int(team_opponent_stats[3][0][0:-2]) <= 100:
            line_2 += team_name + "'s defense has had a great season so far, with opposing teams only scoring " + team_opponent_stats[2][0] + " points per game. "
        elif int(team_opponent_stats[3][0][0:-2]) >= 250:
            line_2 += team_name + "'s defense has had a slow season so far, with opposing teams scoring " + team_opponent_stats[2][0] + " points per game. "
        else:
            line_2 += team_name + "'s defense has had a moderate season so far, with opposing teams scoring " + team_opponent_stats[2][0] + " points per game. "
    report += line_2

    r = random.randint(0,2)
    if r==0:
        line_3 = team_name + " is shooting " + team_opponent_stats[0][1] + " from the field on the season. They make " + team_opponent_stats[0][5] + " three-pointers per game on " + team_opponent_stats[0][3] + " shooting from deep. "
        line_3 += "From the free throw line, they are shooting " + team_opponent_stats[0][4] + ". "
    elif r==1:
        line_3 = "On the season " + team_name + " has scored on " + team_opponent_stats[0][1] + " of their attempts from the field. From beyond the arc they make " + team_opponent_stats[0][5] + " shots per game at a " + team_opponent_stats[0][3] + " clip. "
        line_3 += "They also shoot " + team_opponent_stats[0][4] + " from the foul line. "
    else:
        line_3 = team_name + " puts in " + team_opponent_stats[0][1] + " of their shots this season. "
        line_3 += "They shoot " + team_opponent_stats[0][4] + " on their foul shots. When behind the 3-point line, they make on " + team_opponent_stats[0][3] + " of their long shots on " + team_opponent_stats[0][5] + " tries per game. "
    report += line_3

    line_4 = ""
    r = random.randint(0,2)
    if r==0:
        if team_opponent_stats[0][7] != '':
            streak_array = team_opponent_stats[0][7].split(' ')
            line_4 += team_name + " is currently on a " + streak_array[1] + "-game "
            if streak_array[0] == 'W':
                line_4 += "winning streak. "
            else:
                line_4 += "losing streak. "
            report += line_4
    elif r==1:
        if team_opponent_stats[0][7] != '':
            streak_array = team_opponent_stats[0][7].split(' ')
            line_4 += team_name + " is coming in "
            if streak_array[0] == 'W':
                line_4 += "hot, having won their last " + streak_array[1] + ". "
            else:
                line_4 += "cold, having lost their last " + streak_array[1] + ". "
            report += line_4
    else:
        if team_opponent_stats[0][7] != '':
            streak_array = team_opponent_stats[0][7].split(' ')
            line_4 += team_name
            if streak_array[0] == 'W':
                line_4 += " has won " + streak_array[1] + " in a row on their current hot streak. "
            else:
                line_4 += " has lost " + streak_array[1] + " in a row on their current cold streak. "
            report += line_4

    r = random.randint(0,2)
    if r==0:
        line_5 = team_name + " beats their opponents by an average of " + team_opponent_stats[0][11] + " points when they win, but "
        line_5 += "when they lose, they are outscored by " + team_opponent_stats[0][12] + " points per game.\n\n"
    elif r==1:
        line_5 = "When " + team_name + " wins, they beat their opponents by an average of " + team_opponent_stats[0][11] + " points, but "
        line_5 += "they are bested by " + team_opponent_stats[0][12] + " points in their losses.\n\n"
    else:
        line_5 = "In victory, " + team_name + " puts up " + team_opponent_stats[0][11] + " more points than their opponents, but "
        line_5 += "in losses they put up " + team_opponent_stats[0][12] + " fewer points.\n\n"
    report += line_5

    r = random.randint(0,2)
    if r==0:
        line_6 = top_players[0][0] + " leads the scoring for " + team_name + " with " + str(top_players[0][1]) + " points per game while shooting " + top_players[0][2] + ". "
        line_6 += top_players[0][3] + " also chips in with " + str(top_players[0][4]) + " PPG on " + top_players[0][5] + " shooting. "
        line_6 += top_players[0][6] + " supports " + top_players[0][0].split()[-1] + " and " + top_players[0][3].split()[-1] + ", adding " + str(top_players[0][7]) + " PPG while shooting " + top_players[0][8] + " from the field. "
    elif r==1:
        line_6 = team_name + "'s leading scorer is " + top_players[0][0] + ", who pours in " + str(top_players[0][1]) + " points per game on " + top_players[0][2] + " shooting. "
        line_6 += top_players[0][3] + " contributes " + str(top_players[0][4]) + " PPG while shooting " + top_players[0][5] + ". "
        line_6 += "Giving the team " + str(top_players[0][7]) + " points and shooting at an " + top_players[0][8] + " clip, "+ top_players[0][6] + " complements " + top_players[0][0].split()[-1] + " and " + top_players[0][3].split()[-1] + " nicely as a third option. "
    else:
        line_6 = "The best scorer on " + team_name + " this season is " + top_players[0][0] + ", averaging " + str(top_players[0][1]) + " points per game on " + top_players[0][2] + " shooting. "
        line_6 += "Behind him is " + top_players[0][3] + ", who drops " + str(top_players[0][4]) + " PPG on " + top_players[0][5] + " shooting. "
        line_6 += top_players[0][6] + " adds more scoring to the offensive leaders " + top_players[0][0].split()[-1] + " and " + top_players[0][3].split()[-1] + " by giving the team " + str(top_players[0][7]) + " points while shooting " + top_players[0][8] + " from the field. "
    report += line_6

    r = random.randint(0,2)
    if r==0:
        if top_players[2][0] in report:
            line_7 = top_players[2][0].split()[-1] + " helps control the offense by adding " + str(top_players[2][1]) + " assists per game. "
        else:
            line_7 = top_players[2][0] + " finds the scorers, dishing out " + str(top_players[2][1]) + " assists per game. "
    elif r==1:
        if top_players[2][0] in report:
            line_7 = top_players[2][0].split()[-1] + " is the floor general on offense, throwing " + str(top_players[2][1]) + " assists per game. "
        else:
            line_7 = top_players[2][0] + " affects the scoring in a different way, accumulating " + str(top_players[2][1]) + " assists per game. "
    else:
        if top_players[2][0] in report:
            line_7 = "Passing comes easily to " + top_players[2][0].split()[-1] + " who records " + str(top_players[2][1]) + " assists per game. "
        else:
            line_7 = "Passing comes easily to " + top_players[2][0] + " who records " + str(top_players[2][1]) + " assists per game. "
    report += line_7

    r = random.randint(0,2)
    if r==0:
        if top_players[1][0] in report:
            line_8 = top_players[1][0].split()[-1] + " contributes on the boards as well, collecting " + str(top_players[1][1]) + " rebounds per game. "
        else:
            line_8 = top_players[1][0] + " leads " + team_name + " on the boards, collecting " + str(top_players[1][1]) + " rebounds per game. "
    elif r==1:
        if top_players[1][0] in report:
            line_8 = top_players[1][0].split()[-1] + " is also a great rebounder, grabbing " + str(top_players[1][1]) + " boards per game. "
        else:
            line_8 = "Though not a top-3 scorer, " + top_players[1][0] + " commands the paint, bringing down " + str(top_players[1][1]) + " boards per game. "
    else:
        if top_players[1][0] in report:
            line_8 = top_players[1][0].split()[-1] + " is an aggressive rebounder, and his " + str(top_players[1][1]) + " RPG show it in the stat sheet. "
        else:
            line_8 = top_players[1][0] + " is an aggressive rebounder, and his " + str(top_players[1][1]) + " RPG show it in the stat sheet. "
    report += line_8

    r = random.randint(0,2)
    if r==0:
        if top_players[3][0] in report:
            line_9 = top_players[3][0].split()[-1] + " leads " + team_name + "'s defense with "+ str(top_players[3][1]) + " steals per game. "
        else:
            line_9 = top_players[3][0] + " leads " + team_name + "'s defense with "+ str(top_players[3][1]) + " steals per game. "
        if top_players[4][0] in report:
            line_9 += top_players[4][0].split()[-1] + " defends the basket, racking up " + str(top_players[4][1]) + " blocks per game. "
        else:
            line_9 += top_players[4][0] + " defends the basket, racking up " + str(top_players[4][1]) + " blocks per game. "
    elif r==1:
        if top_players[3][0] in report:
            line_9 = top_players[3][0].split()[-1] + "'s pesky defense results in " + str(top_players[3][1]) + " steals per game. "
        else:
            line_9 = top_players[3][0] + "'s pesky defense results in " + str(top_players[3][1]) + " steals per game. "
        if top_players[4][0] in report:
            line_9 += top_players[4][0].split()[-1] + " makes opponents think twice before entering the lane, sending back " + str(top_players[4][1]) + " shots per game. "
        else:
            line_9 += top_players[4][0] + " makes opponents think twice before entering the lane, sending back " + str(top_players[4][1]) + " shots per game. "
    else:
        if top_players[3][0] in report:
            line_9 = "A nuisance for opposing offenses, " + top_players[3][0].split()[-1] + "'s " + str(top_players[3][1]) + " steals per game help " + team_name + " win the ball back. "
        else:
            line_9 = "A nuisance for opposing offenses, " + top_players[3][0] + "'s " + str(top_players[3][1]) + " steals per game help " + team_name + " win the ball back. "
        if top_players[4][0] in report:
            line_9 += top_players[4][0].split()[-1] + " is a force to be reckoned with in the paint, blocking " + str(top_players[4][1]) + " shots per game. "
        else:
            line_9 += top_players[4][0] + " is a force to be reckoned with in the paint, blocking " + str(top_players[4][1]) + " shots per game. "
    report += line_9

    return report

def print_title_report(school1, school2, site1,date):
    title = ""
    school_array1 = school1.split("-")
    school_array2 = school2.split("-")
    school1 = ""
    school2 = ""
    for i in range(len(school_array1)):
        school_array1[i] = school_array1[i].capitalize()
        if i != len(school_array1)-1:
            school1 += school_array1[i] + ' '
        else:
            school1 += school_array1[i]
                       
    for i in range(len(school_array2)):
        school_array2[i] = school_array2[i].capitalize()
        if i != len(school_array2)-1:
            school2 += school_array2[i] + ' '
        else:
            school2 += school_array2[i]
            
    if site1 == 'h':
        title += date + " " + school2 + " @ " + school1
    elif site1 == 'a':
        title += date + " " + school1 + " @ " + school2
    else:
        title += date + " " + school1 + " vs " + school2
    return title

if __name__ == "__main__":
    date = input("Enter the date: ") #don't use slashes
    school1 = input("Enter school name: ") #as it appears in the url (lower case, dashes instead of spaces)
    school2 = input("Enter school name: ")
    site1 = input("Enter game site (H,A,N): ").lower()
    if site1 == 'h':
        site2 = 'a'
    elif site1 == 'a':
        site2 = 'h'
    else:
        site2 = 'n'
    game_file = open(print_title_report(school1,school2,site1,date), 'w')
    game_file.write(print_title_report(school1,school2,site1,date) + "\n\n\n" + scrape(school1, site1, 1) + "\n\n\n" + scrape(school2, site2, 2))
    game_file.close()
    
    
