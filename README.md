# MLB Stats Project
by Vishal Patel and Scott Bronder

If you follow baseball at all you know baseball is all about stats and advanced statistics is playing a vital role in the evolution of the game. As a viewer you really only get presented the end result during broadcast with little to no insight on how that data was collected. Being fans of baseball we decided to take a deeper dive into some of baseballs data and create some comparisons of our own. 


## Requirements
		- Flask (for the website) 
		- SQL Alchemy (for ORM) 
		- Dash (for graphing)
		- Plotly (for graphing)
		- Beautiful Soup (for scraping)
		- Requests (for making requests to http)
		
		


We started by finding some data. This was an easy task with baseball stats being plentiful on the internet and often times in a very easily digestable format (programatically speaking). We started with a test scrape of Baseball Reference(https://www.baseball-reference.com/) and quickly found the data we would need to get started. It was decided that we wanted to split stats into two tables: offensive and defensive stats and with Beautiful Soup we made quick work of grabbing this data for all current teams for all years dating back to 1906. We then populated this data into our SQLite database creating four tables including Teams, Offensive Stats, Defensive Stats, and World Series Winners. Using SQL Alchemy we queried our database and fed them into Dash to visualize our data. Below are the graphs we created. The team in red each year is the world series winner in order to easily see correlation between stats and/or trends and world series wins.  

![Offensive Stats](https://github.com/vishalpatel2890/mlb-stats-project/blob/master/Screen%20Shot%202018-11-19%20at%208.37.48%20AM.png)

![Defensive Stats](https://github.com/vishalpatel2890/mlb-stats-project/blob/master/Screen%20Shot%202018-11-19%20at%208.27.01%20AM.png)
      
![Comparing Two Stats](https://github.com/vishalpatel2890/mlb-stats-project/blob/master/Screen%20Shot%202018-11-19%20at%208.28.35%20AM.png)



To run : 
	git clone https://github.com/vishalpatel2890/mlb-stats-project.git
	cd mlb-stats-project
	python run.py
	navigate to localhost:5000/dash and localhost:5000/dashboard
