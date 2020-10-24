#!/usr/bin/python

with open('2/int_array.txt', 'r') as f:
    line = f.readline()
    int_array_original = [int(num) for num in line.split(",")]


def find_val(input1, input2):
    int_array = int_array_original[:]
    int_array[1] = input1
    int_array[2] = input2
    i = 0
    while (i <= len(int_array)):

        if int_array[0 + i] == 99:
            break
        elif int_array[0 + i] == 1:
            result = int_array[int_array[1 + i]] + int_array[int_array[2 + i]]
            int_array[int_array[3 + i]] = result
        elif int_array[0 + i] == 2:
            result = int_array[int_array[1 + i]] * int_array[int_array[2 + i]]
            int_array[int_array[3 + i]] = result
        else:
            break

        i = i + 4

    return(int_array[0])

print(find_val(12, 2))

inputs = [i for i in range(100)]

for input1 in inputs:
    for input2 in inputs:
        if find_val(input1, input2) == 19690720:
            print("Found answer: " + str(input1) + " " + str(input2))
            print(str(100 * input1 + input2))

