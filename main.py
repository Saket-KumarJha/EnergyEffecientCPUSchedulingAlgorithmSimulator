"""
╔══════════════════════════════════════════════════════════════════╗
║         ENERGY-EFFICIENT CPU SCHEDULING ALGORITHM               ║
║         EDF + DVFS + C-State Sleep Management                   ║
╠══════════════════════════════════════════════════════════════════╣
║  How to run:                                                     ║
║    python main.py                                                ║
║                                                                  ║
║  Output:                                                         ║
║    • Console — process table + energy report + metrics           ║
║    • results/ — 6 dark-themed graphs saved as PNG               ║
║    • Open index.html in browser for the interactive dashboard    ║
╚══════════════════════════════════════════════════════════════════╝
"""

from process       import Process
from scheduler     import EnergyAwareScheduler
from energy_monitor import EnergyMonitor
from visualizer    import Visualizer


# ══════════════════════════════════════════════════════
#  STEP 1 — Define Processes
#  You can change these or add more!
# ══════════════════════════════════════════════════════
def create_processes():
    return [
        # pid  burst  priority  deadline  type           arrival
        Process(1,  100,  1,   400,   'realtime',   0),
        Process(2,  300,  2,  1200,   'cpu_bound',  50),
        Process(3,  150,  2,   900,   'io_bound',   100),
        Process(4,  200,  3,  2000,   'background', 150),
        Process(5,   80,  1,   500,   'realtime',   200),
        Process(6,  250,  2,  1500,   'cpu_bound',  300),
        Process(7,  120,  2,  1800,   'io_bound',   400),
        Process(8,  180,  3,  2500,   'background', 500),
    ]


def main():
    banner = """
╔══════════════════════════════════════════════════════════╗
║   ENERGY-EFFICIENT CPU SCHEDULING SIMULATION             ║
║   Algorithm: EDF + DVFS + C-State Management             ║
╚══════════════════════════════════════════════════════════╝"""
    print(banner)

    # ── Step 1: Load processes ───────────────────────────────────────
    processes = create_processes()
    print(f"\n  Loaded {len(processes)} processes.\n")

    # ── Step 2: Run your energy-aware scheduler ──────────────────────
    scheduler = EnergyAwareScheduler(processes)
    scheduler.run()

    # ── Step 3: Get summary metrics ──────────────────────────────────
    metrics = scheduler.get_metrics()

    # ── Step 4: Compare against traditional algorithms ───────────────
    monitor     = EnergyMonitor()
    energy_data = monitor.full_report(metrics['total_energy_j'], processes)

    # ── Step 5: Print full metrics ────────────────────────────────────
    print("\n" + "=" * 58)
    print("       PERFORMANCE METRICS SUMMARY")
    print("=" * 58)
    for key, val in metrics.items():
        print(f"  {key:<28}: {val}")
    print("=" * 58)

    # ── Step 6: Generate all 6 graphs ────────────────────────────────
    print("\n  Generating graphs → results/ folder\n")
    viz = Visualizer()

    print("  [1/6] Gantt Chart...")
    viz.gantt_chart(scheduler.timeline)

    print("  [2/6] Energy Comparison Bar Chart...")
    viz.energy_comparison_bar(energy_data)

    print("  [3/6] CPU Frequency Timeline...")
    viz.frequency_timeline(scheduler.timeline)

    print("  [4/6] Turnaround Time Chart...")
    viz.turnaround_chart(processes)

    print("  [5/6] Energy per Process...")
    viz.energy_per_process(processes)

    print("  [6/6] Full Dashboard...")
    viz.dashboard(metrics, energy_data, processes)

    print(f"""
╔══════════════════════════════════════════════════════════╗
║  ✅  Simulation complete!                                ║
║                                                          ║
║  • 6 graphs saved in the results/ folder                 ║
║  • Open index.html in your browser for the              ║
║    full interactive dashboard                            ║
╚══════════════════════════════════════════════════════════╝""")


if __name__ == "__main__":
    main()
