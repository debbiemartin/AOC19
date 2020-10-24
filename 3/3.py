#!/usr/bin/python

# @@@ for testing
#instructions_a = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
#instructions_b = ['U62','R66','U55','R34','D71','R55','D58','R83']

with open('3/instructions.txt', 'r') as f:
    line = f.readline()
    instructions_a = [instruction.strip('\n') for instruction in line.split(",")]
    line = f.readline()
    instructions_b = [instruction.strip('\n') for instruction in line.split(",")]

print(instructions_a)
print(instructions_b)

def list_coords(instruction_set):

    last_coord = (0,0)
    last_time = 0
    coords = dict()

    for instruction in instruction_set:
        for i in range(int(instruction[1:])):
            if instruction[0] == 'R':
                coord = (last_coord[0] + 1, last_coord[1])
            elif instruction[0] == 'L':
                coord = (last_coord[0] - 1, last_coord[1])
            elif instruction[0] == 'U':
                coord = (last_coord[0], last_coord[1] + 1)
            elif instruction[0] == 'D':
                coord = (last_coord[0], last_coord[1] - 1)
            else:
                print("Error: unexpected coord")

            # Create dict of coords indexed by the coord - value is time
            coords[coord] = last_time + 1
            last_coord = coord
            last_time = last_time + 1

    return (coords)

coords_a = list_coords(instructions_a)
coords_b = list_coords(instructions_b)

# take the two dicts and find the intersection - put together into second dict
# with time = time_a + time_b
coords = set.intersection(set(coords_a.keys()), set(coords_b.keys()))
print("coords: " + str(coords))

shortest = 0
for coord in coords:
    print("coord_a: " + str(coords_a[coord]) + " coord_b: " + str(coords_b[coord]))
    time = coords_a[coord] + coords_b[coord]
    if time < shortest or shortest == 0:
        shortest = time
        result = coord

print(shortest)
print(result)

