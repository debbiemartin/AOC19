#!/usr/bin/python3

import sys
sys.path.insert(1, '19/')

import intcode
from collections import deque
import threading

class Computer(object):
    def __init__(self, net_addr, send_packet):
        print(f"starting intcomp {net_addr}")
        self.intcomp = intcode.IntComp("23/intcode_instructions.txt")
        self.net_addr = net_addr
        self.send_packet = send_packet
        self.pack_queue = deque()
        self.pack_queue_lock = threading.Lock()

    def start(self):
        self.stopthread = False
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.start()
    
    def stop(self):
        self.stopthread = True
    
    def run(self):
        # requests its net_addr via input
        self.intcomp.start()
        self.intcomp.input(self.net_addr)
        
        while not self.stopthread:           
            if self.intcomp.output_done():
                # Process received packets via input instructions. 
                # Need the lock for reading/writing the packet queue, but don't
                # do long intcode operations while holding it
                self.pack_queue_lock.acquire()
                if len(self.pack_queue) == 0:
                    input_arr = [-1]
                else:
                    x, y = self.pack_queue.popleft()
                    input_arr = [x, y]
                self.pack_queue_lock.release()
                
                for input_elem in input_arr:
                    self.intcomp.input(input_elem)
            else:
                # Send packets learned via output instructions
                n = self.intcomp.output()
                x = self.intcomp.output()
                y = self.intcomp.output()
                self.send_packet(n, x, y)
        
        self.intcomp.stop()
        
    def receive_packet(self, x, y):
        self.pack_queue_lock.acquire()
        self.pack_queue.append((x, y))
        self.pack_queue_lock.release()

        
class Network(object):
    def __init__(self, size):
        self.computers = []
        for i in range(size):
            self.computers.append(Computer(i, self.send_packet))
        
        for computer in self.computers:
            computer.start()

    def send_packet(self, n, x, y):
        if n < 0 or n >= len(self.computers):
            print(f"attempted to send x {x} y {y} to address {n}")
            if n == 255:
                print("Finished!!!")
                for computer in self.computers:
                    computer.stop()
            return
        self.computers[n].receive_packet(x, y)
            

n = Network(50)