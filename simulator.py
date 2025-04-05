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


    def tournament(self, algorithms):
        names = ["PMCGS (500)", "UCT (500)"]
        results = {}
        for name in names:
            results[name] = []

        for algorimo1 in algorithms:
            for algorimo2 in algorithms:
                if algorimo1 == algorimo2: 
                    continue
                wins = 0
                for _ in range(5):
                    winner = self.game_simulation(algorimo1[0], algorimo1[1], algorimo2[0], algorimo2[1])
                    if winner == 1:
                        wins += 1
                win_rate = wins 
                results[f"{algorimo1[0]} ({algorimo1[1]})"].append(win_rate)

        df = pd.DataFrame(results, index=names)
        return df
