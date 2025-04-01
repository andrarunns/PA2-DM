import random
import math
from game_manager import GameManager

class Node:
    """MCTS Node to track wins, visits, and child nodes."""
    def __init__(self, parent=None, move=None):
        self.parent = parent
        self.move = move
        self.children = {}
        self.wi = 0      # Wins
        self.ni = 0      # Number of visits
        self.qi = 0      # Value estimate (wi / ni)
        self.ucb = 0     # UCB value

    def add_child(self, move):
        """Adds a child node if it doesn't exist."""
        if move not in self.children:
            self.children[move] = Node(self, move)
            print("NODE ADDED")
        return self.children[move]


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
        return [col for col in range(7) if board[0][col] == "O"]

    def random_playout(self, board, player):
        """Simulates a random playout using apply/undo moves."""
        current_player = player
        curr_manager = GameManager(board)
        move_history = []

        while True:
            moves = self.get_legal_moves(board)
            if not moves:
                print("TERMINAL NODE VALUE: 0")
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

                value = 1 if winner == player else -1
                print(f"TERMINAL NODE VALUE: {value}")
                return value

            current_player = 'Y' if current_player == 'R' else 'R'

    def uct_select(self, node, exploration_factor=math.sqrt(2)):
        """Selects a child node using UCT."""
        total_visits = sum(child.ni for child in node.children.values()) + 1

        best_ucb = float('-inf')
        best_move = None

        for move, child in node.children.items():
            if child.ni == 0:
                ucb_value = float('inf')
            else:
                ucb_value = (child.wi / child.ni) + exploration_factor * math.sqrt(math.log(total_visits) / child.ni)

            child.ucb = ucb_value

            if self.verbose:
                print(f"UCB value for move {move + 1}: {ucb_value:.4f}")

            if ucb_value > best_ucb:
                best_ucb = ucb_value
                best_move = move

        return node.children[best_move]

    def next_move(self, board, player, rollouts=500, use_uct=False):
        """Single next_move method for both PMCGS and UCT."""

        # Initialize the root node
        if self.root is None:
            self.root = Node()

        legal_moves = self.get_legal_moves(board)

        # Expand the tree with child nodes if not already present
        for move in legal_moves:
            if move not in self.root.children:
                self.root.add_child(move)

        # MCTS Rollouts
        for _ in range(rollouts):
            current_node = self.root
            current_player = player

            # Tree search and expansion
            while current_node and current_node.children:
                if use_uct:
                    current_node = self.uct_select(current_node)
                else:
                    current_node = random.choice(list(current_node.children.values()))

                # Ensure the node is valid
                if current_node is None:
                    break

                move = current_node.move
                row = self.apply_move(board, move, current_player)
                current_player = 'Y' if current_player == 'R' else 'R'

                # Random playout phase
                result = self.random_playout(board, current_player)

                # Undo the move
                self.undo_move(board, row, move)

                # Backpropagation
                while current_node is not None:
                    current_node.wi += result
                    current_node.ni += 1
                    current_node.qi = current_node.wi / current_node.ni
                    if self.verbose:
                        print(f"Updated values: wi: {current_node.wi}, ni: {current_node.ni}")
                    current_node = current_node.parent

        # Choose the best move based on average value (qi)
        best_move = None
        best_value = float('-inf')

        for move, node in self.root.children.items():
            if node.ni > 0:
                score = node.qi
            else:
                score = float('-inf')

            if score > best_value:
                best_value = score
                best_move = move

        # Print detailed statistics if verbose
        for move, node in self.root.children.items():
            avg_value = node.qi if node.ni > 0 else "Null"
            if self.verbose:
                print(f"Column {move + 1}: {avg_value:.4f}")

        if self.verbose:
            print(f"FINAL Move selected: {best_move + 1}")

        return best_move
