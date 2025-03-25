import sys

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
    iterations = sys.argv[3]

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


# Using the special variable 
# __name__
if __name__=="__main__":
    main()
