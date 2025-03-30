import sys
from uniform_random import UniformRandom

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

def check_winner(board):

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

def main():
    n = len(sys.argv)
    if n != 4:
        print("Incorrect number of arguments passed")
        print("1. Text file name")
        print("2. Algorithm output (Verbose, Brief, None)")
        print("3. # of simulations to run")
        print()
        sys.exit()
   
    file_to_read = sys.argv[1]
    description = sys.argv[2]
    iterations = sys.argv[3]

    valid_description = ['Verbose', 'Brief', 'None']

    if description not in valid_description:
        print("Incorrect description should be Verbose, Brief of None")
        print()
        sys.exit()
    
    algorithm, board, next_player = set_up(file_to_read)

    if algorithm == "UR" and int(iterations) != 0:
        print("With UR algorithm must have 0 as the last parameter")
        print()
        sys.exit()

    if algorithm == "UR":
        ur = UniformRandom()
        print(f"FINAL Move selected: {ur.make_move(board)}")
        pass

# Using the special variable 
# __name__
if __name__=="__main__":
    main()
