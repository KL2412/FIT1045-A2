from __future__ import annotations
from cards import Card, Suit, Rank
from player import Player
from human import HumanPlayer
from basic_ai import BasicAIPlayer

class BetterAIPlayer(Player):
	def __init__(self, name: str) -> None:
		"""
		Purpose:       Adding all dangerous cards into one list
		Arguments:     Self object
					   name: String 
		Return Value:  No return values 
		Function:      Adding cards with the suit of Hearts into the list dangerous_cards
		"""
		#call __init__ method from parent class
		Player.__init__(self, name)

		#append queen of spades into dangerous_card list
		self.dangerous_cards = [Card(Rank.Queen, Suit.Spades)]
		#append all hearts into dangerous_card list
		for dangerous_card in [Card(Rank.Two, Suit.Hearts), Card(Rank.Ace, Suit.Hearts)]:
			self.dangerous_cards.append(dangerous_card)

	def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
		"""
		Purpose:       Better AI choose a card to play
		Arguments:     Self object
					   trick: list[Card]
					   broken_hearts: bool
		Return Value:  card_to_play: Card
		Function:      The AI's hand is first sorted.
					   when the AI is leading the trick, if it is the first round and the AI has the card 2 of clubs in his hand, the
					   AI will play that card. If the AI does not have the 2 of clubs then it plays the first card in the AI's hand.
					   When the AI is not leading the trick, if trick has the card with the suit of Hearts, if the AI has cards with 
					   the suit of Hearts that is lower than the trick, then the AI would select the lowest of the cards with the suit
					   of Hearts to play, if the AI does not have any card smaller than the trick, then the AI would select the card 
					   with the highest rank of suit Hearts and play it. If the trick has the card of suit other than Hearts, then 

		"""	
		#sort card
		self.sort_cards()
		
		#trick is empty (leading trick)
		if not trick:
			#two of clubs in player hand (first round)
			if Card(Rank.Two, Suit.Clubs) in self.hand:
				card_to_play = Card(Rank.Two, Suit.Clubs)
				self.hand.remove(card_to_play)
				return Card(Rank.Two, Suit.Clubs)
			#non_first round
			else:
				card_to_play = self.hand[0]
				self.hand.remove(card_to_play)
				return card_to_play
		#trick is not empty (not leading trick)
		else:
			#there is dangerous card(cards with points) in the trick
			if self.trick_contain_dangerous_card(trick):
				#player got smaller playable card than trick lead
				if self.hand_got_card_smaller_than_trick_lead(trick):
					#play lowest valid card in the hand
					card_to_play = self.lowest_card(trick, broken_hearts)
					self.hand.remove(card_to_play)
					return card_to_play
				#player does not have smaller playable card than trick lead
				else:
					#play largest valid card in the hand since we have a high chance to take the trick, why not get rid of the higher card
					card_to_play = self.highest_card(trick, broken_hearts)
					self.hand.remove(card_to_play)
					return card_to_play
			#there is no dangerous card in the trick
			else:
				#play the highest card since if we take the trick, no point is allocated for us and we can take the initiative for next round if we won the trick
				card_to_play = self.highest_card(trick, broken_hearts)
				self.hand.remove(card_to_play)
				return card_to_play

	def pass_cards(self) -> list[Card]:
		"""
		Purpose:       Better AI chooses 3 cards to pass
		Arguments:     Self object
		Return Value:  to_pass: list[Card]
		Function:      The AI's hand is first sorted.
					   If the AI's hand has cards with the suit of Hearts, the card Queen of Spades and the card 2 of Clubs, then  
					   they would all be added into the list dangerous_cards_in_hand. While the number of dangerous_cards_in_hand is
					   less than 3, the largest card in the AI's hand will be played first.
		"""	
		#sort card
		self.sort_cards()
		dangerous_cards_in_hand = []

		#add all dangerous cards in hand to dangerous_cards_in_hand list
		for my_card in self.hand:
			if my_card in self.dangerous_cards:
				dangerous_cards_in_hand.append(my_card)
		if Card(Rank.Two, Suit.Clubs) in self.hand:
			dangerous_cards_in_hand.append(Card(Rank.Two, Suit.Clubs))

		#while dangerous_cards_in_hand is less than 3, add the largest card in hand to be passed
		while len(dangerous_cards_in_hand) < 3:
			for n_card in range(len(self.hand)):
				if self.hand[len(self.hand) - 1 - n_card] not in dangerous_cards_in_hand:
					dangerous_cards_in_hand.append(self.hand[len(self.hand) - 1 - n_card])

		#add the last three cards in dangerous_cards_in_hand into to_pass list(three largest dangerous cards)
		to_pass = dangerous_cards_in_hand[-3:]
		for cards in to_pass:
			self.hand.remove(cards)
		return to_pass

	def heart_exist(self) -> bool:
		"""
		Purpose:       To check if the AI's hand contains cards with the suit Hearts 
		Arguments:     Self object
		Return Value:  True or False 
		Function:      If any card within the AI's hand contains the suit Hearts then the value True is returned, False otherwise
		"""
		#iterate through self.hand to see if there is any card of suit hearts
		for my_card in self.hand:
			if my_card.suit == Suit.Hearts:
				return True
		return False
	
	def hand_contain_this_suit(self, trick_0_card) -> bool:
		"""
		Purpose:       To check if the AI's hand has cards of the same suit with the first card played in the trick
		Arguments:     Self object
					   trick_0_card: Card - the first card in the trick
		Return Value:  True or False 
		Function:      If cards within the AI's hand contains cards with the same suit of the first card played in the trick then True 
					   value is returned, False otherwise
		"""
		#iterate through self.hand to see if there is any card of the same suit as trick lead
		for card in self.hand:
			if card.suit == trick_0_card.suit:
				return True
		return False

	def sort_cards(self) -> None:
		"""
		Purpose:       Sort the cards in self.hand
		Arguments:     Self object
		Return Value:  No return values
		Function:      For every card in the AI's hand, if the card is lesser than the first card in the AI's hand then that card is 
					   removed from the AI's hand and appended into the list sorted_hand. When there is no more card in self.hand, 
					   assign sorted_hand into self.hand
		"""
		sorted_hand = []
		#while self.hand is not empty, check if there is any card that is smaller than the first card
		while self.hand:
			#assign first card in hand to minimum
			minimum = self.hand[0]
			#if there is a card smaller than minimum card then set that card to minimum card
			for my_card in self.hand: 
				if my_card < minimum:
					minimum = my_card
			#append the minimum card from self.hand into sorted_hand list
			sorted_hand.append(minimum)
			#remove the card from self.hand
			self.hand.remove(minimum) 
		#when self.hand is empty and sorted_hand is full, assign sorted_hand into self.hand
		self.hand = sorted_hand 
	
	def lowest_card(self, trick, broken_hearts) -> Card:
		"""
		Purpose:       To check for the highest valid card in the AI's hand
		Arguments:     Self object
					   trick
					   broken_hearts 
		Return Value:  my_card: Card
		Function:      The first valid card of the AI's sorted hand is returned 
		"""
		#look for smallest valid card to play
		for my_card in self.hand:
			if (self.check_valid_play(my_card, trick, broken_hearts))[0]:
				return my_card

	def lowest_heart(self) -> Card:
		"""
		Purpose:       To check the AI's hand for the lowest valid card with the suit Hearts 
		Arguments:     Self object
		Return Value:  my_card: Card
		Function:      The first valid hearts card of the AI's sorted hand is returned
		"""
		#look for smallest valid card of suit hearts to play
		for my_card in self.hand:
			if my_card.suit == Suit.Hearts:
				return my_card
	
	def highest_card(self, trick, broken_hearts) -> Card:
		"""
		Purpose:       To check for the highest card in the AI's hand
		Arguments:     Self object
					   trick: list[Card]
					   broken_hearts: bool
		Return Value:  my_card: Card
		Function:      The first valid card of the AI's reversed sorted hand is returned 
		"""
		#look for largest valid card of suit hearts to play
		for my_card in reversed(self.hand):
			if (self.check_valid_play(my_card, trick, broken_hearts))[0]:
				return my_card
	
	def trick_contain_dangerous_card(self, trick) -> bool:
		"""
		Purpose:       To check if there are any cards with the suit of Hearts and the Queen of Spades 
		Arguments:     Self object
					   trick: list[Card]
		Return Value:  True or False 
		Function:      If the cards in the trick contains cards from dangerous_cards then the value True is returned, False otherwise
		"""
		#check if trick contain dangerous card by iterating through the list, if found one then return True
		for cards_in_trick in trick:
			if cards_in_trick in self.dangerous_cards:
				return True
		return False
		
	def hand_got_card_smaller_than_trick_lead(self, trick) -> bool:
		"""
		Purpose:       To check if the AI's hand has any cards smaller than the card played in the trick
		Arguments:     Self object
					   trick: list[Card]		
	    Return Value:  True or False
		Function:      For every card within the AI's hand, if the suit of the cards is equals to the first card played in the trick
					   and the card rank is less than the first card played in the trick then the value True is returned, False otherwise.
		"""
		#return true if there is a card in hand which is same suit but smaller than the first card in trick, false otherwise
		for my_card in self.hand:
			if my_card.suit == trick[0].suit and my_card < trick[0]:
				return True
		return False
