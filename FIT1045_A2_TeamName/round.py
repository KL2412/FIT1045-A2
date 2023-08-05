from __future__ import annotations
from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer
from human import HumanPlayer
import time

class Round:

	def __init__(self, players: list[Player]) -> None:

		"""
		Purpose:      	 	Performing round for Hearts game
		Arguments:    		Self object
							Players: list[Player]
		Return Value: 		No return values 
		Visualization:      Each iteration of a round begins with a new trick, initially each player's score is zero,
						 	and players take turns playing one card each, 
							after which the one who played the highest ranking card from the suit of the trick takes the trick.
							The suit of the trick is defined by the suit of the lead card, 
							and the player with the Two of Clubs must lead the first trick of the round.
							After each iteration, the player who takes the trick leads the next trick.
							If someone plays a Hears card, broken_hearts = True	
							When a player takes a trick, they receive one point for every Hearts card in the trick, 
							and the Queen of Spades gives 13 points.
							The round continues until players have played all cards.
							Turns are taken clockwise, in which a list of players means taking turns in increasing order of index.
		"""		

		#initialize the neccessary variables
		two_of_clubs = Card(Rank.Two, Suit.Clubs)
		queen_of_spades = Card(Rank.Queen, Suit.Spades)
		broken_hearts = False
		n_player_turn = -1

		#set round score of all players to 0
		for player in players:
			player.round_score = 0
		
		#for loop to run n times where n = number of cards on player's hand
		for game_round in range(len(players[0].hand)):
			trick = []
			greatest_card_in_trick = (two_of_clubs, -1) #greatest card, index of player who played it

			#first card in the round must be two of clubs
			if game_round == 0:
				#find out which player holding two of clubs and let that player start first
				for player_index, player in enumerate(players):
					for card in player.hand:
						if two_of_clubs == card:
							played_card = player.play_card(trick, broken_hearts)
							trick.append(played_card)
							n_player_turn = player_index
							print(players[n_player_turn].name + " leads with", two_of_clubs)

			#determine how many remaining turns left to run
			if game_round == 0:
				remaining_turns = len(players) - 1
			else:
				remaining_turns = len(players)
			
			#run the remaining turns
			for turn in range(remaining_turns):
				#slow down the output by 1 second
				time.sleep(1)

				#proceed to next player
				n_player_turn += 1
				#if player turn is >= than number of players, set it back to 0
				if n_player_turn >= len(players):
					n_player_turn -= len(players)

				#player plays card and append the played card into trick
				played_card = players[n_player_turn].play_card(trick, broken_hearts)
				trick.append(played_card)
				#print what the player have played
				if remaining_turns == len(players) and turn == 0:
					print(players[n_player_turn].name + " leads with", played_card)
				else:
					print(players[n_player_turn].name + " plays", played_card)

				#check if hearts is broken
				if played_card.suit.value == 4:
					broken_hearts = True
				
				#check if the played card is the largest card in trick
				if (played_card.suit.value == trick[0].suit.value) and (played_card.rank.value > greatest_card_in_trick[0].rank.value):
					greatest_card_in_trick = (played_card, n_player_turn)
			
			#calculate how many scores are carried by the cards in the trick
			scores_to_add = 0
			for card in trick:
				if card.suit.value == 4:
					scores_to_add += 1
				if card == queen_of_spades:
					scores_to_add += 13
				
			#add the score to player's round score if the player takes the trick
			players[greatest_card_in_trick[1]].round_score += scores_to_add

			#print who takes the trick and scores added to round score
			print(players[greatest_card_in_trick[1]].name + " takes the trick. Points received:", scores_to_add)
			
			#the player who takes the trick leads next round
			n_player_turn = greatest_card_in_trick[1] - 1
