import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# set current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(script_dir)
os.chdir(script_dir)

# histograms at planning unit levels ------------------------------------------------

for level in ['town', 'subzone', 'PA']:

    plt.figure()

    data = pd.read_csv(f'output/ratio_{level}.csv')
    data = data[['ratio']]

    # Filter out non-finite values
    data = data.replace([np.inf, -np.inf], np.nan).dropna()
    counts, bins, _ = plt.hist(data, color='gray', bins=20, edgecolor='white')

    # Calculate mean and standard deviation
    mean_value = np.mean(data)
    std_value = np.std(data).values
    median_value = np.median(data)

    print(f'Mean ratio of {level} level:', mean_value)
    print(f'Median ratio of {level} level:', median_value)

    plt.ylim(0, max(counts) + 0.1 * max(counts))

    # Shade area for mean ± standard deviation
    plt.fill_betweenx([0, max(counts) + 10], mean_value - 1.5 * std_value, mean_value + 1.5 * std_value, color='blue',
                      alpha=0.1, label='1.5 Std Dev')
    plt.fill_betweenx([0, max(counts) + 10], mean_value - 0.5 * std_value, mean_value + 0.5 * std_value, color='blue',
                      alpha=0.15, label='0.5 Std Dev')

    # Plot mean line
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label='Mean')
    plt.axvline(median_value, color='yellow', linestyle='dashed', linewidth=1, label='Median')

    # Set labels and title
    plt.xlabel('Ratio of near-to-far visits (duration)')
    if level == 'town':
        plt.ylabel('No. of HDB Towns')
    elif level == 'subzone':
        plt.ylabel('No. of Subzones')
    else:
        plt.ylabel('No. of Planning Areas')

    plt.legend()
    # Save plot
    plt.savefig(f'output/figures/{level}_hist.pdf')

# histogram at overall level ------------------------------------------------

df_pk = pd.read_csv(r'output/park_clean.csv')
df_ngs = pd.read_csv(r'output/ngs_clean.csv')
print(f'overall level median for park: {df_pk.total_dur.median()}')
print(f'overall level median for NGS: {df_ngs.total_dur.median()}')

plt.figure(figsize=(6, 7))

min_value = min(df_pk['total_dur'].min(), df_ngs['total_dur'].min())
max_value = max(df_pk['total_dur'].max(), df_ngs['total_dur'].max())

plt.hist(df_ngs['total_dur'], color='pink', bins=20, edgecolor='white', alpha=1)
plt.hist(df_pk['total_dur'], color='lightblue', bins=20, edgecolor='white', alpha=0.8)

plt.xlabel('Total visit duration in the past year (min)', fontsize=14)
plt.ylabel('Frequency (no. of respondents)', fontsize=14)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.legend(['Neighbourhood', 'Further away'], title='Types of Green Space', fontsize=14, title_fontsize=14)
plt.subplots_adjust(left=0.15)
plt.savefig(f'output/figures/overall_duration_hist.pdf')



