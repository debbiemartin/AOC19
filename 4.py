#!/auto/ensoft/bin/python

def n_qualifies(number):
    list = []

    for i in range(6):
        number_str = str(number)
        list.append(int(number_str[i]))
   
    qualifies = False
    for i in range(5):
        if list[i] == list[i + 1]:
            qualifies = True

    if qualifies:
        for i in range(5):
            if list[i + 1] < list[i]:
                qualifies = False

    return qualifies


count = 0

for i in range(146810, 612565):
    if n_qualifies(i):
        count += 1

print(count)
