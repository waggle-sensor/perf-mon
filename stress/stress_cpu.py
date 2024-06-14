from subprocess import Popen

"""
Simple script that stresses CPU using stress-ng
"""
class StressCPU:
    def __init__(self, num_cores, percentage, time):
        """
        Initializes a StressCPU instance

        num_cores: the number of coures to stress
        percentage: the cpu utilization to stress at
        time: the total length of time that we want to stress for
        """
        self.num_cores = num_cores
        self.percentage = percentage
        self.time = time

    def stress(self):
        """
        Stresses the CPU using stress-ng
        """
        command = "stress-ng --cpu {} -l {} --timeout {}".format(self.num_cores, self.percentage, self.time).split(' ')

        # return pid for waiting
        return Popen(command).pid
