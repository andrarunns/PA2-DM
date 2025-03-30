import random

class UniformRandom:
    def __init__(self):
        pass

    #get_legal_moves used to find legal moves by checking the top row
    #if we have an empty space, that means we can place a piece there
    def get_legal_moves(self, board):
        moves = []
        for col in range(7):
            if board[0][col] == 'O':
                moves.append(col + 1)
        return moves

    #uniform_random used to find the legal moves and return a uniform random strategy
    #all legal moves should be selected with the same probability
    def next_move(self, board):
        #find legal moves
        moves = self.get_legal_moves(board)
        #choose one at random
        #return it
        return random.choice(moves)
