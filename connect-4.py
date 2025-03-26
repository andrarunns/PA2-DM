import random
import sys

class Game:
    def __init__(self, board, player):
        self.board = board
        self.current_player = player
    
    #get_legal_moves used to find legal moves by checking the top row
    #if we have an empty space, that means we can place a piece there
    def get_legal_moves(self, board):
        moves = []
        for col in range(7):
            if board[0][col] == 'O':
                moves.append(col + 1)
        return moves

    
    def apply_move(seft,board, colum, player):
        #creo necesitamos una copy del tablero
        row = 5  
        while row >= 0:
            if board[row][colum] == 'O':  
                board[row][colum] = player  
                break  
            row -= 1 
        
        return board

    # #uniform_random used to find the legal moves and return a uniform random strategy
    # #all legal moves should be selected with the same probability
    # def uniform_random(seft, board):
    #     #find legal moves
    #     moves = seft.get_legal_moves(board)
    #     #choose one at random
    #     #return it
    #     return random.choice(moves)

    def check_winner(self, board):

        # check for horizontal wins 
        for row in range(6):
            for col in range(4): # boundry 
                curr_line = []
                curr_player = board[row][col]
                #check that a player occupies current spot
                if curr_player != "O":
                    for i in range(4):
                        curr_line.append(board[row][col+i])
                    
                    #check if next 4 consecutive spaces are the same
                    if curr_line == [curr_player] * 4:
                        return -1 if curr_player == "R" else 1

    # check for vertical wins 
        for row in range(3):# boundry 
            for col in range(7): 
                curr_line = []
                curr_player = board[row][col]
                #check that a player occupies current spot
                if curr_player != "O":
                    for i in range(4):
                        curr_line.append(board[row+1][col])
                    
                    #check if next 4 consecutive spaces are the same
                    if curr_line == [curr_player] * 4:
                        return -1 if curr_player == "R" else 1

    # check for diagonal bottom left to top right
        for row in range(3, 6):
            for col in range(4):
                if board[row][col] != "O":
                    curr_line = []
                    for i in range(4):
                        curr_line.append(board[row-i][col+i])
                    
                    if curr_line == ["R"] * 4:
                        return -1
                    elif curr_line == ["Y"] * 4:
                        return 1


    # check for diagonal top left to bottom right
        for row in range(3):
            for col in range(4):
                if board[row][col] != "O":
                    curr_line = []
                    for i in range(4):
                        curr_line.append(board[row+i][col-i])
                    
                    if curr_line == ["R"] * 4:
                        return -1
                    elif curr_line == ["Y"] * 4:
                        return 1
        
        #check if there are empty spaces (game can still play)
        for row in range(6):
            for col in range(7):
                if board[row][col] == "O":
                    return None
        
        # if all spaces are filled = draw
        return 0

class Node:
    def __init__ (self, parent, move):
        self.parent = parent
        self.move = move
        self.children = {}
        self.wi = 0 
        self.ni = 0 

def pmcgs(board, next_player, rollouts, verbose=False):
    game = Game(board, next_player)
    root = Node()

    for i in range(rollouts):
        pass


    pass


# Set up metod used to read file to set up and return the following 
# Board, Algorithm, and define the next player
def set_up(self, file_name):
    board = []
    for i in range(6):
        row = []
        for x in range(7):
            row.append('O')
        board.append(row)

    with open(file_name, "r") as file:
        algorithm = file.readline().strip()
        next_player = file.readline().strip()

        for row in range(6):
            board[row] = list(file.readline().strip())
    
    return algorithm, board, next_player

# Defining main function
def main():
    n = len(sys.argv)
    if n != 4:
        print("Incorrect number of arguments passed")
        print("Expected 4 arguments but got ", n)
        print("1. Text file name")
        print("2. Algorithm output (Verbose, Brief, None)")
        print("3. # of simulations to run")
        print()
        sys.exit()
   
    file_to_read = sys.argv[1]
    description = sys.argv[2]
    iterations = int(sys.argv[3])

    valid_description = ['Verbose', 'Brief', 'None']

    if description not in valid_description:
        print("Incorrect description should be Verbose, Brief of None")
        print()
        sys.exit()
    
    algorithm, board, next_player = set_up(file_to_read)
    if algorithm == "UR" and iterations !=0:
        print("With UR algorithm must have 0 as the last parameter")
        print()
        sys.exit()
    
    # if algorithm == "UR":
    #      print(f"FINAL Move selected: {uniform_random(board)}")


# Using the special variable 
# __name__
if __name__=="__main__":
    main()
