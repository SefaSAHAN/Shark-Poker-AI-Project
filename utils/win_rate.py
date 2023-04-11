import pandas as pd
import itertools
from utils.winnercheck import Winner
import random



class WinRate:
	def __init__(self,card_dict,board_cards_list):
		self.card_dict=card_dict
		self.board_cards_list=board_cards_list


	def sort_cards(self,cards):
		values = ['A','2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
		sorted_cards = sorted(cards, key=lambda c: values.index(c))
		return tuple(sorted_cards)
	
	def pre_flop_win_rate(self,bot,value=None):
		hand_letter=(self.card_dict[bot][0][-1],self.card_dict[bot][1][-1])
		hand=(self.card_dict[bot][0][:-1],self.card_dict[bot][1][:-1])
		hand=self.sort_cards(hand)
		frequency_list = [hand_letter.count(element) for element in set(hand_letter)]
		repeat2= any(element == 2 for element in frequency_list)
		if repeat2:
			hand=str(hand[0]+"D"+hand[1]+"D")
		else:
			hand=str(hand[0]+"D"+hand[1]+"C")
		df=pd.read_csv("data/win_rate.csv",low_memory=False)
		row=df[df['bot']==hand]
		win_rate = row["percentage"].iloc[0]
		if value=='value':
			if win_rate>0.6556:
				win_rate+=0.11
		return win_rate
	
	def flop_win_rate(self,bot):
		my_tuple=(	self.card_dict[bot][0],
	     			self.card_dict[bot][1],
	       			self.board_cards_list[0],
					self.board_cards_list[1],
					self.board_cards_list[2])

		my_tuple2=(	self.card_dict[bot][0],
	     			self.card_dict[bot][1],
	       			self.board_cards_list[0],
					self.board_cards_list[1],
					self.board_cards_list[2])
		
		result3 = [element for element in my_tuple2 if my_tuple2.count(element) == 3]
		result4 = [element for element in my_tuple2 if my_tuple2.count(element) == 4]
		result5 = [element for element in my_tuple2 if my_tuple2.count(element) == 5]
		tuple1=(self.card_dict[bot][0][:-1],self.card_dict[bot][1][:-1])
		sorted_tuple=self.sort_cards(tuple1)
		tuple2=(	self.board_cards_list[0][:-1],
	  				self.board_cards_list[1][:-1],
					self.board_cards_list[2][:-1]
					)
		sorted_tuple2=self.sort_cards(tuple2)
		control_tuple=(str(sorted_tuple[0]+sorted_tuple[1]),str(sorted_tuple2[0]+sorted_tuple2[1]+sorted_tuple2[2]))
		
		if len(result3)>0:			
			if my_tuple2[0]==result3[0] and my_tuple2[1]==result3[0]:
				df_string="3double"
								
			elif my_tuple2[0]==result3[0]:
				df_string="31result"
								
			elif my_tuple2[1]==result3[0]:
				if my_tuple[0][:-1]==my_tuple[0][:-1]:
					df_string="31result"
					
				else:
					df_string="32result"
					
			else:
				df_string="03result"
				

		elif len(result4)>0:			
			if my_tuple2[0]==result4[0] and my_tuple2[1]==result4[0]:
				df_string="4double"
				
			elif my_tuple2[0]==result4[0]:
				df_string="41result"
					
			else:
				if my_tuple[0][:-1]==my_tuple[0][:-1]:
					df_string="41result"
					
				else:
					df_string="42result"
				
		
		elif len(result5)>0:
			df_string="5result"
		
		
		else:
			result = [element for element in my_tuple2[2:] if my_tuple2[2:].count(element) == 2]
			if len(result)>0:
				df_string="normal2"
			
			else:
				df_string="normal1"
				

		df=pd.read_csv("data/win_rate.csv",low_memory=False)
		win_rate=df.loc[(df['status'] == df_string) & (df['bot'] == control_tuple[0]) & (df['community_cards'] == control_tuple[1]), 'percentage'].values[0]
		return win_rate
	
	def turn_win_rate(self,bot):
		deck = ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 
	  	'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',    
		'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',      
		'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS']
		bot_hand=(	self.card_dict[bot][0],
					self.card_dict[bot][1],
					self.board_cards_list[0],
					self.board_cards_list[1],
					self.board_cards_list[2],
					self.board_cards_list[3]
	     			)
		for i in self.board_cards_list[:4]:
			deck.remove(i)
		if bot=='bot':		
			for i in self.card_dict['player']:
				deck.remove(i)
		else:
			for i in self.card_dict['bot']:
				deck.remove(i)

		board_combinations = list(itertools.combinations(deck, 1))
		player_combinations= list(itertools.combinations(deck, 2))

		turn_count=0
		true_count=0
		for p1_hand in random.sample(player_combinations,200):
			if set(bot_hand) & set(p1_hand):
				continue
			for combination in board_combinations:
				if any(card in bot_hand or card in p1_hand for card in combination):
					continue
				else:
					turn_count+=1
					dict1={	"player1":[bot_hand[0],bot_hand[1]],
							"player2":[p1_hand[0],p1_hand[1]]
							}
					board=[	bot_hand[2],
							bot_hand[3],
							bot_hand[4],
							bot_hand[5],
							combination[0]
							]
					win = Winner(dict1, board)
					winner_list = win.winner_list
					
					if "player1" in winner_list :	
						true_count+=1	
		win_rate=true_count/turn_count
		return win_rate

	def river_win_rate(self,bot):
		deck = ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 
	  	'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',    
		'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',      
		'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS']
		bot_hand=(	self.card_dict[bot][0],
					self.card_dict[bot][1],
					self.board_cards_list[0],
					self.board_cards_list[1],
					self.board_cards_list[2],
					self.board_cards_list[3],
					self.board_cards_list[4],
	     			)
		for i in self.board_cards_list:
			deck.remove(i)
		if bot=='bot':		
			for i in self.card_dict['player']:
				deck.remove(i)
		else:
			for i in self.card_dict['bot']:
				deck.remove(i)

		player_combinations= list(itertools.combinations(deck, 2))

		turn_count=0
		true_count=0
		for p1_hand in player_combinations:
			turn_count+=1
			dict1={	"player1":[bot_hand[0],bot_hand[1]],
					"player2":[p1_hand[0],p1_hand[1]]
					}
			board=[	bot_hand[2],
					bot_hand[3],
					bot_hand[4],
					bot_hand[5],
					bot_hand[6]
					]
			win = Winner(dict1, board)
			winner_list = win.winner_list
			
			if "player1" in winner_list :	
				true_count+=1	
		win_rate=true_count/turn_count
		return win_rate



# #Try this code to see the reduce method works well but it takes some times
# lista=[]
# a=0
# while a<100000:
# 	a+=1
# 	deck = ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 
# 			'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',    
# 			'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',      
# 			'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS']

# 	player_list=["bot","player"]
# 	board_cards_list = random.sample(deck, 5)
# 	deck2=deck.copy()
# 	for i in board_cards_list:
# 		deck2.remove(i)
# 	bot_cards=random.sample(deck2,2)
# 	card_dict={'bot':bot_cards}

# 	win_class=WinRate(card_dict,board_cards_list)
# 	lista.append(win_class.pre_flop_win_rate('bot'))
# 	lista.append(win_class.flop_win_rate('bot'))

# print(len(lista))

