import numpy as np
import time


# Load sudokus
# numpy array [y_val][x_val]
# [row][row][row]
# [column]
# [column]
# [column]
# [column]
def sudoku_solver(sudoku):

    def location_to_string(location): #function which takes
        return str(location[0]) + str(location[1])




    class sudoku_board():
        def __init__(self, board, changed, possible_vals, last_empty_squares):
            self.board = board
            self.y_size = 9
            self.x_size = 9
            self.square_changed = changed  # square that was changed to create this board
            self.array_possible_values = possible_vals
            self.overall_empty_squares_dict = last_empty_squares
            del self.overall_empty_squares_dict[location_to_string(changed)]

        def get_board(self):
            return self.board

        def create_possible_values(
                self):  # first time we run we are just finding all zeros and working out there possible values
            possible_empty_squares = self.find_empty()

            for this_empty_location in possible_empty_squares:
                self.overall_empty_squares_dict[location_to_string(this_empty_location)] = this_empty_location

                array_of_possible_values = self.work_out_possible_values(this_empty_location)
                self.array_possible_values[this_empty_location[0]][this_empty_location[1]] = array_of_possible_values

        def check_solved(self):  # for it to be correct is has to be full, and valid
            if len(self.overall_empty_squares_dict) == 0:  # i.e there are no empty spaces
                if self.is_valid_specific():  #todo check wether we need to use is valid overall here
                    return True
            else:
                return False

        def print_board(self):
            print(self.board)

        def is_valid_specific(self):  # check if a sudoku board is valid from last change
            row_vals = []
            col_vals = []
            square_vals = []

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

        def work_out_possible_values(self, location):  # location is an array here
            possible_values = []
            for this_value_to_check in range(1, 10):
                if self.is_valid_partial(location, this_value_to_check):
                    possible_values.append[this_value_to_check]
            return possible_values

        def find_empty(self):
            possible_empty_squares = []
            for y in range(0, self.x_size):  ##todo turn into function
                for x in range(0, self.y_size):
                    if self.board[y][x] == 0:
                        possible_empty_squares.append([y, x])
            return possible_empty_squares

        def find_min_constraining(self):  # starting top left of the sudoku board looks through to find an empty square
            possible_empty_squares = self.overall_empty_squares_dict.values()
            if len(possible_empty_squares) == 0:  # this means we have found a full board
                return False
            current_lowest_value = [10, None]  # todo need a catch all here?
            for this_empty_location in possible_empty_squares:
                array_of_possible_values = self.array_possible_values[this_empty_location[0]][this_empty_location[1]]
                if len(array_of_possible_values) == 1 or len(
                        array_of_possible_values) == 2:  # this is a singelton/2 options todo make expalnaiton better
                    return this_empty_location
                elif len(array_of_possible_values) < current_lowest_value[
                    0]:  # elif here for clarity will only run if other is false anyway
                    current_lowest_value[0] = len(array_of_possible_values)
                    current_lowest_value[1] = this_empty_location
            return current_lowest_value[1]

        def is_valid_partial(self, location_check, value):  # partial values for a new state
            row_vals = []
            col_vals = []
            square_vals = []
            board = np.copy(self.board)
            board[location_check] = value
            if location_check[0] == 7:
                pass

            for x_val in range(0, self.x_size):  # checking whether the row is valid
                this_val = board[location_check[0], x_val]
                if this_val != 0:
                    if this_val in row_vals:  # todo could be made more efficent?
                        return False  # same values in row so this state invalid
                    row_vals.append(this_val)
            for y_val in range(0, self.y_size):  # checking whether the column is valid
                this_val = board[y_val, location_check[1]]
                if this_val != 0:
                    if this_val in col_vals:  # todo could be made more efficent?
                        return False  # same values in column so this sate is invalid
                    col_vals.append(this_val)
            # used to work out what square we are in, and check the locaitons in this square
            if 0 <= location_check[0] <= 2:
                y_bias = 0
            elif 3 <= location_check[0] <= 5:
                y_bias = 3
            else:
                y_bias = 6
            if 0 <= location_check[1] <= 2:
                x_bias = 0
            elif 3 <= location_check[1] <= 5:
                x_bias = 3
            else:
                x_bias = 6

            for y_val in range(0 + y_bias, 3 + y_bias):
                for x_val in range(0 + x_bias, 3 + x_bias):
                    this_val = board[y_val, x_val]
                    if this_val != 0:
                        if this_val in square_vals:  # todo could be made more efficent?
                            return False  # same values in sqaure so this state is invalid
                        square_vals.append(this_val)
            return True

        def create_new(self, value):  # remember x_location,y_location needs to be 0 indexed.
            locations = self.find_min_constraining()
            if locations == False: #todo sort this out to exception
                print("something has gone wrong here, we have found a full board, looks like this:")
                self.print_board()
                return False
            new_board = np.copy(self.board)
            new_board[locations[0]][locations[1]] = value
            return sudoku_board(new_board, locations, self.array_possible_values, dict(self.overall_empty_squares_dict))

        def set_invalid(self):
            self.board = np.full((9, 9), -1)

    def go_for_this_square(next_state):
        ##for debugging
        # print("current state of board:")
        # next_state.print_board()
        if next_state.check_solved() == True:
            return next_state
        this_loops_start_state = next_state
        for new_value_to_try in range(1, 10):  # goes through all values from 1 - 9 inclusive
            trial_state = this_loops_start_state.create_new(new_value_to_try)
            if trial_state.check_solved():
                return trial_state
            if trial_state.is_valid_specific():
                lower_state = go_for_this_square(trial_state)
                if lower_state is not False and lower_state.check_solved():
                    return lower_state
        trial_state.set_invalid()  # todo check dont think this is correct
        return trial_state

    def create_3d_array(size):
        overall_array = []
        for y in range(0, size[0]):
            this_array = []
            for x in range(0, size[1]):
                this_array.append([])
            overall_array.append(this_array)
        return overall_array

    ## main
    ##debug only

    ## actual main
    this_board_to_solve = sudoku_board(sudoku, [0, 0], create_3d_array([9, 9]), {"00": [0,0] }) #add a dictionary so our empty square can be removed in setup
    this_board_to_solve.create_possible_values()
    if not this_board_to_solve.is_valid_overall():
        this_board_to_solve.set_invalid()
        returned_val = this_board_to_solve
    else:
        returned_val = go_for_this_square(this_board_to_solve)

    return returned_val.get_board()


##test script
SKIP_TESTS = False
overall_start_time = time.process_time()


def tests():
    import time
    difficulties = ['very_easy', 'easy', 'medium']  # todo re-add hard

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)

            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])

            print("This sudoku took", end_time - start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break


if not SKIP_TESTS:
    tests()

overall_end_time = time.process_time()
print("Overall this took", overall_end_time - overall_start_time, "seconds to solve.\n")
