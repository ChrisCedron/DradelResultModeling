import random
import numpy as np
import math
import matplotlib.pyplot as plt

# Dradel Roles:
#   0: Nothing
#   1: Add 1 To Pot
#   2: Take floor(1/2 of pot)
#   3: Take whole Pot

# Experiments:
#   0: Nothing, Base Game
#   ...

#Experiment Constants
STARTING_COINS = 15     # How Many coins do the players start with
NUM_PLAYERS = 5         # How many players are in the simulation (Need to modify the plot code to show them all)
EXPERIMENT = 1          # What version of the code to run, see note above
NUM_ROUNDS = 1000       # Total Number of rounds to run before terminating
RESOLUTION = 10         # Total Number of Rounds between the data points that are shown on the final graph


#Variables
PlayerScores = np.ones(NUM_PLAYERS) * STARTING_COINS        # Current coin counts for all the players
Pot = 0             #Current pot to pull from
ScoreTracker = np.zeros([math.floor(NUM_ROUNDS/RESOLUTION),NUM_PLAYERS + 1], dtype = int)  # Matrix to track scores for plotting

# Coin Manager Functions
def nothing(players, pot, playerNum):
    return (players, pot)

def addOne(players, pot, playerNum):
    # get the current player
    player = players[playerNum]
    
    #get the current pot state
    newPot = pot

    # check if the current player has enough coins
    if player > 0:
        # modify the curr player coin count
        player = player - 1
        
        # modify the current pot
        newPot = newPot + 1

    # update the local board state
    players[playerNum] = player

    # return the new board state
    return (players,newPot)

def takeHalf(players, pot, playerNum):
    # get the current player
    player = players[playerNum]

    # calc half the pot
    halfPot = math.floor(pot/2)
    
    # modify the curr player coin count
    player = player + halfPot

    # modify the curr pot value
    newPot = pot - halfPot

    # update the local board state
    players[playerNum] = player

    # Return the new board state
    return (players, newPot)

def takeAll(players, pot, playerNum):
    # get curr player
    player = players[playerNum]

    # modify curr player coin count
    player = player + pot

    # modify the current pot value
    newPot = 0

    # update the local board state
    players[playerNum] = player
    
    # Everyone adds coins back into the pot after a take
    (players, newPot) = startRound(players, newPot)

    # return the new board state
    return (players, newPot)

def startRound(players, pot):
    # keep track of the coins to add to the pot
    addToPot = 0
    # for all the players
    for player in range(0, len(players)):
        # get the current player
        currPlayer = players[player]
        # If the player can add a coin
        if currPlayer > 0:
            # take a coin from the player
            currPlayer -= 1
            # add to the pot
            addToPot += 1
        #update the local board state
        players[player] = currPlayer
    
    newPot = pot + addToPot
    # return how many coins need to be added to the pot
    return (players, newPot)


#Runs the game with standard rules, one person starts and ends
def playStandard(PlayerScores, Pot, ScoreTracker):
    #copy over the global variables but dont mess with them in case we need them clean outside for.... reasons?
    playerScores = PlayerScores
    pot = Pot
    scoreTracker = ScoreTracker

    for roundNum in range(0,NUM_ROUNDS):
        # Start the round by adding coins to the pot
        (playerScores, pot) = startRound(playerScores, pot)
        # players take turns in order
        for player in range(len(playerScores)):
            # take a roll
            roll = random.randint(0,3)
            # play by the functions defined above
            rollEffect = rolls.get(roll, "Nothing")
            # update the global board state with the result from the function call
            (playerScores, pot) = rollEffect(playerScores, pot, player)
                                
        # Every so often store the state of the board based on the resultion requested
        if roundNum % RESOLUTION == 0:
            # calculate index to insert data into (for some reason python 3 doesnt let me do this inline)
            index = math.floor(roundNum/RESOLUTION)
            # set the values into the tracking matrix
            scoreTracker[index, 0] = roundNum
            scoreTracker[index, 1:] = playerScores

    return scoreTracker


#Runs the game with a modified rule where the round ends on the same person that started it, causing the first player to change
def playBlinds(PyerScores, Pot, ScoreTracker):
    #copy over the global variables but dont mess with them in case we need them clean outside for.... reasons?
    playerScores = PlayerScores
    pot = Pot
    scoreTracker = ScoreTracker
    currBlind = 0

    for roundNum in range(0,NUM_ROUNDS):
        #Everyone Adds Coins
        (playerScores, pot) = startRound(playerScores, pot)
        
        #Chose New Blinds
        currBlind += 1
        if currBlind >= len(playerScores):
            currBlind -= len(playerScores)
        
        #play everyones turns in order starting at the blind 
        for playerOffset in range(len(playerScores)):
            #find the current player
            currPlayer =(playerOffset + currBlind)-len(playerScores) 
            
            # take a roll
            roll = random.randint(0,3)
            
            # play by the functions defined above
            rollEffect = rolls.get(roll, "Nothing")
            
            # update the global board state with the result from the function call
            (playerScores, pot) = rollEffect(playerScores, pot, currPlayer)
                                
        #end the round on the blind
        # take a roll
        roll = random.randint(0,3)
            
        # play by the functions defined above
        rollEffect = rolls.get(roll, "Nothing")
            
        # update the global board state with the result from the function call
        (playerScores, pot) = rollEffect(playerScores, pot, currBlind)
       

        # Every so often store the state of the board based on the resultion requested
        if roundNum % RESOLUTION == 0:
            # calculate index to insert data into (for some reason python 3 doesnt let me do this inline)
            index = math.floor(roundNum/RESOLUTION)
            # set the values into the tracking matrix
            scoreTracker[index, 0] = roundNum
            scoreTracker[index, 1:] = playerScores
    
    
    return scoreTracker


# switch case for all the rolls that the player can get depending on the PRNG
rolls = {
        0: nothing,
        1: addOne,
        2: takeHalf,
        3: takeAll
        }

experimentalGameChoser = {
        0:playStandard,
        1:playBlinds
        }

# Main Function
# Play every round depending on what experiment value is set
ScoreTracker = experimentalGameChoser.get(EXPERIMENT)(PlayerScores, Pot, ScoreTracker)

# plot the data collected
plotRange = np.arange((NUM_ROUNDS/RESOLUTION))*RESOLUTION

# define the plot UPDATE THIS IF YOU CHANGE NUM PLAYERS
plt.plot(plotRange, ScoreTracker[:,1], 
        plotRange, ScoreTracker[:,2], 
        plotRange, ScoreTracker[:,3],
        plotRange, ScoreTracker[:,4],
        plotRange, ScoreTracker[:,5])
plt.show()
