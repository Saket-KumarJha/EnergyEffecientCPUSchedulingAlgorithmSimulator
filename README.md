# ⚡ EnergyOS — Energy-Efficient CPU Scheduling Algorithm Simulator

A Python-based simulator that demonstrates how modern operating systems can reduce CPU energy consumption using **EDF scheduling**, **DVFS (Dynamic Voltage & Frequency Scaling)**, and **C-State sleep management** — complete with an interactive web dashboard and 6 dark-themed charts.

---

## 🧠 How It Works

Traditional CPU schedulers (FCFS, Round Robin, Priority) always run at maximum frequency and voltage — wasting energy on low-priority tasks. This simulator implements a smarter approach:

| Technique | What It Does | Energy Benefit |
|---|---|---|
| **EDF (Earliest Deadline First)** | Orders processes by deadline, not just priority | Avoids deadline misses without overscheduling |
| **DVFS** | Assigns minimum required frequency per process type | Power drops **cubically** with lower frequency |
| **C-State Management** | Puts CPU into deep sleep during idle gaps | Saves up to **90% power** during idle |
| **Burst Predictor (EMA)** | Predicts next burst time using exponential moving average | Proactively sets frequency before execution |

### Frequency Levels (DVFS)

| Level | Frequency | Voltage | Power | Used For |
|---|---|---|---|---|
| High | 2400 MHz | 1.2V | 4.0W | `realtime` tasks |
| Medium | 1200 MHz | 1.0V | 1.5W | `cpu_bound` tasks |
| Low | 600 MHz | 0.8V | 0.5W | `io_bound` / `background` |

### CPU Sleep States (C-States)

| State | Idle Threshold | Power |
|---|---|---|
| C1 (Halt) | < 10 ms idle | 0.50W |
| C2 (Stop-Clock) | ≥ 10 ms idle | 0.20W |
| C6 (Deep Sleep) | ≥ 50 ms idle | 0.05W |

---

## 📁 Project Structure

```
EnergyOS_CPU_Scheduler/
│
├── main.py             # Entry point — runs full simulation
├── process.py          # Process model (pid, burst, deadline, type)
├── scheduler.py        # EnergyAwareScheduler — EDF + DVFS + C-State
├── dvfs.py             # DVFSController — frequency/voltage/power mapping
├── predictor.py        # BurstPredictor — EMA-based burst time prediction
├── energy_monitor.py   # EnergyMonitor — comparison vs RR / PS / FCFS
├── visualizer.py       # Generates 6 dark-themed matplotlib charts
├── index.html          # Interactive web dashboard (open in browser)
├── requirements.txt    # Python dependencies
└── results/            # Output folder for generated PNG charts
    ├── 1_gantt_chart.png
    ├── 2_energy_comparison.png
    ├── 3_frequency_timeline.png
    ├── 4_turnaround_chart.png
    ├── 5_energy_per_process.png
    └── 6_dashboard.png
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Saket-KumarJha/EnergyEffecientCPUSchedulingAlgorithmSimulator.git
cd EnergyEffecientCPUSchedulingAlgorithmSimulator

# 2. Install dependencies
pip install -r requirements.txt
```

### Run the Simulation

```bash
python main.py
```

### View the Dashboard

After running, open `index.html` in your browser for the full interactive dashboard:

```bash
# Windows
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

---

## 📊 Output

Running `python main.py` produces:

**Console Output:**
- Process table with PID, type, frequency, execution time, energy consumed, turnaround time, and deadline status (✅ MET / ❌ MISS)
- Energy comparison report vs Round Robin, Priority Scheduling, and FCFS
- Full performance metrics summary

**Generated Charts (saved to `results/`):**
1. `1_gantt_chart.png` — Process execution timeline with color-coded types
2. `2_energy_comparison.png` — Bar chart comparing energy across 4 algorithms
3. `3_frequency_timeline.png` — CPU frequency over time
4. `4_turnaround_chart.png` — Turnaround time per process
5. `5_energy_per_process.png` — Energy consumed per process
6. `6_dashboard.png` — Combined full dashboard

---

## ⚙️ Customizing Processes

Edit the `create_processes()` function in `main.py` to change or add processes:

```python
Process(pid, burst_time, priority, deadline, process_type, arrival_time)
```

| Parameter | Description | Example Values |
|---|---|---|
| `pid` | Unique process ID | `1`, `2`, `3` |
| `burst_time` | CPU time required (ms) | `100`, `250` |
| `priority` | 1=Critical, 2=Normal, 3=Background | `1`, `2`, `3` |
| `deadline` | Must complete by (ms) | `500`, `2000` |
| `process_type` | Determines DVFS frequency | `realtime`, `cpu_bound`, `io_bound`, `background` |
| `arrival_time` | When process enters the queue (ms) | `0`, `100`, `300` |

---

## 📦 Dependencies

```
flask
numpy
pandas
matplotlib
scikit-learn
psutil
plotly
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## 📈 Sample Results

Your EDF+DVFS algorithm typically achieves **60–75% energy savings** over traditional schedulers:

| Algorithm | Energy (J) | vs Your Algo |
|---|---|---|
| **Your Algo (EDF + DVFS)** | ~0.85 J | — |
| Round Robin | ~2.90 J | ~70% more efficient |
| Priority Scheduling | ~2.64 J | ~67% more efficient |
| FCFS | ~2.64 J | ~67% more efficient |

*(Exact values depend on your process configuration)*

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 👤 Author

**Saket Kumar Jha**  
GitHub: [@Saket-KumarJha](https://github.com/Saket-KumarJha)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
