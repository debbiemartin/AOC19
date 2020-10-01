#!/auto/ensoft/bin/python

def n_qualifies(number):
    list = []

    for i in range(6):
        number_str = str(number)
        list.append(int(number_str[i]))

    for i in range(5):
        if list[i + 1] < list[i]:
            return False

    for i in range(5):
        if (list[i] == list[i + 1]) and ((i == 4) or (list[i] != list[i + 2])) \
            and ((i == 0) or (list[i] != list[i - 1])):
            return True

    return False

count = 0

for i in range(146810, 612565):
    if n_qualifies(i):
        count += 1

print(count)
