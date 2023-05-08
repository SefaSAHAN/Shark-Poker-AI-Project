import random 


class Bot:
    def __init__(self, pot, player_decision, bot_win_rate, player_raise_amount=None):
        self.pot = pot
        self.player_decision = player_decision
        self.player_raise_amount = player_raise_amount
        self.bot_win_rate = bot_win_rate
        self.bot_decision = ""
        self.bot_raise_amount=0

    def bot_decision_mth(self):
        if self.player_decision == "check" or self.player_decision == "call":
            if self.bot_win_rate < 0.40:
                if random.random() < 0.99:
                    self.bot_raise_amount= 0
                    self.bot_decision = "check"
                else:
                    self.bot_raise_amount = random.choice([400]*36 + [600]*3 + [1200]*2 + [2000]*1 )
                    self.bot_decision = "raise"
            elif self.bot_win_rate < 0.6:
                if random.random() < 0.95:
                    self.bot_raise_amount= 0
                    self.bot_decision = "check"
                else:
                    self.bot_raise_amount = random.choice([400]*18 + [600]*6 + [1200]*2 + [2000]*1 )
                    self.bot_decision = "raise"

            elif 0.6 <= self.bot_win_rate < 0.7:
                if random.random() < 0.75:
                    self.bot_raise_amount = 0
                    self.bot_decision = "check"
                else:
                    self.bot_raise_amount = random.choice([400]*14 + [600]*6 + [1200]*3 + [2000]*2 + [20000]*1)
                    self.bot_decision = "raise"

            else:
                if random.random() < 0.45:
                    self.bot_raise_amount = 0
                    self.bot_decision = "check"
                else:
                    self.bot_raise_amount = random.choice([400]*4 + [600]*10 + [1200]*6 + [2000]*4 + [20000]*2)
                    self.bot_decision = "raise"

        else:
            self.pot-=self.player_raise_amount
            if self.bot_win_rate < 0.40:
                if self.player_raise_amount < 201:
                    if random.random() < 0.85:
                        self.bot_decision = "call"
                        self.bot_raise_amount=self.player_raise_amount
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"

                elif self.player_raise_amount < 400:
                    if random.random() < 0.45:
                        self.bot_decision = "call"
                        self.bot_raise_amount=self.player_raise_amount
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"
                else:
                    self.bot_raise_amount = 0
                    self.bot_decision = "fold"

            elif self.bot_win_rate >= 0.40 and self.bot_win_rate < 0.55:
                if self.player_raise_amount <= self.pot/2:
                    if random.random() < 0.85:
                        if random.random()<0.95:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<95:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"

                elif self.player_raise_amount <= self.pot:
                    if random.random() < 0.6:
                        if random.random()<0.95:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<95:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"

                elif self.player_raise_amount < self.pot*2:
                    if random.random() < 0.4:
                        if random.random()<0.95:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<95:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"
                else:
                    self.bot_raise_amount = 0
                    self.bot_decision = "fold"

            elif self.bot_win_rate >= 0.55 and self.bot_win_rate < 0.70:			
                if self.player_raise_amount <= self.pot/2:
                    if random.random() < 0.90:
                        if random.random()<0.80:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<80:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"
                        
                elif self.player_raise_amount <= self.pot:
                    if random.random() < 0.75:
                        if random.random()<0.80:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<80:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"

                elif self.player_raise_amount <= self.pot*2:
                    if random.random() < 0.5:
                        if random.random()<0.80:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<80:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"
                else:
                    self.bot_raise_amount = 0
                    self.bot_decision = "fold"
            
            elif self.bot_win_rate >= 0.70 and self.bot_win_rate < 0.80:			
                if self.player_raise_amount <= self.pot/2:
                    if random.random() < 0.999:
                        if random.random()<0.70:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<70:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"
                        
                elif self.player_raise_amount <= self.pot:
                    if random.random() < 0.9:
                        if random.random()<0.70:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<70:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"

                elif self.player_raise_amount <= self.pot*3:
                    if random.random() < 0.75:
                        if random.random()<0.70:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<70:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"
                else:
                    if random.random() < 0.35:
                        if random.random()<0.70:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<70:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000

            elif self.bot_win_rate >= 0.80 and self.bot_win_rate < 0.85:
                if self.player_raise_amount <= self.pot*3:
                    if random.random() < 0.75:
                        if random.random()<0.70:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<70:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"
                else:
                    if random.random() < 0.50:
                        if random.random()<0.70:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<70:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000

            elif self.bot_win_rate <= 0.95:			                
                if self.player_raise_amount <= self.pot:
                    if random.random() < 0.99:
                        if random.random()<0.50:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<50:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"

                elif self.player_raise_amount <= self.pot*3:
                    if random.random() < 0.90:
                        if random.random()<0.50:
                            self.bot_decision = "call"
                            self.bot_raise_amount=self.player_raise_amount
                        else:
                            self.bot_decision="raise"
                            if random.random()<50:
                                self.bot_raise_amount=self.player_raise_amount+500
                            else:
                                self.bot_raise_amount=self.player_raise_amount+1000
                    else:
                        self.bot_raise_amount = 0
                        self.bot_decision = "fold"
                else:
                    self.bot_raise_amount = 0
                    self.bot_decision = "fold"		
            else:	
                if random.random()<0.50:
                    self.bot_decision = "call"
                    self.bot_raise_amount=self.player_raise_amount
                else:
                    self.bot_decision="raise"
                    if random.random()<50:
                        self.bot_raise_amount=self.player_raise_amount+500
                    else:
                        self.bot_raise_amount=self.player_raise_amount+1000


import csv

##Create bot dataset when player choose call or check

# a=0
# while a<100000:
#     a+=1
#     bot_win_rate=random.random()
#     value=random.random()
#     pot=value*40000
#     decision_list=["check","call"]
#     player_decision=random.choice(decision_list)
#     shark_poker=Bot(pot,player_decision,bot_win_rate)
#     shark_poker.bot_decision_mth()
#     bot_decision=shark_poker.bot_decision

#     if bot_decision=='check':
#         value=0
#     elif bot_decision=='raise':
#         value=1
#     else:
#         value=500

#     data=[bot_win_rate,value]

#     with open('check.csv', 'a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(data)


##Create bot dataset when player choose raise

# a=0
# while a<100000:
#     a+=1
#     bot_win_rate=random.random()
#     value=random.random()
#     pot=value*40000
#     player_decision="raise"
#     value=random.random()
#     player_raise_amount=value*((40000-pot)/2)
#     shark_poker=Bot(pot,player_decision,bot_win_rate,player_raise_amount)
#     shark_poker.bot_decision_mth()
#     bot_decision=shark_poker.bot_decision

#     if bot_decision=='call':
#         value=1
#     elif bot_decision=='raise':
#         value=2
#     else:
#         value=0

#     data=[bot_win_rate,pot,player_raise_amount,value]

#     with open('raise.csv', 'a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(data)


##Create bot dataset when bot choose raise

# a=0
# while a<50000:

#     bot_win_rate=random.random()
#     value=random.random()
#     pot=value*40000
#     decision_list=["check","call"]
#     player_decision=random.choice(decision_list)
#     shark_poker=Bot(pot,player_decision,bot_win_rate)
#     shark_poker.bot_decision_mth()
#     bot_decision=shark_poker.bot_decision
#     raise_amount=shark_poker.bot_raise_amount


#     if bot_decision=='check':
#         value=0
#     elif bot_decision=='raise':
#         value=1
#     else:
#         value=500

#     if value==1 :
#         if raise_amount==400:
#             raise_amount=0
#         if raise_amount==600:
#             raise_amount=1
#         if raise_amount==1200:
#             raise_amount=2
#         if raise_amount==2000:
#             raise_amount=3
#         if raise_amount==20000 :
#             raise_amount=4
#         data=[bot_win_rate,raise_amount]
#         a+=1
#         with open('raise_amount.csv', 'a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(data)



# import pandas as pd

# # load the csv file
# df = pd.read_csv('output.csv')

# # split the data into features (X) and target (y)
# X = df.drop('bot_decision', axis=1)
# y = df['bot_decision']

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score

# # split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # train a Random Forest Classifier on the training data
# rfc = RandomForestClassifier()
# rfc.fit(X_train, y_train)

# # make predictions on the testing data
# y_pred = rfc.predict(X_test)

# # evaluate the accuracy of the model
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)
