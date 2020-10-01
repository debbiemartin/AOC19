#!/auto/ensoft/bin/python


class Intcode():

    def __init__(self, cb, phase):
        self.cb = cb
        self.i = 0
        self.int_array = int_array[:]
        self.phase = phase

    def operate(self, phase, input): #@@@ could we change this to actually just run ./5.py
        print("run input: " + str(input))

        while (self.i <= len(self.int_array)):

            self.code = str(self.int_array[self.i])
            self.op_code = int(self.code[-2:])

            self.param_codes = [0,0,0]
            self.values = [0,0,0]
            for self.j in range(3):
                if len(self.code) >= self.j + 3:
                self.param_codes[j] = int(self.code[-3 - self.j])

            for self.val in range(3):
                if self.param_codes[val] == 0:
                    if len(self.int_array) > self.i + 1 + self.val and \
                       len(self.int_array) > self.int_array[self.i + 1 + self.val]:
                        self.values[val] = self.int_array[self.int_array[self.i + 1 + self.val]]
                elif self.param_codes[self.val] == 1:
                    if len(self.int_array) > i + 1 + self.val:
                        self.values[self.val] = self.int_array[self.i + 1 + self.val]

            if self.op_code == 99:
                break
            elif self.op_code == 1:
                self.int_array[self.int_array[3 + self.i]] = self.values[0] + self.values[1]
                self.i += 4
            elif self.op_code == 2:
                self.int_array[self.int_array[3 + self.i]] = self.values[0] * self.values[1]
                self.i += 4
            elif self.op_code == 3:
                self.int_array[self.int_array[1 + self.i]] = #@@@ look at phase and input here
                self.i += 2
            elif self.op_code == 4:
                print(self.values[0]) #@@@ call callback function
                self.i += 2
            elif self.op_code == 5:
                if self.values[0] != 0:
                    self.i = self.values[1]
                else:
                    self.i += 3
            elif self.op_code == 6:
                if self.values[0] == 0:
                    self.i = self.values[1]
                else:
                    self.i += 3
            elif self.op_code == 7:
                if self.values[0] < self.values[1]:
                    self.int_array[self.int_array[3 + self.i]] = 1
                else:
                    self.int_array[self.int_array[3 + self.i]] = 0
                self.i += 4
            elif self.op_code == 8:
                if self.values[0] == self.values[1]:
                    self.int_array[self.int_array[3 + self.i]] = 1
                else:
                    self.int_array[self.int_array[3 + self.i]] = 0
                self.i += 4
            else:
                print("Unexpected array element " + str(self.op_code))
                print(self.int_array[:7])
                print(self.code)
                break

with open('int_array7.txt', 'r') as f:
    line = f.readline()
    int_array = [int(num) for num in line.split(",")]

phases = [0,1,2,3,4]

a = Intcode(b.operate, phases[0])
b = Intcode(c.operate, phases[1])
c = Intcode(d.operate, phases[2])
d = Intcode(e.operate, phases[3])
e = Intcode(print(), phases[4])


a.operate()
