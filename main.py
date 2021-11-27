import numpy as np

# Load sudokus
# numpy array [y_val][x_val]
# [row][row][row]
# [column]
# [column]
# [column]
# [column]



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
        for y_val in range(0, self.y_size):
            for x_val in range(0, self.x_size):
                if self.board[y_val][x_val] == 0:
                    return False
        return True
    def print_board(self):
        print(self.board)
    def is_valid_specific(self): #check if a sudoko board is valid from last change
        row_vals = []
        col_vals = []
        square_vals = []
        for x_val in range (0,self.x_size ): #checking whether the row is valid
            this_val = self.board[self.square_changed[0], x_val]
            if this_val !=0:
                if this_val in row_vals: #todo could be made more efficent?
                    return False # same values in row so this state invalid
                row_vals.append(this_val)
        for y_val in range (0,self.y_size): #checking whether the column is valid
            this_val = self.board[y_val, self.square_changed[1]]
            if this_val !=0:
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

        for y_val in range (0+ y_bias,3+ y_bias):
            for x_val in range(0 + x_bias,3+x_bias):
                this_val = self.board[y_val, x_val]
                if this_val !=0:
                    if this_val in square_vals:  # todo could be made more efficent?
                        return False #same values in sqaure so this state is invalid
                    square_vals.append(this_val)
        return True
    def is_valid_overall(self):
        for y_val in range(0,self.x_size):
            row_vals = []
            for x_val in range(0, self.x_size):  # checking whether the row is valid
                this_val = int(self.board[y_val, x_val])
                if this_val != 0: #0 represents an empty square, so we don't care if there are mutiple of these
                    if this_val in row_vals:  # todo could be made more efficent?
                        return False  # same values in row so this state invalid
                    row_vals.append(this_val)
        for x_val in range(0,self.y_size):
            col_vals = []
            for y_val in range(0, self.y_size):  # checking whether the column is valid
                this_val = int(self.board[y_val, x_val])
                if this_val != 0:
                    if this_val in col_vals:  # todo could be made more efficent?
                        return False  # same values in column so this sate is invalid
                    col_vals.append(this_val)
        x_bias = 0
        for y_bias in [0,3,6]:
            square_vals = []
            for y_val in range (0+ y_bias,3+ y_bias):
                for x_val in range(0 + x_bias,3+x_bias):
                    this_val = int(self.board[y_val, x_val])
                    if this_val != 0:
                        if this_val in square_vals:  # todo could be made more efficent?
                            return False #same values in sqaure so this state is invalid
                        square_vals.append(this_val)
        y_bias = 0
        for x_bias in [0,3,6]:
            square_vals = []
            for y_val in range(0 + y_bias, 3 + y_bias):
                for x_val in range(0 + x_bias, 3 + x_bias):
                    this_val = self.board[y_val, x_val]
                    if this_val != 0:
                        if this_val in square_vals:  # todo could be made more efficent?
                            return False  # same values in sqaure so this state is invalid
                        square_vals.append(this_val)
        return True

    def find_empty(self): #startin top left of the sudoko board looks through to find an empty square
        for y in range(0, self.x_size ):
            for x  in range(0, self.y_size ):
                if self.board[y][x] == 0:
                    return(y,x)
        return False
    def create_new(self,value): # remeber x_location,y_location needs to be 0 indexed.
        locations = self.find_empty()
        if locations == False:
            print("something has gone wrong here, we have found a full board, looks like this:")
            self.print_board()
            return False
        new_board = np.copy(self.board)
        new_board[locations] = value
        return sudoku_board(new_board,locations)

    def set_invalid(self):
        self.board = np.array([[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1]])


def go_for_this_square(next_state):
    print("current state of board:")
    next_state.print_board()
    if next_state.check_solved() == True:
        return True
    this_loops_start_state = next_state
    for new_value_to_try in range(1, 10): #goes through all values from 1 - 9 inclusive
        trial_state = this_loops_start_state.create_new(new_value_to_try)
        #trial_state.print_board()
        if trial_state.check_solved():
            return trial_state
        if trial_state.is_valid_specific():
            lower_state = go_for_this_square(trial_state)
            if lower_state is not False and lower_state.check_solved():

                return lower_state
    return trial_state




## load sudokus
sudoku = np.load("data/easy_puzzle.npy")
solution = np.load("data/easy_solution.npy")
print("easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")



## main
initial_sudoko_list = [sudoku_board(sudoku[7],[0,0])]
#for this_sudoko_board in sudoku:
 #   initial_sudoko_list.append(sudoku_board(this_sudoko_board,[0,0]))# here we are creating the sudoko board class for our first board, and parsing in the numpy array of our first board
counter = 0
for this_board_to_solve in initial_sudoko_list:


    if not this_board_to_solve.is_valid_overall():
        this_board_to_solve.set_invalid()
        returned_val = this_board_to_solve
    else:
        returned_val = go_for_this_square(this_board_to_solve)
    print("Sudoku from program:")
    returned_val.print_board()
    print("Sudoko solution:")
    print(solution[7]) #todo changes this back to counter once debugging is done
    counter +=1
    print("\n")