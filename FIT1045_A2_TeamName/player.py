from __future__ import annotations
from cards import Card, Rank, Suit									

class Player:														
	def __init__(self, name: str) -> None:
		"""
		Purpose:       To update self.name to the current player's name along with self.hand to the current player's hand 
				       and reset the round and totoal scores to 0
		Arguments:     Self object
					   name: String 
		Return Value:  No return values 
		Function:      Sets self.name to the current player's name,sets self.hand to the current player's card in their hand 
					   and self.round_score and self.total_score is reset to 0
		"""		

		#initialize 4 instance variables					
		self.name = name											
		self.hand = []		
		self.round_score = 0										
		self.total_score = 0
																	
	def __str__(self):
		"""
		Function:     To return player's name
		Argument:     Self object
		Return Value: Player's Name: String
		"""
		return f'Player name is {self.name}'

	def __repr__(self):
		"""
		Function:     To return player's name
		Argument:     Self object
		Return Value: Player's Name: String
		"""
		return f'Player(name = {self.name})'

	def check_valid_play(self, card: Card, trick: list[Card], broken_hearts: bool) -> (bool, str):
		"""
		Purpose:         Check the validity of play by the players    
		Arguments:       Self object
		Return Values:   valid: bool
						 error_message: str
		Function:        When a player is leading the trick, if the player chooses to play a card other than the two of clubs even though it is in the 
						 player's hand, an error message will be sent saying "Must play 2 clubs first". 
						 When a player is leading the trick, if the player has cards with other suits and the suit of Hearts but chooses to play a card 
						 with a suit other than Hearts, then game goes on normally. 
						 When a player is leading the trick, if the player has cards only with the suits other than Hearts and chooses to play the cards 
						 with those suits, then the game goes on normally but a condition is updated where it shows that the player does not have a card 
						 in the suit of hearts within their hand.
						 When a player is leading the trick, if the player chooses a card with the suit of hearts then other players must play cards of
						 the same suit if they have cards that are the suit of Hearts, otherwise an error messsage is sent saying that "Hearts has not 
						 been broken <3". 
						 When a player is not leading, if the player tries to play a different suited card from the trick, then an 
				         error message will pop out saying "Player still has cards from the suit of the current trick"		
		"""

		#initialize error message as empty string
		error_message = ''
		two_of_clubs = Card(Rank.Two, Suit.Clubs)
		valid = True

		#player is leading (trick is empty)
		if not trick:
			#player's hand got two of clubs and player not playing this card
			if two_of_clubs in self.hand and card != two_of_clubs:
				valid = False
				error_message = "Must play 2 clubs first"

			#check if player's hand got cards other than hearts
			only_hearts = True
			for my_card in self.hand:
				if my_card.suit.value != 4:
					only_hearts = False

			#got other card to play but player chose hearts card to lead the trick
			if not broken_hearts and card.suit.value == Suit.Hearts.value and (not only_hearts):
				valid = False
				error_message = "Heart is not broken <3"
		#player is not leading (trick is not empty)
		else:
			#player not playing the card from the same suit as first card in trick
			for my_card in self.hand:
				if my_card.suit.value == trick[0].suit.value and card.suit.value != trick[0].suit.value:
					valid = False
					error_message = "Player still has cards from the suit of the current trick"
		return (valid, error_message)
	
	



