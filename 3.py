#!/auto/ensoft/bin/python

# @@@ for testing
#instructions_a = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
#instructions_b = ['U62','R66','U55','R34','D71','R55','D58','R83']

with open('instructions.txt', 'r') as f:
    line = f.readline()
    instructions_a = [instruction for instruction in line.split(",")]
    line = f.readline()
    instructions_b = [instruction for instruction in line.split(",")]

print(instructions_a)
print(instructions_b)

def list_coords(instruction_set):
    
    last_coord = (0,0)
    coords = []
    
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
            coords.append(coord)
            last_coord = coord

    return (coords)

coords_a = list_coords(instructions_a)
coords_b = list_coords(instructions_b)

intersections = set.intersection(set(coords_a), set(coords_b))

shortest = 0
for intersection in intersections:
    distance = abs(intersection[0]) + abs(intersection[1])
    if shortest == 0 or distance < shortest:
        shortest = distance
        result = intersection

print(result)
print(shortest)

