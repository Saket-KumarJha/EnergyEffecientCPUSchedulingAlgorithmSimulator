class DVFSController:
    """
    Dynamic Voltage and Frequency Scaling (DVFS) Controller.

    Maps each process type to the minimum frequency/voltage level needed.
    Uses the physics formula:  P = C * V^2 * f
    By reducing frequency, voltage also drops — power falls cubically.

    Frequency Levels:
      High   : 2400 MHz, 1.2V, 4.0W  → Real-time tasks (strict deadlines)
      Medium : 1200 MHz, 1.0V, 1.5W  → CPU-bound tasks (heavy computation)
      Low    :  600 MHz, 0.8V, 0.5W  → I/O-bound & Background tasks

    CPU Sleep States (C-States for idle periods):
      C1 (Halt)        : ~0.5W, wakes in ~1 µs
      C2 (Stop-Clock)  : ~0.2W, wakes in ~10 µs
      C6 (Deep Sleep)  : ~0.05W, wakes in ~200 µs
    """

    FREQ_LEVELS = {
        'high':   {'freq': 2400, 'voltage': 1.2, 'power': 4.0},
        'medium': {'freq': 1200, 'voltage': 1.0, 'power': 1.5},
        'low':    {'freq': 600,  'voltage': 0.8, 'power': 0.5},
    }

    SLEEP_STATES = {
        'C1': {'min_idle_ms': 0,  'power': 0.50},
        'C2': {'min_idle_ms': 10, 'power': 0.20},
        'C6': {'min_idle_ms': 50, 'power': 0.05},
    }

    # Map process type → frequency level
    TYPE_TO_FREQ = {
        'realtime':   'high',
        'cpu_bound':  'medium',
        'io_bound':   'low',
        'background': 'low',
    }

    def get_frequency(self, process):
        """Return the frequency level dict for a given process."""
        level = self.TYPE_TO_FREQ.get(process.process_type, 'medium')
        return self.FREQ_LEVELS[level]

    def get_sleep_state(self, idle_ms):
        """Return the deepest safe sleep state for a given idle duration."""
        if idle_ms >= self.SLEEP_STATES['C6']['min_idle_ms']:
            return self.SLEEP_STATES['C6']
        elif idle_ms >= self.SLEEP_STATES['C2']['min_idle_ms']:
            return self.SLEEP_STATES['C2']
        return self.SLEEP_STATES['C1']

    def calculate_energy(self, power_watts, duration_ms):
        """Energy (Joules) = Power (W) × Time (s)"""
        return power_watts * (duration_ms / 1000.0)

    def print_levels(self):
        print("\n── DVFS Frequency Levels ──────────────────────────────")
        print(f"{'Level':<10} {'Freq (MHz)':<14} {'Voltage (V)':<14} {'Power (W)'}")
        print("─" * 52)
        for name, info in self.FREQ_LEVELS.items():
            print(f"{name.capitalize():<10} {info['freq']:<14} {info['voltage']:<14} {info['power']}")
        print()
