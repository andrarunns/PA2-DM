import random
from game_manager import GameManager

class Node:
    """MCTS Node to track wins, visits, and child nodes."""
    def __init__(self, parent, move):
        self.parent = parent
        self.move = move
        self.children = {}
        self.wi = 0      # Wins
        self.ni = 0      # Number of visits
        self.qi = 0      # Value estimate (wi / ni)
        self.uct = 0     # Upper confidence bound

class PMCGS:
    def __init__(self, verbose=False):
        self.root = None
        self.verbose = verbose

    def apply_move(self, board, col, player):
        """Applies a move in place and returns the row where it was made."""
        for row in range(5, -1, -1):
            if board[row][col] == 'O':
                board[row][col] = player
                return row
        return -1

    def undo_move(self, board, row, col):
        """Undoes the move by resetting the cell to 'O'."""
        board[row][col] = 'O'

    def get_legal_moves(self, board):
        """Returns a list of legal moves (columns)."""
        return [col for col in range(7) if board[0][col] == 'O']

    def random_playout(self, board, player):
        """Simulates a random playout using apply/undo moves."""
        current_player = player
        curr_manager = GameManager(board)
        move_history = []

        while True:
            moves = self.get_legal_moves(board)
            if not moves:
                return 0  # Draw

            move = random.choice(moves)
            
            # Apply and store the move
            row = self.apply_move(board, move, current_player)
            move_history.append((row, move))

            winner = curr_manager.check_winner(board)

            if winner is not None:
                # Undo all moves before returning the result
                for r, c in reversed(move_history):
                    self.undo_move(board, r, c)

                if winner == player:
                    return 1
                elif winner != 'O':
                    return -1
                else:
                    return 0

            current_player = 'Y' if current_player == 'R' else 'R'

    def next_move(self, board, player, rollouts=500):
        """Selects the next move using MCTS with in-place move handling."""
        
        legal_moves = self.get_legal_moves(board)
        move_scores = {move: Node(None, move) for move in legal_moves}

        # MCTS Rollouts
        for move in legal_moves:
            for _ in range(rollouts):
                # Apply the move
                row = self.apply_move(board, move, player)

                # Simulate the random playout
                result = self.random_playout(board, 'Y' if player == 'R' else 'R')

                # Undo the applied move
                self.undo_move(board, row, move)

                # Update MCTS statistics
                move_scores[move].wi += result
                move_scores[move].ni += 1
                move_scores[move].qi = move_scores[move].wi / move_scores[move].ni  # Average value
                if self.verbose:
                    print(f"Updated values for move {move}:")
                    print(f"wi: {move_scores[move].wi}")
                    print(f"ni: {move_scores[move].ni}")
                    print(f"qi (average value): {move_scores[move].qi:.4f}")

        # Choose the best move based on average value
        best_move = None
        best_value = float('-inf')

        for move, node in move_scores.items():
            if node.ni > 0:
                score = node.qi
            else:
                score = float('-inf')

            if score > best_value:
                best_value = score
                best_move = move

        # Print detailed statistics if verbose
        for move, node in move_scores.items():
            avg_value = node.qi if node.ni > 0 else "Null"
            if self.verbose:
                print(f"Column {move + 1}: {avg_value}")

        if self.verbose:
            print(f"FINAL Move selected: {best_move}")

        return best_move
