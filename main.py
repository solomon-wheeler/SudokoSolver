import numpy as np


# Load sudokus
# numpy array [y_val][x_val]
# [row][row][row]
# [column]
# [column]
# [column]
# [column]

class sudoku_board():
    def __init__(self, board, changed):
        self.board = board
        self.solved = False  # todo not using this
        self.y_size = 9
        self.x_size = 9
        self.square_changed = changed  # square that was changed to create this board

    def get_board(self):
        return self.board

    def check_solved(self): #for it to be correct is has to be full, and valid
        if self.find_empty() == False: #i.e there are no empty spaces
            if self.is_valid_overall() == True: #full thing is valid
                return True
        else:
            return False

    def print_board(self):
        print(self.board)

    def is_valid_specific(self):  # check if a sudoku board is valid from last change
        row_vals = []
        col_vals = []
        square_vals = []
        #debug only
        if self.square_changed[0] == 7:
            pass


        for x_val in range(0, self.x_size):  # checking whether the row is valid
            this_val = self.board[self.square_changed[0], x_val]
            if this_val != 0:
                if this_val in row_vals:  # todo could be made more efficent?
                    return False  # same values in row so this state invalid
                row_vals.append(this_val)
        for y_val in range(0, self.y_size):  # checking whether the column is valid
            this_val = self.board[y_val, self.square_changed[1]]
            if this_val != 0:
                if this_val in col_vals:  # todo could be made more efficent?
                    return False  # same values in column so this sate is invalid
                col_vals.append(this_val)
        # used to work out what square we are in, and check the locaitons in this square
        if 0 <= self.square_changed[0] <= 2:
            y_bias = 0
        elif 3 <= self.square_changed[0] <= 5:
            y_bias = 3
        else:
            y_bias = 6
        if 0 <= self.square_changed[1] <= 2:
            x_bias = 0
        elif 3 <= self.square_changed[1] <= 5:
            x_bias = 3
        else:
            x_bias = 6

        for y_val in range(0 + y_bias, 3 + y_bias):
            for x_val in range(0 + x_bias, 3 + x_bias):
                this_val = self.board[y_val, x_val]
                if this_val != 0:
                    if this_val in square_vals:  # todo could be made more efficent?
                        return False  # same values in sqaure so this state is invalid
                    square_vals.append(this_val)
        return True

    def is_valid_overall(self):
        for y_val in range(0, self.x_size):
            row_vals = []
            for x_val in range(0, self.x_size):  # checking whether the row is valid
                this_val = int(self.board[y_val, x_val])
                if this_val != 0:  # 0 represents an empty square, so we don't care if there are mutiple of these
                    if this_val in row_vals:  # todo could be made more efficent?
                        return False  # same values in row so this state invalid
                    row_vals.append(this_val)
        for x_val in range(0, self.y_size):
            col_vals = []
            for y_val in range(0, self.y_size):  # checking whether the column is valid
                this_val = int(self.board[y_val, x_val])
                if this_val != 0:
                    if this_val in col_vals:  # todo could be made more efficent?
                        return False  # same values in column so this sate is invalid
                    col_vals.append(this_val)
        x_bias = 0
        for y_bias in [0, 3, 6]:
            square_vals = []
            for y_val in range(0 + y_bias, 3 + y_bias):
                for x_val in range(0 + x_bias, 3 + x_bias):
                    this_val = int(self.board[y_val, x_val])
                    if this_val != 0:
                        if this_val in square_vals:  # todo could be made more efficent?
                            return False  # same values in sqaure so this state is invalid
                        square_vals.append(this_val)
        y_bias = 0
        for x_bias in [0, 3, 6]:
            square_vals = []
            for y_val in range(0 + y_bias, 3 + y_bias):
                for x_val in range(0 + x_bias, 3 + x_bias):
                    this_val = self.board[y_val, x_val]
                    if this_val != 0:
                        if this_val in square_vals:  # todo could be made more efficent?
                            return False  # same values in sqaure so this state is invalid
                        square_vals.append(this_val)
        return True

    def find_empty(self):  # starting top left of the sudoku board looks through to find an empty square
        for y in range(0, self.x_size):
            for x in range(0, self.y_size):
                if self.board[y][x] == 0:
                    return (y, x)
        return False

    def create_new(self, value):  # remember x_location,y_location needs to be 0 indexed.
        locations = self.find_empty()
        if locations == False:
            print("something has gone wrong here, we have found a full board, looks like this:")
            self.print_board()
            return False
        new_board = np.copy(self.board)
        new_board[locations] = value
        return sudoku_board(new_board, locations)

    def set_invalid(self):
        self.board = np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1]])


def go_for_this_square(next_state):
    ##for debugging
    print("current state of board:")
    next_state.print_board()
    if next_state.check_solved() == True:
        return next_state
    this_loops_start_state = next_state
    for new_value_to_try in range(1, 10):  # goes through all values from 1 - 9 inclusive
        trial_state = this_loops_start_state.create_new(new_value_to_try)
        # trial_state.print_board()
        if trial_state.check_solved():
            return trial_state
        if trial_state.is_valid_specific():
            lower_state = go_for_this_square(trial_state)
            if lower_state is not False and lower_state.check_solved():
                return lower_state
    trial_state.set_invalid() #todo check dont think this is correct
    return trial_state

def boards_identical(program_board,solution_board): #check if two boards are the same
    for y in range(0,9): #todo change this to variable for differtent seize maybe??
        for x in range(0,9):
            program_board_value = str(program_board[y,x])
            solution_board_value = str(int(solution_board[y,x]))
            if program_board_value not in solution_board_value:
                return x,y
    return 0,0

## load sudokus
sudoku = np.load("data/easy_puzzle.npy")
solution = np.load("data/easy_solution.npy")
print("easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

## main
##debug only
debug = True
if debug == True:
    sudoku_to_check = 5
    initial_sudoku_list = [sudoku_board(sudoku[5], [0,0])]

    for this_board_to_solve in initial_sudoku_list:

        if not this_board_to_solve.is_valid_overall():
            this_board_to_solve.set_invalid()
            returned_val = this_board_to_solve
        else:
            returned_val = go_for_this_square(this_board_to_solve)
        print("Sudoku from program:")
        returned_val.print_board()
        print("Sudoku solution:")
        print(solution[sudoku_to_check])
        # todo if statement below for debugging
        print(boards_identical(returned_val.get_board(),solution[sudoku_to_check]))

        print("\n")

else:


    ## actual main
    initial_sudoku_list = []
    for this_sudoku_board in sudoku:
        initial_sudoku_list.append(sudoku_board(this_sudoku_board, [0,0]))  # here we are creating the sudoku board class for our first board, and parsing in the numpy array of our first board
    counter = 0
    for this_board_to_solve in initial_sudoku_list:

        if not this_board_to_solve.is_valid_overall():
            this_board_to_solve.set_invalid()
            returned_val = this_board_to_solve
        else:
            returned_val = go_for_this_square(this_board_to_solve)
        print("Sudoku from program:")
        returned_val.print_board()
        print("Sudoku solution:")
        print(solution[counter])
        # todo if statement below for debugging
        print(boards_identical(returned_val.get_board(),solution[counter]))

        counter += 1
        print("\n")

