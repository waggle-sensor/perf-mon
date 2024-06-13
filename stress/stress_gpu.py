import torch
import time
import os
import sys

class StressGPU:
    def __init__(self, gpu_timeout, time, size):
        self.gpu_timeout = gpu_timeout
        self.time = time
        self.size = size

    def stress(self):
        pid = os.fork()
        if pid > 0:
            return pid
        
        # child process computes matrix multiplication
        x = torch.linspace(0, 4, self.size).cuda()
        timeout = time.time() + self.time

        while True:
            x = x * (1.0 - x)
            time.sleep(self.gpu_timeout)
            if time.time() > timeout:
                sys.exit(os.EX_OK)

