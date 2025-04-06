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

    #add a child if it does not exist
    #display in the terminal of a new node 
    def add_child(self, move):
        if move not in self.children:
            self.children[move] = Node(self, move)
            print("NODE ADDED")
        return self.children[move]
    
class UCTPlus_v2:
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

    # estimate ucb value for each node and make the move of the node with the highest value
    def uct_select(self, node, exploration_factor=math.sqrt(2)):
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


    # place the first pieces in the middle positions of the board in this case to the column 3 and 4, 
    # this is a good strategy because when we place in the middle of the board, 
    # we increases our chances to win because we have more to explore.
    def apply_center_moves(self, game_manager, player, legal_moves, max_moves=4):
        applied_moves = 0
        center_columns = [3, 4]  

        for col in center_columns:
            if col in legal_moves:
                row = game_manager.apply_move(col, player)
                applied_moves += 1
                if self.verbose:
                    print("MOVE APPLIED TO THE CENTER")
            if applied_moves >= max_moves:
                break 
        return legal_moves
        

    def next_move(self, game_manager, player, rollouts=500):
        
        # Initialize the root node
        if self.root is None:
            self.root = Node()

        legal_moves = game_manager.get_legal_moves()

        legal_moves = self.apply_center_moves(game_manager, player, legal_moves, max_moves=4)

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

    

