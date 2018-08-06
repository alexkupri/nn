#!/usr/bin/python
#program to play all-pass from terminal
import players
import allpass_rules

def play():
	gameplay=allpass_rules.Gameplay(False)
	player=players.FastRandomPlayer()
	#
	line0=raw_input()
	player.deal([allpass_rules.deck.index(x) for x in line0.split()])
	mynumber=int(raw_input())
	player.setNumber(mynumber)
	#
	while True:
		if gameplay.curplayer==mynumber:
			card=player.getCard(gameplay)
			print allpass_rules.deck[card]
		else:
			card=allpass_rules.deck.index(raw_input().strip())
			player.move(gameplay,card)
		gameplay.makeMove(card)

play()
