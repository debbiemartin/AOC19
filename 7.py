#!/auto/ensoft/bin/python3

from subprocess import Popen, PIPE, STDOUT
import time

MAXIMUM=0
class Intcode():
    def __init__(self, cb, phase):
        self.cb = cb
        self.phase = phase

    def operate(self, input):
        p = Popen(['./5.py'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        phasestr = str(self.phase) + "\n"
        p.stdin.write(phasestr.encode('utf-8'))
        stdout, stderr = p.communicate(input=input)
        self.cb(stdout)

def phase_answer(input):
    global MAXIMUM
    #print("Output from E is: {}".format(input.decode('utf-8')))
    if int(input.decode('utf-8')) > MAXIMUM:
        MAXIMUM = int(input.decode('utf-8'))

def test_permutation(phases):
    e = Intcode(phase_answer, phases[4])
    d = Intcode(e.operate, phases[3])
    c = Intcode(d.operate, phases[2])
    b = Intcode(c.operate, phases[1])
    a = Intcode(b.operate, phases[0])

    a.operate("0\n".encode('utf-8'))

def test_phase(phases, index):
    if index < 4:
        for i in range(5):
            if not any(i == phases[j] for j in range(index + 1)):
                phases[index + 1] = i
                test_phase(phases, index + 1)
    elif index == 4:
        # All filled in - test permutation
        test_permutation(phases)

for i in range(5):
    test_phase([i,0,0,0,0], 0)

print("Maximum found: {}".format(MAXIMUM))
