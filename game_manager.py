class GameManager():
    def __init__(self, board):
        self.board = board
        pass

    def apply_move(self, column, player):
        #creo necesitamos una copy del tablero
        row = 5  
        while row >= 0:
            if self.board[row][column] == 'O':  
                self.board[row][column] = player  
                break  
            row -= 1 
        
        return self.board

    def check_winner(self, board = None):

        # Use self.board if board is None
        if board is None:
            board = self.board

        # check for horizontal wins 
        for row in range(6):
            for col in range(4): # boundry 
                curr_line = []
                curr_player = self.board[row][col]
                #check that a player occupies current spot
                if curr_player != "O":
                    for i in range(4):
                        curr_line.append(self.board[row][col+i])
                    
                    #check if next 4 consecutive spaces are the same
                    if curr_line == [curr_player] * 4:
                        return -1 if curr_player == "R" else 1

        # check for vertical wins 
            for row in range(3):# boundry 
                for col in range(7): 
                    curr_line = []
                    curr_player = self.board[row][col]
                    #check that a player occupies current spot
                    if curr_player != "O":
                        for i in range(4):
                            curr_line.append(self.board[row+1][col])
                        
                        #check if next 4 consecutive spaces are the same
                        if curr_line == [curr_player] * 4:
                            return -1 if curr_player == "R" else 1

        # check for diagonal bottom left to top right
            for row in range(3, 6):
                for col in range(4):
                    if self.board[row][col] != "O":
                        curr_line = []
                        for i in range(4):
                            curr_line.append(self.board[row-i][col+i])
                        
                        if curr_line == ["R"] * 4:
                            return -1
                        elif curr_line == ["Y"] * 4:
                            return 1


        # check for diagonal top left to bottom right
            for row in range(3):
                for col in range(4):
                    if self.board[row][col] != "O":
                        curr_line = []
                        for i in range(4):
                            curr_line.append(self.board[row+i][col-i])
                        
                        if curr_line == ["R"] * 4:
                            return -1
                        elif curr_line == ["Y"] * 4:
                            return 1
            
            #check if there are empty spaces (game can still play)
            for row in range(6):
                for col in range(7):
                    if self.board[row][col] == "O":
                        return None
            
            # if all spaces are filled = draw
            return 0
