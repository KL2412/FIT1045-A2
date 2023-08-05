from cards import Card, Rank, Suit
from player import Player

class BasicAIPlayer(Player):
	def play_card(self, trick: list[Card], broken_hearts: bool)-> Card:
		"""
		Purpose:      	 	Basic AI always play the lowest ranking card possible
		Arguments:    		Self object
							trick: list[Card]
							hearts: bool
		Return Value: 		Lowest ranking card to be played 
		Visualization:      Trick: ┌─────┐
								   |7    |
							 	   |  ♤  |
								   |    7|
								   └─────┘
							Self.hand : ┌──────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
                                        |10    | |J    | |Q    | |4    | |7    | |8    |
                                        |  ♤   | |  ♤  | |  ♤  | |  ♡  | |  ♡  | |  ♡  |
                                        |    10| |    J| |    Q| |    4| |    7| |    8|
                                        └──────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
							BasicAI will play: ┌──────┐
								   			   |10    |
							 	               |  ♤   |
								               |    10|
								               └──────┘
												
		"""		
		#sort card in self.hand
		self.sort_cards()
		#check if cards in hand is valid to be played ascendingly(from lowest card to highest), if found a valid card, return the card to break from the loop
		for my_card in self.hand:
			if (self.check_valid_play(my_card, trick, broken_hearts))[0]:
				self.hand.remove(my_card)
				return my_card
		#print error message if no valid card is played
		print(self.check_valid_play(my_card, trick, broken_hearts)[1])

	def pass_cards(self) -> list[Card]:
		"""
		Purpose:      	 	Basic AI must always return/pass the 3 highest ranking cards
		Arguments:    		Self object: list[Card]
		Return Value: 		3 highest ranking cards
		Visualization:      Trick: ┌─────┐
								   |7    |
							 	   |  ♤  |
								   |    7|
								   └─────┘
							Self.hand : ┌──────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
                                        |10    | |J    | |Q    | |4    | |7    | |8    |
                                        |  ♤   | |  ♤  | |  ♤  | |  ♡  | |  ♡  | |  ♡  |
                                        |    10| |    J| |    Q| |    4| |    7| |    8|
                                        └──────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
							BasicAI will pass: ┌─────┐ ┌─────┐ ┌─────┐
								   			   |8    | |7    | |4    |
							 	               |  ♡  | |  ♡  | |  ♡  | 
								               |    8| |    7| |    4|
								               └─────┘ └─────┘ └─────┘
												
		"""											
		#sort card in self.hand
		self.sort_cards()
		#reverse the cards in hand
		reversed_hand = self.hand[::-1]
		#assign 3 largest card to to_pass list
		to_pass = reversed_hand[0:3]
		#remove the cards from player hand
		for cards in to_pass:
			self.hand.remove(to_pass)
		#return the 3 cards to be passed
		return to_pass

	def sort_cards(self) -> None:
		"""
		Purpose:      	 	BasicAI has his/her cards sorted from the lowest to the highest value
		Arguments:    		Self object
		Return Value: 		No return values 
		Visualization:      Self.hand (before update): ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
                                                       |4    | |K    | |7    | |Q    | |3    | |8    |
                                                       |  ♢  | |  ♡  | |  ♤  | |  ♡  | |  ♧  | |  ♤  |
                                                       |    4| |    K| |    7| |    Q| |    3| |    8|
                                                       └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
												
							Self.hand (after update) : ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
                                                       |3    | |4    | |7    | |8    | |Q    | |K    |
                                                       |  ♧  | |  ♢  | |  ♤  | |  ♤  | |  ♡  | |  ♡  |
                                                       |    3| |    4| |    7| |    8| |    Q| |    K|
                                                       └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
		"""		
		#create an empty list
		sorted_hand = []

		#find the minimum card in hand -> append it into sorted_hand -> remove it from hand -> repeat until self.hand is empty -> self.hand = sorted_hand
		while self.hand:
			minimum = self.hand[0]
			for my_card in self.hand: 
				if my_card < minimum:
					minimum = my_card
			sorted_hand.append(minimum)
			self.hand.remove(minimum)  
		self.hand = sorted_hand  

