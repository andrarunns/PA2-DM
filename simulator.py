import random
from game_manager import GameManager
from pmcgs import PMCGS
from uniform_random import UniformRandom
import pandas as pd

class Simulator:

    def __init__(self, verbose=False):
        self.verbose = verbose
    
    # Returns the appropriate class for the given algorithm
    # used to initalize the competitors
    def get_player(self, algorithm):
        
        if algorithm == "UR":
            return UniformRandom()
        elif algorithm == "PMCGS":
            return PMCGS(verbose=False)
        elif algorithm == "UCT":
            return PMCGS(verbose=False)

    # Takes in both players algorithms and their rollouts
    # Simulates a game between both algorithms, taking turns placing a letter on the board
    # Continues until the board is filled or a winner is found
    def game_simulation(self, alg1, rollouts1, alg2, rollouts2):
        
        board = []
        for row in range(6):
            board.append(["O"] * 7)
        
        game_manager = GameManager(board)

        #set player objects
        red_player = self.get_player(alg1)
        yellow_player = self.get_player(alg2)
        
        curr_player = "R"
        move_count = 0

        while True:
            move_count += 1

            #apply the next move depending on the algorithm and player
            if curr_player == "R":
                if alg1 == "UR":
                    move = red_player.next_move(game_manager.board)
                    row = game_manager.apply_move(move, curr_player)
                else:
                    move = red_player.next_move(game_manager, curr_player, rollouts=rollouts1)
                    row = game_manager.apply_move(move, curr_player)
            else:
                if alg2 == "UR":
                    move = yellow_player.next_move(game_manager.board)
                    row = game_manager.apply_move(move, curr_player)
                else:
                    move = yellow_player.next_move(game_manager, curr_player, rollouts=rollouts2)
                    row = game_manager.apply_move(move, curr_player)

            
            # print("Current Board ---------------------")
            # for r in board:
            #     print(r)
            # print("-----------------------------------")

            # Check for a winner
            winner = game_manager.check_winner()

            if winner == "R":
                print("Red won")
                return 1
            elif winner == "Y":
                print("Yellow won")
                return -1
            elif winner == 0: 
                print("Draw")
                return 0

            #a turn has completed so we switch players
            curr_player = "Y" if curr_player == "R" else "R"

    #method to create a tournament and evalua each of the algorthm with different values
    #we pass a list with the algorthm we want to tets, and we create a list
    def tournament(self, algorithms):
        games = 5
        names = []
        for alg in algorithms:
            names.append(f"{alg[0]} ({alg[1]})")
        
        #we create a hashmap with each of the algorithm as a key
        #then we assign all the values to 0 of all the future evaluations
        results = {}
        for name in names:
            results[name] = {}
            for x in names:
                results[name][x] = 0

        #we will traverse the algorithms that we will test
        for i, algorimo1 in enumerate(algorithms):
            for j, algorimo2 in enumerate(algorithms):
                #we should compare the same algorithm so we skip and add a "-"
                if i == j: 
                    results[names[i]][names[j]] = "-"
                    continue

                wins1, wins2 = 0, 0
                for _ in range(games):
                    #from game_simulation we return either 1 for red or -1 for yellow
                    #we start playing as a algorhtm 1
                    winner = self.game_simulation(algorimo1[0], algorimo1[1], algorimo2[0], algorimo2[1])
                    #1 will be represt the first algorithm won 
                    if winner == 1: 
                        wins1 += 1
                    #1 will be represt the seconf algorithm won 
                    elif winner == -1:  
                        wins2 += 1

                #we have to diving by the numbers of games played
                win_rate1 = wins1 / games
                win_rate2 = wins2 / games

                #after we detetermined the win we will just addd the value to to each different algotihm
                results[names[i]][names[j]] = win_rate1
                results[names[j]][names[i]] = win_rate2

        #we will use padas to create the table to display the information
        df = pd.DataFrame(results)
        return df