import numpy as np
import pandas as pd

mov2 = pd.read_csv('pitch_movement_2022.csv')
mov1 = pd.read_csv('pitch_movement_2021.csv')
mov0 = pd.read_csv('pitch_movement_2020.csv')
data = pd.read_csv("spin-direction-pitches.csv")

mov2.loc[(mov2['pitch_type_name'] == '4-Seamer'),'pitch_type_name']='FF'
mov2.loc[(mov2['pitch_type_name'] == 'Slider'),'pitch_type_name']='SL'
mov2.loc[(mov2['pitch_type_name'] == 'Sinker'),'pitch_type_name']='SI'
mov2.loc[(mov2['pitch_type_name'] == 'Cutter'),'pitch_type_name']='FC'
mov2.loc[(mov2['pitch_type_name'] == 'Splitter'),'pitch_type_name']='FS'
mov2.loc[(mov2['pitch_type_name'] == 'Curveball'),'pitch_type_name']='CU'
mov2.loc[(mov2['pitch_type_name'] == 'Changeup'),'pitch_type_name']='CH'

mov1.loc[(mov1['pitch_type_name'] == '4-Seamer'),'pitch_type_name']='FF'
mov1.loc[(mov1['pitch_type_name'] == 'Slider'),'pitch_type_name']='SL'
mov1.loc[(mov1['pitch_type_name'] == 'Sinker'),'pitch_type_name']='SI'
mov1.loc[(mov1['pitch_type_name'] == 'Cutter'),'pitch_type_name']='FC'
mov1.loc[(mov1['pitch_type_name'] == 'Splitter'),'pitch_type_name']='FS'
mov1.loc[(mov1['pitch_type_name'] == 'Curveball'),'pitch_type_name']='CU'
mov1.loc[(mov1['pitch_type_name'] == 'Changeup'),'pitch_type_name']='CH'

mov0.loc[(mov0['pitch_type_name'] == '4-Seamer'),'pitch_type_name']='FF'
mov0.loc[(mov0['pitch_type_name'] == 'Slider'),'pitch_type_name']='SL'
mov0.loc[(mov0['pitch_type_name'] == 'Sinker'),'pitch_type_name']='SI'
mov0.loc[(mov0['pitch_type_name'] == 'Cutter'),'pitch_type_name']='FC'
mov0.loc[(mov0['pitch_type_name'] == 'Splitter'),'pitch_type_name']='FS'
mov0.loc[(mov0['pitch_type_name'] == 'Curveball'),'pitch_type_name']='CU'
mov0.loc[(mov0['pitch_type_name'] == 'Changeup'),'pitch_type_name']='CH'

mov2 = mov2[['pitcher_id', 'pitch_type_name', 'pitches_thrown', 'pitcher_break_z', 'pitcher_break_x']]
mov1 = mov1[['pitcher_id', 'pitch_type_name', 'pitches_thrown', 'pitcher_break_z', 'pitcher_break_x']]
mov0 = mov0[['pitcher_id', 'pitch_type_name', 'pitches_thrown', 'pitcher_break_z', 'pitcher_break_x']]
for i in range(len(mov2)):
    id2 = mov2.iloc[i]['pitcher_id']
    p_type2 = mov2.iloc[i]['pitch_type_name']
    row1 = np.where((mov1['pitcher_id']==id2) & (mov1['pitch_type_name']==p_type2))
    row0 = np.where((mov0['pitcher_id']==id2) & (mov0['pitch_type_name']==p_type2))
    p2 = mov2.iloc[i]['pitches_thrown']
    z2 = mov2.iloc[i]['pitcher_break_z']
    x2 = mov2.iloc[i]['pitcher_break_x']
    if len(row1[0]) > 0:
        p1 = mov1.iloc[row1[0][0]]['pitches_thrown']
        z1 = mov1.iloc[row1[0][0]]['pitcher_break_z']
        x1 = mov1.iloc[row1[0][0]]['pitcher_break_x']
    else:
        p1=0
        z1=0
        x1=0
    if len(row0[0]) > 0:
        p0 = mov0.iloc[row0[0][0]]['pitches_thrown']
        z0 = mov0.iloc[row0[0][0]]['pitcher_break_z']
        x0 = mov0.iloc[row0[0][0]]['pitcher_break_x']
    else:
        p0=0
        z0=0
        x0=0
    mov2.at[i, 'pitches_thrown'] = p2+p1+p0
    mov2.at[i, 'pitcher_break_z'] = (p2*z2+p1*z1+p0*z0)/(p2+p1+p0)
    mov2.at[i, 'pitcher_break_x'] = (p2*x2+p1*x1+p0*x0)/(p2+p1+p0)
    
    mov1.drop(mov1.index[row1[0]])
    mov0.drop(mov0.index[row0[0]])

for i in range(len(mov1)):
    id1 = mov1.iloc[i]['pitcher_id']
    p_type1 = mov1.iloc[i]['pitch_type_name']
    row0 = np.where((mov0['pitcher_id']==id2) & (mov0['pitch_type_name']==p_type2))
    
    p1 = mov1.iloc[row1[0][0]]['pitches_thrown']
    z1 = mov1.iloc[row1[0][0]]['pitcher_break_z']
    x1 = mov1.iloc[row1[0][0]]['pitcher_break_x']
    if len(row0[0]) > 0:
        p0 = mov0.iloc[row0[0][0]]['pitches_thrown']
        z0 = mov0.iloc[row0[0][0]]['pitcher_break_z']
        x0 = mov0.iloc[row0[0][0]]['pitcher_break_x']
    else:
        p1=0
        z1=0
        x1=0
    mov1.at[i, 'pitches_thrown'] = p1+p0
    mov1.at[i, 'pitcher_break_z'] = (p1*z1+p0*z0)/(p1+p0)
    mov1.at[i, 'pitcher_break_x'] = (p1*x1+p0*x0)/(p1+p0)
    
    mov0.drop(mov0.index[row0[0]])
    
mov2 = mov2.append(mov1, ignore_index=True)
mov2 = mov2.append(mov0, ignore_index=True)

empties = np.where(mov2['pitcher_break_x']==0)
mov2.drop(mov2.index[empties[0]])
# mov2['movement_ratio'] = mov2['pitcher_break_x']/mov2['pitcher_break_z']

features = ['spin_rate', 'active_spin', 'diff_clock_label', 'release_speed', 'movement_inches']
for i in range(len(mov2)):
    id = mov2.iloc[i]['pitcher_id']
    p_type = mov2.iloc[i]['pitch_type_name']
    row = np.where((data['player_id']==id) & (data['api_pitch_type']==p_type))
    for f in features:
        mov2.at[i,f] = data.iloc[row[0][0]][f]

mov2.to_csv('full_data.csv', index=False)