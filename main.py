from PyQt5.QtWidgets import  QApplication, QMainWindow 
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import warnings
from utils.win_rate import WinRate
from utils.winnercheck import Winner
from utils.ui_screen import Ui_MainWindow
import pandas as pd
import sys
import random

warnings.filterwarnings("ignore")


class Deck:
	def __init__(self, player_list=None):
		self.suits = ["D", "C", "H", "S"]
		self.board_cards_list = []
		self.deck = []
		self.player_list = player_list
		self.card_dict = {}

	def create_deck(self):
		# create the deck of cards using list comprehensions
		self.deck = [str(rank) + suit for suit in self.suits for rank in range(2, 11)]
		self.deck += ['A' + suit for suit in self.suits] + ['J' + suit for suit in self.suits] + ['Q' + suit for suit in self.suits] + ['K' + suit for suit in self.suits]
		
	def deal_cards(self):        
		self.create_deck()
		self.board_cards_list = random.sample(self.deck, 5)
		# remove the board cards from the deck
		self.deck = [card for card in self.deck if card not in self.board_cards_list]
		# deal 2 cards to each player and add the cards to the player's hand
		for player in self.player_list:
			hand = random.sample(self.deck, 2)
			self.card_dict[player] = hand
			# remove the player cards from the deck
			self.deck = [card for card in self.deck if card not in hand]


class Game(QMainWindow):
	def __init__(self):
		super().__init__() 
		# Initialize the UI
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		# Set initial budget for the bot and player
		self.budget={"bot":20000,"player":20000}
		# Connect the buttons to their corresponding functions
		self.ui.btn_call.clicked.connect(self.call_btn)
		self.ui.btn_fold.clicked.connect(self.fold_btn)
		self.ui.btn_bet.clicked.connect(self.raise_btn)
		#Train Model
		self.train()
		# Start the round
		self.start_round()
		# Make the bot's decision
		self.bot_decision_mthd()

	def train(self):
		# Load the dataset
		df = pd.read_csv("data/check.csv")


		
		# separate the features (win_rate) and target (bot_decision)
		X = df['win_rate'].values.reshape(-1, 1)
		y = df['bot_decision']

		# train the decision tree classifier
		self.model_check = DecisionTreeClassifier()
		self.model_check.fit(X, y)

		# set the feature names
		self.model_check.feature_names = ['win_rate']	

		# Load the dataset
		df = pd.read_csv("data/raise.csv")

		# separate the features (win_rate, pot, player_raise_amount) and target (bot_decision)
		X = df[['win_rate', 'pot', 'player_raise_amount']]
		y = df['bot_decision']

		# train the Random Forest classifier
		self.model_raise = RandomForestClassifier()
		self.model_raise.fit(X, y)

		# Load the dataset
		df = pd.read_csv("data/raise_amount.csv")

		# separate the features (win_rate, pot, player_raise_amount) and target (bot_decision)
		X = df['win_rate'].values.reshape(-1, 1)
		y = df['bot_decision']

		# train the Random Forest classifier
		self.model_raise_amount = RandomForestClassifier()
		self.model_raise_amount.fit(X, y)
	
	def predict_check(self):
		data=[[self.bot_win_rate]]
		
		prediction=self.model_check.predict(data)
		if prediction==0:
			self.bot_decision='check'
		else:
			self.bot_decision='raise'

	def predict_raise(self):
		data=[[self.bot_win_rate,self.pot,self.player_raise_amount]]
		prediction=self.model_raise.predict(data)
		if prediction==0:
			self.bot_decision='fold'
		elif prediction==1:
			self.bot_decision='call'
		else:
			self.bot_decision='raise'

	def predict_raise_amount(self):
		data=[[self.bot_win_rate]]
		prediction=self.model_check.predict(data)
		if prediction==0:
			self.bot_raise_amount=400
		if prediction==1:
			self.bot_raise_amount=600
		if prediction==2:
			self.bot_raise_amount=1200
		if prediction==3:
			self.bot_raise_amount=2000
		if prediction==4 :
			self.bot_raise_amount=20000
		if self.player_decision=='raise':
			self.bot_raise_amount+=self.player_raise_amount





	def table_set(self):
		# Adjust the table settings
		self.ui.table.clearContents()
		self.ui.table.horizontalHeader().setStyleSheet("::section { background-color: #007C00; }")
		self.ui.table.verticalHeader().setStyleSheet("::section { background-color: #007C00; }")
		self.ui.table.resizeColumnsToContents()
		self.ui.table.resizeRowsToContents()
		self.ui.table.setMinimumHeight(self.ui.table.rowHeight(0) * self.ui.table.rowCount() + self.ui.table.horizontalHeader().height())
		self.ui.table.setMaximumHeight(self.ui.table.minimumHeight())
		self.ui.table.setMinimumWidth(self.ui.table.columnWidth(0) * self.ui.table.columnCount() + self.ui.table.verticalHeader().width())
		self.ui.table.setMaximumWidth(self.ui.table.minimumWidth())
		self.ui.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.ui.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

	def bot_decision_mthd(self):
		# Make the bot's decision based on the player's decision
		if self.player_decision=="raise":
			self.predict_raise()
			self.ui.p_bet_chip.setVisible(False)
			self.ui.p_bet.setVisible(False)
		else:
			self.predict_check()
		if self.bot_decision=='raise':
			self.predict_raise_amount()
		

		# Fold if bot decides to fold
		if self.bot_decision=='fold':
			self.ui.table.setItem(self.poker_phase, 0, QtWidgets.QTableWidgetItem("fold"))
			self.finish_turn()
			# If it's still not the end of the game, make the bot's decision again after a delay
			if self.poker_phase<2:
				QTimer.singleShot(1000, self.bot_decision_mthd)
			else:
				self.bot_decision_mthd()
		else:
			# Check if the bot's raise amount is more than its budget or the player's budget
			if self.bot_raise_amount>self.budget['bot']+self.bet['bot']:
				self.bot_raise_amount=self.budget['bot']+self.bet['bot']
			if self.bot_raise_amount>self.budget['player']+self.player_raise_amount:
				self.bot_raise_amount=self.budget['player']+self.player_raise_amount

			# Make the bot's decision visible on the table
			if self.poker_phase==0 and self.bot_raise_amount==0 and self.player_decision!='raise':
				self.ui.table.setItem(0, 0, QtWidgets.QTableWidgetItem("r200"))
				self.ui.bot_decision.setText("check")
				self.bot_raise_amount=200			
			else:
				self.ui.bot_decision.setText(self.bot_decision)
				if self.bot_decision=='raise':
					self.ui.table.setItem(self.poker_phase, 0, QtWidgets.QTableWidgetItem(f"r{self.bot_raise_amount}"))
				elif self.bot_decision=='call':
					self.ui.table.setItem(self.poker_phase, 0, QtWidgets.QTableWidgetItem(f"c{self.player_raise_amount}"))
				else:
					self.ui.table.setItem(self.poker_phase, 0, QtWidgets.QTableWidgetItem(self.bot_decision))
			
			if self.poker_phase>0 and self.bot_decision=='check':
				self.ui.bot_bet_chip.setVisible(False)
				self.ui.bot_bet.setVisible(False)
			else:
				self.ui.bot_bet_chip.setVisible(True)
				self.ui.bot_bet.setVisible(True)
					
			if self.player_decision=='raise':
				self.budget['bot']-=self.bot_raise_amount-self.bet['bot']
				self.total_bet['bot']+=self.bot_raise_amount-self.bet['bot']
			else:	
				self.budget['bot']-=self.bot_raise_amount
				self.total_bet['bot']+=self.bot_raise_amount

			self.bet['bot']=self.bot_raise_amount
			self.ui_budget_pot()

			if self.control_player=="bot":
				if self.bot_decision=='raise':
					self.control_player='player'
				else:
					self.show_community_cards()
					self.player_raise_amount=0
					self.bot_raise_amount=0
					self.ui_budget_pot()
					self.poker_phase+=1
					self.player_hand_check()
					self.bot_hand_check()
					any_zero = any(value == 0 for value in self.budget.values())

					if any_zero:
						self.finish_turn()
						if self.poker_phase<2:
							QTimer.singleShot(1000, self.bot_decision_mthd)
						else:
							self.bot_decision_mthd()
					
					if self.poker_phase==4:
						self.finish_turn()
						if self.poker_phase<2:
							QTimer.singleShot(1000, self.bot_decision_mthd)
						else:
							self.bot_decision_mthd()

	def raise_btn(self):
		# Activate call_btn method when unproper usage of raise button
		if self.slider_value==self.bot_raise_amount:
			self.call_btn()
		else:
			# Make the player's raise amount visible on the table
			self.ui.p_bet_chip.setVisible(True)
			self.ui.p_bet.setVisible(True)
			self.ui.p_bet.setText(str(self.slider_value))

			# Deduct the raise amount from the player's budget and update the total bet
			if self.player_decision=='raise':
				self.budget['player']-=self.slider_value-self.bot_raise_amount
				self.total_bet['player']+=self.slider_value-self.bot_raise_amount
			else:
				self.budget['player']-=self.slider_value
				self.total_bet['player']+=self.slider_value

			# Set player's decision to raise and update control player	
			self.player_decision='raise'
			self.control_player='bot'
			self.player_raise_amount=self.slider_value

			# Update the pot and display the raise on the table
			self.pot=self.pot=40000-sum(self.budget.values())
			self.ui.table.setItem(self.poker_phase, 1, QtWidgets.QTableWidgetItem(f"r{self.slider_value}"))

			# Call the bot's decision method with a delay
			if self.poker_phase<2:
				QTimer.singleShot(1000, self.bot_decision_mthd)
			else:
				self.bot_decision_mthd()

	def ui_budget_pot(self):
		# Determine the maximum bet value based on the current budgets and raise amounts
		if self.budget['bot']+self.bot_raise_amount<=self.budget['player']+self.player_raise_amount:
			max_value=self.budget['bot']+self.bot_raise_amount
		else:
			max_value=self.budget['player']+self.player_raise_amount

		# Set the slider's maximum and minimum values, and its current value to the bot's raise amount
		self.ui.slider.setMaximum(max_value)
		self.ui.btn_bet.setText(str(self.bot_raise_amount))
		self.ui.slider.setMinimum(self.bot_raise_amount)
		self.ui.slider.setValue(self.bot_raise_amount)

		# Show or hide the bot's bet chip and bet label depending on whether the bot is checking or not
		if self.poker_phase>0 and self.bot_decision=='check':
			self.ui.bot_bet_chip.setVisible(False)
			self.ui.bot_bet.setVisible(False)
		else:
			self.ui.bot_bet_chip.setVisible(True)
			self.ui.bot_bet.setVisible(True)

		# Update the budget and pot displays
		self.ui.bot_budget.setText(str(self.budget['bot']))
		self.pot=40000-sum(self.budget.values())
		self.ui.pot.setText(str(self.pot))
		if self.bot_raise_amount==0:
			self.ui.bot_bet.setText(str(''))
		else:
			self.ui.bot_bet.setText(str(self.bot_raise_amount))
		self.ui.player_budget.setText(str(self.budget['player']))

	def call_btn(self):
		# Reset the bet and update the player decision
		self.bet={"bot":0,"player":0}
		self.total_bet['player']=self.total_bet['bot']
		self.budget['player']-=self.bot_raise_amount
		self.player_decision="call"

		# Update the table with the player's decision
		if self.bot_raise_amount==0:
			self.ui.table.setItem(self.poker_phase, 1, QtWidgets.QTableWidgetItem("check"))
		else:
			self.ui.table.setItem(self.poker_phase, 1, QtWidgets.QTableWidgetItem(f"c{self.bot_raise_amount}"))
		
		# Update the UI with the budget and pot values
		self.ui_budget_pot()

		# If it's the control player's turn, show the community cards, update the pot, and move to the next phase
		if self.control_player=="player":
			self.show_community_cards()
			self.player_raise_amount=0
			self.bot_raise_amount=0
			self.ui_budget_pot()
			self.poker_phase+=1

			# Check the hands qualities and finish the turn if either player has no budget left or it's the last phase
			self.player_hand_check()
			self.bot_hand_check()
			any_zero = any(value == 0 for value in self.budget.values())
			if any_zero:
				self.finish_turn()
			if self.poker_phase==4:
				self.finish_turn()

		# Hide the player's bet 
		if self.poker_phase>0 :
			self.ui.p_bet_chip.setVisible(False)
			self.ui.p_bet.setVisible(False)
		else:
			self.ui.p_bet_chip.setVisible(True)
			self.ui.p_bet.setVisible(True)
		if self.poker_phase<2:
			QTimer.singleShot(1000, self.bot_decision_mthd)
		else:
			self.bot_decision_mthd()
		
	def fold_btn(self):
		self.ui.table.setItem(self.poker_phase, 1, QtWidgets.QTableWidgetItem("fold"))
		self.player_decision='fold'
		self.finish_turn()	
		QTimer.singleShot(1000, self.bot_decision_mthd)

	def finish_turn(self):
		# Create an empty list to store the winner(s) of the round
		winner_list=['']
		# Show the bot's cards on the UI
		self.ui.bot_card1.setPixmap(QtGui.QPixmap(f":/images/{self.card_dict['bot'][0]}.png"))
		self.ui.bot_card2.setPixmap(QtGui.QPixmap(f":/images/{self.card_dict['bot'][1]}.png"))

		# If the bot folded, add the pot to the player's budget and set the winner as "Player"
		if self.bot_decision=='fold':
			self.budget['player']+=self.pot
			winner='Player'

		# If the player folded, add the pot to the bot's budget and set the winner as "Shark Poker"
		elif self.player_decision=='fold':
			self.budget['bot']+=self.pot
			winner='Shark Poker'

		# If neither the bot nor the player folded, show the board cards on the UI and determine the winner
		else:
			self.ui.desk_card1.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[0]}.png"))
			self.ui.desk_card2.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[1]}.png"))
			self.ui.desk_card3.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[2]}.png"))
			self.ui.desk_card4.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[3]}.png"))
			self.ui.desk_card5.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[4]}.png"))
			# Create a dictionary of the bot and player's cards and pass it to the Winner class to determine the winner(s)
			new_dict={	"player1":self.card_dict["bot"],
		 				'player2':self.card_dict['player']}
			win=Winner(new_dict,self.board_cards_list)
			winner_list=win.winner_list

			# If both the bot and player have the same ranking hand, split the pot and set the winner as "Shark Poker & Player"
			if "player1" in winner_list and "player2" in winner_list:
				winner='Shark Poker & Player'
				self.budget['player']+=int(self.pot/2)
				self.budget['bot']+=self.pot/2

			# If only the bot has the highest ranking hand, add the pot to the bot's budget and set the winner as "Shark Poker"	
			elif "player1" in winner_list :
				winner='Shark Poker'
				self.budget['bot']+=self.pot
			
			# If only the player has the highest ranking hand, add the pot to the player's budget and set the winner as "Player"
			else:
				self.budget['player']+=self.pot
				winner='Player'

		# Display a message box showing the winner(s) and their ranking hand
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/images/ICON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.messagebox=QtWidgets.QMessageBox()
		self.messagebox.setText(f"{winner} \n{winner_list[-1]}")
		self.messagebox.setWindowTitle('Winner            ')
		self.messagebox.setWindowIcon(icon)
		self.messagebox.exec_()

		# Check if any player's budget is zero, and if so, end the game, show the winner as message and reset the budgets
		any_zero = any(value == 0 for value in self.budget.values())
		if any_zero:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(":/images/ICON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.messagebox=QtWidgets.QMessageBox()
			self.messagebox.setText(f"Winner is {winner} \n")
			self.messagebox.setWindowTitle('Game Finish    ')
			self.messagebox.setWindowIcon(icon)
			self.messagebox.exec_()
			self.budget={"bot":20000,"player":20000}

		self.ui_budget_pot()
		self.start_round()
		
	def start_round(self):
		# Set control player to player
		self.control_player="player"

		# Set all cards on the table and in bot's hand to be face down (1B.png)
		self.ui.bot_card1.setPixmap(QtGui.QPixmap(f":/images/1B.png"))
		self.ui.bot_card2.setPixmap(QtGui.QPixmap(f":/images/1B.png"))
		self.ui.desk_card1.setPixmap(QtGui.QPixmap(f":/images/1B.png"))
		self.ui.desk_card2.setPixmap(QtGui.QPixmap(f":/images/1B.png"))
		self.ui.desk_card3.setPixmap(QtGui.QPixmap(f":/images/1B.png"))
		self.ui.desk_card4.setPixmap(QtGui.QPixmap(f":/images/1B.png"))
		self.ui.desk_card5.setPixmap(QtGui.QPixmap(f":/images/1B.png"))

		# Set the table (betting area) to its initial state
		self.table_set()

		# Set the player_list to ["bot", "player"] and bet and total_bet dictionaries to 0
		self.player_list=["bot","player"]
		self.bet={"bot":0,"player":0}
		self.total_bet={"bot":0,"player":0}
		self.pot=0
		self.ui.slider.valueChanged.connect(self.slider_increase)

		# Create a new deck of cards and deal the cards to each player and the board
		self.deck = Deck(self.player_list)
		self.deck.deal_cards()
		self.card_dict = self.deck.card_dict
		self.board_cards_list=self.deck.board_cards_list

		# Set the poker phase, player and bot raise amounts, and player and bot decisions to their initial values
		self.poker_phase=0
		self.player_raise_amount=0
		self.bot_raise_amount=0
		self.player_decision="check"
		self.bot_decision="check"

		# Set the control player to player, and check the bot and player's hands for possible combinations
		self.control_player='player'
		self.bot_hand_check()
		self.player_hand_check()

		# Show the player's hand on the UI
		self.show_player_hand()
		
	def slider_increase(self,value):
		self.ui.btn_bet.setText(str(value))
		self.slider_value=value

	def show_community_cards(self):
		if self.poker_phase==0:
			self.ui.desk_card1.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[0]}.png"))
			self.ui.desk_card2.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[1]}.png"))
			self.ui.desk_card3.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[2]}.png"))
		elif self.poker_phase==1:
			self.ui.desk_card4.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[3]}.png"))
		elif self.poker_phase==2:
			self.ui.desk_card5.setPixmap(QtGui.QPixmap(f":/images/{self.board_cards_list[4]}.png"))

	def player_hand_check(self):
		self.win_rate=WinRate(self.card_dict,self.board_cards_list)
		if self.poker_phase==0:	
			self.player_win_rate=self.win_rate.pre_flop_win_rate("player")

		elif self.poker_phase==1:
			self.player_win_rate=self.win_rate.flop_win_rate("player")

		elif self.poker_phase==2:
			self.player_win_rate=self.win_rate.turn_win_rate("player")

		else:
			self.player_win_rate=self.win_rate.river_win_rate("player")
			
		self.show_player_hand()
			
	def bot_hand_check(self):
		self.win_rate=WinRate(self.card_dict,self.board_cards_list)

		if self.poker_phase==0:	
			self.bot_win_rate=self.win_rate.pre_flop_win_rate("bot",'value')
			
				
		elif self.poker_phase==1:
			self.bot_win_rate=self.win_rate.flop_win_rate("bot")

		elif self.poker_phase==2:
			self.bot_win_rate=self.win_rate.turn_win_rate("bot")
				
		else:
			self.bot_win_rate=self.win_rate.river_win_rate("bot")
			
		self.bot_win_rate=float(self.bot_win_rate)
		# print(self.bot_win_rate)	
	
	def show_player_hand(self):
		self.ui.p_card1.setPixmap(QtGui.QPixmap(f":/images/{self.card_dict['player'][0]}.png"))
		self.ui.p_card2.setPixmap(QtGui.QPixmap(f":/images/{self.card_dict['player'][1]}.png"))
		self.player_win_rate = round(float(self.player_win_rate) * 100)
		value = int(self.player_win_rate)
		# Set the value of the progress bar
		self.ui.progressBar.setValue(value)
		# Change the color based on the value
		if value < 45:
			color = "#ff6666" # red
		elif value < 60:
			color = "#ffd966" # orange
		elif value < 70:
			color =  "#55aadd" # blue
		else:
			color = "#85bb65" # green
		style = f"QProgressBar::chunk {{ background-color: {color} }};"
		self.ui.progressBar.setStyleSheet(style)
		 		
app = QApplication(sys.argv)
mainwindow = Game()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("SHARK POKER GAME")
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap(":/images/ICON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
widget.setWindowIcon(icon)
widget.setFixedHeight(643)
widget.setFixedWidth(742)
widget.show()
sys.exit(app.exec())