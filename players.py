import random 

import allpass_rules

def chooseCard(strategy,cardset):
	bestcard=cardset[0]
	if not strategy is None:
		for j in cardset:
			if strategy[j]>strategy[bestcard]:
				bestcard=j
	return bestcard

class FastRandomPlayer:
	def __init__(self,strategy=None):
		self.strategy=strategy
	def deal(self,cards):
		self.cards=cards
	def setNumber(self,number):
		pass
	def move(self,game,card):
		pass
	def getCard(self,game):
		return chooseCard(self.strategy,game.getPossibleMoves(self.cards))

class PlayerHist():
	def __init__(self):
		self.discarded=[0 for j in xrange(32)]
		self.donthave=[0,0,0,0]
	def track(self,card,donthave):
		self.discarded[card]=1
		if donthave!=allpass_rules.NOTRUMP:
			self.donthave[donthave]=1

def buildVector(vectors):
	res,svect=[],[[]]*4
	for v in vectors:
		l=len(v)/4
		for j in xrange(4):
			svect[j]=svect[j]+v[l*j:l*(j+1)]
	for s in svect:
		res=res+s
	return res

class Player():
	def __init__(self,nn_probability=0,strategy=None,network=None,params=None):
		self.prev_player,self.next_player=PlayerHist(),PlayerHist()
		self.vectors,self.answers=[],[]
		self.nn_probability,self.strategy=nn_probability,strategy
		self.network,self.params=network,params
	def deal(self,cards):
		self.cards=cards
		self.cards_as_bool=[0]*32
		for c in cards:
			self.cards_as_bool[c]=1
	def setNumber(self,number):
		self.next_player_num,self.prev_player_num=(number+1)%3,(number+2)%3
	def move(self,game,card):
		donthave=allpass_rules.NOTRUMP
		if (game.trump!=allpass_rules.NOTRUMP and 
			allpass_rules.suit(card)!=allpass_rules.suit(game.trump)):
			donthave=allpass_rules.suit(game.trump)
		if game.curplayer==self.prev_player_num:
			self.prev_player.track(card,donthave)
		elif game.curplayer==self.next_player_num:
			self.next_player.track(card,donthave)
	def getInputVector(self,game):
		cardset=game.getPossibleMoves(self.cards)
		if (game.trump==allpass_rules.NOTRUMP or
			allpass_rules.suit(cardset[0])!=allpass_rules.suit(game.trump)):
			suit_av=[1,1,1,1]
			strict=0
		else:
			suit_av=[0,0,0,0]
			suit_av[allpass_rules.suit(game.trump)]=1
			strict=1
		looser_card=[0]*32
		if game.loosecard!=allpass_rules.NOTRUMP:
			looser_card[game.loosecard]=1
		discarded=[0]*32
		for c in game.discarded:
			discarded[c]=1
		general=[game.move,game.step,strict]*4
		vector=buildVector([self.cards_as_bool,discarded,looser_card,
							self.next_player.discarded,self.prev_player.discarded,
							self.next_player.donthave,self.prev_player.donthave,
							suit_av,general])
		return vector
	def getCard(self,game):
		input_vector=self.getInputVector(game)
		if random.random<self.nn_probability:
			strategy,pen=self.network.prop(input_vector,self.params)
		else:
			strategy=self.strategy
		answer=chooseCard(strategy,game.getPossibleMoves(self.cards))
		self.vectors.append(input_vector)
		self.answers.append(answer)
		return answer
