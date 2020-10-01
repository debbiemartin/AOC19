#!/auto/ensoft/bin/python


class Intcode():

    def __init__(self, cb):
        self.cb = cb
        self.i = 0
        self.int_array = int_array[:]
        self.operate(None)

    def operate(self, input):
        print("run input: " + str(input))

        while (self.i <= len(self.int_array)):

            code = str(self.int_array[self.i])
            op_code = int(code[-2:])

            param_codes = [0,0,0]
            for j in range(3):
                if len(code) >= j + 3:
                    param_codes[j] = int(code[-3 - j])

            if op_code == 1 or op_code == 2 or op_code == 4:
                if param_codes[0] == 0:
                    value1 = self.int_array[self.int_array[self.i + 1]]
                elif param_codes[0] == 1:
                    value1 = self.int_array[self.i + 1]

            if op_code == 1 or op_code == 2:
                if param_codes[1] == 0:
                    value2 = self.int_array[self.int_array[self.i + 2]]
                elif param_codes[1] == 1:
                    value2 = self.int_array[self.i + 2]

            if op_code == 99:
                break
            elif op_code == 1:
                self.int_array[self.int_array[3 + self.i]] = value1 + value2
                self.i = self.i + 4
            elif op_code == 2:
                self.int_array[self.int_array[3 + self.i]] = value1 * value2
                self.i = self.i + 4
            elif op_code == 3:
                if input is not None:
                    self.int_array[self.int_array[1 + self.i]] = int(input)
                    self.i = self.i + 2
                    input = None
                else:
                    break
            elif op_code == 4:
                print("Output: " + str(value1))
                self.cb(value1)
                self.i = self.i + 2
            else:
                print("Unexpected array element " + str(op_code) + " code: " + code)
                print(self.int_array)
                break


def cb_a(output):
    b.operate(output)

def cb_b(output):
    c.operate(output)

def cb_c(output):
    d.operate(output)

def cb_d(output):
    e.operate(output)

def cb_e(output):
    print(output)

with open('int_array3.txt', 'r') as f:
    line = f.readline()
    int_array = [int(num) for num in line.split(",")]


#@@@ DGM improve with arrays
a = Intcode(cb_a)
b = Intcode(cb_b)
c = Intcode(cb_c)
d = Intcode(cb_d)
e = Intcode(cb_e)

a.operate(1)
b.operate(0)
c.operate(4)
d.operate(3)
e.operate(2)


# Initial input for amp a is 0
a.operate(0)

