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

def apply_move(board, colum, player):
    #creo necesitamos una copy del tablero
    row = 5  
    while row >= 0:
        if board[row][colum] == 'O':  
            board[row][colum] = player  
            break  
        row -= 1 
    
    return board

def simulate_random_playout(board, player):
    current_player = player
    while True:
        moves = get_legal_moves(board)
        if not moves: 
            return 0
        move = random.choice(moves)  
        board = apply_move(board, move - 1, current_player)  
        
        if check_win(board, current_player):
            if current_player == player:
                return 1
            else:
                return -1  
        
        if current_player == 'R':
            current_player = 'Y'
        else:
            current_player = 'R'


def check_win(board, player):
    #horizontal
    for row in range(6):
        for col in range(4):
            win = True
            for i in range(4):
                if board[row][col + i] != player:
                    win = False
                    break
            if win:
                return True

    #vertical check
    for col in range(7):
        for row in range(3):
            win = True
            for i in range(4):
                if board[row + i][col] != player:
                    win = False
                    break
            if win:
                return True

    #giagonal
    for row in range(3):
        for col in range(4):
            win = True
            for i in range(4):
                if board[row + i][col + i] != player:
                    win = False
                    break
            if win:
                return True

    #diagonal (otra)
    for row in range(3, 6):
        for col in range(4):
            win = True
            for i in range(4):
                if board[row - i][col + i] != player:
                    win = False
                    break
            if win:
                return True

    return False

def pure_monte_carlo_game_search(board, rollouts, verbose, next_player):
    legal_moves = get_legal_moves(board)

    for i in range(rollouts):
        move = random.choice(legal_moves)

        #apply move
        update_move = apply_move(board, move - 1, next_player)

        #simulate the game
        game = simulate_random_playout(update_move, next_player)


        if verbose:
          
            print("wi: ")
            print("ni: ", )
            print("----")

    pass
    
# Defining main function
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
