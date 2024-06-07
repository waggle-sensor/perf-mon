import random
import time
import stress_cpu
import stress_gpu

class Resource:
    def __init__(self, num_cores, max_stress):
        self.cpu_cores = random.randrange(num_cores)
        self.cpu_stress = random.randrange(max_stress)
        self.gpu_stress = random.randrange(max_stress)

class ProgramSim:
    def __init__(self, max_num_programs, max_seconds):
        random.seed()
        self.number = random.randrange(1, max_num_programs)
        max_time = max_seconds / self.number
        self.times = [random.random() * max_time for _ in range(self.number)]
        self.resources = [Resource() for _ in range(self.number)]

    def simulate(self):
        for i in range(self.number):
            r = self.resources[i]
            t = self.times[i]
            
            # start 
            stress_cpu.StressCPU(r.cpu_cores, r.cpu_stress, t).stress()
            stress_gpu.StressGPU(r.gpu_stress, t).stress()

            # sleep and continue
            time.sleep(self.times[i])

            # ensure that gpu and cpu are done being stressed


if __name__ == "main":
    ProgramSim(5, 10).simulate()
