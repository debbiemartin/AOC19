#!/usr/bin/python3

import sys
sys.path.insert(1, '19/')

import intcode
from collections import deque
import threading
class Computer(object):
    def __init__(self, net_addr, send_packet):
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
                    self.idle = True
                else:
                    print(f"popping from queue computer {self.net_addr}")
                    x, y = self.pack_queue.popleft()
                    input_arr = [x, y]
                    self.idle = False
                self.pack_queue_lock.release()
                
                for input_elem in input_arr:
                    self.intcomp.input(input_elem)
            elif self.intcomp.output_ready():
                print(f"getting output computer {self.net_addr}")
                # Send packets learned via output instructions
                n = self.intcomp.output()
                x = self.intcomp.output()
                y = self.intcomp.output()
                self.send_packet(n, x, y)
                self.idle = False
        
        self.intcomp.stop()
        
    def receive_packet(self, x, y):
        self.pack_queue_lock.acquire()
        print(f"computer {self.net_addr} received packet ({x}, {y})")
        self.pack_queue.append((x, y))
        self.pack_queue_lock.release()
    
    def is_idle(self):
        return self.idle

class NAT(object):
    def __init__(self, computers):
        self.packet = None
        self.last_y = None
        self.computers = computers
        self.pack_receive = threading.Event()
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.start()
    
    def run(self):
        # Monitor for whether comps are idle
        while True:
            self.pack_receive.wait()
            print(f"None idle computers: {list([i for i in range(50) if not self.computers[i].is_idle()])}")
            if all(computer.is_idle() for computer in self.computers):
                print("NAT has detected that all computers are idle")
                self.computers[0].receive_packet(self.packet[0], self.packet[1])
                self.pack_receive.clear()
                if self.packet[1] == self.last_y:
                    print(f"NAT sent y value {self.last_y} twice")
                    for computer in self.computers:
                        computer.stop()
                    return
                self.last_y = self.packet[1]

    def receive_packet(self, x, y):
        print(f"NAT received packet ({x}, {y})")
        self.packet = (x, y)
        if not self.pack_receive.is_set():
            print("setting the pack receive")
            self.pack_receive.set()
    
class Network(object):
    def __init__(self, size):
        self.computers = []
        for i in range(size):
            self.computers.append(Computer(i, self.send_packet))
        
        for computer in self.computers:
            computer.start()
        
        self.nat = NAT(self.computers)
        
    def send_packet(self, n, x, y):
        print(f"sending packet ({x}, {y}) to {n}")
        if n < 0 or n >= len(self.computers):
            if n == 255:
                self.nat.receive_packet(x, y)
            return
        self.computers[n].receive_packet(x, y)
            

n = Network(50)