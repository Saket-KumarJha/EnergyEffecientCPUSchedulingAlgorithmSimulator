from dvfs import DVFSController


class EnergyMonitor:
    """
    Compares the energy consumption of your EDF+DVFS algorithm
    against three traditional CPU scheduling algorithms.

    Traditional algorithms always run at maximum frequency (2400 MHz, 4.0W)
    with no awareness of process types, deadlines, or power states.

    This class quantifies how much energy your algorithm saves.
    """

    def __init__(self):
        self.dvfs      = DVFSController()
        self.max_power = self.dvfs.FREQ_LEVELS['high']['power']   # 4.0 W

    def simulate_round_robin(self, processes, overhead_pct=0.10):
        """
        Round Robin: fixed time quantum, max frequency always.
        Context switching overhead adds ~10% extra execution time.
        """
        energy = 0.0
        for p in processes:
            exec_time = p.burst_time * (1 + overhead_pct)
            energy += self.dvfs.calculate_energy(self.max_power, exec_time)
        return round(energy, 5)

    def simulate_priority_scheduling(self, processes):
        """Priority Scheduling: ordered by priority, always max frequency."""
        energy = 0.0
        for p in processes:
            energy += self.dvfs.calculate_energy(self.max_power, p.burst_time)
        return round(energy, 5)

    def simulate_fcfs(self, processes):
        """FCFS: First Come First Served, always max frequency."""
        energy = 0.0
        for p in processes:
            energy += self.dvfs.calculate_energy(self.max_power, p.burst_time)
        return round(energy, 5)

    def energy_savings_pct(self, your_energy, baseline_energy):
        if baseline_energy == 0:
            return 0.0
        return round((baseline_energy - your_energy) / baseline_energy * 100, 2)

    def full_report(self, your_energy, processes):
        """Print a full energy comparison report and return data dict."""
        rr    = self.simulate_round_robin(processes)
        ps    = self.simulate_priority_scheduling(processes)
        fcfs  = self.simulate_fcfs(processes)

        W = 60
        print("\n" + "=" * W)
        print("       ENERGY COMPARISON REPORT")
        print("=" * W)
        print(f"{'Algorithm':<32} {'Energy (J)':<14} {'Savings'}")
        print("─" * W)
        print(f"{'Your Algorithm  (EDF + DVFS)':<32} {your_energy:<14} {'← baseline'}")
        print(f"{'Round Robin':<32} {rr:<14} {self.energy_savings_pct(your_energy,rr)}% more efficient")
        print(f"{'Priority Scheduling':<32} {ps:<14} {self.energy_savings_pct(your_energy,ps)}% more efficient")
        print(f"{'FCFS':<32} {fcfs:<14} {self.energy_savings_pct(your_energy,fcfs)}% more efficient")
        print("=" * W)

        return {
            'your_algo':  your_energy,
            'round_robin':rr,
            'priority':   ps,
            'fcfs':       fcfs,
            'savings_vs_rr': self.energy_savings_pct(your_energy, rr),
            'savings_vs_ps': self.energy_savings_pct(your_energy, ps),
        }
