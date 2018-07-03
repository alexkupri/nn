suits=['S','C','D','H']
deck=[str(j)+s for s in suits for j in xrange(7,15)]

def suit(card):
	return card/8

def rank(card):
	return card%8

TALON=3
GAMEOVER=4
NOTRUMP=-1
playerNames=['X','Y','Z','TALON']

#State of the game (gamerules), whose turn and which cards can be played
#Whose turn can be detected by variable curplayer
class Gameplay:
	def __init__(self,verbose):
		self.move,self.step,self.curplayer,self.trump=0,0,3,NOTRUMP
		self.verbose,self.line=verbose,''
		self.discarded=[]
		self.curmoves=[0,0,0,0]
		self.bids=[0,0,0]
	#Possible cards, having initialcards
	def getPossibleMoves(self,initialcards):
		possible_cards=[x for x in initialcards if x not in self.discarded]
		if self.trump!=NOTRUMP:
			possible_same_cards=[x for x in possible_cards if suit(x)==suit(self.trump)]
			if len(possible_same_cards)>0:
				possible_cards=possible_same_cards
		return possible_cards
	def makeMove(self,card):
		self.line=self.line+playerNames[self.curplayer]+':'+deck[card]+' '
		self.curmoves[self.curplayer]=card
		self.discarded.append(card)
		self.curplayer=self.curplayer+1 if self.curplayer<2 else 0
		self.step=self.step+1
		if self.step==1:
			self.trump=card
		elif self.step==4 or (self.step==3 and self.move>=2):
			for j in xrange(3):
				if suit(self.curmoves[j])==suit(self.trump):
					looser,loosecard=j,self.curmoves[j]
			for j in xrange(3):
				if suit(self.curmoves[j])==suit(loosecard) and rank(self.curmoves[j])>rank(loosecard):
					looser,loosecard=j,self.curmoves[j]
			if self.verbose:
				print self.line+' ('+playerNames[looser]+')'
			self.bids[looser]=self.bids[looser]+1
			self.move=self.move+1
			self.step,self.line,self.trump=0,'',NOTRUMP
			if self.move==1:
				self.curplayer=TALON
			elif self.move==2:
				self.curplayer=0
			elif self.move>=10:
				if self.verbose:
					print ''.join([playerNames[j]+' got '+str(self.bids[j])+' bid(s). ' for j in xrange(3)])
				self.curplayer=GAMEOVER
			else:
				self.curplayer=looser

def play(pl,cards,verbose=False):
	pcards=[cards[0:10],cards[10:20],cards[20:30]]
	talon=cards[30:32]
	for j in xrange(3):
		pl[j].deal(pcards[j])
		pl[j].setNumber(j)
		if verbose:
			print(playerNames[j]+': '+''.join([deck[k]+' ' for k in sorted(pcards[j],reverse=True)]))
	game=Gameplay(verbose)
	while True:
		curplayer=game.curplayer
		if curplayer==TALON:
			card=talon.pop(0)
		elif curplayer==GAMEOVER:
			return game.bids
		else:
			card=pl[curplayer].getCard(game)
		for j in xrange(3):
			if j!=curplayer:
				pl[j].move(curplayer,card)
		game.makeMove(card)
