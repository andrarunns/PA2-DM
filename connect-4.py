import sys
from uniform_random import UniformRandom
from game_manager import GameManager
from pmcgs import PMCGS

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
        print(f"FINAL Move selected: {ur.next_move(board)}")
        pass

    elif algorithm == "PMCGS":
        gm = GameManager(board)  
        pmcgs = PMCGS()  
        move = pmcgs.next_move(gm.board, next_player, rollouts=int(iterations)) 
        print(f"FINAL Move selected by PMCGS: {move}")

        gm.apply_move(move, next_player)
        print("Updated Board After Move:")
        for row in gm.board:
            print(" ".join(row))

# Using the special variable 
# __name__
if __name__=="__main__":
    main()
