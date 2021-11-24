import numpy as np

# Load sudokus
# numpy array [y_val][x_val]
# [row][row][row]
# [column]
# [column]
# [column]
# [column]
sudoku = np.load("data/very_easy_puzzle.npy")
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")


class sudoku_board():
    def __init__(self, board):
        self.board = board
        self.solved = False
        y_size = 9
        x_size = 9


    def check_solved(self):
        for y_val in range(0, self.y_size -1 ):
            for x_val in range(0, self.x_size -1 ):
                if self.board[y_val][x_val] == 0:
                    return False
        return True
    def is_valid(self,location):
        row_vals = []
        col_vals = []
        square_vals = []
        for x_val in range (0,self.x_size -1): #checking whether the row is valid
            this_val = self.board[location[0],x_val]
            if this_val in row_vals: #todo could be made more efficent?
                return False # same values in row so this state invalid
            row_vals.append[this_val]
        for y_val in range (0,self.y_size -1): #checking whether the column is valid
            this_val = self.board[y_val, location[1]]
            if this_val in col_vals:  # todo could be made more efficent?
                return False #same values in column so this sate is invalid
            col_vals.append[this_val]
        # used to work out what square we are in, and check the locaitons in this square
        if 0 <= location[0] <= 2:
            y_bias = 0
        elif 3<= location[0] <= 5:
            y_bias = 3
        else:
            y_bias = 6
        if 0 <= location[1] <= 2:
            x_bias = 0
        elif 3 <= location[1] <= 5:
            x_bias = 3
        else:
            x_bias = 6

        for y_val in range (0+ y_bias,2+ y_bias):
            for x_val in range(0 + x_bias,2+x_bias):
                this_val = self.board[y_val, location[1]]
                if this_val in square_vals:  # todo could be made more efficent?
                    return False #same values in sqaure so this state is invalid
                square_vals.append[this_val]
        return True



## main
first_sudoku = sudoku_board(sudoku[
                                0])  # here we are creating the sudoko board class for our first board, and parsing in the numpy array of our first board
