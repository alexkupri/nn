import allpass_rules

class FastRandomPlayer:
	def __init__(self,strategy=None):
		self.strategy=strategy
	def deal(self,cards):
		self.cards=cards
	def setNumber(self,number):
		self.number=number
	def move(self,player,card):
		pass
	def getCard(self,game):
		cardset=game.getPossibleMoves(self.cards)
		bestcard=cardset[0]
		if self.strategy!=None:
			for j in cardset:
				if self.strategy[j]>self.strategy[bestcard]:
					bestcard=j
		return bestcard
