import random
import sys
from game_manager import GameManager

class Node:
    def __init__(self, parent, move):
        self.parent = parent
        self.move = move
        self.children = {}
        self.wi = 0 
        self.ni = 0 

class PMCGS:
    def __init__(self, verbose=False):
        self.root = None
        self.verbose = verbose
    
    def copy_board(self, board):
        board_copy = []
        for row in board:
            board_copy.append(row.copy())
        return board_copy
    
    def apply_move(self, board, col, player):
        new_board = self.copy_board(board)
        for row in range(5, -1, -1):
            if new_board[row][col] == 'O':
                new_board[row][col] = player
                break
        return new_board
    
    def get_legal_moves(self, board):
        moves = []
        for col in range(7):
            if board[0][col] == 'O':
                moves.append(col)
        return moves
    
    def random_playout(self, board, player):
        board = self.copy_board(board)
        current_player = player
        
        while True:
            moves = self.get_legal_moves(board)
            if not moves:
                return 0 
            
            move = random.choice(moves)
            if self.verbose:
                print(f"Move selected: {move}")
            board = self.apply_move(board, move, current_player)
            winner = GameManager.check_winner(board)
            
            if winner is not None:
                if self.verbose:
                    if winner == player:
                        print("TERMINAL NODE VALUE: 1")
                    elif winner != 'O':
                        print("TERMINAL NODE VALUE: -1")
                    else:
                        print("TERMINAL NODE VALUE: 0")
                
                if winner == player:
                    return 1
                elif winner != 'O':
                    return -1
                else:
                    return 0

            
            current_player = 'Y' if current_player == 'R' else 'R'

    def next_move(self, board, player, rollouts=500):
        legal_moves = self.get_legal_moves(board)
        move_scores = {move: Node(None, move) for move in legal_moves}
        
        for move in legal_moves:
            for _ in range(rollouts):
                simulated_board = self.apply_move(board, move, player)
                result = self.random_playout(simulated_board, 'Y' if player == 'R' else 'R')
                
                move_scores[move].wi += result
                move_scores[move].ni += 1
                if self.verbose:
                    print(f"Updated values for move {move}:")
                    print(f"wi: {move_scores[move].wi}")
                    print(f"ni: {move_scores[move].ni}")
        
        best_move = None
        best_value = float('-inf')
        
        for move in move_scores:
            if move_scores[move].ni > 0:
                score = move_scores[move].wi / move_scores[move].ni
            else:
                score = float('-inf')
            
            if score > best_value:
                best_value = score
                best_move = move
        
        for move in move_scores:
            avg_value = move_scores[move].wi / move_scores[move].ni if move_scores[move].ni > 0 else "Null"
            if self.verbose:
                print(f"Column {move + 1}: {avg_value}")
        
        if self.verbose:
            print(f"FINAL Move selected: {best_move}")
        
        return best_move
