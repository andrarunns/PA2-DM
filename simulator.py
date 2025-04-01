import random
from game_manager import GameManager
from pmcgs import PMCGS
from uniform_random import UniformRandom

class Simulator:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def game_simulation(self, alg1, alg2, rollouts1, rollouts2):
        # Initialize empty board
        board = []
        for i in range(6):
            board.append(["O"] * 7)
        
        game_manager = GameManager(board)

        # Set up algorithms
        if alg1 == "UR":
            red_player = UniformRandom()
        else:
            red_player = PMCGS(verbose=False)

        if alg2 == "UR":
            yellow_player = UniformRandom()
        else:
            yellow_player = PMCGS(verbose=False)
        
        curr_player = "R"
        move_count = 0
        game_over = False

        while not game_over:
            move_count += 1

            if curr_player == "R":
                move = red_player.next_move(board)
                if alg1 == "UR":
                    row = self.apply_uniform_move(board, move, curr_player)
                else:
                    row = red_player.apply_move(board, move, curr_player)
            elif curr_player == "Y":
                move = yellow_player.next_move(board)
                if alg2 == "UR":
                    row = self.apply_uniform_move(board, move, curr_player)
                else:
                    row = yellow_player.apply_move(board, move, curr_player)

            print("Current Board ---------------------")
            for row in board:
                print(row)
            print("-----------------------------------")
            
            winner = game_manager.check_winner(board)

            if winner == "R":
                print("Red won")
                return 1
            elif winner == "Y":
                print("Yellow won")
                return -1
            elif move_count == 42:  # Board is full (draw)
                print("Draw")
                return 0

            # Swap players
            curr_player = "Y" if curr_player == "R" else "R"

    def apply_uniform_move(self, board, move, curr):
        """Directly apply a move for UniformRandom player."""
        for row in range(5, -1, -1):  # Start from the bottom row
            if board[row][move - 1] == 'O':  # Check if the column is available
                board[row][move - 1] = curr  # Place the move for the current player
                return row
        return -1  # 

