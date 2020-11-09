#!/usr/bin/python3

import sys
sys.path.insert(1, '19/')

import intcode

class SpringDroid(object):
    def __init__(self, txt):
        with open(txt) as f:
            self.lines = f.readlines()
        self.intcomp = intcode.IntComp("21/intcode_instructions.txt")

    def print_output(self):
        while not self.intcomp.output_done():
            output = self.intcomp.output()
            if output > 137:
                print(f"Big number: {output}")
            else:
                print(chr(output), end="")

    def run(self):
        self.intcomp.start()
        # prompt
        self.print_output()
        for line in self.lines:
            for char in line:
                self.intcomp.input(ord(char))

        # result
        self.print_output()
        self.intcomp.stop()
        

droid = SpringDroid("21/springscript_walk.txt")
print("PART 1:")
droid.run()
        
droid = SpringDroid("21/springscript_run.txt")  
print("PART 2:")
droid.run()
        
