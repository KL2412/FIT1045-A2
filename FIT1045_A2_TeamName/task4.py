from __future__ import annotations
from basic_ai import BasicAIPlayer
from cards import Card, Rank, Suit
from round import Round
import random as rand

class Hearts:
	def __init__(self) -> None:
		while True:
			target_score = int(input("Please enter a target score to end the game: "))
			if target_score > 0:
				break
			else:
				print("Invalid target score")

		while True:
			number_of_players = int(input("Please enter the number of players (3-5): "))
			if 3 <= number_of_players <= 5:
				break
			else:
				print("Invalid target score")

		#game_options
		self.target_score = target_score
		self.number_of_players = number_of_players

		#create player objects
		self.players = []
		for index in range(number_of_players):
			self.players.append(BasicAIPlayer("Player " + str(index + 1)))   #may need to change later on

		#game run until someone hits the targer score
		game_end = False
		game_round = 1
		while not game_end:
			#generate deck
			print("========= Starting round " + str(game_round) + " =========")
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
				for index, player in enumerate(self.players):
					player.hand = self.deck[index * (52//number_of_players):(index + 1) * (52//number_of_players)]
				
				#check for rare situation which can break the game
				for player in self.players:
					if Card(Rank.Queen, Suit.Spades) in player.hand:
						rare_situation = True
						for cards in player.hand:
							if cards.suit.value != 4:
								rare_situation = False
				
			#print cards after dealt, should remove later on
			for player in self.players:
				print(player.name + " was dealt " + str(player.hand))

			#pass cards 
			cards_to_be_added = []
			for index, player in enumerate(self.players):
				cards_to_be_passed = player.pass_cards()
				index_of_card_receiver = (index + game_round) % len(self.players)

				#remove this line later
				print(player.name + " passed " + str(cards_to_be_passed) + " to " + self.players[index_of_card_receiver].name)

				#remove cards from original player
				for i in range(3):
					player.hand.remove(cards_to_be_passed[i])

				#save which cards to be passed
				cards_to_be_added.append((index_of_card_receiver, cards_to_be_passed))
			
			#add cards to the receiver
			for tuplee in cards_to_be_added:
				for card in tuplee[1]:
					self.players[tuplee[0]].hand.append(card)

			#starts round
			Round(self.players)
			print('========= End of round ' + str(game_round) + ' =========')

			shot_the_moon = False
			for player in self.players:
				if player.round_score == 26:
					print(player.name + " has shot the mooon! Everyone else receives 26 points")
					shot_the_moon = True

			if shot_the_moon:
				for player in self.players:
					if player.round_score == 26:
						player.round_score = 0
					else:
						player.round_score = 26

			for player in self.players:
				player.total_score += player.round_score
				print(player.name + "'s total score:", player.total_score)
				
			
			#check game end
			for player in self.players:
				if player.total_score >= self.target_score:
					game_end = True
					break
			
			minimum_score = (-1, 9999) #(index, score)
			for index, player in enumerate(self.players):
				if player.total_score < minimum_score[1]:
					minimum_score = (index, player.total_score)
			
			if game_end:
				print(self.players[minimum_score[0]].name + " is the winner!")
			
			game_round += 1
		
	def generate_deck(self) -> list:
		suit_list = []
		rank_list = []
		full_deck = []
		for suits in Suit:
			suit_list.append(suits)
		for ranks in Rank:
			rank_list.append(ranks)
		for suit_i in suit_list:
			for rank_j in rank_list:
				full_deck.append(Card(rank_j, suit_i))
		return full_deck
