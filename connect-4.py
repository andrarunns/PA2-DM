# The work below was implemented by
# Andrea Villagomez
# Emilio Rojero
# Arturo Flores

import sys
from uniform_random import UniformRandom
from game_manager import GameManager
from pmcgs import PMCGS
# from uct import UCT

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
    iterations = int(sys.argv[3])

    valid_description = ['Verbose', 'Brief', 'None']

    if description not in valid_description:
        print("Incorrect description should be Verbose, Brief, or None")
        print()
        sys.exit()
    
    algorithm, board, next_player = set_up(file_to_read)

    if algorithm == "UR" and iterations != 0:
        print("With UR algorithm, the last parameter must be 0")
        print()
        sys.exit()

    if algorithm == "UR":
        ur = UniformRandom()
        print(f"FINAL Move selected: {ur.next_move(board)}")

    elif algorithm == "PMCGS":
        pmcgs = PMCGS(verbose=(description == "Verbose"))

        print("\nRunning PMCGS with:")
        print(f"- Iterations: {iterations}")
        print(f"- Verbose: {pmcgs.verbose}")
        print()

        # Select the next move
        move = pmcgs.next_move(board, next_player, rollouts=iterations)
        print(f"\nFINAL Move selected by PMCGS: {move}")

        # Apply the move and print the updated board
        row = pmcgs.apply_move(board, move, next_player)

        print("\nUpdated Board After Move:")
        for row in board:
            print(" ".join(row))

# Using the special variable 
# __name__
if __name__ == "__main__":
    main()
