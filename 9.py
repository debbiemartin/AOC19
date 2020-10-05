#!/auto/ensoft/bin/python3

from collections import defaultdict

RELATIVE_BASE=0

with open('13/instructions.txt', 'r') as f: #@@@ changed for 13
    line = f.readline()
    int_array_temp = [int(num) for num in line.split(",")]

#convert to defaultdict
int_array = defaultdict(lambda: 0)
for i in range(len(int_array_temp)):
    int_array[i] = int_array_temp[i]

i = 0
while (True):

    code = str(int_array[i])
    op_code = int(code[-2:])

    param_codes = [0,0,0]
    values = [0,0,0]
    for j in range(3):
        if len(code) >= j + 3:
            param_codes[j] = int(code[-3 - j])

    for val in range(3):
        if param_codes[val] == 0:
            # Position mode
            values[val] = int_array[i + 1 + val]
        elif param_codes[val] == 1:
            # Immediate mode
            values[val] = i + 1 + val
        elif param_codes[val] == 2:
            # Relative mode
            values[val] = RELATIVE_BASE + int_array[i + 1 + val]

    if op_code == 99:
        break
    elif op_code == 1:
        int_array[values[2]] = int_array[values[0]] + int_array[values[1]]
        i = i + 4
    elif op_code == 2:
        int_array[values[2]] = int_array[values[0]] * int_array[values[1]]
        i = i + 4
    elif op_code == 3:
        int_array[values[0]] = int(input())
        i = i + 2
    elif op_code == 4:
        print(int_array[values[0]])
        i = i + 2
    elif op_code == 5:
        if int_array[values[0]] != 0:
            i = int_array[values[1]]
        else:
            i = i + 3
    elif op_code == 6:
        if int_array[values[0]] == 0:
            i = int_array[values[1]]
        else:
            i = i + 3
    elif op_code == 7:
        if int_array[values[0]] < int_array[values[1]]:
            int_array[values[2]] = 1
        else:
            int_array[values[2]] = 0
        i = i + 4
    elif op_code == 8:
        if int_array[values[0]] == int_array[values[1]]:
            int_array[values[2]] = 1
        else:
            int_array[values[2]] = 0
        i = i + 4
    elif op_code == 9:
        RELATIVE_BASE += int_array[values[0]]
        i += 2
    else:
        print("Unexpected array element " + str(op_code))
        print(int_array[:7])
        print(code)
        break

