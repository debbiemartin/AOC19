#!/auto/ensoft/bin/python3

WIDTH=25
HEIGHT=6

def count_occurrences(layer, num):
    count = 0
    for row in layer:
        count += row.count(num)
    return count

with open("image.txt", 'r') as file:
    data = file.readline()

layercount = int(len(data)/(WIDTH*HEIGHT))

# create layers matrix
layers=[]
for layernum in range(layercount):
    layer = []
    for rownum in range(HEIGHT):
        row = []
        for colnum in range(WIDTH):
            row.append(int(data[layernum*HEIGHT*WIDTH + rownum*WIDTH + colnum]))
        layer.append(row)
    layers.append(layer)

# find layer with fewest 0 digits
min_zeros = 0
for layer in layers:
    # count 0 digits
    zeros = count_occurrences(layer, 0)
    if zeros < min_zeros or min_zeros == 0:
        min_zeros = zeros
        answer = count_occurrences(layer, 1) * count_occurrences(layer, 2)

print(answer)
