#!/auto/ensoft/bin/python

with open('int_array.txt', 'r') as f:
    line = f.readline()
    int_array = [int(num) for num in line.split(",")]

print(int_array)
print(len(int_array))

int_array[1] = 12
int_array[2] = 2

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
        print("Unexpected array element")
        break

    i = i + 4

print(int_array)
