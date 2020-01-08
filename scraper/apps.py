from django.apps import AppConfig
import requests 
from bs4 import BeautifulSoup
import json

SPRITE_DATA = {
	"CSK" : " -163px 0px",
	"DC" : " -489px 0px",
	"DD" : " 0px -163px",
	"DEC" : " -163px -163px",
	"GL" : " -326px 0px",
	"KKR" : " -326px -163px",
	"KTK" : " 0px -326px",
	"KXIP" : " -163px -326px",
	"MI" : " -326px -326px",
	"PWI" : " 0px 0px",
	"RCB" : " -489px -163px",
	"RPS" : " -489px -326px",
	"RR" : " 0px -489px",
	"SPN" : " -163px -489px",
	"SRH" : " -326px -489px",
	"TBC" : " -489px -489px",
	"TBD" : " -652px 0px",
	"TRL" : " -652px -163px",
	"VEL" : " -652px -326px",
}

class ScraperConfig(AppConfig):
    name = 'scraper'

class Scraper:
	ROOT = "https://www.iplt20.com"
	TEAMS = "https://www.iplt20.com/teams"
	TEAM_HOME = "https://www.iplt20.com/teams/{team_slug}"
	SQUAD_PAGE = "https://www.iplt20.com/teams/{team_slug}/squad"
	LOGO_SPRITES = "https://www.iplt20.com/resources/ver/i/sprites/tLogo158x-sprite.png"
	PLAYER_API = "https://api.platform.iplt20.com/content/ipl/bios/EN/?page=0&pageSize=1&tagNames=&references=CRICKET_PLAYER%3A{player_id:d}"
	SQUAD_API = "https://cricketapi.platform.iplt20.com/stats/players?teamIds={team_id:d}&tournamentIds=18790&scope=TOURNAMENT&pageSize=30"

	@classmethod
	def get_team_ids(cls,check_list):
		remaining_calls = 10;
		team_ids = {} 
		team_data = {}
		tid = 1;

		while(check_list and remaining_calls):
			x = requests.get(cls.SQUAD_API.format(team_id=tid))

			if x.status_code == 200:
				d = json.loads(x.content.decode("UTF-8"))
				if 'team' in d and d['team']['fullName'] in check_list:
					team_ids[d['team']['fullName']] = tid
					check_list.remove(d['team']['fullName'])
					team_data[tid] = d
				else:
					#TODO: is this even necessary
					pass
			else:
				# TODO: add error handling
				pass
			tid+=1
			remaining_calls-=1
		return team_ids,team_data

	@classmethod
	def get_teams(cls):
		r = requests.get(cls.TEAMS) 
		doc = BeautifulSoup(r.content, 'html5lib')
		r_teams = doc.select("li.team-card-grid__item")
		teams = []
		team_names = set()
		op = ""
		for r_team in r_teams:
			team = {}
			team['slug'] = r_team.select_one("a")['href']
			name = r_team.select_one("div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > h3:nth-child(1)").contents
			team['name'] = ''.join(map(str,filter(lambda x: isinstance(x, str),name)))
			team['pretty_name'] = ''.join(map(str,name))
			team['homeground'] = r_team.select_one("div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > p:nth-child(2)").contents[0].strip()
			team['code'] = r_team.select_one(".team-card__inner")["class"][-1];
			team['sprite_position'] = SPRITE_DATA[team["code"]];
			team_names.add(team['name'])
			teams.append(team)
		team_ids = cls.get_team_ids(team_names);
		return str(teams);