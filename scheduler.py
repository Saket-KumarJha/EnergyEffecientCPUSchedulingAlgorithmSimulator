from dvfs import DVFSController
from predictor import BurstPredictor


class EnergyAwareScheduler:
    """
    Energy-Efficient CPU Scheduling Algorithm
    ==========================================
    Combines three key techniques:

    1. EDF  — Earliest Deadline First ordering
               Proven optimal for real-time scheduling.

    2. DVFS — Dynamic Voltage & Frequency Scaling
               Assigns minimum required frequency per process type.
               Lower freq = lower voltage = power drops cubically.

    3. C-State Management
               CPU enters deep sleep during idle gaps between processes.
               Saves up to 90% power vs staying active (C6 state).

    Additionally uses a Burst Predictor to estimate burst times
    for proactive frequency assignment before a process starts.
    """

    MAX_FREQ = 2400   # MHz — reference for execution time scaling

    def __init__(self, processes):
        # Sort by deadline (EDF)
        self.processes    = sorted(processes, key=lambda p: p.deadline)
        self.dvfs         = DVFSController()
        self.predictor    = BurstPredictor(alpha=0.5)
        self.current_time = 0.0
        self.total_energy = 0.0
        self.idle_energy  = 0.0
        self.active_energy= 0.0
        self.log          = []    # Per-process detailed log
        self.timeline     = []    # For Gantt chart

    # ── Internal helpers ────────────────────────────────────────────────
    def _handle_idle(self, idle_ms):
        """Put CPU into deepest available sleep state during idle gap."""
        if idle_ms <= 0:
            return
        state  = self.dvfs.get_sleep_state(idle_ms)
        energy = self.dvfs.calculate_energy(state['power'], idle_ms)
        self.idle_energy  += energy
        self.total_energy += energy
        self.timeline.append({
            'label': 'IDLE',
            'start': round(self.current_time, 2),
            'end':   round(self.current_time + idle_ms, 2),
            'type':  'idle',
            'freq':  0,
        })

    def _type_color(self, ptype):
        return {'realtime':'#ff4757','cpu_bound':'#00d4ff',
                'io_bound':'#00ff88','background':'#a855f7'}.get(ptype,'#888')

    # ── Main simulation ─────────────────────────────────────────────────
    def run(self):
        W = 65
        print("\n" + "=" * W)
        print("   ENERGY-EFFICIENT CPU SCHEDULING SIMULATION")
        print("   Algorithm: EDF + DVFS + C-State Sleep Management")
        print("=" * W)
        print(f"{'PID':<5} {'Type':<13} {'Freq':<10} {'Exec(ms)':<10} "
              f"{'Energy(J)':<11} {'TAT(ms)':<10} {'Deadline'}")
        print("─" * W)

        for process in self.processes:

            # ── Handle idle gap before this process ──────────────────
            if process.arrival_time > self.current_time:
                idle_ms = process.arrival_time - self.current_time
                self._handle_idle(idle_ms)
                self.current_time = process.arrival_time

            # ── DVFS: assign frequency for this process type ─────────
            freq_info = self.dvfs.get_frequency(process)
            process.frequency_used = freq_info['freq']

            # ── Burst predictor (for proactive freq setting) ─────────
            predicted = self.predictor.predict(process.pid, process.burst_time)
            self.predictor.update(process.pid, process.burst_time)

            # ── Execution time (slower freq = longer wall-clock time) ─
            exec_time = process.burst_time * (self.MAX_FREQ / freq_info['freq'])
            process.actual_exec_time = exec_time

            # ── Energy for this process ──────────────────────────────
            energy = self.dvfs.calculate_energy(freq_info['power'], exec_time)
            process.energy_consumed = energy
            self.active_energy += energy
            self.total_energy  += energy

            # ── Timing metrics ───────────────────────────────────────
            start_time               = self.current_time
            process.completion_time  = self.current_time + exec_time
            process.turnaround_time  = process.completion_time - process.arrival_time
            process.waiting_time     = max(0, self.current_time - process.arrival_time)
            process.deadline_met     = process.completion_time <= process.deadline
            self.current_time        = process.completion_time

            # ── Gantt timeline entry ─────────────────────────────────
            self.timeline.append({
                'label': f'P{process.pid}',
                'start': round(start_time, 2),
                'end':   round(process.completion_time, 2),
                'type':  process.process_type,
                'freq':  freq_info['freq'],
                'color': self._type_color(process.process_type),
            })

            # ── Log entry ────────────────────────────────────────────
            self.log.append({
                'pid':            process.pid,
                'type':           process.process_type,
                'freq_mhz':       freq_info['freq'],
                'power_w':        freq_info['power'],
                'burst_ms':       process.burst_time,
                'exec_ms':        round(exec_time, 2),
                'energy_j':       round(energy, 5),
                'waiting_ms':     round(process.waiting_time, 2),
                'turnaround_ms':  round(process.turnaround_time, 2),
                'deadline_ms':    process.deadline,
                'completion_ms':  round(process.completion_time, 2),
                'deadline_met':   process.deadline_met,
                'predicted_burst':round(predicted, 2),
            })

            status = "✅ MET" if process.deadline_met else "❌ MISS"
            print(f"P{process.pid:<4} {process.process_type:<13} "
                  f"{freq_info['freq']:<10} {exec_time:<10.1f} "
                  f"{energy:<11.5f} {process.turnaround_time:<10.1f} {status}")

        print("─" * W)
        print(f"\n{'Total Energy (Your Algo)':<30}: {self.total_energy:.5f} J")
        print(f"{'  Active Execution Energy':<30}: {self.active_energy:.5f} J")
        print(f"{'  Idle/Sleep State Energy':<30}: {self.idle_energy:.5f} J")

    # ── Summary metrics ─────────────────────────────────────────────────
    def get_metrics(self):
        procs = self.processes
        n     = len(procs)
        met   = sum(1 for p in procs if p.deadline_met)
        return {
            'total_energy_j':     round(self.total_energy,  5),
            'active_energy_j':    round(self.active_energy, 5),
            'idle_energy_j':      round(self.idle_energy,   5),
            'avg_turnaround_ms':  round(sum(p.turnaround_time for p in procs) / n, 2),
            'avg_waiting_ms':     round(sum(p.waiting_time   for p in procs) / n, 2),
            'deadlines_met':      met,
            'deadlines_missed':   n - met,
            'total_processes':    n,
            'deadline_miss_rate': round((n - met) / n * 100, 2),
        }
