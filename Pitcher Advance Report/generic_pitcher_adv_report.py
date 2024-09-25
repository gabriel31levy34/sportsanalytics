import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pybaseball import statcast_pitcher, playerid_lookup, statcast
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from shiny import App, render, ui

### META INFORMATION
batter_stand = 'R'
firstname = 'yu'
lastname = 'darvish'
mlbam = None

if datetime.now().month >= 10:
    start_date = str(datetime.now().year) + "-03-20"
    end_date = str(datetime.now().year) + "-11-20"
else:
    start_date = str(datetime.now().year - 1) + "-03-20"
    end_date = str(datetime.now().year - 1) + "-11-20"
all_data = statcast(start_date, end_date)
all_data[['pfx_x', 'pfx_z']] = all_data[['pfx_x', 'pfx_z']] * 12
all_data.dropna(subset='pitch_type', axis=0, inplace=True)
all_data = all_data[all_data.pitch_type != "PO"]

bottom_strike_zone = 1.52166
top_strike_zone = 3.67333
left_strike_zone = -0.83083
right_strike_zone = 0.83083

early = [(0,0), (1,0), (0,1), (1,1)]
ahead = [(2,0), (3,1), (3,0), (2,1)]
two_k = [(0,2), (1,2), (2,2), (3,2)]

target_cols = ['Pitch Type', 'Pitch%', 'Speed', 'Effective Speed', 'Spin', 'Extension', 'HB', 'VB', 'xwOBA']


def classify_count(row):
    count = (row['balls'], row['strikes'])
    if count in early:
        return "Early"
    elif count in ahead:
        return "Ahead"
    elif count in two_k:
        return "2K"
    else:
        return np.nan
    
def manip_df(df, qual_count):
    if qual_count != None:
        df = df[df.qual_count == qual_count].drop('qual_count', axis=1)
    total = df.num_pitches.sum()
    df['pitch_percent'] = ((df.num_pitches / total).round(3) * 100).round(1)
    df = df[['pitch_type', 'pitch_percent', 'release_speed', 'effective_speed', 'release_spin_rate', 'release_extension', 'pfx_x', 'pfx_z', 'estimated_woba_using_speedangle']]
    df.rename(columns={'pitch_type': 'Pitch Type', 
                       'pitch_percent': 'Pitch%', 
                       'release_speed': 'Speed', 
                       'effective_speed': 'Effective Speed', 
                       'release_spin_rate': 'Spin', 
                       'release_extension': 'Extension',
                       'pfx_x': 'HB',
                       'pfx_z': 'VB',
                       'estimated_woba_using_speedangle': 'xwOBA'}, inplace=True)
    return df

def apply_quantile_colormap(value, series):
    value = float(value)
    # Calculate the absolute differences and sort to find the closest value
    diffs = (series - value).abs()
    closest_index = diffs.idxmin()  # Get the index of the closest value
    # Calculate the relative position of the closest value in the series quantiles
    quantile_position = series.rank(pct=True)[closest_index]
    return plt.cm.coolwarm(quantile_position)


def create_table(ax, data, columns, all_data, target_cols, cell_height=0.45):
    data = data.iloc[:4, :]
    # Remove axes lines
    ax.axis('off')
    table = ax.table(cellText=data.values,
                     colLabels=columns,
                     loc='center',
                     cellLoc='left',
                     rowLoc='left')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(columns))))
    for (row, col), cell in table.get_celld().items():
        cell.set_height(cell_height)
        if row > 0 and col > 1:
            ptype = data.iloc[row - 1, 0]
            series = all_data[all_data['Pitch Type'] == ptype][target_cols[col]]
            value = data.iloc[row - 1, col]
            cell_color = apply_quantile_colormap(value, series)
            cell.set_facecolor(cell_color)
            cell.set_text_props(color='black')
    return table


def create_heatmap(ax_grid, data, unique_pitch_types, strike_zone_bounds):
    for j in range(4):
        ptype = unique_pitch_types[j]
        ptype_data = data[data.pitch_type == ptype]
        ax_sub = plt.subplot(ax_grid[0, j])
        ptype_data[['plate_x', 'plate_z']] = ptype_data[['plate_x', 'plate_z']].astype('float')
        sns.kdeplot(data=ptype_data, x='plate_x', y='plate_z', 
                    fill=True, cmap='coolwarm',
                    cbar=False, bw_adjust=0.75)
        plot_strike_zone(ax_sub, strike_zone_bounds)
        ax_sub.set_aspect('equal')
        ax_sub.set_xlim(-2.5, 2.5)
        ax_sub.set_ylim(-1, 5)
        ax_sub.set_xticks([])
        ax_sub.set_yticks([])
        ax_sub.set_title(ptype)
        ax_sub.set_xlabel('')
        ax_sub.set_ylabel('')

def plot_strike_zone(ax, bounds):
    left, right, bottom, top = bounds
    ax.plot([left, right, right, left, left],
            [bottom, bottom, top, top, bottom], 
            color='black', linestyle='-', linewidth=2)
    ax.plot([left, right, right, (left + right) / 2, left, left],
            [.2, .2, 0, -.2, 0, .2], 
            color='black', linestyle='-', linewidth=2)

def create_movement_profile(ax, data, unique_pitch_types):
    reduced_pitch_types = unique_pitch_types[:6]
    data = data[data.pitch_type.isin(reduced_pitch_types)]
    colors = plt.cm.viridis(np.linspace(0, 1, len(reduced_pitch_types)))
    color_map = dict(zip(reduced_pitch_types, colors))
    ax.scatter(data.pfx_x, data.pfx_z, c=data['pitch_type'].map(color_map))
    ax.grid(True)
    ax.set_aspect('equal')
    legend_labels = {ptype: color for ptype, color in zip(reduced_pitch_types, colors)}
    markers = [plt.Line2D([0], [0], color=color, marker='o', linestyle='') for color in legend_labels.values()]
    ax.legend(markers, legend_labels.keys(), title="Pitch Types")
    

### PULL POPULATION DATA
def get_all_data(batter_stand):
    all_data_manip = all_data.copy()
    all_data_manip['qual_count'] = all_data_manip.apply(classify_count, axis=1)
    
    all_stand_df = all_data_manip[all_data_manip.stand == batter_stand]
    
    all_group_sizes = all_data_manip.groupby(['pitcher', 'pitch_type']).size().reset_index(name='num_pitches')
    all_grouped_df = all_data_manip.groupby(['pitcher', 'pitch_type'])[['release_speed', 'effective_speed', 'release_spin_rate', 'release_extension', 'pfx_x', 'pfx_z', 'estimated_woba_using_speedangle']].mean() \
        .reset_index() \
        .merge(all_group_sizes, on=['pitcher', 'pitch_type'])
    all_grouped_df[['release_speed', 'effective_speed', 'pfx_x', 'pfx_z', 'release_extension']] = all_grouped_df[['release_speed', 'effective_speed', 'pfx_x', 'pfx_z', 'release_extension']].round(2)
    all_grouped_df[['estimated_woba_using_speedangle']] = all_grouped_df[['estimated_woba_using_speedangle']].round(3)

    all_grouped_df = manip_df(all_grouped_df, None).drop(columns=['Pitch%'])
    
    return all_stand_df, all_grouped_df


def get_player_data(all_stand_df):
    if mlbam is not None:
        stand_df = all_stand_df[all_stand_df.pitcher == mlbam]
    else:
        pitcher_mlbam = playerid_lookup(lastname, firstname).key_mlbam.iloc[0]
        stand_df = all_stand_df[all_stand_df.pitcher == pitcher_mlbam]
    
    group_sizes = stand_df.groupby(['pitch_type', 'qual_count']).size().reset_index(name='num_pitches')
    grouped_df = stand_df.groupby(['pitch_type', 'qual_count'])[['release_speed', 'effective_speed', 'release_spin_rate', 'release_extension', 'pfx_x', 'pfx_z', 'estimated_woba_using_speedangle']].mean() \
        .reset_index() \
        .merge(group_sizes, on=['pitch_type', 'qual_count'])
    grouped_df[['release_speed', 'effective_speed', 'pfx_x', 'pfx_z', 'release_extension']] = grouped_df[['release_speed', 'effective_speed', 'pfx_x', 'pfx_z', 'release_extension']].round(2)
    grouped_df[['estimated_woba_using_speedangle']] = grouped_df[['estimated_woba_using_speedangle']].round(3)
    grouped_df.release_spin_rate = grouped_df.release_spin_rate.round().astype(int)

    early_grouped_df = manip_df(grouped_df, 'Early').sort_values(by='Pitch%', ascending=False)
    ahead_grouped_df = manip_df(grouped_df, 'Ahead').sort_values(by='Pitch%', ascending=False)
    two_k_grouped_df = manip_df(grouped_df, '2K').sort_values(by='Pitch%', ascending=False)
    
    unique_pitch_types = manip_df(grouped_df, None).sort_values(by='Pitch%', ascending=False)['Pitch Type'].unique()
    
    return unique_pitch_types, stand_df, early_grouped_df, ahead_grouped_df, two_k_grouped_df

    

def create_one_sheeter(pdf):
    all_stand_df, all_grouped_df = get_all_data(batter_stand)
    unique_pitch_types, stand_df, early_grouped_df, ahead_grouped_df, two_k_grouped_df = get_player_data(all_stand_df)

    fig = plt.figure(figsize=(16, 8))
    columns = ['Pitch\nType', 'Pitch%', 'Speed', 'Effective\nSpeed', 'Spin', 'Extension', 'HB', 'VB', 'xwOBA']
    strike_zone_bounds = [left_strike_zone, right_strike_zone, bottom_strike_zone, top_strike_zone]

    # Early Count Table
    plt.figtext(0.11, 0.9, 'Early Count', ha='left', va='top', c='black', fontsize=12)
    ax1 = fig.add_axes([0.05, 0.7, 0.2, 0.1])
    create_table(ax1, early_grouped_df, columns, all_grouped_df, target_cols)

    # Early Count Heatmap
    ax2_grid = plt.GridSpec(1, 4, fig, left=0.00005, bottom=0.5, right=0.3, top=0.6)
    create_heatmap(ax2_grid, stand_df[stand_df.qual_count == 'Early'], unique_pitch_types, strike_zone_bounds)

    # Ahead Count Table
    plt.figtext(0.11, 0.4, "Hitter's Count", ha='left', va='top', c='black', fontsize=12)
    ax3 = fig.add_axes([0.05, 0.2, 0.2, 0.1])
    create_table(ax3, ahead_grouped_df, columns, all_grouped_df, target_cols)

    # Ahead Count Heatmap
    ax4_grid = plt.GridSpec(1, 4, fig, left=0.00005, bottom=0, right=0.3, top=0.1)
    create_heatmap(ax4_grid, stand_df[stand_df.qual_count == 'Ahead'], unique_pitch_types, strike_zone_bounds)

    # 2K Count Table
    plt.figtext(0.62, 0.9, '2K Count', ha='left', va='top', c='black', fontsize=12)
    ax5 = fig.add_axes([0.55, 0.7, 0.2, 0.1])
    create_table(ax5, two_k_grouped_df, columns, all_grouped_df, target_cols)

    # 2K Heatmap
    ax6_grid = plt.GridSpec(1, 4, fig, left=0.5, bottom=0.5, right=0.8, top=0.6)
    create_heatmap(ax6_grid, stand_df[stand_df.qual_count == '2K'], unique_pitch_types, strike_zone_bounds)

    # Movement Profile
    plt.figtext(0.62, 0.4, 'Movement Profiles', ha='left', va='top', c='black', fontsize=12)
    ax7 = fig.add_axes([0.5, 0, 0.35, 0.35])
    create_movement_profile(ax7, stand_df, unique_pitch_types)

    # Set up figure text for player
    plt.figtext(0.29, 0.95, firstname.capitalize() + ' ' + lastname.capitalize() + ' Versus ' + ('Righties' if batter_stand == 'R' else 'Lefties'), ha='left', va='top', c='black', fontsize=15, fontweight='bold')

    pdf.savefig(fig, dpi=100, bbox_inches='tight')
    
    plt.close(fig)

pdf = PdfPages('/Users/gabriellevy/Documents/generic_adv_report.pdf')
create_one_sheeter(pdf)
pdf.close()