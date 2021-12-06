## Implementation overview
My Sudoku solving implementation models the Sudoku solver as a constraint satisfaction problem, and uses a depth first search with backtracking to explore the search space. It does this using a class based model, w ith each state (specific combinations of values for the Sudoku board) as a different class. The representation of the class is shown here:

![Uml Diagram of Sudoku_board ](/uml.png)

### Constraint satisfaction
To model the Sudoku as a constraint satisfaction problem we set our constraints as the following
**C =**
1.  There must be no repetition of a number within a unit (where a unit is a row, column or square)

We then have our set of variables as each location within this board: ![X = {S_0,0 , S_0,1 .... S_n,n} ](/variables.png)

And we have a list of domains specifying the values that each of our variables above can take, for instance: ![[domains.png]]

We are aiming for a state that is consistent, so our constraint is not violated and complete, and complete, so all variables have been assigned a value. 

We can then do this by searching through partials states, which allows us to improve on a classic depth first search. We have already been checking that the constraints above are satisfied within each step of our depth first search, and pruning branches that have an invalid state. However by keeping our domains for each variables within the object we no longer have to check whether a state is valid, we only create states that are consistent. For instance instead of trying 1,2,3,4,5,6,7,8,9 for each variable and checking if each is valid we can know just check the values within our domain for that variable. 

This is implemented within my program using a 3d array, with the locations on the board as a 9 by 9 array, and lists with the domain for each location stored within this. This is then serviced each we create a new object, by removing the value that was changed to create this object from the units that were changed, e.g if we changed location 5,4 by adding the value 7 in this location we would remove 7 from the domain of every variable within the same row,column or square. 

I also store a dictionary of empty squares, to allow for the program to check through variables that we can change without having to search through all of them individually, and remove squares from this when we fill them. 

### Depth first search with backtracking
My program implements a depth first search recursively, in the `depth_first_search()` function. This function first checks if a state is solved, in which case it returns this. If not it creates a new object, based on the domain of possible values. For each of these it creates a new state with the value, and then runs the function again with this state, until it either finds a solution or runs out of locations to check, in this case it backtracks and tries again with a different value.


### Heuristics
The program uses heuristics to choose the next location to check, the goal of these is to reduce the number of states we have to evaluate before finding a solution or realising the problem is invalid. The one I used within my solution was the minimum remaining value, this involves choosing the location with the least values in it's domain, so we explore the trees with less nodes to see if they will lead to our solution before trying those with more nodes to explore.

When it finds a singleton (a variable with only one value in it's domain) we instantly explore this, and if there are none of these we explore the variable with the smallest domain. Here the program will favour those locations that share a unit with the location we have just changed, as this is more likely to lead to a contradiction. 

### Naked Grouping
We can eliminate some values from domains based on rules within Sudoku, an example of this is where naked couples and naked triples arise. A naked couple is where we have two identical domains of size 2 within the same unit, for instance if we have the domains {7,8} and {7,8} within the same row, then we know that one of these variables has to be assigned 7 and the other 8, this means we can eliminate 7 and 8 from all other values in the row. This is again possible with naked triples, where we have 3 identical domains with size 3/2 (with at least one of them 3) within a unit, and the same logic follows with these 3 variables. This allows us to decrease the number of nodes in our search tree we have to visit, by decreasing the domains of variables 

### Hidden singles
We are already exploring singletons (naked singles) because when we search through our domain if there is a variable with a domain of length 1 we explore this. However there are some cases where we have  a hidden singleton, where this is only one occurrence of a value within a unit, but it is hidden within a larger domain. For instance if we have a domain of {1,7,8}  and the value is not in any other variables domains within a unit (7 is not in any of the domains of the same row/column/square) then the value of this variable must be equal to 7, so we can set it to 7, creating a singleton and reducing the need to search through other values. I run this once when the Sudoku board is created, and do not need to run it again when we change the domains of our variables, since all of the hidden singles will already have been revealed. There are relatively few hidden singles within most Sudoku problems, however since we only have to run it once at the start of our program it has a small overhead and is worth the time needed to check through all of the domains, and the values within them. 

#### Application 
Within my program this is applied using two main functions, `remove_naked_specific()`and `remove_naked_overall()`. I introduced the `remove_naked_specific()` function to improve the efficiency of my program. I store a value within the object of the square that was changed to create it, and I use this to only check for naked groups within the units that were changed, i.e the row column and square including the variable that was changed. This saves time instead of checking through the whole board. The overall function is run when we create a new object for the first time, with an unchanged board, and checks through all of the locations for naked groups. Originally this included code to test for all units, however after some testing I found that naked groups where very rare within the same square, and where often within the same row/ column anyway, meaning that some of the values had already been taken out of the square. This meant that searching for them on instantiation of our start class actually decreased the efficency of the program, so my program only checks within squares in the `remove_naked_specific()`function. This is alot less computationally expensive as it means we only have to check through one square instead of 9.
 
## Python Implementation
As well as implementing the overall algorithm to solving Sudoku problems outlined above, and improving this to reduce the number of nodes we have to explore within our search tree. There were also improvements to be made with the specific implementation of this in python. 

### Deep copy 
Originally I was using the `copy.deepcopy()` function from the inbuilt copy library to copy my 3d array of possible values, since arrays are passed by reference in python(known as a shallow copy), we need to manually copy each of the values to a new array, so that if we change one of the values within this new array it will not affect our original array. However this function takes up a lot of cpu time, since it cannot assume that the types of our array will be the same (because an array in python can be made up of multiple different data types), it has to check each data type individually. The array used within my program is exclusively made up of integers, so we can simply use list comprehension to create a deep copy of our array, like so:
`self.array_possible_values = [[j[:] for j in x] for x in possible_vals]`

### Use of sets
Originally where I was storing a list of values that I would have to search through them to check if there was a value in them, for instance to remove_values from domains in the `take_out_possible_values()`, I used lists for this purpose and then check if the valid was in the list. However since domains are unordered, and cannot contain repeating values. I found sets where a more appropriates data structure for this, since on creation they create a hash for each of the values, searching through them to see if a value is in them is much more efficient. 

### Finding the minimum remaining 
I was originally finding the minimum constraining value for each object, however I found this could be optimised by finding the minimum constraining value for an object at the start of my recursive function `depth_first_search` and then resetting this every time we run the function I reduced the number of times it was nessecary to run the function. 

### Use of list comprehension


### Use of for loops
A weird quirk I found when testing my code was that when checking through the board, or part of the board using two for loops to iterate through x and y values, that it was actually quicker to run these seperatly than to combine them in to one loop. This can be explained by the fact that our loops will not always run to there full extent, for instance in the 'is_valid_partial()' function we will return false if a value is not valid, and don't need to run the rest of the function. If we run through our y_loop at the same time as the x one then this will have to reach it's conclusion before being able to see if the domain is valid, which means although we have to iterate through twice as many values it is actually faster to do these seperately. 