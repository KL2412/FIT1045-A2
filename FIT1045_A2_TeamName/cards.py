from __future__ import annotations
from enum import Enum

class Rank(Enum):
	Two = 2
	Three = 3
	Four = 4
	Five = 5
	Six = 6
	Seven = 7
	Eight = 8
	Nine = 9
	Ten = 10
	Jack = 11
	Queen = 12
	King = 13
	Ace = 14
	
	def __lt__(self, other: Rank) -> bool:
		"""
		Purpose:Use for sorting and comparing object
		Argument: 1:self object 2: other(Rank object)
		Return Value: Boolean(True or False)
		"""
		#return true if self.value is less than other,value and viceversa
		return self.value < other.value

class Suit(Enum):
	Clubs = 1
	Diamonds = 2
	Spades = 3
	Hearts = 4
	
	def __lt__(self, other: Suit) -> bool:
		"""
		Purpose: use for sorting and comparing
		Argument: 1: self objects 2:other(Suit object)
		Return value : Boolean(True or False)
		"""
		#return true if self.value is less than other.value and viceversa
		return self.value < other.value


class Card:
	def __init__(self, rank: Rank, suit: Suit) -> None:
		"""
		Purpose: initialize the card object
		Argument: 1:rank(the value of Rank) 2:suit(the value of Suit)
		Return Value:None
		"""
		#assign suit and rank into the object card
		self.rank = rank
		self.suit = suit

	def __repr__(self) -> str:
		return self.__str__()

	def __str__(self) -> str:
		"""
		Purpose: To make the card become the actual card art display
		Argument:1:self objects
		Return value: Exact String of the card art

		Function body:
				4 if statement to check the card.suit and store the icon into the suit_icon variable as a string.
				create a empty string variable spaces to store the number of spaces we want and use a if statement 
				to check the rank value as rank.value = 10 will be taken one more spaces than other so the number of spaces
				inside the variable spaces for rank.value = 10 will always 1 lesser than the others.[eg:'    '(4spaces),'     '(five spaces)]
				Create a variable card_number to store the card.rank.value[eg:1,2,3...,10] as a string and use a if statement to
				check the card.rank.value is lesser or equal than 10, we cast it into a string and then store into the variable card_number.
				Else card.rank.value which is greater than 10[eg:11,12,13 which will be Jack,queen and King] store the first letter of the
				card.rank.name by indexing into the variable card_number.
				Create a variable output_string to store the final exact card art we want by string concanation.[eg:┌─────┐]
																													|4    |
																													|  ♣  |
																													|    4|
																													└─────┘
		Visualization example:
				Suit = clubs , Rank = 4
				suit.value = 1
				rank.value = 4
				suit_icon = '♣'
				spaces = '    '
				card_number = '4'
				output_string = [eg:┌─────┐]
									|4    |
									|  ♣  |
									|    4|
									└─────┘

		"""
		#determine the suit of card
		if self.suit.value == 1:
			suit_icon = '♣'
		elif self.suit.value == 2:
			suit_icon = '♦'
		elif self.suit.value == 3:
			suit_icon = '♠'
		elif self.suit.value == 4:
			suit_icon = '♥'

		#determine how many spaces to be printed in card
		spaces = ''
		if self.rank.value != 10:
			spaces = '    '
		else:
			spaces = '   '

		#determine the card number
		card_number = ''
		if self.rank.value <= 10:
			card_number = str(self.rank.value)
		else:
			card_number = self.rank.name[0]

		#combine suit, card_number and spaces to form a card
		output_string = '\n┌─────┐\n' 
		output_string += '│' + card_number + spaces + '│\n'
		output_string += '│  ' + suit_icon + '  │\n'
		output_string += '│' + spaces + card_number + '│\n'
		output_string += '└─────┘'

		#return the final output(card)
		return output_string

	def __eq__(self, other: Card) -> bool:
		"""
		Purpose:Check the two objects are equal or not
		Argument: 1:Self object 2:other(Card object)
		Return value: Boolean(True or False)
		"""
		return (self.rank.value == other.rank.value and self.suit.value == other.suit.value)

	def __lt__(self, other: Card) -> bool:
		"""
		Purpose: Use to sorting and comparing the value of two object
		Argument:1: self object 2: other(Card object)
		Return value : Boolean (True or False)

		Function body:
				first if statement to check the suit.value,return true if self.suit.value is less than other.suit.value
				Second elif statement execute when the situation become self.suit.value is equal to other.suit.value,
				compare the self.rank.value with other.rank.value and return true if self.rank.value is less than
				other.rank.value
				Else for these situation,always return False

		Visualization example:
				self.suit= Clubs
				self.suit.value = 1
				self.rank= Jack
				self.rank.value=11
				other.suit= Clubs
				other.suit.value = 1
				other.rank= Ace
				other.rank.value=14
				
				In this case self.suit.value is equal to other.suit.value(both Clubs),elif statement execute to compare
				the self.rank.value and other.rank.value[11<14] then return true
				
		"""
		#return true if the suit value of SELF is lower than OTHER
		if self.suit.value < other.suit.value:
			return True
		elif self.suit.value == other.suit.value:
			#return true if the rank value of SELF is lower than OTHER
			if self.rank.value < other.rank.value:
				return True
		#if non of the above requirement is satisfied, return false
		return False


	
