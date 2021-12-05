import numpy as np
import time

def sudoku_solver(sudoku):

    #
    # Creates an empty 3d array
    # Arguments: size ( array )
    #
    def create_3d_array(size):
        overall_array = []
        for y in range(0, size[0]):
            this_array = []
            for x in range(0, size[1]):
                this_array.append([])
            overall_array.append(this_array)
        return overall_array

    #
    # Takes a 2d location coordinate and returns a string value for this
    # Arguments: Location( array )
    #
    def location_to_string(location):
        return str(location[0]) + str(location[1])

    #
    # Used to work out which square we are checking in, and returns the bias (i.e 0 for first square, 3 for second, 6 for third)
    # Arguments : location (array)
    # Returns : y_bias, x_bias (tuple)
    #
    def workout_square_bias(location_to_check):
        if 0 <= location_to_check[0] <= 2:
            y_bias = 0
        elif 3 <= location_to_check[0] <= 5:
            y_bias = 3
        else:
            y_bias = 6
        if 0 <= location_to_check[1] <= 2:
            x_bias = 0
        elif 3 <= location_to_check[1] <= 5:
            x_bias = 3
        else:
            x_bias = 6
        return y_bias, x_bias

    #
    # Class that is used to store our sudoku board, we create new instances of these for every node in our search tree
    # Arguments :
    # Board, state of current board (array)
    # changed_location, square that was changed to create this board (array)
    # changed_value, value of the square that was changed to create this board (integer)
    # possible_values, this is a 3d array with empty squares filled with arrays of possible values for that squares (array)
    # last_empty_squares, empty squares from our last board (dictionary)
    #
    class sudoku_board():

        def __init__(self, board, changed_location, changed_value, possible_vals, last_empty_squares):
            self.board = board
            self.square_changed = changed_location
            self.value_of_changed_square = changed_value
            self.array_possible_values = [[j[:] for j in x] for x in
                                          possible_vals]  # creating a deep copy of our 3d array
            self.overall_empty_squares_dict = last_empty_squares
            del self.overall_empty_squares_dict[location_to_string(
                changed_location)]  # Deleting the value we have just filled from our empty squares list, since it is no longer empty
            self.take_out_possible_values()
            self.remove_naked_specific()

        def get_board(self):
            return self.board

        def create_possible_values(
                self):  # first time we run we are just finding all zeros and working out there possible values, by going through each value and checking if it is valid
            possible_empty_squares = self.find_empty()

            for this_empty_location in possible_empty_squares:
                self.overall_empty_squares_dict[location_to_string(this_empty_location)] = this_empty_location

                array_of_possible_values = self.work_out_possible_values(this_empty_location)
                self.array_possible_values[this_empty_location[0]][this_empty_location[1]] = array_of_possible_values

        def remove_naked_specific(self):
            y_location = self.square_changed[0]
            row_array = []
            for x_location in range(0, 9):
                this_val = self.array_possible_values[y_location][x_location]
                length = len(this_val)
                if length == 2 or length == 3:
                    counter = 0
                    triple_locations = []
                    found_two = False

                    for this_check in row_array:
                        if this_val == this_check:
                            if found_two == True:
                                triple_locations.append(counter)
                                self.remove_naked_row(y_location, triple_locations, this_val)
                            elif length == 2:
                                pair_locations = [x_location, counter]
                                self.remove_naked_row(y_location, pair_locations, this_val)
                            else:
                                triple_locations.append(x_location)
                                triple_locations.append(counter)
                                found_two = True

                        counter += 1
                row_array.append(this_val)

            x_location = self.square_changed[1]
            col_array = []
            for y_location in range(0, 9):
                this_val = self.array_possible_values[y_location][x_location]
                length = len(this_val)
                if length == 2 or length == 3:
                    counter = 0
                    triple_locations = []
                    found_two = False
                    for this_check in col_array:
                        if this_val == this_check:
                            if found_two:
                                triple_locations.append(counter)
                                self.remove_naked_col(x_location, triple_locations, this_val)
                            elif length == 2:
                                pair_locations = [y_location, counter]
                                self.remove_naked_col(x_location, pair_locations, this_val)
                            else:
                                triple_locations.append(y_location)
                                triple_locations.append(counter)
                                found_two = True

                        counter += 1
                col_array.append(this_val)

            y_bias, x_bias = workout_square_bias(self.square_changed)
            square_array = []
            counter_overall = 0
            for y_location in range(0 + y_bias, 3 + y_bias):
                for x_location in range(0 + x_bias, 3 + x_bias):
                    this_val = self.array_possible_values[y_location][x_location]
                    length = len(this_val)
                    if length == 2 or length == 3:
                        counter = 0
                        triple_locations = []
                        found_two = False
                        for this_check in square_array:
                            if this_val == this_check:
                                if found_two:
                                    triple_locations.append(counter)
                                    self.remove_naked_square(y_bias, x_bias, triple_locations, this_val)
                                elif length == 2:
                                    pair_locations = [counter_overall, counter]
                                    self.remove_naked_square(y_bias, x_bias, pair_locations, this_val)
                                else:
                                    triple_locations.append(counter_overall)
                                    triple_locations.append(counter)
                                    found_two = True

                            counter += 1
                    square_array.append(this_val)
                    counter_overall += 1

        def remove_naked_overall(self):
            for y_location in range(0, 9):
                row_array = []
                for x_location in range(0, 9):
                    this_val = self.array_possible_values[y_location][x_location]
                    length = len(this_val)
                    if length == 2 or length == 3:
                        counter = 0
                        triple_locations = []
                        found_two = False

                        for this_check in row_array:
                            if this_val == this_check:
                                if found_two == True:
                                    triple_locations.append(counter)
                                    self.remove_naked_row(y_location, triple_locations, this_val)
                                elif length == 2:
                                    pair_locations = [x_location, counter]
                                    self.remove_naked_row(y_location, pair_locations, this_val)
                                else:
                                    triple_locations.append(x_location)
                                    triple_locations.append(counter)
                                    found_two = True
                            counter += 1
                    row_array.append(this_val)

            for x_location in range(0, 9):
                col_array = []
                for y_location in range(0, 9):
                    this_val = self.array_possible_values[y_location][x_location]
                    length = len(this_val)
                    if length == 2 or length == 3:
                        counter = 0
                        triple_locations = []
                        found_two = False
                        for this_check in col_array:
                            if this_val == this_check:
                                if found_two:
                                    triple_locations.append(counter)
                                    self.remove_naked_col(x_location, triple_locations, this_val)
                                elif length == 2:
                                    pair_locations = [y_location, counter]
                                    self.remove_naked_col(x_location, pair_locations, this_val)
                                else:
                                    triple_locations.append(y_location)
                                    triple_locations.append(counter)
                                    found_two = True

                            counter += 1
                    col_array.append(this_val)

        def remove_naked_square(self, y_bias, x_bias, locations_to_skip, values):
            naked_list = set(values)
            counter = 0
            for y_location in range(0 + y_bias, 3 + y_bias):
                for x_location in range(0 + x_bias, 3 + x_bias):
                    if counter not in locations_to_skip:

                        possible_values = set(self.array_possible_values[y_location][x_location])
                        for this_check in naked_list:
                            if len(possible_values) != 0:
                                if this_check in possible_values:
                                    possible_values.remove(this_check)
                        self.array_possible_values[y_location][x_location] = list(possible_values)
                    counter += 1

        def remove_naked_row(self, row_down, naked_locations, values):
            naked_list = set(values)
            locations_without_pair = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            for this_location in naked_locations:
                locations_without_pair.remove(this_location)

            for x_val in locations_without_pair:
                possible_values = set(self.array_possible_values[row_down][x_val])
                for this_check in naked_list:
                    if this_check in possible_values:
                        possible_values.remove(this_check)
                self.array_possible_values[row_down][x_val] = list(possible_values)

        def remove_naked_col(self, col_across, pair_locations, values):
            naked_list = set(values)
            locations_without_pair = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            for this_location in pair_locations:
                locations_without_pair.remove(this_location)

            for y_val in locations_without_pair:
                possible_values = set(self.array_possible_values[y_val][col_across])
                for this_check in naked_list:
                    if this_check in possible_values:
                        possible_values.remove(this_check)
                self.array_possible_values[y_val][col_across] = list(possible_values)



        #
        # Taking out the values that are no longer possible when we add a new value, e.g if we add 4 we must take out all 4's in the appropraite row/column/square
        #
        def take_out_possible_values(self):
            for x_val in range(0, 9):
                this_val = self.array_possible_values[self.square_changed[0]][x_val]
                if self.value_of_changed_square in this_val:
                    this_val.remove(self.value_of_changed_square)
                    self.array_possible_values[self.square_changed[0]][x_val] = this_val
            for y_val in range(0, 9):
                this_val = self.array_possible_values[y_val][self.square_changed[1]]
                if self.value_of_changed_square in this_val:
                    this_val.remove(self.value_of_changed_square)
                    self.array_possible_values[y_val][self.square_changed[1]] = this_val
            y_bias, x_bias = workout_square_bias(self.square_changed)
            for y_val in range(0 + y_bias, 3 + y_bias):  # we are looping through each of the values in the square
                for x_val in range(0 + x_bias, 3 + x_bias):
                    this_val = self.array_possible_values[y_val][x_val]
                    if self.value_of_changed_square in this_val:
                        this_val.remove(self.value_of_changed_square)
                        self.array_possible_values[y_val][x_val] = this_val

        #
        # checks whether a board is solved, for it to be correct is has to be full, and valid
        #
        def check_solved(self):
            if len(self.overall_empty_squares_dict) == 0:  # i.e there are no empty spaces
                # we don't need to check if it is valid because the state won't have been created if it wasn't
                return True
            else:
                return False

        #
        # takes the bias, either 0,3,6 to indicate what square we are checking and returns wether it is valid or not
        # Arguments, y_bias, x_bias (integer)
        #
        def check_square(self, y_bias, x_bias):
            square_vals = set([])
            for y_val in range(0 + y_bias, 3 + y_bias):  # we are looping through each of the values in the square
                for x_val in range(0 + x_bias, 3 + x_bias):
                    this_val = self.board[y_val, x_val]
                    if this_val != 0:
                        if this_val in square_vals:
                            return False  # same values in square so this state is invalid
                        square_vals.add(this_val)
            return True

        #
        # checks if overall a sudoku board is valid, used at start when we don't know what last changed square is
        #
        def is_valid_overall(self):
            for y_val in range(0, 9):
                row_vals = []
                for x_val in range(0, 9):  # checking whether the row is valid
                    this_val = int(self.board[y_val, x_val])
                    if this_val != 0:  # 0 represents an empty square, so we don't care if there are mutiple of these
                        if this_val in row_vals:
                            return False  # same values in row so this state invalid
                        row_vals.append(this_val)
            for x_val in range(0, 9):
                col_vals = []
                for y_val in range(0, 9):  # checking whether the column is valid
                    this_val = int(self.board[y_val, x_val])
                    if this_val != 0:
                        if this_val in col_vals:
                            return False  # same values in column so this sate is invalid
                        col_vals.append(this_val)
            for x_bias in [0, 3, 6]:
                for y_bias in [0, 3, 6]:
                    if not self.check_square(y_bias, x_bias):
                        return False
            return True

        #
        # takes a location and works out valid numbers for it
        # Arguments, location (array)
        #
        def work_out_possible_values(self,
                                     location):
            possible_values = []
            for this_value_to_check in range(1, 10):
                if self.is_valid_partial(location, this_value_to_check):
                    possible_values.append(this_value_to_check)
            return possible_values

        #
        # finds all empty squares in the sudoko board, by going through and checking for 0s
        #
        def find_empty(self):
            possible_empty_squares = []
            for y in range(0, 9):
                for x in range(0, 9):
                    if self.board[y][x] == 0:
                        possible_empty_squares.append([y, x])
            return possible_empty_squares

        #
        # returns the minimum constraining value, by going through all empty squares and checking how many possible values they have
        #
        def find_min_constraining(
                self):
            possible_empty_squares = self.overall_empty_squares_dict.values()
            if len(possible_empty_squares) == 0:  # this means we have found a full board
                return False
            current_lowest_value = [10,
                                    None]  # sets our lowest value to 10, this is higher than the possible amount for one square so will always be replaced by the actual location
            for this_empty_location in possible_empty_squares:
                array_of_possible_values = self.array_possible_values[this_empty_location[0]][this_empty_location[1]]
                length = len(array_of_possible_values)  # avoids us running this twice
                if length == 1:  # this is a singelton so we immediatly investiage this state todo just fill in this value instead of investiaging
                    return this_empty_location
                elif length < current_lowest_value[0]:  # elif here for clarity will only run if other is false anyway
                    current_lowest_value[0] = length
                    current_lowest_value[1] = this_empty_location
                elif length == current_lowest_value[0]:
                    if this_empty_location[0] == self.square_changed[0] or this_empty_location[1] == \
                            self.square_changed[1]:
                        current_lowest_value[0] = length
                        current_lowest_value[1] = this_empty_location
            return current_lowest_value[1]

        #
        # Returns the values that are currently valid for a location
        # Arguments, location (array)
        #
        def get_pos_values(self, location):
            return self.array_possible_values[location[0]][location[1]]

        def is_valid_partial(self, location_check, value):  # checks whether partial values for a new state are valid
            row_vals = set([])
            col_vals = set([])
            square_vals = set([])
            self.board[location_check[0], location_check[1]] = value
            if location_check[0] == 7:
                pass

            for x_val in range(0, 9):  # checking whether the row is valid
                this_val = self.board[location_check[0], x_val]
                if this_val != 0:
                    if this_val in row_vals:
                        self.board[location_check[0], location_check[1]] = 0

                        return False  # same values in row so this state invalid
                    row_vals.add(this_val)

            for y_val in range(0, 9):  # checking whether the column is valid
                this_val = self.board[y_val, location_check[1]]
                if this_val != 0:
                    if this_val in col_vals:
                        self.board[location_check[0], location_check[1]] = 0
                        return False  # same values in column so this state is invalid
                    col_vals.add(this_val)
            # used to work out what square we are in, and check the locations in this square
            y_bias, x_bias = workout_square_bias(location_check)
            for y_val in range(0 + y_bias, 3 + y_bias):
                for x_val in range(0 + x_bias, 3 + x_bias):
                    this_val = self.board[y_val, x_val]
                    if this_val != 0:
                        if this_val in square_vals:
                            self.board[location_check[0], location_check[1]] = 0
                            return False  # same values in square so this state is invalid
                        square_vals.add(this_val)
            self.board[location_check[0], location_check[1]] = 0
            return True

        #
        # Returns a new object based upon value we are currently checking, and which location is minimum constraining.
        # Arguments:
        # location_to_test, the location we are going to change
        # value, the number we are going to place in this location (Integer)
        #
        def create_new(self, value,
                       location_to_test):
            locations = location_to_test
            new_board = np.copy(self.board)
            new_board[locations[0]][locations[1]] = value
            return sudoku_board(new_board, locations, value, self.array_possible_values,
                                dict(self.overall_empty_squares_dict))

        #
        # sets our board to invalid state, stipulated as filled with -1
        #
        def set_invalid(self):
            self.board = np.full((9, 9), -1)

    #
    # Recursive function that checks all values, if they are valid it calls itself and continues down the tree. If
    # not it prunes this branch and backtracks
    #
    def depth_first_search(
            next_state):

        if next_state.check_solved():
            return next_state
        this_loops_start_state = next_state  # we overwrite next state in our loop, so we need to keep a copy of the original.
        location_to_test = this_loops_start_state.find_min_constraining()  # finds the min constraining value
        possible_values = this_loops_start_state.get_pos_values(
            location_to_test)  # finds the possible values for this location
        for new_value_to_try in possible_values:  # goes through all values that are possible
            trial_state = this_loops_start_state.create_new(new_value_to_try, location_to_test)
            if trial_state.check_solved():
                return trial_state
            else:
                lower_state = depth_first_search(trial_state)
                if lower_state is not False and lower_state.check_solved():
                    return lower_state
        this_loops_start_state.set_invalid()
        return this_loops_start_state



    # Main
    this_board_to_solve = sudoku_board(sudoku, [0, 0], 0, create_3d_array([9, 9]),
                                       {"00": [0, 0]}, )  # add a dictionary so our empty square can be removed in setup
    this_board_to_solve.create_possible_values()
    this_board_to_solve.remove_naked_overall()

    if not this_board_to_solve.is_valid_overall():  # we check wether the board is valid at the start, to avoid going through recursively when it is invalid
        this_board_to_solve.set_invalid()
        returned_val = this_board_to_solve
    else:
        returned_val = depth_first_search(this_board_to_solve)

    return returned_val.get_board()


# Test script
SKIP_TESTS = False
overall_start_time = time.process_time()


def tests():
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard']

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
print("Overall this  took", overall_end_time - overall_start_time, "seconds to solve.\n")
