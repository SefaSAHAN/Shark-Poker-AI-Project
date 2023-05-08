# Shark-Poker-AI-Project

Shark Poker Bot is a machine learning project aimed at developing a bot that can play 1 vs 1 poker games. The bot uses various machine learning techniques to make decisions while playing. In this project, I focused on developing a bot that can play Texas Hold'em No Limit, one of the most popular types of poker games.

## Texas Hold'em No-Limit Poker Rules

In Texas Hold'em no-limit poker, each player is dealt two private cards (hole cards) and five community cards are dealt face up in the middle of the table. Players can use any combination of their hole cards and the community cards to make the best five-card hand possible. The game has four rounds of betting: pre-flop, flop, turn, and river. The goal is to have the highest-ranking hand at the end of the game.

## Project Details

To reduce the number of possible combinations of cards, the project uses a formula that reduces the combinations. This results in a dataset of 300,000 hands that shows the bot's win rate for each combination in the pre-flop and flop positions. The dataset can be found in the data folder under the name win_rate.csv.

To make decisions during the game, Three separate datasets were also created to assist the bot in making decisions: one for when the opponent checks, one for when the opponent raises, and one for when the bot decides to raise. These datasets, named check.csv, raise.csv, and raise_amount.csv, respectively, are located in the data folder. Various machine learning models were utilized to create these datasets, which can be found in the predict.ipynb notebook in the data folder.

The reduce_card_combination folder contains the code for the combination reduction method used to create the win rate dataset, as well as the code to check that the method is working correctly.

The utils folder contains two modules: win_rate.py and winnercheck.py. The win_rate.py module uses the combination reduction method to find the appropriate row in the win rate dataset for a given combination of cards. The winnercheck.py module determines the winner of a game based on the final hands of the players.


## Usage

To run the Shark Poker Bot, you can use the main.py file.

This file uses the ui modules in the utils folder to display the game interface and prompt the user for input.

Before running the program, make sure to install the required libraries by running pip install -r requirements.txt.

"Note: Due to the three different machine learning models used in this program, it may take between 1 to 2 minutes for the program to open."


## Analysis

To analyze the project and results win_rate dataset, I created various notebook in the data folder. These notebooks show the results of the dataset.

## Conclusion

Shark Poker Bot is a machine learning project that aims to develop a bot that can play 1 vs 1 poker games. Using various machine learning techniques, I created a bot that can make decisions based on the opponent's actions and the cards in its hand. The project is still in its early stages and there is room for improvement. However, the bot shows promising results and can be a great tool for learning and practicing poker.


