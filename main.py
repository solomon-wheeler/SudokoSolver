import numpy as np

# Load sudokus
# numpy array [y_val][x_val]
# [row][row][row]
# [column]
# [column]
# [column]
# [column]
sudoku = np.load("data/easy_puzzle.npy")
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

class sudoku_board():
    def __init__(self, board,changed):
        self.board = board
        self.solved = False #todo not using this
        self.y_size = 9
        self.x_size = 9
        self.square_changed = changed #square that was changed to create this board

    def get_board(self):
        return self.board
    def check_solved(self):
        for y_val in range(0, self.y_size -1 ):
            for x_val in range(0, self.x_size -1 ):
                if self.board[y_val][x_val] == 0:
                    return False
        return True
    def print_board(self):
        print(self.board)
    def is_valid(self): #check if a sudoko board is valid from last change
        row_vals = []
        col_vals = []
        square_vals = []
        for x_val in range (0,self.x_size -1): #checking whether the row is valid
            this_val = self.board[self.square_changed[0], x_val]
            if this_val in row_vals: #todo could be made more efficent?
                return False # same values in row so this state invalid
            row_vals.append(this_val)
        for y_val in range (0,self.y_size -1): #checking whether the column is valid
            this_val = self.board[y_val, self.square_changed[1]]
            if this_val in col_vals:  # todo could be made more efficent?
                return False #same values in column so this sate is invalid
            col_vals.append(this_val)
        # used to work out what square we are in, and check the locaitons in this square
        if 0 <= self.square_changed[0] <= 2:
            y_bias = 0
        elif 3<= self.square_changed[0] <= 5:
            y_bias = 3
        else:
            y_bias = 6
        if 0 <= self.square_changed[1] <= 2:
            x_bias = 0
        elif 3 <= self.square_changed[1] <= 5:
            x_bias = 3
        else:
            x_bias = 6

        for y_val in range (0+ y_bias,2+ y_bias):
            for x_val in range(0 + x_bias,2+x_bias):
                this_val = self.board[y_val, self.square_changed[1]]
                if this_val in square_vals:  # todo could be made more efficent?
                    return False #same values in sqaure so this state is invalid
                square_vals.append(this_val)
        return True
    def find_empty(self): #startin top left of the sudoko board looks through to find an empty square
        for y in range(0, self.x_size - 1):
            for x  in range(0, self.y_size -1):
                if self.board[y][x] == 0:
                    return(y,x)
        return False
    def create_new(self,value): # remeber x_location,y_location needs to be 0 indexed.
        locations = self.find_empty()
        if locations == False:
            return False
        new_board = self.board
        new_board[locations[0]][locations[1]] = value
        return sudoku_board(new_board,locations)

class Solver():
    def __init__(self):
        self.states_generate = 0
        self.prior_states = None #need to implement?

    def go_for_this_square(self, next_state):
        next_state.print_board()
        if next_state.check_solved() == True:
            return True

        for new_value_to_try in range(0, 9):
                next_state = next_state.create_new(new_value_to_try)
                if next_state.is_valid():
                    current_state = next_state
                    self.go_for_this_square(current_state)

        return False

    def solve(self,initial_state):

        final_value = self.go_for_this_square(initial_state)
        if self.current_state.is_valid() == True:
            return self.current_state.get_board()
        else:
            print("invaliddddd") #todo do fancy thing with the board here so that is has [-1][-1]





## main
initital_sudoku = sudoku_board(sudoku[0],[0,0])  # here we are creating the sudoko board class for our first board, and parsing in the numpy array of our first board
solver = Solver()
print(solver.solve(initital_sudoku))