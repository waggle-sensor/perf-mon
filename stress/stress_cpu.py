from subprocess import Popen

class StressCPU:
    def __init__(self, num_cores, percentage, time):
        self.num_cores = num_cores
        self.percentage = percentage
        self.time = time

    def stress(self):
        """
        Run stress-ng with the given parameters
        """
        command = "stress-ng --cpu {} -l {} --timeout".format(self.num_cores, self.percentage, self.time).split(' ')

        # return proc for waiting
        return Popen(command).pid
