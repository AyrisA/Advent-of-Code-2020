"""
--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
"""

from itertools import product
import numpy as np


def count_neighbors(seat, grid):
    r0 = seat[0]-1 if seat[0] >= 1 else 0
    r1 = seat[0]+2 if seat[0] < grid.shape[0]-1 else grid.shape[0]
    c0 = seat[1]-1 if seat[1] >= 1 else 0
    c1 = seat[1]+2 if seat[1] < grid.shape[1]-1 else grid.shape[1]
    neighbors = [e for e in product(range(r0, r1), range(c0, c1)) if e != seat]

    filled = [grid[n] for n in neighbors if grid[n] == '#']
    return len(filled)


def count_visible_neighbors(seat, grid):
    count = 0
    
    # Right neighbors
    if seat[1]+1 < grid.shape[1]:
        for s in grid[seat[0], seat[1]+1:]:
            if s == 'L':
                break
            elif s == '#':
                count += 1
                break

    # Left neighbors
    if seat[1]-1 >= 0:
        for s in np.flip(grid[seat[0], :seat[1]]):
            if s == 'L':
                break
            elif s == '#':
                count += 1
                break

    # Down neighbors
    if seat[0]+1 < grid.shape[0]:
        for s in grid[seat[0]+1:, seat[1]]:
            if s == 'L':
                break
            elif s == '#':
                count += 1
                break

    # Up neighbors
    if seat[0]-1 >= 0:
        for s in np.flip(grid[:seat[0], seat[1]]):
            if s == 'L':
                break
            elif s == '#':
                count += 1
                break

    # Down right neighbors
    spot = tuple(s+1 for s in seat)
    while (spot[0] < grid.shape[0]) and (spot[1] < grid.shape[1]):
        if grid[spot] == 'L':
            break
        elif grid[spot] == '#':
            count += 1
            break
        spot = tuple(s+1 for s in spot)
    
    # Up left neighbors
    spot = tuple(s-1 for s in seat)
    while (spot[0] >= 0) and (spot[1] >= 0 ):
        if grid[spot] == 'L':
            break
        elif grid[spot] == '#':
            count += 1
            break
        spot = tuple(s-1 for s in spot)

    # Down left neighbors
    spot = (seat[0]+1, seat[1]-1)
    while (spot[0] < grid.shape[0]) and (spot[1] >= 0):
        if grid[spot] == 'L':
            break
        elif grid[spot] == '#':
            count += 1
            break
        spot = (spot[0]+1, spot[1]-1)

    # Up right neighbors
    spot = (seat[0]-1, seat[1]+1)
    while (spot[0] >= 0) and (spot[1] < grid.shape[1]):
        if grid[spot] == 'L':
            break
        elif grid[spot] == '#':
            count += 1
            break
        spot = (spot[0]-1, spot[1]+1)

    return count
        

with open('./input11.txt', 'r') as f:
    grid_in = np.array([list(x.strip()) for x in f.readlines()])

flip_grid = np.zeros(grid_in.shape).astype(int)

# Part 1
grid = grid_in.copy()
while True:
    changed = False
    for spot, val in np.ndenumerate(grid):
        if val != '.':
            nn = count_neighbors(spot, grid)
            if (val == 'L' and nn == 0):
                flip_grid[spot] = 1
                changed = True
            if(val == '#' and nn >= 4):
                flip_grid[spot] = -1
                changed = True
    grid[np.where(flip_grid == 1)] = '#'
    grid[np.where(flip_grid == -1)] = 'L'
    flip_grid[:] = 0
    if not changed:
        break

occupied = len(grid[np.where(grid == '#')])
print("{} seats are occupied".format(occupied))

# Part 2
grid = grid_in.copy()
# print(grid)
# print()
while True:
    changed = False
    for spot, val in np.ndenumerate(grid):
        if val != '.':
            nn = count_visible_neighbors(spot, grid)
            if (val == 'L' and nn == 0):
                flip_grid[spot] = 1
                changed = True
            if(val == '#' and nn >= 5):
                flip_grid[spot] = -1
                changed = True
    grid[np.where(flip_grid == 1)] = '#'
    grid[np.where(flip_grid == -1)] = 'L'
    flip_grid[:] = 0
    # print(grid)
    # print()
    count_visible_neighbors((1,1), grid)
    if not changed:
        break

occupied = len(grid[np.where(grid == '#')])
print("New rules: {} seats are occupied".format(occupied))