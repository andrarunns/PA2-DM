import random
import sys

# Set up metod used to read file to set up and return the following 
# Board, Algorithm, and define the next player
def set_up(file_name):
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

#get_legal_moves used to find legal moves by checking the top row
#if we have an empty space, that means we can place a piece there
def get_legal_moves(board):
    moves = []
    for col in range(7):
        if board[0][col] == 'O':
            moves.append(col + 1)
    return moves

#uniform_random used to find the legal moves and return a uniform random strategy
#all legal moves should be selected with the same probability
def uniform_random(board):
    #find legal moves
    moves = get_legal_moves(board)
    #choose one at random
    #return it
    return random.choice(moves)
    
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
    #iterations = sys.argv[3]
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
    
    if algorithm == "UR":
         print(f"FINAL Move selected: {uniform_random(board)}")


# Using the special variable 
# __name__
if __name__=="__main__":
    main()
