from __future__ import annotations
from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer

class Round:
	def __init__(self, players: list[Player]) -> None:
		two_of_clubs = Card(Rank.Two, Suit.Clubs)
		queen_of_spades = Card(Rank.Queen, Suit.Spades)
		broken_hearts = False
		n_player_turn = -1

		#set round score to 0
		for player in players:
			player.round_score = 0

		for game_round in range(len(players[0].hand)):
		# for game_round in range(4):
			trick = []
			greatest_card_in_trick = (two_of_clubs, -1) #greatest card, player who played it
			#first card
			if game_round == 0:
				for player_index, player in enumerate(players):
					for card in player.hand:
						if two_of_clubs == card:
							trick.append(two_of_clubs)
							player.hand.remove(two_of_clubs)
							n_player_turn = player_index
							print("Player " + str(n_player_turn + 1) + " plays", two_of_clubs)

			if game_round == 0:
				remaining_turns = len(players) - 1
			else:
				remaining_turns = len(players)
				
			for _ in range(remaining_turns):
				n_player_turn += 1
				if n_player_turn >= len(players):
					n_player_turn -= len(players)

				played_card = players[n_player_turn].play_card(trick, broken_hearts)
				trick.append(played_card)
				print("Player " + str(n_player_turn + 1) + " plays", played_card)

				if played_card.suit.value == 4:
					broken_hearts = True
				if (played_card.suit.value == trick[0].suit.value) and (played_card.rank.value > greatest_card_in_trick[0].rank.value):
					greatest_card_in_trick = (played_card, n_player_turn)
				
			scores_to_add = 0
			for card in trick:
				if card.suit.value == 4:
					scores_to_add += 1
				if card == queen_of_spades:
					scores_to_add += 13

			players[greatest_card_in_trick[1]].round_score += scores_to_add

			print("Player " + str(greatest_card_in_trick[1] + 1) + " takes the trick. Points received:", scores_to_add)
			
			n_player_turn = greatest_card_in_trick[1] - 1
