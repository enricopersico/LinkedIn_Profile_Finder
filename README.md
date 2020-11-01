## Creator/Author: Enrico Persico, 2020

# 'linkFinder' program
This is the program I created using the scrapy python framework to get links based on a set of csv's which included any of the following criteria: name, affiliation, and country of origin. It takes these criteria and formulates a bing search query url, and finds the webpage, from which it can then take all the viable links. It outputs all these links to an unfiltered output csv. Then, I used PostgreSQL to create other csv's based on certain criteria, like the amount of matches to the name, or for the amount of initial information associated with the name (country of origin/affiliation). I then put these filtered and unfiltered output csv's into the outputs_from_linkFinder folder for easy access.
### go to 'linkFinder/linkFinder/spiders/prospectProfiles.py' for information on how to actually run the program

# 'outputs_from_linkFinder' folder of csv's
This folder is used to store the csv's created by my linkFinder program and postreSQL queries.
### 'outputs_from_linkFinder/filtered' is for the csv's created by the postgreSQL queries, which are filtered by number of matches and by the amount of initial information associated with the name (country of origin/affiliation)
### 'outputs_from_linkFinder/unfiltered' is for the csv created by the linkFinder program which I copied into the 'profileScraper/input' folder of  the profileScraper program

# 'profileScraper' program
This is the program I created using the selenium webdriver library to scrape the links based on the output csv's from the 'linkFinder' program. It takes these links, logs into linkedIn, follows the links to the pages, reveals all the hidden information in the pages, and then saves the raw html to an output directory at 'profileScraper/output' for later parsing. This directory is based on the person's name, and then profile url because there may be multiple profiles per name.
### go to 'profileScraper/profile_scraper.py' for information on how to actually run the program