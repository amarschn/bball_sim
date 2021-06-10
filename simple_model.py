"""
Simple bball model:
- 5 players per team
- Each offensive player has prob function for:
	- Score
	- Pass
	- Turnover
- Each defensive player has prob function for:
	- Steal
- Game has 20 plays, each play has 5 actions
"""


import random
import pprint

POSSESSIONS = 20
MOVES = 5
FIRST_NAMES = open('first_names').read().split('\n')
LAST_NAMES = open('last_names').read().split('\n')
TEAM_NAMES = open('team_names').read().split('\n')


class Player(object):
	"""Player class
	params
	"""
	def __init__(self, params):
		self.params = params
		self.name = params.get('name')
		self.fg_prob = params.get('fg_prob')
		self.three_prob = params.get('three_prob')
		self.pass_prob = params.get('pass_prob')
		self.steal_prob = params.get('steal_prob')
		self.turn_prob = params.get('turn_prob')

	def action(self):
		weights = [self.fg_prob + self.three_prob, self.pass_prob, self.turn_prob]
		return random.choices(["SCORE", "PASS", "TURNOVER"], weights=weights)[0]

	def score(self):
		return random.choices([2,3], weights=[self.fg_prob, self.three_prob])[0]


class Team(object):
	"""
	Team class
	params
	"""
	def __init__(self, params=None):
		self.name = random.choice(TEAM_NAMES)
		self.generate_players()

	def generate_players(self):
		"""Create players
		"""
		self.players = []
		for i in range(5):
			params = {
				'name': random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES),
				'fg_prob': random.random(),
				'three_prob': random.random()/2,
				'pass_prob': random.random(),
				'steal_prob': random.random()/10,
				'turn_prob': random.random()/5
			}
			self.players.append(Player(params))

	def select_player(self):
		return random.choice(self.players)

	def gets_steal(self):
		for player in self.players:
			steal = random.choices([0,1], \
				weights=[1-player.steal_prob, player.steal_prob])[0]
			if steal:
				return True
		return False

	def print_players(self):
		print("Team {} Roster:\n============================".format(self.name))
		for player in self.players:
			pprint.pprint(player.params, width=1)


def game():
	score = [0,0]
	teams = [Team(), Team()]

	for team in teams:
		team.print_players()

	offense_bool = random.choice([0,1])
	offense = teams[offense_bool]
	defense = teams[not offense_bool]

	for p in range(POSSESSIONS):
		print("Possession: {} - {}".format(p, offense.name))
		player = offense.select_player()
		for move in range(MOVES):
			print("Move: {} - {}".format(move, player.name))
			if defense.gets_steal():
				print("Steal!")
				break
			else:
				a = player.action()
				if a == "SCORE":
					score[offense_bool] += player.score()
					print("Score! - {}".format(score))
					break
				elif a == "PASS":
					player = offense.select_player()
					print("Pass!")
				elif a == "TURNOVER":
					print("Turnover!")
					break
		offense_bool = not offense_bool
		offense = teams[offense_bool]
		defense = teams[not offense_bool]
	return score

if __name__ == '__main__':
	print(game())
