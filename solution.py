from utils import *
import copy
import pprint
import itertools

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    # find out all boes that contains 2 digits
    double_boxes = []
    for box in values.keys():
        poss = len(values[box])
        if poss == 2:
            double_boxes.append(box)
    
    for pair in itertools.combinations(double_boxes,2):
        if pair[0] in peers[pair[1]] and values[pair[0]] == values[pair[1]]:
            for box in peers[pair[0]] & peers[pair[1]]:                
                assign_value(values, box, values[box].replace(values[pair[0]][0],''))
                assign_value(values, box, values[box].replace(values[pair[0]][1],''))
                   
    return values    

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Your code here: Use the Naked Twin Strategy
        values = naked_twins(values)        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        # pprint.pprint(values)
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    min_poss = 9
    choosen_box = 0
    poss_values = []
    answers = []
    flag = False
    for box in values.keys():
        poss = len(values[box])
        if poss > 1 and poss < min_poss:
            choosen_box = box
            min_poss = poss
    # pprint.pprint(choosen_box + ': ' + str(min_poss) +
    #               ' - ' + str(values[choosen_box]))
    for digit in values[choosen_box]:
        tmp = copy.deepcopy(values)
        tmp[choosen_box] = digit
        poss_values.append(tmp)

    # Now use recursion to solve each one of the resulting sudokus, and if one
    for poss_value in poss_values:
        tmp = search(poss_value)
        if tmp:
            flag = True
            values = tmp
            break

    if flag == True:
        return values
    else:
        return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
