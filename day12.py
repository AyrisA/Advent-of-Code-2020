"""
--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11
These instructions would be handled as follows:

F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
N3 would move the ship 3 units north to east 10, north 3.
F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
"""


with open('./input12.txt', 'r') as f:
    actions = [x.strip() for x in f.readlines()]

# Part 1
loc = [0, 0]
facing = 90  #East
for a in actions:
    action = a[0]
    val = int(a[1:])
    if action == 'N':
        loc[1] += val
    elif action == 'S':
        loc[1] -= val
    elif action == 'E':
        loc[0] += val
    elif action == 'W':
        loc[0] -= val
    elif action == 'L':
        facing -= val
        facing = facing % 360
    elif action == 'R':
        facing += val
        facing = facing % 360
    else:
        if facing == 0:
            loc[1] += val
        elif facing == 90:
            loc[0] += val
        elif facing == 180:
            loc[1] -= val
        else:
            loc[0] -= val

mdist = sum([abs(x) for x in loc])
print("The Manhattan distance is: {}".format(mdist))

# Part 2
# def quadrant(coord):
#     if coord[0] >= 0 and coord[1] >= 0:
#         quad = 1
#     elif coord[0] < 0 and coord[1] >= 0:
#         quad = 1
#     elif coord[0] < 0 and coord[1] < 0:
#         quad = 3
#     else:
#         quad = 4
#     return quad

loc = [0, 0]
waypoint = [10, 1]
for a in actions:
    action = a[0]
    val = int(a[1:])
    if action == 'N':
        waypoint[1] += val
    elif action == 'S':
        waypoint[1] -= val
    elif action == 'E':
        waypoint[0] += val
    elif action == 'W':
        waypoint[0] -= val
    elif action in ['L', 'R']:
        if val == 180:
            waypoint = [-w for w in waypoint]      
        elif (val == 90 and action == 'L') or (val == 270 and action == 'R'):      
            waypoint = [-waypoint[1], waypoint[0]]
        else:
            waypoint = [waypoint[1], -waypoint[0]]

    else:
        loc[0] += val * waypoint[0]
        loc[1] += val * waypoint[1]

mdist = sum([abs(x) for x in loc])
print("The real Manhattan distance is: {}".format(mdist))