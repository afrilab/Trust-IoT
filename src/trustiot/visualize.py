import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from trustiot.core import Simulation

def display_enhanced_results(results, model_name, setup_func):
    """Displays the simulation results in a series of plots and tables.

    Args:
        results (dict): A dictionary containing the simulation results.
        model_name (str): The name of the simulation model.
        setup_func (function): The user-defined setup function.
    """
    print("\n\n" + "="*70)
    print(f"          FINAL BENCHMARKING RESULTS ({model_name} Model)")
    print("="*70)

    final_metrics = {
        'Algorithm': ['Game-Theoretic', 'Greedy', 'Random'],
        'Avg. Device Utility (Higher is Better)': [results['game_theory']['avg_device_utility_mean'][-1], results['greedy']['avg_device_utility_mean'][-1], results['random']['avg_device_utility_mean'][-1]],
        'Server Load Std. Dev. (Lower is Better)': [results['game_theory']['server_load_std_dev_mean'][-1], results['greedy']['server_load_std_dev_mean'][-1], results['random']['server_load_std_dev_mean'][-1]],
        'Task Completion Ratio (%)': [results['game_theory']['completion_ratio_mean'][-1] * 100, results['greedy']['completion_ratio_mean'][-1] * 100, results['random']['completion_ratio_mean'][-1] * 100],
        'Deadline Adherence (%)': [results['game_theory']['deadline_adherence_mean'][-1] * 100, results['greedy']['deadline_adherence_mean'][-1] * 100, results['random']['deadline_adherence_mean'][-1] * 100],
        'Malicious Task Acceptance (%)': [results['game_theory']['malicious_accepted_mean'][-1] * 100, results['greedy']['malicious_accepted_mean'][-1] * 100, results['random']['malicious_accepted_mean'][-1] * 100],
    }
    df_final = pd.DataFrame(final_metrics).set_index('Algorithm')
    print("\n**Final Mean Metrics Comparison:**\n")
    print(df_final.to_string(formatters={col: '{:,.4f}'.format for col in df_final.columns}))

    sns.set_theme(style="whitegrid", palette="viridis")
    fig = plt.figure(figsize=(22, 20))
    gs = fig.add_gridspec(3, 2)
    fig.suptitle(f'Comprehensive Performance Analysis ({model_name} Model)', fontsize=24, weight='bold')

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    for algo in results.keys():
        iterations = range(len(results[algo]['avg_device_utility_mean']))
        ax1.plot(iterations, results[algo]['avg_device_utility_mean'], label=algo.replace('_', ' ').title())
        ax1.fill_between(iterations, results[algo]['avg_device_utility_mean'] - results[algo]['avg_device_utility_std'], results[algo]['avg_device_utility_mean'] + results[algo]['avg_device_utility_std'], alpha=0.2)
        ax2.plot(iterations, results[algo]['server_load_std_dev_mean'], label=algo.replace('_', ' ').title())
        ax2.fill_between(iterations, results[algo]['server_load_std_dev_mean'] - results[algo]['server_load_std_dev_std'], results[algo]['server_load_std_dev_mean'] + results[algo]['server_load_std_dev_std'], alpha=0.2)
    ax1.set_title('Average Device Utility Convergence', fontsize=18, weight='bold')
    ax1.set_xlabel('Simulation Iteration'); ax1.set_ylabel('Average Utility'); ax1.legend(); ax1.axhline(0, color='grey', linestyle='--', linewidth=1)
    ax2.set_title('Server Load Std. Dev. Convergence', fontsize=18, weight='bold')
    ax2.set_xlabel('Simulation Iteration'); ax2.set_ylabel('Load Standard Deviation'); ax2.legend()

    ax3 = fig.add_subplot(gs[1, 0])
    iterations = range(len(results['game_theory']['avg_trust_honest_mean']))
    ax3.plot(iterations, results['game_theory']['avg_trust_honest_mean'], label='Honest Devices', color='green')
    ax3.fill_between(iterations, results['game_theory']['avg_trust_honest_mean'] - results['game_theory']['avg_trust_honest_std'], results['game_theory']['avg_trust_honest_mean'] + results['game_theory']['avg_trust_honest_std'], alpha=0.2, color='green')
    ax3.plot(iterations, results['game_theory']['avg_trust_malicious_mean'], label='Malicious Devices', color='red')
    ax3.fill_between(iterations, results['game_theory']['avg_trust_malicious_mean'] - results['game_theory']['avg_trust_malicious_std'], results['game_theory']['avg_trust_malicious_mean'] + results['game_theory']['avg_trust_malicious_std'], alpha=0.2, color='red')
    ax3.set_title('Trust Score Discrimination (Game-Theoretic)', fontsize=18, weight='bold')
    ax3.set_xlabel('Simulation Iteration'); ax3.set_ylabel('Average Trust Score'); ax3.legend(); ax3.set_ylim(0, 1.1)

    ax4 = fig.add_subplot(gs[1, 1], polar=True)
    radar_labels = ['Avg. Device Utility', 'Load Balancing\\n(1/StdDev)', 'Avg. Trust Score', 'Completion Ratio', 'Deadline Adherence']
    radar_values = {
        'Game-Theoretic': [max(0, df_final.loc['Game-Theoretic']['Avg. Device Utility (Higher is Better)']), 1 / (df_final.loc['Game-Theoretic']['Server Load Std. Dev. (Lower is Better)'] + 1e-6), results['game_theory']['avg_trust_honest_mean'][-1], df_final.loc['Game-Theoretic']['Task Completion Ratio (%)'], df_final.loc['Game-Theoretic']['Deadline Adherence (%)']],
        'Greedy': [0, 1 / (df_final.loc['Greedy']['Server Load Std. Dev. (Lower is Better)'] + 1e-6), results['greedy']['avg_trust_honest_mean'][-1], df_final.loc['Greedy']['Task Completion Ratio (%)'], df_final.loc['Greedy']['Deadline Adherence (%)']],
        'Random': [0, 1 / (df_final.loc['Random']['Server Load Std. Dev. (Lower is Better)'] + 1e-6), results['random']['avg_trust_honest_mean'][-1], df_final.loc['Random']['Task Completion Ratio (%)'], df_final.loc['Random']['Deadline Adherence (%)']]
    }
    df_radar = pd.DataFrame(radar_values, index=radar_labels)
    df_radar_normalized = df_radar.div(df_radar.max(axis=1) + 1e-9, axis=0)
    angles = np.linspace(0, 2 * np.pi, len(radar_labels), endpoint=False).tolist(); angles += angles[:1]
    ax4.set_title('Multi-Metric Performance Comparison (Normalized)', fontsize=18, weight='bold', y=1.15)
    ax4.set_xticks(angles[:-1]); ax4.set_xticklabels(radar_labels); ax4.set_ylim(0, 1.1)
    for algo in df_radar_normalized.columns:
        values = df_radar_normalized[algo].tolist(); values += values[:1]
        ax4.plot(angles, values, label=algo, linewidth=2, linestyle='solid'); ax4.fill(angles, values, alpha=0.25)
    ax4.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15))

    ax5 = fig.add_subplot(gs[2, :])
    devices_sample, servers_sample = setup_func()
    sim_sample = Simulation(devices_sample, servers_sample)
    heatmap_data = []
    server_ids = [str(s.id) for s in servers_sample]
    for algo in results.keys():
        sim_sample.run(algo, iterations=50)
        loads = [s.get_current_cpu_load() for s in sim_sample.servers]
        for s_idx, load in enumerate(loads):
            heatmap_data.append({'Algorithm': algo.replace('_', ' ').title(), 'Server': server_ids[s_idx], 'Load': load})
    df_heatmap = pd.DataFrame(heatmap_data).pivot_table(index='Server', columns='Algorithm', values='Load')
    try:
        df_heatmap.index = pd.Categorical(df_heatmap.index, categories=sorted(server_ids, key=lambda x: int(str(x).split('-')[-1])), ordered=True)
        df_heatmap.sort_index(inplace=True)
    except (ValueError, TypeError): # Handle non-integer sortable IDs
        df_heatmap.sort_index(inplace=True)
    sns.heatmap(ax=ax5, data=df_heatmap, cmap="viridis", annot=True, fmt=".2f", linewidths=.5)
    ax5.set_title('Final Server Load Heatmap (Sample Run)', fontsize=18, weight='bold')
    ax5.set_xlabel('Algorithm'); ax5.set_ylabel('Server ID')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
