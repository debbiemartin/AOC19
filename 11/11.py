#!/auto/ensoft/bin/python3

from subprocess import Popen, PIPE, STDOUT

p = Popen(['python3', '-u', './9.py'], stdout=PIPE, stdin=PIPE, stderr=PIPE)

matrix = {}
coord = (0, 0)
dir = (0, 1)

while True:
    p.stdin.write(b"1\n")

    p.stdin.flush()
    output1 = p.stdout.readline()
    output2 = p.stdout.readline()

    if output1 == b'' or output2 == b'':
        print("finished")
        break

    num1 = int(output1.decode('utf-8').strip('\n'))
    num2 = int(output2.decode('utf-8').strip('\n'))

    # decide what to paint the current tile based on output1
    matrix[coord] = output1

    # transform coord based on output2
    #    0 - turn left (0,1) > (-1,0) > (0,-1) > (1,0)
    #    1 - turn right (0,1) > (1,0) > (0,-1) > (-1,0)
    dir = (dir[1], dir[0])
    factor = (-1 if dir[num2] != 0 else 1)
    dir = tuple(x * factor for x in dir)

    coord = tuple(map(sum,zip(coord,dir))) #@@@ list would have been easier

    if coord in matrix:
        p.stdin.write(matrix[coord])
    else:
        p.stdin.write(b"0\n")

print("Matrix size at end: {}".format(len(matrix)))

# Plot matrix
# get x and y extent of coords in keys
XMAX = max(coord[0] for coord in matrix.keys())
XMIN = min(coord[0] for coord in matrix.keys())
YMAX = max(coord[1] for coord in matrix.keys())
YMIN = min(coord[1] for coord in matrix.keys())

print("{} {} {} {}".format(XMAX, XMIN, YMAX, YMIN))

plot = [[" "]  * (XMAX - XMIN + 1) for i in range(YMAX - YMIN + 1)]

# paint (0,0 white)
plot[- YMIN][-XMIN] = "O"

# paint each matrix element:
for key, val in sorted(matrix.items()):
    print(key)
    plot[- key[1] + YMAX][key[0] - XMIN] = (" " if val == b"0\n" else "O")

#print it
print(*(' '.join(row) for row in plot), sep='\n')


