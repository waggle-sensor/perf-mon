import random
import stress_cpu
import stress_gpu
import os

class Resource:
    def __init__(self, num_cores, max_stress, min_gpu_timeout, max_gpu_timeout):
        self.cpu_cores = random.randrange(num_cores)
        self.cpu_stress = random.randrange(max_stress)
        self.gpu_stress_timeout = random.random() * (max_gpu_timeout - min_gpu_timeout) + min_gpu_timeout

class ProgramSim:
    def __init__(self, max_num_programs, max_seconds, num_cores, max_stress, max_gpu_timeout, min_gpu_timeout):
        random.seed()
        self.number = random.randrange(1, max_num_programs)
        max_time = max_seconds / self.number
        self.times = [random.random() * max_time for _ in range(self.number)]
        self.resources = [Resource(num_cores, max_stress, max_gpu_timeout, min_gpu_timeout) for _ in range(self.number)]

    def simulate(self):
        for i in range(self.number):
            r = self.resources[i]
            t = self.times[i]
            
            # start stressing
            pids = [
                stress_cpu.StressCPU(r.cpu_cores, r.cpu_stress, t).stress(), 
                stress_gpu.StressGPU(r.gpu_stress_timeout, t, 16 * 1024 ** 2).stress()
            ]

            # wait until processes end
            for pid in pids:
                os.waitid(pid)


if __name__ == "main":
    ProgramSim(5, 10, 6, 80, 0.01, 0.01).simulate()
