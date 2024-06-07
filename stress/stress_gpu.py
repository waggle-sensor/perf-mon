import os

class StressGPU:
    def __init__(self, percentage, time):
        self.percentage = percentage
        self.time = time

    def stress(self):
        """
        Run gpu_burn with the given parameters
        """
        command = "gpu_burn -d -tc -m {}% {}".format(self.percentage, self.time)
        os.system(command)