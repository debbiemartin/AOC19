#!/usr/bin/python3

from collections import defaultdict
import sys
import copy
import threading

class IntComp(object):
    def __init__(self, txtfile):

        with open(txtfile, 'r') as f:
            line = f.readline()
            self.int_array = {i:int(num) for i, num in enumerate(line.split(","))}

        self.events = {}
        for key in ["input_write", "input_read", "output_write", "output_read"]:
            self.events[key] = threading.Event()

    def run(self):
        int_array = defaultdict(lambda: 0, self.int_array.items())
        
        i = 0
        relative_base = 0
        while (True):
            code = str(int_array[i])
            op_code = int(code[-2:])
        
            param_codes = [0,0,0]
            values = [0,0,0]
            for j in range(3):
                if len(code) >= j + 3:
                    param_codes[j] = int(code[-3 - j])
        
            for val in range(3):
                if param_codes[val] == 0:
                    # Position mode
                    values[val] = int_array[i + 1 + val]
                elif param_codes[val] == 1:
                    # Immediate mode
                    values[val] = i + 1 + val
                elif param_codes[val] == 2:
                    # Relative mode
                    values[val] = relative_base + int_array[i + 1 + val]
        
            if op_code == 99:
                break
            elif op_code == 1:
                int_array[values[2]] = int_array[values[0]] + int_array[values[1]]
                i = i + 4
            elif op_code == 2:
                int_array[values[2]] = int_array[values[0]] * int_array[values[1]]
                i = i + 4
            elif op_code == 3:
                self.events["input_write"].wait()
                self.events["input_write"].clear()
                int_array[values[0]] = self.input_val
                self.events["input_read"].set()
                i = i + 2
            elif op_code == 4:
                assert(not self.events["output_write"].set())
                self.events["output_write"].set()
                self.output_val = int_array[values[0]]
                self.events["output_read"].wait()
                self.events["output_read"].clear()
                i = i + 2
            elif op_code == 5:
                if int_array[values[0]] != 0:
                    i = int_array[values[1]]
                else:
                    i = i + 3
            elif op_code == 6:
                if int_array[values[0]] == 0:
                    i = int_array[values[1]]
                else:
                    i = i + 3
            elif op_code == 7:
                if int_array[values[0]] < int_array[values[1]]:
                    int_array[values[2]] = 1
                else:
                    int_array[values[2]] = 0
                i = i + 4
            elif op_code == 8:
                if int_array[values[0]] == int_array[values[1]]:
                    int_array[values[2]] = 1
                else:
                    int_array[values[2]] = 0
                i = i + 4
            elif op_code == 9:
                relative_base += int_array[values[0]]
                i += 2
            else:
                assert(False)
    
    def start(self):
        x = threading.Thread(target=self.run, args=())
        x.start()
    
    def input(self, number):
        assert(not self.events["input_write"].is_set())
        self.events["input_write"].set()
        self.input_val = number
        self.events["input_read"].wait()
        self.events["input_read"].clear()
    
    def output(self):
        self.events["output_write"].wait()
        self.events["output_write"].clear()
        rc, self.ouput_val = self.output_val, None
        self.events["output_read"].set()       

        return rc
        
    
intcomp = IntComp("19/int_array9.txt")
intcomp.start()
intcomp.input(1)
intcomp.input(1)
print(intcomp.output())

        
