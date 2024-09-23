# mystery_driver

This is a game where the player has 6 guesses to name one of the 55 drivers that have driven at least a single race since 2014 (last updated 4/25/2024).

Each guess will either deliver the message "You Win" or information regarding the team, flag driven under, year of first f1 race, birth year, car number, and number of race wins.

After 6 guesses, the player will lose if they have not gotten the correct guess.

This is currently version 2.0 as of 2024-04-25

There are currently 2 ways to play:

## In terminal 
Before playing, you will need to run
pip install -r requirements.txt

The game begins with the command:
python3 mystery_driver.py

This will be purely text-based terminal.
If the player does not type a name exactly as it appears in the database, a fuzzy match will suggest names for the player to try again with.

## In web browser using Flask

Before playing, you will need to run
pip install -r requirements.txt

The game begins with the command:
flask run

(You may need to copy the web address into your browser to play. It will look like this:  
 * Running on http://127.0.0.1:5000
)

This version is more user friendly, has more colors, and is easier to see all guesses in one place.

This also uses the fuzzy match to give live recommendations to ease the issues with spelling a driver's name.

# Reinforcement Learned Approach

Mystery_Driver_Robot_Player.ipynb contains the reinforcement learning program.

The reinforcement program finds the answer with the following assumptions:

No driver who is impossible (from previous information) to be the answer is picked.

"Best" is defined by lowest average number of guesses while always winning (we find we can win starting with any driver as a first guess)