# Project Luther - Predicting a Hike's Rating
## Spencer Tollefson
## October 12, 2018

# Project Design
WTA.org is a website that has a database of 3,555 hikes (at the time of scraping) which includes hike details, trip reports, and a voting system allowing users to rate a scale on a scale of 1-5. The idea of this project was to see if the given information in this database would allow one to predict how highly a hike scored on the voting system. A good model potentially could aid "trail planners" with the foresight to predict how well-liked a newly opened hike would do before they invested in creating the trail.

Although I originally hoped to use nearly all the features I scraped as well as create some new ones, time constraints did not allow in time for project completion. Chiefly, the lat/long coordinates and sub-regions of the hikes both offer unique insights and were not incorporated in my models. Additionally, using other sources of data such as weather patterns/history and alltrails.com were skipped due to time constraints.

Initially, I hoped to create the model without using features that a trail planner would not have access to: such as the use of how many times people had rated a trail and the number of trip reports that were left for the trail. After some simple linear regressions built with those features excluded, it became clear the model had little value. Thus, I decided to use all data available to me.

This project used the following models:

# Tools

# Data

# What I Would Do Differently

# Appendix


