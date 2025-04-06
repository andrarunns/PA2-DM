# This class holds its own board and functions to manipulate it

class GameManager:
    def __init__(self, board):
        self.board = board

    #replaces a spot on the board with the current player
    #finds the lowest available spot of a column and places player letter
    #returns the row where the move was made
    def apply_move(self, col, player):
        for row in range(5, -1, -1):
            if self.board[row][col] == 'O':
                self.board[row][col] = player
                return row
        return -1
    
    #undoes a move
    #restates the space as open "O"
    def undo_move(self, row, col):
        self.board[row][col] = 'O'
    
    #finds all the cols that are not all filled
    #returns a list with the cols that are available
    def get_legal_moves(self):
        legal = []
        for col in range(7):
            if self.board[0][col] == "O":
                legal.append(col)
        return legal

    def check_winner(self, board=None):
        # Use self.board if board is None
        if board is None:
            board = self.board

        # Check for horizontal wins 
        for row in range(6):
            for col in range(4):  # Boundaries
                curr_player = self.board[row][col]
                if curr_player != "O":  # Check that a player occupies current spot
                    # Check if next 4 consecutive spaces are the same
                    if self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3]:
                        return "R" if curr_player == "R" else "Y"

        # Check for vertical wins
        for row in range(3):  # Boundaries
            for col in range(7):
                curr_player = self.board[row][col]
                if curr_player != "O":  # Check that a player occupies current spot
                    # Check if next 4 consecutive spaces are the same
                    if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col]:
                        return "R" if curr_player == "R" else "Y"

        # Check for diagonal bottom left to top right
        for row in range(3, 6):
            for col in range(4):
                if self.board[row][col] != "O":
                    curr_player = self.board[row][col]
                    # Check diagonal from bottom-left to top-right
                    if self.board[row][col] == self.board[row-1][col+1] == self.board[row-2][col+2] == self.board[row-3][col+3]:
                        return "R" if curr_player == "R" else "Y"

        # Check for diagonal top left to bottom right
        for row in range(3):
            for col in range(4):
                if self.board[row][col] != "O":
                    curr_player = self.board[row][col]
                    # Check diagonal from top-left to bottom-right
                    if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3]:
                        return "R" if curr_player == "R" else "Y"

        # Check if there are empty spaces (game can still play)
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == "O":
                    return None  # No winner yet, the game is still ongoing

        # If all spaces are filled, it's a draw
        return 0
