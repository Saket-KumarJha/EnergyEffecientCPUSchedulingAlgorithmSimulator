class Process:
    """
    Represents a CPU process in the simulation.
    Each process has timing attributes, a type, and results filled after scheduling.
    """
    def __init__(self, pid, burst_time, priority, deadline, process_type, arrival_time=0):
        # Input attributes
        self.pid          = pid
        self.burst_time   = burst_time        # CPU time needed (ms)
        self.priority     = priority          # 1=Critical, 2=Normal, 3=Background
        self.deadline     = deadline          # Must complete by this time (ms)
        self.process_type = process_type      # 'realtime' | 'cpu_bound' | 'io_bound' | 'background'
        self.arrival_time = arrival_time      # When process enters the queue (ms)

        # Result attributes (filled after scheduling)
        self.completion_time  = 0
        self.waiting_time     = 0
        self.turnaround_time  = 0
        self.energy_consumed  = 0.0
        self.frequency_used   = 0
        self.actual_exec_time = 0.0
        self.deadline_met     = False

    def __repr__(self):
        return (f"Process(pid={self.pid}, type={self.process_type}, "
                f"burst={self.burst_time}ms, deadline={self.deadline}ms, "
                f"arrival={self.arrival_time}ms)")
