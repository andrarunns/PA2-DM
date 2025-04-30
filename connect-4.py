# The work below was implemented by
# Andrea Villagomez
# Emilio Rojero
# Arturo Flores

import sys
from uniform_random import UniformRandom
from game_manager import GameManager
from pmcgs import PMCGS
from simulator import Simulator
from uct_plus import UCTPlus
from uct_plus_v2 import UCTPlus_v2

#This method reads a file and returns the  algorithm, board and next player
#used as initial configuration of the board
def set_up(file_name):
    board = []
    for i in range(6):
        row = ['O'] * 7
        board.append(row)

    with open(file_name, "r") as file:
        algorithm = file.readline().strip()
        next_player = file.readline().strip()

        for row in range(6):
            board[row] = list(file.readline().strip())
    
    return algorithm, board, next_player

def empty_board():
    board = []
    for i in range(6):
        row = ['O'] * 7
        board.append(row)
    return board

#Method is used to try a single move for a single algorithm
#to run this uncoment it from the script
#you will need to run this with three parameters
#a text file that has algorithm on the first line,next player on the next line, and board set up
#a description = verbose, brief or none / this will indicate how much details will be printed
# and a number to indicate how many itterations to run
# it will print the selected final move
def ineterim_sumbission():
    
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
    iterations = int(sys.argv[3])

    valid_description = ['Verbose', 'Brief', 'None']

    if description not in valid_description:
        print("Incorrect description should be Verbose, Brief, or None")
        print()
        sys.exit()
    
    algorithm, board, next_player = set_up(file_to_read)

    # Uniform Random (UR)
    if algorithm == "UR" and iterations != 0:
        print("With UR algorithm, the last parameter must be 0")
        print()
        sys.exit()

    if algorithm == "UR":
        ur = UniformRandom()
        print(f"FINAL Move selected: {ur.next_move(board)}")

    # PMCGS or UCT algorithms
    elif algorithm in ["PMCGS", "UCT"]:
        
        pmcgs = PMCGS(verbose=(description == "Verbose"))

        print(f"\nRunning {algorithm} with:")
        print(f"- Iterations: {iterations}")
        print(f"- Verbose: {pmcgs.verbose}")
        print()

        # Select the next move using UCT or PMCGS
        move = pmcgs.next_move(board, next_player, rollouts=iterations, use_uct=(algorithm == "UCT"))
        print(f"\nFINAL Move selected by {algorithm}: {move}")

        # Apply the move and print the updated board
        row = pmcgs.apply_move(board, move, next_player)

        print("\nUpdated Board After Move:")
        for row in board:
            print(" ".join(row))


#method is used to run the tournament simulation
def main():

    algorithms = [
        ("UR", 0),
        ("PMCGS", 1000),
        ("PMCGS", 500),
        ("UCT", 1000),
        ("UCT", 500)
    ]

    # # tournament simulation
    game = Simulator()
    game.tournament(algorithms)

    # game simulation between the original uct and the move block optimization
    game1 = Simulator()
    uct_game_win = 0
    uct_plus_game_win = 0
    for i in range(10):
        game = game1.game_simulation("UCT" ,10000, "UCTPlus", 10000)
        if game == 1:
            uct_game_win +=1
        elif game == -1:
            uct_plus_game_win +=1
    
    print("UCT Game win count", uct_game_win)
    print("UCT Plus Game win count", uct_plus_game_win)


    # game simulation between original uct and the second optimization
    game2 = Simulator()
    uct_game_win = 0
    uct_plus_game_win = 0
    for i in range(10):
        game = game2.game_simulation("UCT" ,10000, "uct_plus_v2", 10000)
        if game == 1:
            uct_game_win +=1
        elif game == -1:
            uct_plus_game_win +=1
    
    print("UCT Game win count", uct_game_win)
    print("UCT Plus V2 Game win count", uct_plus_game_win)

if __name__ == "__main__":
    main()
