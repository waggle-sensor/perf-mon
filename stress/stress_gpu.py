import torch
import time
import os
import sys

"""
Simple torch script that stresses the GPU using matrix multiplication
with CUDA
"""
class StressGPU:
    def __init__(self, gpu_timeout, time, size):
        """
        Initializes a StressGPU instance
        
        gpu_timeout: the timeout between each matrix multiplication. THis is
            used to vary the stress placed on the GPU
        time: the total length of time that we want to stress for
        size: the size of the matrix that we are multiplying
        """
        self.gpu_timeout = gpu_timeout
        self.time = time
        self.size = size

    def stress(self):
        """
        Stresses the GPU with the given parameters
        """
        pid = os.fork()
        if pid > 0:
            return pid
        
        # child process computes matrix multiplication for 
        # the specified time and then exits
        x = torch.linspace(0, 4, self.size).cuda()
        timeout = time.time() + self.time

        while time.time() < timeout:
            x = x * (1.0 - x)
            time.sleep(self.gpu_timeout)
                
        sys.exit(os.EX_OK)

