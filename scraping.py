import requests
from bs4 import BeautifulSoup


class TeamStatsBuilder:
    def run(self):
        ts = TeamScraper()
        ss = StatsScraper()
        ts.teamsHTML()
        teamParser = TeamParser()
        statParser = StatParser()
        teams = []
        for team in ts.teamList()[0:2]:
            teamName = teamParser.team_name(team)
            if teamName:
                # create Team Instance
                new_team_instance = teamName
                teams.append(new_team_instance)
                # get pitching/batting data
                url = teamParser.team_url(team)

                for row in ss.battingHTML(url)[0:2]:
                    league = statParser.league(row)
                    if league:
                        division = statParser.division(row)
                        year = statParser.year(row)
                        wins = statParser.wins(row)
                        runs_scored = statParser.runs_scored(row)
                        home_runs = statParser.home_runs(row)
                        batting_average = statParser.batting_average(row)
                        ops = statParser.ops(row)
                        avg_age = statParser.avg_age(row)

                for row in ss.pitchingHTML(url)[1:3]:
                    year = statParser.year(row)
                    if year:
                        print(year)
                        losses = statParser.losses(row)
                        runs_allowed = statParser.runs_allowed(row)
                        era = statParser.era(row)
                        earned_runs = statParser.earned_runs(row)
                        strikeouts = statParser.strikeouts(row)
                        fielding_percent = statParser.fielding_percent(row)
                        avg_age = statParser.avg_age_picther(row)

                        print(year, losses, runs_allowed, era, earned_runs, strikeouts, fielding_percent, avg_age)
        return teams


class TeamScraper:
    def teamsHTML(self):
        url = 'https://www.baseball-reference.com/teams/'
        br_request = requests.get(url)
        br_content = br_request.content
        self.br_soup = BeautifulSoup(br_content, 'html.parser')
        print(br_request)
        return self.br_soup

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


class TeamParser:
    def team_name(self, html):
        teamNameElement = html.find('td', {'data-stat': 'franchise_name'})
        if teamNameElement:
            return teamNameElement

    def team_url(self, html):
        teamURLElement = html.find('td', {'data-stat': 'franchise_name'}).findNext()
        return teamURLElement.get('href')


class StatParser:
    def league(self, html):
        leagueElement = html.find('td', {'data-stat': 'lg_ID'})
        if leagueElement:
            return leagueElement.findNext().text[:2]

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


sb = TeamStatsBuilder()
x = sb.run()
