README

CSC353 Final Project
Authors: Izzy Moody, Henry Howell, Dominic Flocco, Gabe Levy

This project implements a full-stack application that creates and maintains a working webpage
of season- and game-level baseball data. Data is scraped from various online sources, stores this data
into a local mySQL database, creates procedures to aggregate and query the data usefully, and implements
a front-end user interface for users to explore the database.

Data is scraped from baseball-reference.com and baseballsavant.mlb.com and reflects game and season level
statistics for pitchers and batters in Major League Baseball (MLB) from 2015 through the 2021 season.

Here is a brief description of how the repository is organized, and how it can be executed:

data -> contains BSB reference data, savant data, stathead data, game results, and player info scraped from web
scraping -> includes 3 python data scrapers:
	scraperGames.py: scrapes game result data from baseball-reference.com
	scraperPlayerData.py: scrapes player info data from baseball-reference.com
	scraperGamelogs.py: scrapes game leve data for all players from baseball-reference.com
WebPage -> folder which contains:
	index.php -> homepage for main website
	assets -> folder which holds css style sheet, an image and 7 php pages
sql -> includes sql schema, functions and procedures
	8 sql procedures, 2 sql functions and 6 table schema

BaseballDataImporter.py -> imports scraped data into mySQL database (takes about 20 minutes to run)


Steps for compiling stack: 
	Prep) scrape data using py files in scraping directory and save to csv in data directory
	1) Run BaseballDataImporter.py to populate database 
	2) Run procedure scripts in sql directory to create procedures and functions to query data
	3) a localhost via PHP within the WebPage directory through the command "php -S localhost:3333"
		+ then navigate to the index.php file on the localhost
		+ assets/php -> contains each PHP handler page that runs each procedure from procedures.sql
