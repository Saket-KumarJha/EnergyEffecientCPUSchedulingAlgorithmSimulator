import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
import os

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

# ── Dark theme ─────────────────────────────────────────────────────────────
BG      = '#080c14'
BG2     = '#0d1320'
CARD    = '#0f1929'
BORDER  = '#1e2d45'
TEXT    = '#e8f0fe'
TEXT2   = '#8ba3c7'
ACCENT  = '#00d4ff'
GREEN   = '#00ff88'
RED     = '#ff4757'
ORANGE  = '#ffa502'
PURPLE  = '#a855f7'

TYPE_COLORS = {
    'realtime':   '#ff4757',
    'cpu_bound':  '#00d4ff',
    'io_bound':   '#00ff88',
    'background': '#a855f7',
    'idle':       '#2a3a52',
}

def _apply_dark(fig, axes):
    fig.patch.set_facecolor(BG)
    for ax in (axes if hasattr(axes,'__iter__') else [axes]):
        ax.set_facecolor(BG2)
        ax.tick_params(colors=TEXT2)
        ax.xaxis.label.set_color(TEXT2)
        ax.yaxis.label.set_color(TEXT2)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER)
        ax.yaxis.grid(True, color=BORDER, linestyle='--', alpha=0.4, linewidth=0.5)
        ax.set_axisbelow(True)

def _save(fig, name):
    path = os.path.join(RESULTS_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"    ✓ Saved → {path}")
    return path


class Visualizer:
    """Generates 6 publication-quality dark-themed graphs."""

    # ── 1. Gantt Chart ─────────────────────────────────────────────────────
    def gantt_chart(self, timeline):
        fig, ax = plt.subplots(figsize=(16, 3.5))
        _apply_dark(fig, ax)
        fig.subplots_adjust(left=0.04, right=0.98, top=0.78, bottom=0.18)

        total = max(b['end'] for b in timeline)

        for block in timeline:
            w     = block['end'] - block['start']
            color = TYPE_COLORS.get(block['type'], '#444')
            rect  = ax.barh(0, w, left=block['start'], height=0.55,
                            color=color, alpha=0.85, edgecolor='white',
                            linewidth=0.4, zorder=3)
            mid = block['start'] + w / 2
            if w / total > 0.03:
                label = block['label']
                if block.get('freq'):
                    label += f"\n{block['freq']}MHz"
                ax.text(mid, 0, label, ha='center', va='center',
                        fontsize=7.5, color='white', fontweight='bold', zorder=4)

        # Axis
        ax.set_xlim(0, total)
        ax.set_ylim(-0.5, 0.7)
        ax.set_yticks([])
        ax.set_xlabel('Time (ms)', fontsize=9, color=TEXT2)
        ax.set_title('Gantt Chart — CPU Execution Timeline', fontsize=13,
                     color=TEXT, fontweight='bold', pad=14)

        # Legend
        patches = [mpatches.Patch(color=TYPE_COLORS[t],
                   label=t.replace('_',' ').title())
                   for t in ['realtime','cpu_bound','io_bound','background','idle']]
        ax.legend(handles=patches, loc='upper right', fontsize=8,
                  facecolor=CARD, labelcolor=TEXT2, edgecolor=BORDER,
                  framealpha=0.9)

        return _save(fig, '1_gantt_chart.png')

    # ── 2. Energy Comparison Bar ────────────────────────────────────────────
    def energy_comparison_bar(self, energy_data):
        fig, ax = plt.subplots(figsize=(10, 6))
        _apply_dark(fig, ax)

        labels  = ['Your Algorithm\n(EDF + DVFS)', 'Round Robin', 'Priority\nScheduling', 'FCFS']
        values  = [energy_data['your_algo'], energy_data['round_robin'],
                   energy_data['priority'],  energy_data['fcfs']]
        colors  = [GREEN, RED, ORANGE, '#ff6450']
        alphas  = [0.9, 0.75, 0.75, 0.7]

        for i, (label, val, color, alpha) in enumerate(zip(labels, values, colors, alphas)):
            bar = ax.bar(i, val, color=color, alpha=alpha, width=0.5,
                         edgecolor='white', linewidth=0.4, zorder=3)
            ax.text(i, val + max(values)*0.01, f'{val:.4f} J',
                    ha='center', va='bottom', fontsize=9, color=TEXT,
                    fontweight='bold', zorder=4)

        # Savings annotations
        base = values[0]
        for i in range(1, len(values)):
            saving = round((values[i]-base)/values[i]*100, 1)
            ax.text(i, values[i]*0.5, f'{saving}%\nmore\nenergy',
                    ha='center', va='center', fontsize=8.5, color='white',
                    alpha=0.9, zorder=5)

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=9, color=TEXT2)
        ax.set_ylabel('Energy Consumed (Joules)', fontsize=10)
        ax.set_title('Energy Comparison — Your Algorithm vs Traditional Schedulers',
                     fontsize=13, color=TEXT, fontweight='bold', pad=14)
        ax.set_xlim(-0.5, len(labels)-0.5)

        return _save(fig, '2_energy_comparison.png')

    # ── 3. CPU Frequency Timeline ───────────────────────────────────────────
    def frequency_timeline(self, timeline):
        fig, ax = plt.subplots(figsize=(14, 5))
        _apply_dark(fig, ax)

        times, freqs = [], []
        for block in timeline:
            freq = block.get('freq', 0) if block['type'] != 'idle' else 0
            times += [block['start'], block['end']]
            freqs += [freq, freq]

        ax.step(times, freqs, where='post', color=ACCENT, linewidth=2.5,
                zorder=4, solid_joinstyle='miter')
        ax.fill_between(times, freqs, step='post', alpha=0.15, color=ACCENT, zorder=3)

        # Reference lines
        refs = [(2400, 'High (2400 MHz)', RED),
                (1200, 'Medium (1200 MHz)', ORANGE),
                (600,  'Low (600 MHz)', GREEN)]
        for freq, label, color in refs:
            ax.axhline(y=freq, linestyle='--', color=color, alpha=0.4,
                       linewidth=1, zorder=2)
            ax.text(times[-1]*1.001, freq, label, va='center',
                    fontsize=8, color=color, alpha=0.8)

        ax.set_ylim(-150, 2900)
        ax.set_xlim(0, times[-1])
        ax.set_xlabel('Time (ms)', fontsize=10)
        ax.set_ylabel('CPU Frequency (MHz)', fontsize=10)
        ax.set_title('CPU Frequency Over Time — DVFS in Action',
                     fontsize=13, color=TEXT, fontweight='bold', pad=14)
        ax.set_yticks([0, 600, 1200, 2400])
        ax.set_yticklabels(['Sleep', '600', '1200', '2400'], color=TEXT2)

        return _save(fig, '3_frequency_timeline.png')

    # ── 4. Turnaround Time per Process ─────────────────────────────────────
    def turnaround_chart(self, processes):
        fig, ax = plt.subplots(figsize=(12, 6))
        _apply_dark(fig, ax)

        n      = len(processes)
        x      = np.arange(n)
        w      = 0.28
        labels = [f"P{p.pid}\n({p.process_type[:3]})" for p in processes]
        exec_t = [p.actual_exec_time for p in processes]
        wait_t = [p.waiting_time for p in processes]
        tat_t  = [p.turnaround_time for p in processes]

        ax.bar(x - w, exec_t, w, label='Execution Time', color=ACCENT,
               alpha=0.8, edgecolor='white', linewidth=0.3, zorder=3)
        ax.bar(x,     wait_t, w, label='Waiting Time',   color=ORANGE,
               alpha=0.8, edgecolor='white', linewidth=0.3, zorder=3)
        ax.bar(x + w, tat_t,  w, label='Turnaround Time',color=PURPLE,
               alpha=0.8, edgecolor='white', linewidth=0.3, zorder=3)

        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=9, color=TEXT2)
        ax.set_ylabel('Time (ms)', fontsize=10)
        ax.set_title('Process Timing — Execution, Waiting & Turnaround',
                     fontsize=13, color=TEXT, fontweight='bold', pad=14)
        ax.legend(fontsize=9, facecolor=CARD, labelcolor=TEXT2, edgecolor=BORDER)

        return _save(fig, '4_turnaround_chart.png')

    # ── 5. Energy per Process (Pie + Bar) ──────────────────────────────────
    def energy_per_process(self, processes):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        _apply_dark(fig, [ax1, ax2])

        labels   = [f"P{p.pid} ({p.process_type.replace('_',' ')})" for p in processes]
        energies = [p.energy_consumed for p in processes]
        colors   = [TYPE_COLORS.get(p.process_type, '#888') for p in processes]

        # Donut
        wedges, texts, autos = ax1.pie(energies, labels=labels, colors=colors,
                                        autopct='%1.1f%%', startangle=140,
                                        textprops={'color': TEXT2, 'fontsize': 8},
                                        wedgeprops={'edgecolor':'white','linewidth':0.6},
                                        pctdistance=0.78)
        for a in autos:
            a.set_color(TEXT); a.set_fontweight('bold')
        # Donut hole
        circle = plt.Circle((0,0), 0.55, fc=BG2)
        ax1.add_patch(circle)
        ax1.set_title('Energy Share per Process', fontsize=11,
                      color=TEXT, fontweight='bold', pad=14)

        # Horizontal bar
        bars = ax2.barh(labels, energies, color=colors, alpha=0.8,
                        edgecolor='white', linewidth=0.4, zorder=3)
        for bar, val in zip(bars, energies):
            ax2.text(bar.get_width()+max(energies)*0.01,
                     bar.get_y()+bar.get_height()/2,
                     f'{val:.5f} J', va='center', fontsize=8,
                     color=TEXT2, zorder=4)
        ax2.set_xlabel('Energy (Joules)', fontsize=10)
        ax2.set_title('Energy Consumed per Process', fontsize=11,
                      color=TEXT, fontweight='bold', pad=14)
        ax2.tick_params(axis='y', colors=TEXT2)

        plt.tight_layout(pad=2)
        return _save(fig, '5_energy_per_process.png')

    # ── 6. Full Dashboard ──────────────────────────────────────────────────
    def dashboard(self, metrics, energy_data, processes):
        fig = plt.figure(figsize=(16, 10), facecolor=BG)
        fig.suptitle('Energy-Efficient CPU Scheduler — Performance Dashboard',
                     fontsize=16, color=TEXT, fontweight='bold', y=0.98)

        gs = gridspec.GridSpec(2, 3, figure=fig, wspace=0.35, hspace=0.45)

        # ── Subplot 1: Energy comparison ──────────────────────────────
        ax1 = fig.add_subplot(gs[0,0])
        ax1.set_facecolor(BG2)
        algos  = ['EDF+DVFS\n(Yours)', 'Round\nRobin', 'Priority', 'FCFS']
        vals   = [energy_data['your_algo'], energy_data['round_robin'],
                  energy_data['priority'],  energy_data['fcfs']]
        colors = [GREEN, RED, ORANGE, '#ff6450']
        for i,(v,c) in enumerate(zip(vals,colors)):
            ax1.bar(i,v,color=c,alpha=0.8,edgecolor='white',linewidth=0.4,width=0.55,zorder=3)
            ax1.text(i,v*0.5,f'{v:.3f}J',ha='center',va='center',
                     fontsize=8,color='white',fontweight='bold',zorder=4)
        ax1.set_xticks(range(4)); ax1.set_xticklabels(algos,fontsize=7.5,color=TEXT2)
        ax1.set_title('Total Energy by Algorithm',fontsize=10,color=TEXT,fontweight='bold')
        ax1.set_ylabel('Joules',fontsize=8,color=TEXT2)
        ax1.tick_params(colors=TEXT2)
        for s in ax1.spines.values(): s.set_edgecolor(BORDER)
        ax1.yaxis.grid(True,color=BORDER,linestyle='--',alpha=0.4,linewidth=0.5)
        ax1.set_axisbelow(True)

        # ── Subplot 2: Savings donut ──────────────────────────────────
        ax2 = fig.add_subplot(gs[0,1])
        ax2.set_facecolor(BG2)
        saved = max(0, energy_data['round_robin']-energy_data['your_algo'])
        used  = energy_data['your_algo']
        wedges,_,autos = ax2.pie([used,saved],
                                  labels=['Used','Saved vs RR'],
                                  colors=[RED,GREEN], autopct='%1.1f%%',
                                  startangle=90,
                                  textprops={'color':TEXT2,'fontsize':8},
                                  wedgeprops={'edgecolor':BG,'linewidth':2},
                                  pctdistance=0.75)
        for a in autos: a.set_color(TEXT); a.set_fontweight('bold')
        ax2.add_patch(plt.Circle((0,0),0.55,fc=BG2))
        ax2.set_title('Energy Savings vs Round Robin',fontsize=10,color=TEXT,fontweight='bold')

        # ── Subplot 3: Deadlines ──────────────────────────────────────
        ax3 = fig.add_subplot(gs[0,2])
        ax3.set_facecolor(BG2)
        met    = metrics['deadlines_met']
        missed = metrics['deadlines_missed']
        ax3.bar(['Met','Missed'],[met,missed],color=[GREEN,RED],
                alpha=0.8,edgecolor='white',linewidth=0.4,width=0.4,zorder=3)
        for i,(label,val) in enumerate(zip(['Met','Missed'],[met,missed])):
            ax3.text(i,val+0.05,str(val),ha='center',va='bottom',
                     fontsize=12,color=TEXT,fontweight='bold',zorder=4)
        ax3.set_title('Deadline Achievement',fontsize=10,color=TEXT,fontweight='bold')
        ax3.tick_params(colors=TEXT2)
        for s in ax3.spines.values(): s.set_edgecolor(BORDER)
        ax3.yaxis.grid(True,color=BORDER,linestyle='--',alpha=0.4,linewidth=0.5)
        ax3.set_axisbelow(True)

        # ── Subplot 4: Turnaround ─────────────────────────────────────
        ax4 = fig.add_subplot(gs[1,:2])
        ax4.set_facecolor(BG2)
        n = len(processes); x = np.arange(n); w = 0.28
        ax4.bar(x-w,[p.actual_exec_time for p in processes],w,label='Execution',
                color=ACCENT,alpha=0.8,edgecolor='white',linewidth=0.3,zorder=3)
        ax4.bar(x,[p.waiting_time for p in processes],w,label='Waiting',
                color=ORANGE,alpha=0.8,edgecolor='white',linewidth=0.3,zorder=3)
        ax4.bar(x+w,[p.turnaround_time for p in processes],w,label='Turnaround',
                color=PURPLE,alpha=0.8,edgecolor='white',linewidth=0.3,zorder=3)
        ax4.set_xticks(x)
        ax4.set_xticklabels([f'P{p.pid}' for p in processes],fontsize=9,color=TEXT2)
        ax4.set_ylabel('Time (ms)',fontsize=9,color=TEXT2)
        ax4.set_title('Process Timing Breakdown',fontsize=10,color=TEXT,fontweight='bold')
        ax4.legend(fontsize=8,facecolor=CARD,labelcolor=TEXT2,edgecolor=BORDER)
        ax4.tick_params(colors=TEXT2)
        for s in ax4.spines.values(): s.set_edgecolor(BORDER)
        ax4.yaxis.grid(True,color=BORDER,linestyle='--',alpha=0.4,linewidth=0.5)
        ax4.set_axisbelow(True)

        # ── Subplot 5: Metrics panel ──────────────────────────────────
        ax5 = fig.add_subplot(gs[1,2])
        ax5.set_facecolor('#0a1525')
        ax5.axis('off')
        rows = [
            ("Total Energy",       f"{metrics['total_energy_j']} J",       ACCENT),
            ("Avg Turnaround",     f"{metrics['avg_turnaround_ms']} ms",    TEXT),
            ("Avg Waiting",        f"{metrics['avg_waiting_ms']} ms",       TEXT),
            ("Deadlines Met",      f"{met}/{metrics['total_processes']}",   GREEN if met==metrics['total_processes'] else RED),
            ("Miss Rate",          f"{metrics['deadline_miss_rate']}%",     RED if metrics['deadline_miss_rate']>0 else GREEN),
            ("Saved vs RR",        f"{energy_data['savings_vs_rr']}%",      GREEN),
        ]
        ax5.set_title('Key Metrics',fontsize=10,color=TEXT,fontweight='bold')
        for i,(k,v,c) in enumerate(rows):
            y = 0.88 - i*0.145
            ax5.text(0.05,y,k,transform=ax5.transAxes,
                     fontsize=9,color=TEXT2,va='center')
            ax5.text(0.98,y,v,transform=ax5.transAxes,
                     fontsize=10,color=c,va='center',ha='right',fontweight='bold',
                     fontfamily='monospace')

        return _save(fig, '6_dashboard.png')
