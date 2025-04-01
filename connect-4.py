# The work below was implemented by
# Andrea Villagomez
# Emilio Rojero
# Arturo Flores

import sys
from uniform_random import UniformRandom
from game_manager import GameManager
from pmcgs import PMCGS
from simulator import Simulator


def set_up(file_name):
    """Sets up the board and reads the initial configuration."""
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
    """Main execution function."""
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
        use_uct = (algorithm == "UCT")
        pmcgs = PMCGS(verbose=(description == "Verbose"))

        print(f"\nRunning {algorithm} with:")
        print(f"- Iterations: {iterations}")
        print(f"- Verbose: {pmcgs.verbose}")
        print()

        # Select the next move using UCT or PMCGS
        move = pmcgs.next_move(board, next_player, rollouts=iterations, use_uct=use_uct)
        print(f"\nFINAL Move selected by {algorithm}: {move}")

        # Apply the move and print the updated board
        row = pmcgs.apply_move(board, move, next_player)

        print("\nUpdated Board After Move:")
        for row in board:
            print(" ".join(row))

def main2():
    game1 = Simulator()
    game1.game_simulation("UR", "UR", 0, 0)
# Using the special variable 
# __name__
if __name__ == "__main__":
    main2()
