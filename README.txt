Q. How to make competetion of programs?
A. 1) Download these programs (if not yet).
   2) Download numpy (it's necessary for my player).
   3) Allow permissions to execute for moderator.py (it's multiplayer moderator) and cheburator.py (it's my player).
   4) Implement your program using the protocol.
   5) Insert in moderator.py command line of your program:
       tournament(['./cheburator.py','./program1','./program2'],1000,1)
   6) Run moderator.py

Q. Is the all-pass protocol difficult?
A. No. It consists of three stages:
   1) Each program is given a set of cards
   2) Each program is given a number (0,1 and 2)
   3) Gameplay, when one player makes a move (or a card from talon is opened) and this card is sent to other players.
   Note, that each program must know, when to make a move, basing on the rules.
   It sees only the next card, which appears on the deck, and it's enough.

Q. How cards are designated?
A. Ranks are designated 7,8,9,10, 11 for Jack, 12 for Queen, 13 for King, 14 for ace.
   Suits are designated H, D, C, S. So, 12H is queen of hearts.
   
Q. How to understand the protocol better?
A. Explore the file log_example.txt

Q. What the program cheburator.py does?
A. Currently (6 August) it is a rndom player. Real player is not yet implemented.

Q. How to make sure that there is no cheating?
A. Explore only two files: moderator and allpass_rules
   Besides, all programs, including mine, are started via command-line.
