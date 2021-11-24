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
        for x_val in range (0,self.x_size -1):
            this_val = self.board[location[0],x_val]
            if this_val in row_vals: #todo could be made more efficent?
                return False
            row_vals.append



## main
first_sudoku = sudoku_board(sudoku[
                                0])  # here we are creating the sudoko board class for our first board, and parsing in the numpy array of our first board
