#!/auto/ensoft/bin/python

with open('int_array5b.txt', 'r') as f:
    line = f.readline()
    int_array = [int(num) for num in line.split(",")]


i = 0
while (i <= len(int_array)):

    code = str(int_array[i])
    op_code = int(code[-2:])

    param_codes = [0,0,0]
    values = [0,0,0]
    for j in range(3):
        if len(code) >= j + 3:
            param_codes[j] = int(code[-3 - j])

    for val in range(3):
        if param_codes[val] == 0:
            if len(int_array) > i + 1 + val and \
               len(int_array) > int_array[i + 1 + val]:
                values[val] = int_array[int_array[i + 1 + val]]
        elif param_codes[val] == 1:
            if len(int_array) > i + 1 + val:
                values[val] = int_array[i + 1 + val]

    if op_code == 99:
        break
    elif op_code == 1:
        int_array[int_array[3 + i]] = values[0] + values[1]
        i = i + 4
    elif op_code == 2:
        int_array[int_array[3 + i]] = values[0] * values[1]
        i = i + 4
    elif op_code == 3:
        int_array[int_array[1 + i]] = int(input())
        i = i + 2
    elif op_code == 4:
        print(values[0])
        i = i + 2
    elif op_code == 5:
        if values[0] != 0:
            i = values[1]
        else:
            i = i + 3
    elif op_code == 6:
        if values[0] == 0:
            i = values[1]
        else:
            i = i + 3
    elif op_code == 7:
        if values[0] < values[1]:
            int_array[int_array[3 + i]] = 1
        else:
            int_array[int_array[3 + i]] = 0
        i = i + 4
    elif op_code == 8:
        if values[0] == values[1]:
            int_array[int_array[3 + i]] = 1
        else:
            int_array[int_array[3 + i]] = 0
        i = i + 4
    else:
        print("Unexpected array element " + str(op_code))
        print(int_array[:7])
        print(code)
        break

