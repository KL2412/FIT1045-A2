from __future__ import annotations
from basic_ai import BasicAIPlayer
from better_ai import BetterAIPlayer
from cards import Card, Rank, Suit
from human import HumanPlayer
from round import Round
import random as rand

class Hearts:
	def __init__(self) -> None:
		'''
		Purpose: Initiate the game when Hearts object is created.
		Argument: self object
		Return value: None

		Function Body:
			Prompt TARGET SCORE and NUMBER OF PLAYERS 
			Create Player objects
			While loop to start the game:
				Generate a full deck
				Shuffle the deck
				Remove some of the cards if number of players is not 4
				Check for rare situation (one player take all hearts and queen of spades)
				If rare situation happens:
					Distribute the cards again
				Every user gets to pass 3 cards, adds passed cards to target players
				Call Round() to run the rounds for this game
				Check if shoot the moon happens and add the scores to respective players' total_score
				Check if game has ended, if yes, find the player with lowest total_score and print, continue to next round otherwise
				Add one to game_round
		'''
		#print the header
		print("Welcome to ❤ HEARTS ❤")

		#Prompt and validate TARGET SCORE and NUMBER OF PLAYERS 
		self.prompt_score_and_player_number()
		number_of_players = self.number_of_players
		target_score = self.target_score

		#create player objects accordingly using for loop
		self.players = []
		for index in range(number_of_players - 2):
			self.players.append(BetterAIPlayer("Player " + str(index + 1)))   #may need to change later on
		self.players.append(BetterAIPlayer("Player " + str(number_of_players - 1)))
		self.players.append(HumanPlayer())

		#game run until someone hits the targer score
		game_end = False
		game_round = 1
		while not game_end:
			#print banner
			print("========= Starting round " + str(game_round) + " =========")
			
			#generate deck
			self.deck = []
			self.deck = self.generate_deck()

			#shuffle deck
			rand.shuffle(self.deck)

			#distribute cards to players
			if number_of_players == 3 or number_of_players == 5:
				self.deck.remove(Card(Rank.Two, Suit.Diamonds))
				if number_of_players == 5:
					self.deck.remove(Card(Rank.Two, Suit.Spades))
			
			rare_situation = True
			while rare_situation:
				#distribute cards to the players
				for index, player in enumerate(self.players):
					player.hand = self.deck[index * (52//number_of_players):(index + 1) * (52//number_of_players)]
				
				#check for rare situation which can break the game (one player takes all hearts and queen of spades)
				for player in self.players:
					if Card(Rank.Queen, Suit.Spades) in player.hand:
						rare_situation = True
						for cards in player.hand:
							if cards.suit.value != 4:
								rare_situation = False
			
			#call pass_cards method on all players to determine which 3 cards to be passed
			cards_to_be_added = []
			for index, player in enumerate(self.players):
				index_of_card_receiver = (index + game_round) % len(self.players)
				if type(player) != HumanPlayer:
					cards_to_be_passed = player.pass_cards()
				else:
					cards_to_be_passed = player.pass_cards(index_of_card_receiver)

				cards_to_be_added.append((index_of_card_receiver, cards_to_be_passed))
			
			#add cards to the receiver
			for tuplee in cards_to_be_added:
				for card in tuplee[1]:
					self.players[tuplee[0]].hand.append(card)

			#starts round
			Round(self.players)

			#print end round banner
			print('========= End of round ' + str(game_round) + ' =========')
			
			#check if shot the moon occurs
			shot_the_moon = False
			for player in self.players:
				if player.round_score == 26:
					print(player.name + " has shot the mooon! Everyone else receives 26 points")
					shot_the_moon = True

			#if a player shot the moon, set his round score to 0 and others round score to 26 
			if shot_the_moon:
				for player in self.players:
					if player.round_score == 26:
						player.round_score = 0
					else:
						player.round_score = 26

			#add round score of each player into their total_score respectively
			for player in self.players:
				player.total_score += player.round_score
				print(player.name + "'s total score:", player.total_score)
				
			#check for game end
			for player in self.players:
				if player.total_score >= self.target_score:
					game_end = True
					break
			
			#determine which player have lowest score and save the index and score of the player into minimum_score (tuple)
			minimum_score = (-1, 9999) #(index, score)
			for index, player in enumerate(self.players):
				if player.total_score < minimum_score[1]:
					minimum_score = (index, player.total_score)
			
			#if game ends, print the name of winner
			if game_end:
				print(self.players[minimum_score[0]].name + " is the winner!")
			
			#add 1 to game_round (proceed to next round)
			game_round += 1
		
	def prompt_score_and_player_number(self):
		'''
		Purpose: Prompt score to end the game and number of players and check if the input is valid
		Argument: self object
		Return: None

		Function Body:
			while loop until the input is valid:
				prompt user for input target score
			while loop until number of player is valid:
				prompt user for input number of players
		'''

		#while loop to let user insert a valid target score
		while True:
			target_score = int(input("Please enter a target score to end the game: "))
			if target_score > 0:
				break
			else:
				print("Invalid target score")

		#while loop to let user input a valid number of players
		while True:
			number_of_players = int(input("Please enter the number of players (3-5): "))
			if 3 <= number_of_players <= 5:
				break
			else:
				print("Invalid number of players")

		#save the valid targer score and number of players into instance variable of object
		self.target_score = target_score
		self.number_of_players = number_of_players
	
	def generate_deck(self) -> list:
		'''
		Purpose: Generate a full deck, from two of clubs to ace of hearts
		Argument: self object
		Return: Full card deck : List[Cards]

		Function body:
			Add all suits into suit list
			Add all ranks into rank list
			Add every combination of rank and suit into full_deck list

		Visualization example of double for loop:
			suit_list = [Suit.Clubs, Suit.Diamonds, Suit.Spades, Suit.Hearts]
			rank_list = [Rank.Two, Rank.Three, ...., Rank.Ace]
			FIRST ITERATION (suit_i = Suit.Clubs, rank_j = Rank.Two)
			SECOND ITERATION (suit_i = Suit.Clubs, rank_j = Rank.Three)
			LAST ITERATION (suit_i = Suit.Hearts, rank_j = Rank.Ace)
		'''

		#initialize empty lists needed for later
		suit_list = []
		rank_list = []
		full_deck = []

		#append 4 suits into the suit list
		for suits in Suit:
			suit_list.append(suits)

		#append 13 ranks into the rank list
		for ranks in Rank:
			rank_list.append(ranks)
		
		#double for loop to append cards into full deck list
		for suit_i in suit_list:
			for rank_j in rank_list:
				full_deck.append(Card(rank_j, suit_i))
		return full_deck

if __name__ == '__main__':
	Hearts()
