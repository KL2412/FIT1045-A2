from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player


class HumanPlayer(Player):
    def __init__(self):
        """
        Purpose: Override the init method inheritance from Player class by getting user input
        Arguments:1: self object
        Return value:None

        Function body:
                ask for the user input and store it into local variable name as a string.
                call Player.__init__ method, pass the variable name as the argument to crete the object.

        Visualization example:
                When HumanPlayer() is called, ask user to input a string [eg:'John'],store it into variable name.
                Call the Player.__init__(),pass the string 'John' as a argument.
                The human player now has a name 'John' as it attribute.
        """
        name = input('Please enter your name: ')
        Player.__init__(self, name)

    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
        """
        Purpose:Get the input choice from user by indexing to check which card to play.
        Argument:1:trick(list of card object)
                 2:broken_hearts(Boolean)
        Return value : Card object

        Function body:
                Call self.sort_cards to sort the card in the clear order.
                Print the card using method self.print_hand
                While loop to get the user choice in int value[0,1,2...]
                    store the int input into local variable choice.
                    if statement to check the value of choice is in the range of the self.hand[eg:self.hand only have 10 card,but the value of choice>10]
                    else value of choice is not in the range, print a error message and prompt again the input.
                    create a local variable choice_card which store the card in self.hand by passing choice as the index.
                    call the self.check_valid_play method,store the return boolean into variable valid_move.
                        if statement to check if valid_move is True,remove the choice_card from self.hand and return choice_card
                        else print an error message.

        Visualization example:
                Card=[Ten of spades,Two of clubs,Three of Diamonds](all in card art string!)
                self.sort_cards() called.
                Card=[Two of clubs,Three of Diamonds,Ten of spades]
                print the list of Card in actual card art[eg.Two of clubs,┌─────┐]
                                                                          |2    |
                                                                          |  ♣  |
                                                                          |    2|
                                                                          └─────┘
                While loop iterate:
                        choice = 0
                        choice_card = self.hand[0]
                        valid true= true
                        self.hand.remove(choice_card)
                        return choice card(card art of Two of clubs)
        """
        #sort cards in hand
        self.sort_cards()

        #print player's hand to let player choose a card to play
        print("Your current hand:")
        print(self.print_hand())

        #while loop which keep looping until player chooses a valid card
        while(True):
            choice = int(input("Select a card to play: "))

            #choice is in self.hand range
            if(choice >= 0 and choice <= len(self.hand)-1):
                choice_card = self.hand[choice]
                valid_move = self.check_valid_play(choice_card, trick, broken_hearts)[0]
                #valid card is chosen
                if(valid_move):
                    self.hand.remove(choice_card)
                    return choice_card
                #invalid card is chosen
                else:
                    print(self.check_valid_play(
                        choice_card, trick, broken_hearts)[1])
            #choice is not in self.hand range
            else:
                print("Index is not defined!")

    def pass_cards(self, passing_to: str) -> list[Card]:
        """
        Purpose: Choose three card to pass
        Argument: 1:self object 2:passing_to:String
        Return value: List of card object

        Function body:
                sort.card into a clear way.
                print the card in self.hand.
                While loop iterate:
                        create variable outofrange,duplicatevalues,indexnegative,lessthan3cards and initialize with value 0.
                        Ask the user input in String[eg:1,2,3] and split into a list with .split(,)method,store the list into
                        variable list_choice.
                    For loop loop through the element in list_choice:
                        if statement to check the situation if the index input bu user is in the range of self.hand
                        print a error message show index card is out of range.
                        Add the value of outofrange.
                        if statement to check the given index input is a positive int
                        print a error message if index input is negative int
                        Add the value of indexnegative.
                    Two if statement to check the index input if it is duplicate and the element in list_choice is three.
                    Last if statement to check if the list_choice is true for all situation.
                        A empty list to_pass create
                        for loop literate the element list_choice and append the three element into to_pass.
                         for loopp literate through to_pass list ,pass the element as a argument and remove it from self.hand
                         return to_pass list

        """
        #sort cards in hand
        self.sort_cards()

        #print players hand to let player choose which cards to be passed
        print("Your current hand:")
        print(self.print_hand())

        #keeps looping if invalid choices are made by player
        while(True):
            #declare variable to act as flags
            outofrange = 0
            duplicatevalues = 0
            indexnegative = 0
            lessthan3cards = 0

            #prompt user for input selection
            choice = input("Select 3 cards to pass off [e.g. '0, 4, 5'] to Player " + str(passing_to + 1) + ": ")
            #split the string into a list of number characters
            list_choice = choice.strip().split(',')

            #check if any of the number is out of range or negetive
            for i in list_choice:
                if(int(i) > len(self.hand)-1):
                    print("Index card -", "'", i, "'", "is out of range!")
                    outofrange = outofrange + 1
                if(int(i) < 0):
                    print("Index cannot be negative!")
                    indexnegative = indexnegative + 1

            #check if user has entered duplicated values
            if(len(list_choice) > len(set(list_choice))):
                print("User input has duplicate values!")
                duplicatevalues = duplicatevalues + 1

            #check if user has entered more or less than 3 cards
            if(len(set(list_choice)) != 3):
                print("Need to select 3 cards!")
                lessthan3cards = lessthan3cards + 1

            #remove spaces from string if player enter 1, 2, 3 - the space before 2 and before 3 can be removed
            for i in range(len(list_choice)):
                list_choice[i] = list_choice[i].strip()

            #if the selection is valid, return the passed card and remove the cards from the player's hand
            if(outofrange == 0 and duplicatevalues == 0 and indexnegative == 0 and lessthan3cards == 0):
                to_pass = []
                for indexes in list_choice:
                    to_pass.append(self.hand[int(indexes)])
                for cards_to_pass in to_pass:
                    self.hand.remove(cards_to_pass)
                print('Cards have been passed')
                return to_pass

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

    def print_hand(self) -> str:
        """
        Purpose:Print all the card in the hand
        Argument:1:self object
        Return value: output_string

        Function body:
                for loop literate through the card in player hand
                    determine the suit of card using 4 if statement
                    determine how many spaces to be print in Card as value 10 take different space with value 1
                    determine the card number(value) with if else statement[eg:1,2,3...10 or J,Q,K]
                    Append all three factor into the tuple for indexing
                    print the card horizontally by for loop in range(6)
                    return output_string

        """

        #initialize a tuple
        cards_tuple = []

        #for every card in player hand
        for card in self.hand:
            #determine the suit of card
            if card.suit.value == 1:
                suit_icon = '♣'
            elif card.suit.value == 2:
                suit_icon = '♦'
            elif card.suit.value == 3:
                suit_icon = '♠'
            elif card.suit.value == 4:
                suit_icon = '♥'

            #determine how many spaces to be printed in card
            spaces = ''
            if card.rank.value != 10:
                spaces = '    '
            else:
                spaces = '   '

            #determine the card number
            card_number = ''
            if card.rank.value <= 10:
                card_number = str(card.rank.value)
            else:
                card_number = card.rank.name[0]
                
            #append all three factors above into tuple
            cards_tuple.append((suit_icon, spaces, card_number))

        #print the cards horizontally
        output_string = ''
        for row in range(6):
            for index, cards in enumerate(cards_tuple):
                if row == 0:
                    output_string += '┌─────┐' 
                elif row == 1:
                    output_string += '│' + cards[2] + cards[1] + '│'
                elif row == 2:
                    output_string += '│  ' + cards[0] + '  │'
                elif row == 3:
                    output_string += '│' + cards[1] + cards[2] + '│'
                elif row == 4:
                    output_string += '└─────┘'
                elif row == 5:
                    if index < 10:
                        output_string += "   " 
                    else:
                        output_string += "  "
                    output_string += str(index) + "   "
            output_string += '\n'

        return output_string

