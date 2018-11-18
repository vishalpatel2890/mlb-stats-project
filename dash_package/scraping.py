import requests
from bs4 import BeautifulSoup

from dash_package.model import *
import re
from sqlalchemy.orm import sessionmaker
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///baseball.db')

# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#build Teams
class TeamStatsBuilder:
    def run(self):
        #class for scraping teams
        ts = TeamScraper()
        #class for scraping stats
        ss = StatsScraper()
        #get html of teams page
        ts.teamsHTML()
        #for parsing html elements and returning desired text
        teamParser = TeamParser()
        statParser = StatParser()
        teams = []
        #for each team
        for team in ts.teamList():
            #clear new_team_instance so if nothing is found previous team_instance doesn't get duplicated
            #we pulled all 'tr' classes some are empty
            new_team_instance = None
            teamName = teamParser.team_name(team)
            # create Team Instance
            if teamName:
                new_team_instance = Team(name=teamName)
            # url for offese/defense data
            if new_team_instance:
                url = teamParser.team_url(team)
            #for each batting stat (year) create offensive stats instance
            # add offensive stat to team
            for row in ss.battingHTML(url)[0:]:
                league = statParser.league(row)
                if league:
                    division = statParser.division(row)
                    year = statParser.year(row)
                    wins = statParser.wins(row)
                    runs_scored = statParser.runs_scored(row)
                    home_runs = statParser.home_runs(row)
                    batting_avg = statParser.batting_average(row)
                    ops = statParser.ops(row)
                    avg_age = statParser.avg_age(row)
                    offensive_stats_instance = Offensive_Stats(league=league, division=division, year=year, wins=wins, runs_scored=runs_scored, home_runs=home_runs, batting_avg=batting_avg, ops=ops, avg_age=avg_age)
                    offensive_stats_instance.team = new_team_instance
            #for each pitching stat (year) create defensive stats instance
            # add defensive stat to team
            for row in ss.pitchingHTML(url)[1:]:
                year = statParser.year(row)
                if year:
                    print(year)
                    losses = statParser.losses(row)
                    runs_allowed = statParser.runs_allowed(row)
                    era = statParser.era(row)
                    earned_runs = statParser.earned_runs(row)
                    strikeouts = statParser.strikeouts(row)
                    field_percent = statParser.fielding_percent(row)
                    avg_age = statParser.avg_age_picther(row)
                    defensive_stats_instance = Defensive_Stats(year=year, losses=losses, runs_allowed=runs_allowed, era=era, earned_runs=earned_runs, strikeouts=strikeouts, field_percent=field_percent)
                    defensive_stats_instance.team = new_team_instance
            if new_team_instance:
                teams.append(new_team_instance)
        #return list of teams with offensive and defensive teams -> session.addall -> session.commit
        return teams

#build WS winner instance for each year WS was wan
class WSStatsBuilder:
    def run(self):
        wswins = []
        wsParser = WSParser()
        for team in wsParser.zip():
            team_obj = session.query(Team).filter(Team.name.like(f"%{team[0]}%")).first()
            ws_instance = WS_Winners(year=team[1], name=team[0], team=team_obj)
            wswins.append(ws_instance)
        return wswins


class TeamScraper:
    #scrape html from teams page
    def teamsHTML(self):
        url = 'https://www.baseball-reference.com/teams/'
        br_request = requests.get(url)
        br_content = br_request.content
        self.br_soup = BeautifulSoup(br_content, 'html.parser')
        print(br_request)
        return self.br_soup

    #create list of team elements('tr')
    def teamList(self):
        teams_soup = self.br_soup
        teams = teams_soup.findAll('tr')[2:]
        self.teams = teams
        return self.teams


class StatsScraper:
    def battingHTML(self, url):
        batting_request = requests.get('https://www.baseball-reference.com' + url + 'batteam.shtml')
        soup = BeautifulSoup(batting_request.content, 'html.parser')
        return soup.findAll('tr')

    def pitchingHTML(self, url):
        pitching_request = requests.get('https://www.baseball-reference.com' + url + 'pitchteam.shtml')
        soup = BeautifulSoup(pitching_request.content, 'html.parser')
        return soup.findAll('tr')


class WSScraper:
    def ws_winners(self):
        ws_team_request = requests.get('https://www.topendsports.com/events/baseball-world-series/winning-teams.htm')
        soup = BeautifulSoup(ws_team_request.content, 'html.parser')
        return soup.findAll('td')[572::-5]

    def ws_years(self):
        ws_year_request = requests.get('https://en.wikipedia.org/wiki/List_of_World_Series_champions')
        soup = BeautifulSoup(ws_year_request.content, 'html.parser')
        return soup.findAll('th', {'scope': 'row'})

#winners and years scraper
class WSScraper:
    def ws_winners(self):
        ws_team_request = requests.get('https://www.topendsports.com/events/baseball-world-series/winning-teams.htm')
        soup = BeautifulSoup(ws_team_request.content, 'html.parser')
        return soup.findAll('td')[571:: -5]

    def ws_years(self):
        ws_year_request = requests.get('https://en.wikipedia.org/wiki/List_of_World_Series_champions')
        soup = BeautifulSoup(ws_year_request.content, 'html.parser')
        return soup.findAll('th', {'scope': 'row'})

#parse team elements 
class TeamParser:
    def team_name(self, html):
        try:
            teamNameElement = html.find('td', {'data-stat': 'franchise_name'}).findNext()
        except:
            teamNameElement = None
        if teamNameElement:
            return teamNameElement.text

    def team_url(self, html):
        teamURLElement = html.find('td', {'data-stat': 'franchise_name'}).findNext()
        return teamURLElement.get('href')

#parser class for parsing different elements
class StatParser:
    def league(self, html):
        leagueElement = html.find('td', {'data-stat': 'lg_ID'})
        if leagueElement:
            return leagueElement.findNext().text[: 2]

    def division(self, html):
        leagueText = html.find('td', {'data-stat': 'lg_ID'}).text
        if len(leagueText) > 2:
            division_text = leagueText[3:]
        else:
            division_text = leagueText
        return division_text

    def year(self, html):
        return html.find('th', {'data-stat': 'year_ID'}).findNext().text

    def wins(self, html):
        return self.parse_data_stat(html, 'W').text

    def runs_scored(self, html):
        return self.parse_data_stat(html, 'R').text

    def home_runs(self, html):
        return self.parse_data_stat(html, 'HR').text

    def batting_average(self, html):
        return self.parse_data_stat(html, 'batting_avg').text

    def ops(self, html):
        return self.parse_data_stat(html, 'onbase_plus_slugging').text

    def avg_age(self, html):
        return self.parse_data_stat(html, 'age_bat').text

    def losses(self, html):
        return self.parse_data_stat(html, 'L').text

    def runs_allowed(self, html):
        return self.parse_data_stat(html, 'R_p').text

    def earned_runs(self, html):
        return self.parse_data_stat(html, 'ER').text

    def era(self, html):
        return self.parse_data_stat(html, 'earned_run_avg').text

    def strikeouts(self, html):
        return self.parse_data_stat(html, 'SO_p').text

    def fielding_percent(self, html):
        return self.parse_data_stat(html, 'fielding_perc').text

    def avg_age_picther(self, html):
        return self.parse_data_stat(html, 'age_pit').text

    def parse_data_stat(self, html, string):
        return html.find('td', {'data-stat': string})


class WSParser:
    #get list of ws_winners
    def parse_ws_winner(self):
        ws = WSScraper()
        ws_team_list = []
        winner = ws.ws_winners()
        for team in winner:
            ws_team_list.append(re.sub(' +', ' ', team.findNext().text))
        #add 'Boston Red Sox' because list was mising 2018 winner
        return ws_team_list + ['Boston Red Sox']

    #scrape and parse years that there winners
    def parse_ws_year(self):
        ws = WSScraper()
        ws_year_list = []
        year = ws.ws_years()
        for y in year:
            ws_year_list.append(y.findNext().text[: 4])
        return ws_year_list[0: 116]

    #zip together list of winners and years
    def zip(self):
        return zip(self.parse_ws_winner(), self.parse_ws_year())
