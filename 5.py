#!/auto/ensoft/bin/python

with open('int_array2.txt', 'r') as f:
    line = f.readline()
    int_array = [int(num) for num in line.split(",")]

#int_array[1] = 12
#int_array[2] = 2

i = 0
while (i <= len(int_array)): 

    code = str(int_array[i])
    op_code = int(code[-2:])

    param_codes = [0,0,0]
    for j in range(3):
        if len(code) >= j + 3:
            param_codes[j] = int(code[-3 - j])

    if op_code == 1 or op_code == 2 or op_code == 4:
        if param_codes[0] == 0:
            value1 = int_array[int_array[i + 1]]
        elif param_codes[0] == 1:
            value1 = int_array[i + 1]

    if op_code == 1 or op_code == 2:
        if param_codes[1] == 0:
            value2 = int_array[int_array[i + 2]]
        elif param_codes[1] == 1:
            value2 = int_array[i + 2]
    

    if op_code == 99:
        break
    elif op_code == 1:
        int_array[int_array[3 + i]] = value1 + value2
        i = i + 4
    elif op_code == 2:
        int_array[int_array[3 + i]] = value1 * value2
        i = i + 4
    elif op_code == 3:
        int_array[int_array[1 + i]] = int(input())
        i = i + 2
    elif op_code == 4:
        print(value1)
        i = i + 2 
    else:
        print("Unexpected array element " + str(op_code))
        print(int_array[:7])
        print(code)
        print(i)
        break

