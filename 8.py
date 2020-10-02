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
layers = []
for layernum in range(layercount):
    layer = []
    for rownum in range(HEIGHT):
        row = []
        for colnum in range(WIDTH):
            row.append(int(data[layernum*HEIGHT*WIDTH + rownum*WIDTH + colnum]))
        layer.append(row)
    layers.append(layer)

# add each element through the layers in following:
#   if 0 hit first then black
#   if 1 hit first then white
image = []
for rownum in range(HEIGHT):
    row = []
    for colnum in range(WIDTH):
        for layer in layers:
            if layer[rownum][colnum] == 0:
                row.append(' ')
                break
            elif layer[rownum][colnum] == 1:
                row.append('O')
                break
        else:
            print("didnt find non-transparent")
    image.append(row)

print(print(*(' '.join(row) for row in image), sep='\n'))
