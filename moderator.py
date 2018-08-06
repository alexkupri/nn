#!/usr/bin/python
import subprocess
import pty
import os
import random
import signal
from datetime import datetime

#As you can see, this file imports only the gamerules.
#The gamerules file imports nothing.
#So you can explore two files to make sure there is no cheat.
import allpass_rules

def clearlog(verbosity):
	if verbosity==2:
		with open('log.txt','w'):
			pass

def log(s,verbose):
	if verbose:
		with open('log.txt','a') as f:
			f.write(datetime.now().strftime('%H:%M:%S.%f ')+s+'\n')

def err(s,verbose):
	log(s,verbose)
	print s
	raise Exception(s)

class RemotePlayer:
	def __init__(self,cmdline,name,verbose):
		log('Starting player '+name+' with commandline: '+cmdline,verbose);
		self.master,self.slave = pty.openpty()
		self.subpr=subprocess.Popen(cmdline,shell=True,preexec_fn=os.setsid,
									stdin=subprocess.PIPE,stdout=self.slave)
		self.verbose,self.name,self.cmdline=verbose,name,cmdline
	def __send__(self,line):
		log('Sending to player '+self.name+' line:'+line,self.verbose)
		self.subpr.stdin.write(line+'\n')
	def deal(self,cards):
		self.cards=cards
		self.__send__(allpass_rules.cards_to_str(cards))
	def setNumber(self,number):
		self.__send__(str(number))
	def move(self,player,card):
		self.__send__(allpass_rules.deck[card])
	def getCard(self,game):
		log('Requesting move from player '+self.name,self.verbose)
		ln=''
		while True:
			char=os.read(self.master,1)
			if char=='\n':
				break
			else:
				ln=ln+char
		if ln.strip() not in allpass_rules.deck:
			err('Player '+self.name+' returned a string "'+ln+'" which is not a card. Terminating',self.verbose)
		card=allpass_rules.deck.index(ln.strip())
		if card not in game.getPossibleMoves(self.cards):
			err('Player '+self.name+' made an invalid move: "'+ln+'". Terminating',self.verbose)
		log('Player '+self.name+' responded:'+ln,self.verbose)
		return card
	def stop(self):
		log('Terminating player '+self.name,self.verbose)
		try:
			os.killpg(os.getpgid(self.subpr.pid), signal.SIGTERM)
		except e:
			pass
		try:
			os.close(self.master)
			os.close(self.slave)
		except e:
			pass

def gameplay_cards(lines,cards,verbosity):
	clearlog(verbosity)
	pl=[RemotePlayer(lines[j],allpass_rules.playerNames[j],verbosity>=2) for j in xrange(3)]
	if verbosity>=0:
		for p in pl:
			print p.name+' : '+p.cmdline
		print 'Deck: '+allpass_rules.cards_to_str(cards)
	bids=allpass_rules.play(pl,cards,verbosity>=1)
	for p in pl:
		p.stop()
	return bids
	
def gameplay(lines,cards_as_strings,verbosity):
	gameplay_cards(lines,[allpass_rules.deck.index(s) for s in cards_as_strings.split()],verbosity)

def tournament(lines,number,verbosity):
	bids=[0,0,0]
	permutations=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]
	def output_stats():
		for j in xrange(3):
			print 'Totally ',bids[j],' bids (',bids[j]*100.0/sum(bids),' %) were got by the program ',lines[j]
		print ''
	for j in xrange(number):
		for perm in permutations:
			curlines=[lines[perm[k]] for k in xrange(3)]
			cards=range(32)
			random.shuffle(cards)
			currentbids=gameplay_cards(curlines,cards,verbosity)
			for j in xrange(3):
				bids[j]=bids[j]+currentbids[perm[j]]
			if verbosity>=1:
				output_stats()
	if verbosity<1:
		output_stats()
				
def comparison(line1,line2,number,verbosity):
	dummyline='./cheburator.py random'
	score1,score2=0,0
	for j in xrange(number):
		for k in xrange(3):
			lines=[dummyline for l in xrange(3)]
			cards=range(32)
			random.shuffle(cards)
			lines[k]=line1
			bids1=gameplay_cards(lines,cards,verbosity)
			lines[k]=line2
			bids2=gameplay_cards(lines,cards,verbosity)
			if bids1[k]!=bids2[k]:
				print 'The results of the players differ!!!'
			score1=score1+bids1[k]
			score2=score2+bids2[k]
	print score1,'bids were taken by ',line1
	print score2,'bids were taken by ',line2

#Uncomment these lines to reproduce the exact game or to debug your program.
#First argument is their command lines (exactly as in bash).
#Second argument is cards in text format (you can copypaste it from log).
#Third argument is verbosity (0,1,2). To debug your program, use 2.

#gameplay(['./cheburator.py','./cheburator.py','./cheburator.py'],
#         '12C 13C 8C 14D 9C 9D 14H 12D 13S 12S 7D 14C 7C 10S '
#         '11D 14S 11C 13D 12H 8H 8S 9S 10H 7H 10D 10C 7S 13H 11S 9H 8D 11H',2)

#Uncomment this line to understand, why two programs behave differently
#or why one program wins always.
#The programs play against two dummies with the exact the same cards.
#(A,dummy,dummy,cards1) (B,dummy,dummy,cards1)
#First two arguments are command lines.
#Third argument is number of round (each round is 6 games).
#Fourth argument is verbosity (1 or 2) recommended.

#comparison('./cheburator.py','./cheburator.py',1,1)

#Uncomment this line to make tournament with three programs.
#First argument is their command lines (exactly as in bash).
#Second argument is the number of rounds (each round is 6 games).
#Third argument is verbosity (0,1,2).
#When verbosity is 0, only the final results are written in console.
#When verbosity is 1, the games are written to console.
#When verbosity is 2, the games are written to console and
#all process interactions of the last game are written to log.txt
#When verbosity is 3, the file log.txt contains lof for all games (it grows).
#Use verbosity=2 to understand the protocol or to debug your program.

tournament(['./cheburator.py','./cheburator.py','./cheburator.py'],1,2)
