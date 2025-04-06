import random
import math
from game_manager import GameManager

class Node:
    def __init__(self, parent=None, move=None):
        self.parent = parent
        self.move = move
        self.children = {}
        self.wi = 0      # Wins
        self.ni = 0      # Number of visits
        self.qi = 0      # Value estimate (wi / ni)
        self.ucb = 0     # UCB value

    #adda child if it does not exist
    #display in the terminal of a new node 
    def add_child(self, move):
        if move not in self.children:
            self.children[move] = Node(self, move)
            print("NODE ADDED")
        return self.children[move]
    
class UCTPlus:
    def __init__(self, verbose=False):
        self.root = None
        self.verbose = verbose
    
    #this method will simulate the random plauout using apply move and undo moves
    def random_playout(self, board, player):
        current_player = player
        curr_manager = GameManager([row[:] for row in board])
        move_history = []

        while True:
            moves = curr_manager.get_legal_moves()
            if not moves:
                # print("TERMINAL NODE VALUE: 0")
                return 0  # Draw

            move = random.choice(moves)
            
            # Apply and store the move
            row = curr_manager.apply_move(move, current_player)
            move_history.append((row, move))

            winner = curr_manager.check_winner()

            if winner is not None:
                # Undo all moves before returning the result
                for r, c in reversed(move_history):
                    curr_manager.undo_move(r, c)

                value = 1 if winner == player else -1
                # print(f"TERMINAL NODE VALUE: {value}")
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


    def find_blocking_move(self, game_manager, player):
        """Check if the opponent has a winning move next turn and return the move to block it."""
        opponent = 'Y' if player == 'R' else 'R'
        legal_moves = game_manager.get_legal_moves()

        for move in legal_moves:
            row = game_manager.apply_move(move, opponent)
            if row != -1:
                if game_manager.check_winner() == opponent:
                    game_manager.undo_move(row, move)
                    if self.verbose:
                        print(f"Blocking opponent's winning move at column {move + 1}")
                    return move
                game_manager.undo_move(row, move)

        return None

    def next_move(self, game_manager, player, rollouts=500):
        """Single next_move method for both PMCGS and UCT."""

        # First check if we need to block opponent's winning move
        blocking_move = self.find_blocking_move(game_manager, player)
        if blocking_move is not None:
            print("BLOCKING MOVE SELECTED")
            return blocking_move

        
        # Initialize the root node
        if self.root is None:
            self.root = Node()

        legal_moves = game_manager.get_legal_moves()

        # Expand the tree with child nodes if not already present
        for move in legal_moves:
            if move not in self.root.children:
                self.root.add_child(move)

        # MCTS Rollouts
        for _ in range(rollouts):
            current_node = self.root
            current_player = player
            path = []  # Keep track of the path taken in the tree

            # Tree search and expansion
            while current_node.children:  # Traverse until a leaf or non-expanded node
                current_node = self.uct_select(current_node)
                move = current_node.move
                row = game_manager.apply_move(move, current_player)
                path.append((current_node, row, move))  # Track the move

                current_player = 'Y' if current_player == 'R' else 'R'

            # Random playout phase
            result = self.random_playout(game_manager.board, 'Y' if current_player == 'R' else 'R')

            # Undo the moves along the path
            for node, row, move in reversed(path):
                game_manager.undo_move(row, move)

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

    

