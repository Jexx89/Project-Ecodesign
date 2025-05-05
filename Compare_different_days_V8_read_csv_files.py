# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 15:50:48 2023

@author: Marcello Nitti

THIS SCRIPT LOAD THE SAVED VECTOR AND PLOT THEM ON THE SAME GRAPH
"""

#%% THIS SECTION IS FOR IMPORTING SEVERAL PACKAGES

import numpy as np # importing numpy library
import os # importing the correct separator between folder and files depending on the operating system

import pandas as pd # importing pandas dataframe
import time
import datetime

import CLASS_import_csv_txt as rd_csv
impt_csv_txt_obj = rd_csv.impt_files()

import CLASS_res_timing as adj_t_ax
impt_adj_t_ogj = adj_t_ax.timing_reset()

from tqdm import tqdm # showing how long a for loop usually takes

import plotly.graph_objects as go # importing plotly for plotting figures
from plotly.offline import plot
from plotly.subplots import make_subplots # importing subplots to plot several curves in the same graph

# %% THIS SECTION LOADS THE DIFFERENT ARRAYS

# test_num = [["HM", "70kW", "HM70TC", "24078", "C", 2, "SEEB", 0],
#             ["HM", "70kW", "HM70TC", "24078", "D", 2, "SEEB", 0]]

# test_num = [["HM", "70kW", "HM70TC", "24078", "O", 6, "SEEB", 267],
#             ["HM", "70kW", "HM70TC", "24078", "P", 6, "SEEB", 0]]

# test_num = [["HM", "70kW", "HM70TC", "24078", "N", 6, "SEEB", 716],
#             ["HM", "70kW", "HM70TC", "24122", "E", 1, "SEEB", 0],
#             ["HM", "70kW", "HM70TC", "24122", "F", 4, "SEEB", -330],
#             ["HM", "70kW", "HM70TC", "24122", "G", 5, "SEEB", -388]]

# test_num = [["HM", "70kW", "HM70TC", "24122", "A", 1, "SEEB", 0],
#             ["HM", "70kW", "HM70TC", "24122", "B", 2, "SEEB", 0],
#             ["HM", "70kW", "HM70TC", "24122", "C", 1, "SEEB", 0]]

# test_num = [["HM", "70kW", "HM70TC", "24078", "N", 6, "SEEB", 515],
#             ["HM", "70kW", "HM70TC", "24122", "J", 7, "SEEB", 0]]

# test_num = [["HM", "70kW", "HM70TC", "24122", "G", 5, "SEEB", 334],
#             ["HM", "70kW", "HM70TC", "24122", "Q", 9, "SEEB", 0]]

# test_num = [["HM", "120kW", "HM120TC", "24108", "A", 1, "microPLAN", 0],
#             ["HM", "120kW", "HM120TC", "24108", "B", 2, "microPLAN", 0]]

# test_num = [["HM", "45XkW", "HM45XTC", "24082", "A", 1, "SEEB", 0],
#             ["HM", "45XkW", "HM45XTC", "24082", "B", 2, "SEEB", 552]]   #591 to have tapping sincronised

# test_num = [["HM", "45XkW", "HM45XTC", "24077", "K", 6, "microPLAN", 100],
#             ["HM", "45XkW", "HM45XTC", "24077", "L", 7, "microPLAN", 0],
#             ["HM", "45XkW", "HM45XTC", "24082", "B", 2, "SEEB", 3256]]

# test_num = [["HM", "25XkW", "HM25XTC", "24092", "C", 1, "SEEB", 474],
#             ["HM", "25XkW", "HM25XTC", "24092", "D", 3, "SEEB", 0]]

# test_num = [["HM", "120kW", "HM120TC", "24108", "C", 3, "microPLAN", 0], 
#             ["HM", "120kW", "HM120TC", "24108", "D", 4, "microPLAN", 0]]

# test_num = [["HM", "120kW", "HM120TC", "24108", "J", 9, "microPLAN", 0], 
#             ["HM", "120kW", "HM120TC", "24108", "K", 10, "microPLAN", 54]] 

# test_num = [["HM", "120kW", "HM120TC", "24108", "L", 11, "microPLAN", 0], 
#             ["HM", "120kW", "HM120TC", "25017", "A", 1, "microPLAN", 70]] 

# test_num = [["HM", "120kW", "HM120TC", "24108", "L", 11, "microPLAN", 0], 
#             ["HM", "120kW", "HM120TC", "24108", "M", 11, "SEEB", 657],
#             ["HM", "120kW", "HM120TC", "25017", "A", 1, "microPLAN", 70]] 

# test_num = [["HM", "85kW", "HM85TC", "25021", "B", 2, "microPLAN", 0],
#             ["HM", "85kW", "HM85TC", "25021", "C", 3, "microPLAN", 0]]

# test_num = [["HM", "85kW", "HM85TC", "25021", "B", 2, "microPLAN", 10],
#             ["HM", "85kW", "HM85TC", "25021", "D", 2, "microPLAN", 0],
#             ["HM", "85kW", "HM85TC", "25021", "E", 4, "microPLAN", -38]]

#TO SINC THE BURNER OF THE FIRST CYCLE USE THE FOLLOWING SECONDS: 80 - 70 - 32

# test_num = [["HM", "85kW", "HM85TC", "25021", "H", 7, "microPLAN", 0],
#             ["HM", "85kW", "HM85TC", "25021", "M", 7, "microPLAN", 0]]

# test_num = [["HM", "85kW", "HM85TC", "25021", "O", 11, "microPLAN", 0],
#             ["HM", "85kW", "HM85TC", "25021", "P", 12, "microPLAN", 36]]

# test_num = [["HM", "85kW", "HM85TC", "25021", "P", 12, "microPLAN", 20],
#             ["HM", "85kW", "HM85TC", "25021", "Q", 13, "microPLAN", 0]]

# test_num = [["HM", "25XkW", "HM25XTC", "24079", "C", 3, "microPLAN", 0],
#             ["HM", "25XkW", "HM25XTC", "24092", "E", 4, "SEEB", 2052]]

####KIWA tests
# test_num = [["HM", "35kW", "HM35TC", "24074", "B", 3, "microPLAN", 704],
#             ["HM", "35kW", "HM35TC", "24058", "D", 3, "SEEB", 1761]]

# test_num = [["HM", "120kW", "HM120TC", "24064", "F", 1, "microPLAN", 0],
#             ["HM", "120kW", "HM120TC", "24064", "G", 2, "microPLAN", 0]]

# test_num = [["HM", "45XkW", "HM45XTC", "24077", "C", 3, "microPLAN", 0],
#             ["HM", "45XkW", "HM45XTC", "24077", "D", 3, "microPLAN", 0]]

# test_num = [["HM", "60kW", "HM60TC", "25028", "D", 4, "SEEB", 207],
#             ["HM", "60kW", "HM60TC", "25028", "E", 5, "SEEB", 0]]

# test_num = [["HM", "60kW", "HM60TC", "25028", "E", 5, "SEEB", 0],
#             ["HM", "60kW", "HM60TC", "25028", "F", 6, "SEEB", 264]]

# test_num = [["HM", "60kW", "HM60TC", "25028", "F", 6, "SEEB", 155],
#             ["HM", "60kW", "HM60TC", "25028", "G", 7, "SEEB", 0]]

# test_num = [["HM", "60kW", "HM60TC", "25028", "I", 8, "SEEB", 909],
#             ["HM", "60kW", "HM60TC", "25013", "A", 1, "microPLAN", 0]]

# test_num = [["HM", "70kW", "HM70TC", "25027", "A", 7, "SEEB", 0],
#             ["HM", "70kW", "HM70TC", "25066", "D", 2, "SEEB", 24]]
test_num = [["HM", "35kW", "HM35TC", "24123", "C", 3, "microPLAN", 0],
             ["HM", "35kW", "HM35TC", "25063", "H", 1, "microPLAN", 102]]
             
# test_num = [["HM", "70kW", "HM70TC", "25027", "A", 3, "SEEB", 0], # si le test 1 est devant alors on avance l'autre
#              ["HM", "70kW", "HM70TC", "25066", "H", 1, "SEEB", 392]] #si le test 2 est devant alors on avance l'autre

Plt_MiPLAN = "Yes" # [Yes or No] - Sting type. Variable to define if we have to load MicroPLAN data and plot them
Plt_SEEB = "No" # [Yes or No] - Sting type. Variable to define if we have to load SEEB data and plot them
Plt_MiCOM = "Yes" # [Yes or No] - Sting type. Variable to define if we have to load MicroCOM data and plot them
Plt_DHW = "No" # [Yes or No] - Sting type. Variable to define if we have to load FieldLogger data and plot them
Plt_Side_T = "No" # [Yes or No] - Sting type. Variable to define if we have to load thermocouples data and plot them
Plt_PLC = "No" # [Yes or No] - Sting type. Variable to define if we have to load PLC data and plot them

microPLAN_data_prm_ax = [
    ["_Test_T_in_DHW","T°in DHW [°C]"], # Inlet temperature coming from the grid [°C]
    ["_Test_T_out_avg","T°out AV.  [°C]"], # Average outlet temperature for the domestic hot water [°C]
    ["_Test_T_fume_mPLAN","T°Fume [°C]"], # Outlet temperature of the smoke exiting the Heat Master [°C]
    ["_Test_flow_DHW_L/min","FLDHW [L/min]"], # Water flow [L/min]
    ["_Test_flow_DHW_kg/min","FLDHW [kg/min]"], # Water flow [kg/min]. This is the flow corrected with the density and Cp. It is not computed if the value is less than 0.5. It will be considered as 0.
    ["_Test_T_Amb","T°Amb [°C]"]
] # Vector names of microPLAN to be loaded and plotted on the primary axes

microCOM_data_prm_ax = [
    ["_Test_T_sup","Supply [°C]"], # Temperature on the main tank [°C]
    ["_Test_T_ret","Return [°C]"], # Temperature on the pump pipe to cool down the burner [°C]
    ["_Test_T_DHW_stor_t","DHW stor (°C)"], # Temperature inside the big ballon [°C]
    ["_Test_Flame_current","Flame Curent [uA]"], # Flame current [A] * 10^-6
    ["_Test_T_fume_mCOM","Flue temp [0,01°C]"], # Temperature on the fume [°C]
    ["_Test_Burn_mod","Actual measured load"] # Burner modulation
] # Vector names of microCOM to be loaded and plotted on the primary axes

microPLAN_data_scd_ax = [
    ["_Test_Gas_vol_consp","Cumul. Gaz Vol. Corr.[L]"], # Volume of gas consumption [L]
    # ["_Test_Power_consp","Power Absorbed [W]"], # Energy consumption of the whole electronic: fan, pump and boards [W]
    ["_Test_P_valv_in","pin DHW [bar]"], # Pressure of the inlet valve [bar]
    ["_Test_P_ATM","patm [mbar]"]
] # Vector names to be loaded on the secondary axes

SEEB_data_prm_ax = [
    ["_Test_T_in_DHW","T°in DHW [°C]"], # Inlet temperature coming from the grid [°C]
    ["_Test_T_out_avg","T°out TC  [°C]"], # Average outlet temperature for the domestic hot water [°C]
    ["_Test_T_fume_SEEB","T°Fume [°C]"], # Outlet temperature of the smoke exiting the Heat Master [°C]
    ["_Test_flow_DHW_kg/min","FLDHW [kg/min]"], # Water flow [m^3/h] of the first valve
    ["_Test_flow_DHW_L/min","FLDHW [l/min]"], # Water flow [L/min] of the second valve
    ["_Test_T_Amb","T°Amb [°C]"]
] # Vector names to be loaded on the secondary axes

SEEB_data_sdc_ax = [
    ["_Test_Gas_vol_L","Cumul. Gaz Vol. Corr.[L]"], # Counter of amount of gas consumed when burner is on [L]
    ["_Test_P_val_in","pin DHW [bar]"], # Pressure of the inlet valve [bar]
    ["_Test_P_ATM","patm [mbar]"]
] # Vector names to be loaded on the secondary axes

# SEEB_data_prm_ax = [
#     ["_Test_T_in_DHW","TE1"], # Inlet temperature coming from the grid [°C]
#     ["_Test_T_out_avg","TE2"], # Average outlet temperature for the domestic hot water [°C]
#     ["_Test_T_fume_SEEB","TF1"], # Outlet temperature of the smoke exiting the Heat Master [°C]
#     ["_Test_flow_DHW_val1","DE1"], # Water flow [m^3/h] of the first valve
#     ["_Test_flow_DHW_val2","DE2"], # Water flow [m^3/h] of the second valve
#     ["_Test_By_pass_val_ON","EVE6"], # Counter 0-1 to know when the by-pass valve is on
#     ["_Test_Tap_val_ON","EVE7"] # Counter 0-1 to know when the tapping valve is on
# ] # Vector names to be loaded on the secondary axes

# SEEB_data_sdc_ax = [
#     ["_Test_Gas_vol","DG1"], # Total amount of gas consumed during the three days [m^3]
#     ["_Test_Gas_counter_L","DebitGaz_DG1"], # Counter of amount of gas consumed when burner is on [m^3/h]
#     ["_Test_P_val_in","PE1"] # Pressure of the inlet valve [bar]
# ] # Vector names to be loaded on the secondary axes

# DHW_sens_data = [
#     ["_Test_T1_top [°C]","T1 Top"],
#     ["_Test_T2 [°C]","T2"],
#     ["_Test_T3 [°C]","T3"],
#     ["_Test_T4 [°C]","T4"],
#     ["_Test_T5_bottom [°C]","T5 Bottom"]
# ]

DHW_sens_data = [
    ["_Test_T1_top [°C]","T1 Top"],
    ["_Test_T2 [°C]","T2"],
    ["_Test_T3 [°C]","T3"],
    ["_Test_T4 [°C]","T4"],
    ["_Test_T5 [°C]","T5"],
    ["_Test_T6 [°C]","T6"],
    ["_Test_T7_bottom [°C]","T7 bas"]
]

# DHW_sens_data = [
#     ["_Test_T1_bottom [°C]","T1 bas"],
#     ["_Test_T2 [°C]","T2"],
#     ["_Test_T3 [°C]","T3"],
#     ["_Test_T4 [°C]","T4"],
#     ["_Test_T5_top [°C]","T5 haut"]
# ]

side_T_data = [
    ["_Test_CH1 [°C]","CH1"],
    ["_Test_CH2 [°C]","CH2"],
    ["_Test_CH3 [°C]","CH3"],
    ["_Test_CH4 [°C]","CH4"],
    ["_Test_CH5 [°C]","CH5"],
    ["_Test_CH6 [°C]","CH6"],
    ["_Test_CH7 [°C]","CH7"],
    ["_Test_CH8 [°C]","CH8"],
    ["_Test_CH9 [°C]","CH9"]
    # ["_Test_CH10 [°C]","CH10"],
    # ["_Test_CH11 [°C]","CH11"],
    # ["_Test_CH12 [°C]","CH12"],
    # ["_Test_CH13 [°C]","CH13"],
    # ["_Test_CH14 [°C]","CH14"],
    # ["_Test_CH15 [°C]","CH15"]
    # ["_Test_CH16 [°C]","CH16"]
]


PLC_data = [
    # ["_Test_T_sup","SUPPLY DEG"],
    # ["_Test_T_ret","RETURN DEG"],
    # ["_Test_T_DHW_stor_t","DHW DEG"],
    # ["_Test_Flame_current","FLAME µA"],
    # ["_Test_T_fume_PLC","FLUE DEG"],
    # ["_Test_Burn_mod","MICROCOM Mod."],
    ["_Test_ON/OFF Pump","PUMP"],
    ["_Test_Pump setpoint [°C]","PUMP SP"],
    ["_Test_Pump speed [%]","PUMP SPEED %"]
]

all_dict_prm_ax_mPLAN = {} # Creating a dictionary to store all the other dictionary
all_dict_scd_ax_mPLAN = {} # Creating a dictionary to store all the other dictionary
all_dict_prm_ax_SEEB = {} # Creating a dictionary to store all the other dictionary
all_dict_scd_ax_SEEB = {} # Creating a dictionary to store all the other dictionary
all_dict_prm_ax_mCOM = {} # Creating a dictionary to store all the other dictionary
all_dict_DHW_sens = {} # Creating a dictionary to store all the other dictionary
all_dict_side_T = {} # Creating a dictionary to store all the other dictionary
all_dict_PLC = {} # Creating a dictionary to store all the other dictionary
all_dict_time = {} # Creating a dictionary to store all the other dictionary
all_dict_corr_time = {} # Creating a dictionary to store all the other dictionary

for i in tqdm(test_num, desc="ESTIMATOR LOOP 1"):

    fol_path = i[0] + os.sep + i[1] + os.sep + i[3] + i[4]

    # file_name_microPLAN = i[3] + i[4] + "_XXL_" + i[2] + "_Algo" + str(i[5]) + "_Microplan_Log"
    # file_name_SEEB = i[3] + i[4] + "_XXL_" + i[2] + "_Algo" + str(i[5]) + "_SEEB_Enr5"
    # file_name_microCOM = i[3] + i[4] + "_XXL_" + i[2] + "_Algo" + str(i[5]) + "_Microcom"
    # file_name_DHW = i[3] + i[4] + "_XXL_" + i[2] + "_Algo" + str(i[5]) + "_DHW_Temperature"
    # file_name_side_T = i[3] + i[4] + "_XXL_" + i[2] + "_Algo" + str(i[5]) + "_Side_Temperature"
    # file_name_PLC = i[3] + i[4] + "_XXL_" + i[2] + "_Algo" + str(i[5]) + "_PLC"
    file_name_microPLAN = i[3] + i[4] + "_XXL_" + i[2] + "_Microplan_Log"
    file_name_SEEB = i[3] + i[4] + "_XXL_" + i[2] + "_SEEB_Enr5"
    file_name_microCOM = i[3] + i[4] + "_XXL_" + i[2] + "_Microcom"
    file_name_DHW = i[3] + i[4] + "_XXL_" + i[2] + "_DHW_Temperature"
    file_name_side_T = i[3] + i[4] + "_XXL_" + i[2] + "_Side_Temperature"
    file_name_PLC = i[3] + i[4] + "_XXL_" + i[2] + "_PLC"
    if i[6] == "microPLAN":
        
        dt_microPLAN = impt_csv_txt_obj.read_csv_file_v2(fol_path,file_name_microPLAN,",")
    
    elif i[6] == "SEEB":
        
        # dt_SEEB = impt_csv_txt_obj.read_csv_file_v2(fol_path,file_name_SEEB,"\t")
        dt_SEEB = impt_csv_txt_obj.read_csv_file_v2(fol_path,file_name_SEEB,",")
    
    dt_microCOM = impt_csv_txt_obj.read_csv_file_v2(fol_path,file_name_microCOM,",")
    # dt_DHW = impt_csv_txt_obj.read_csv_file_v2(fol_path,file_name_DHW,",")
    # # dt_side_T = impt_csv_txt_obj.read_csv_file_v2(fol_path,file_name_side_T,",")
    # dt_PLC = impt_csv_txt_obj.read_csv_file_v2(fol_path,file_name_PLC,",")
    
    dict_stor_prm_ax_mPLAN = {} # Create an empty dictionary where storing the loading variables
    dict_stor_scd_ax_mPLAN = {} # Create an empty dictionary where storing the loading variables
    dict_stor_prm_ax_SEEB = {} # Create an empty dictionary where storing the loading variables
    dict_stor_scd_ax_SEEB = {} # Create an empty dictionary where storing the loading variables
    dict_stor_prm_ax_mCOM = {} # Create an empty dictionary where storing the loading variables
    dict_stor_DHW_sens = {} # Create an empty dictionary where storing the loading variables
    dict_stor_side_T = {} # Create an empty dictionary where storing the loading variables
    dict_stor_PLC = {} # Create an empty dictionary where storing the loading variables
    dict_stor_time_ax = {} # Create an empty dictionary where storing the loading variables
    dict_stor_corr_time_ax = {} # Create an empty dictionary where storing the loading variables

    dict_stor_corr_time_ax["Time_microPLAN"] = [] # inizialising the dict with an empty list in order to have a comparison if the vector does not exist
    dict_stor_corr_time_ax["Time_SEEB"] = [] # inizialising the dict with an empty list in order to have a comparison if the vector does not exist

    if i[6] == "microPLAN":

        for j in tqdm(microPLAN_data_prm_ax, desc="ESTIMATOR LOOP 2"):

            dict_stor_prm_ax_mPLAN[i[0] + "_" + i[4] + j[0]] = dt_microPLAN[j[1]]
            dict_stor_prm_ax_mPLAN["Delta_T_norm_test_Test_" + i[4]] = dt_microPLAN["T°out AV.  [°C]"] - dt_microPLAN["T°in DHW [°C]"]

        for l in tqdm(microPLAN_data_scd_ax, desc="ESTIMATOR LOOP 3"):

            dict_stor_scd_ax_mPLAN[i[0] + "_" + i[4] + l[0]] = dt_microPLAN[l[1]]
    
    elif i[6] == "SEEB":

        for p in tqdm(SEEB_data_prm_ax, desc="ESTIMATOR LOOP 4"):

            dict_stor_prm_ax_SEEB[i[0] + "_" + i[4] + p[0]] = dt_SEEB[p[1]]
            # dict_stor_prm_ax_SEEB["Delta_T_norm_test_Test_" + i[4]] = dt_SEEB["TE2"] - dt_SEEB["TE1"]
            dict_stor_prm_ax_SEEB["Delta_T_norm_test_Test_" + i[4]] = dt_SEEB["T°out TC  [°C]"] - dt_SEEB["T°in DHW [°C]"]

        for q in tqdm(SEEB_data_sdc_ax, desc="ESTIMATOR LOOP 5"):

            dict_stor_scd_ax_SEEB[i[0] + "_" + i[4] + q[0]] = dt_SEEB[q[1]]

        # dict_stor_prm_ax_SEEB [i[0] + "_" + i[4] + "_Test_flow_DHW_val1"] = dict_stor_prm_ax_SEEB[i[4] + "_Test_flow_DHW_val1"]*1000/60
        # dict_stor_prm_ax_SEEB [i[0] + "_" + i[4] + "_Test_flow_DHW_val2"] = dict_stor_prm_ax_SEEB[i[4] + "_Test_flow_DHW_val2"]*1000/60
        # dict_stor_scd_ax_SEEB [i[0] + "_" + i[4] + "_Test_Gas_vol"] = (dict_stor_scd_ax_SEEB[i[4] + "_Test_Gas_vol"] - dict_stor_scd_ax_SEEB[i[4] + "_Test_Gas_vol"][14000])*1000
        # dict_stor_scd_ax_SEEB [i[0] + "_" + i[4] + "_Test_Gas_counter_L"] = dict_stor_scd_ax_SEEB[i[4] + "_Test_Gas_counter_L"]*1000/3600
        # dict_stor_prm_ax_SEEB [i[0] + "_" + i[4] + "_Test_By_pass_val_ON"] = dict_stor_prm_ax_SEEB[i[4] + "_Test_By_pass_val_ON"]*50
        # dict_stor_prm_ax_SEEB [i[0] + "_" + i[4] + "_Test_Tap_val_ON"] = dict_stor_prm_ax_SEEB[i[4] + "_Test_Tap_val_ON"]*50

    for k in tqdm(microCOM_data_prm_ax, desc="ESTIMATOR LOOP 6"):

        dict_stor_prm_ax_mCOM[i[0] + "_" + i[4] + k[0]] = dt_microCOM[k[1]]

    # for m in tqdm(DHW_sens_data, desc="ESTIMATOR LOOP 7"):

    #     dict_stor_DHW_sens[i[0] + "_" + i[4] + m[0]] = dt_DHW[m[1]]

    # # for n in tqdm(side_T_data, desc="ESTIMATOR LOOP 8"):

    # #     dict_stor_side_T[i[0] + "_" + i[4] + n[0]] = dt_side_T[n[1]]

    # for o in tqdm(PLC_data, desc="ESTIMATOR LOOP 9"):

    #     dict_stor_PLC[i[0] + "_" + i[4] + o[0]] = dt_PLC[o[1]]

# most probably we can put this if cycle with the one above. It will make code easier

    if i[6] == "microPLAN":
        
        dict_stor_time_ax["Time_microPLAN"] = dt_microPLAN["Timestamp"]

        day_0 = pd.to_datetime(dt_microPLAN["Timestamp"][0],dayfirst="True")

        dict_stor_corr_time_ax["Time_microPLAN"] = impt_adj_t_ogj.res_timing_comparison_bypass(dt_microPLAN,"Timestamp",day_0,i[7])
        
    elif i[6] == "SEEB":

        dict_stor_time_ax["Time_SEEB"] = dt_SEEB["Timestamp"]
        # dict_stor_time_ax["Time_SEEB"] = dt_SEEB["Date Time"]
        # dict_stor_time_ax["Time_SEEB"] = dt_SEEB["Unnamed: 0"]

        day_0 = pd.to_datetime(dt_SEEB["Timestamp"][0],dayfirst="True")
        # day_0 = pd.to_datetime(dt_SEEB["Date Time"][0],dayfirst="True")
        # day_0 = pd.to_datetime(dt_SEEB["Unnamed: 0"][0],dayfirst="True")

        # dict_stor_corr_time_ax["Time_SEEB"] = impt_adj_t_ogj.res_timing_comparison_bypass(dt_SEEB,"Unnamed: 0",day_0,i[7])
        # dict_stor_corr_time_ax["Time_SEEB"] = impt_adj_t_ogj.res_timing_comparison_bypass(dt_SEEB,"Date Time",day_0,i[7])
        dict_stor_corr_time_ax["Time_SEEB"] = impt_adj_t_ogj.res_timing_comparison_bypass(dt_SEEB,"Timestamp",day_0,i[7])
    
    dict_stor_time_ax["Time_microCOM"] = dt_microCOM["Time DMY"]
    # dict_stor_time_ax["Time_DHW_sens"] = dt_DHW["Date-Time"]
    # # dict_stor_time_ax["Time_side_T"] = dt_side_T["Date&Time"]
    # dict_stor_time_ax["Time_PLC"] = dt_PLC["DATE-TIME"]

    dict_stor_corr_time_ax["Time_microCOM"] = impt_adj_t_ogj.res_timing_comparison_bypass(dt_microCOM,"Time DMY",day_0,i[7])
    # dict_stor_corr_time_ax["Time_DHW_sens"] = impt_adj_t_ogj.res_timing_comparison_bypass(dt_DHW,"Date-Time",day_0,i[7])
    # # dict_stor_corr_time_ax["Time_side_T"] = impt_adj_t_ogj.res_timing_comparison_bypass(dt_side_T,"Date&Time",day_0,i[7])
    # dict_stor_corr_time_ax["Time_PLC"] = impt_adj_t_ogj.res_timing_comparison_bypass(dt_PLC,"DATE-TIME",day_0,i[7])
    
    if i[6] == "microPLAN":

        all_dict_prm_ax_mPLAN["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_prm_ax_mPLAN
        all_dict_scd_ax_mPLAN["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_scd_ax_mPLAN

    elif i[6] == "SEEB":

        all_dict_prm_ax_SEEB["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_prm_ax_SEEB
        all_dict_scd_ax_SEEB["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_scd_ax_SEEB
    
    all_dict_prm_ax_mCOM["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_prm_ax_mCOM
    all_dict_DHW_sens["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_DHW_sens
    # all_dict_side_T["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_side_T
    all_dict_PLC["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_PLC
    all_dict_time["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_time_ax
    all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_corr_time_ax

    if len(dict_stor_corr_time_ax["Time_microPLAN"]) > len(dict_stor_corr_time_ax["Time_SEEB"]):

        tm_ax_T_45 = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_microPLAN"]

    elif len(dict_stor_corr_time_ax["Time_SEEB"]) > len(dict_stor_corr_time_ax["Time_microPLAN"]):

        tm_ax_T_45 = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_SEEB"]

    x_val_str_line = max(len(dict_stor_corr_time_ax["Time_microPLAN"]),len(dict_stor_corr_time_ax["Time_SEEB"]))


#%% THIS SECTION PLOTS THE VALUES

# def trace_fig(x_axis,y_axis,name,secd_y_ax,opac,typ_line):

#     """
#     Function to add the trace on the graphs

#     Parameters
#     -----------------

#     x: array
#         Array with values to be plotted on the x axis
#     y: array
#         Array with values to be plotted on the y axis
#     name: string
#         Name of the curve to plot
#     col: string
#         Colour of the curve on the graph
#     secd_y_ax: Boolean
#         True or False. True: plotting on the secondary y axins. False: plot on the primary
#     opac: integer
#         Value from 0 to 1 to set the opacity of the line
#     typ_line: string
#         Set the line layout

#     Returns
#     -----------

#     The trace that can be added to the main figure plot

#     """

#     # Adding the trace
#     fig.add_trace(go.Scatter
#                   (x = x_axis,
#                    y = y_axis,
#                    name = name,
#                    opacity = opac,
#                 #    mode = typ_line,
#                 #    marker = {"color" : col}),
#                 #    line = dict(color=col, width=1.5, dash=typ_line)),
#                    line = dict(width=1.5, dash=typ_line)),
#                    secondary_y=secd_y_ax,
#                 )



def trace_fig(x_axis,y_axis,group,gourp_ttl,name,secd_y_ax,opac,typ_line):

    """
    Function to add the trace on the graphs

    Parameters
    -----------------

    x: array
        Array with values to be plotted on the x axis
    y: array
        Array with values to be plotted on the y axis
    name: string
        Name of the curve to plot
    col: string
        Colour of the curve on the graph
    secd_y_ax: Boolean
        True or False. True: plotting on the secondary y axins. False: plot on the primary
    opac: integer
        Value from 0 to 1 to set the opacity of the line
    typ_line: string
        Set the line layout

    Returns
    -----------

    The trace that can be added to the main figure plot

    """
    
    # Adding the trace
    fig.add_trace(go.Scatter
                  (x = x_axis,
                   y = y_axis,
                   yaxis="y",
                   legendgroup=group,
                   legendgrouptitle_text=gourp_ttl,
                   name = name,
                   opacity = opac,
                #    mode = typ_line,
                #    marker = {"color" : col}),
                   line = dict(width=1.5, dash=typ_line)),
                   secondary_y=secd_y_ax,
                )



def update_lay_fig(
        lab_x_ax,
        lab_prim_y_ax_,
        lab_sec_y_ax_,
        txt_size_num_ax,
        txt_siz_lbl_xy,
        txt_siz_leg,
        title,
        txt_siz_tit):

    """
    Function to edit the layout of the figure

    Parameters
    -----------------

    lab_x_ax: string
        Lable of the x axis
    lab_prim_y_ax_: string
        Lable of the primary y axis
    lab_sec_y_ax_: string
        Lable of the seconday y axis
    txt_size_num_ax: int
        Size of the x and y values
    txt_siz_lbl_xy: int
        Size of the x and y axis lable
    txt_siz_leg: int
        Size of legend
    title: string
        Title of the graph
    txt_siz_tit: string
        Size of the title

    Returns
    -----------

    The editated trace of the graph

    """

    # Editing the layout
    fig.update_layout(template="simple_white")
    
    fig.update_xaxes(
        title=lab_x_ax,
        title_font={"size": txt_siz_lbl_xy}
        )
    
    fig.update_yaxes(
        title=lab_prim_y_ax_,
        title_font={"size": txt_siz_lbl_xy},
        secondary_y=False
        )  # ,type = "log"
    
    fig.update_yaxes(
        title=lab_sec_y_ax_,
        title_font={"size": txt_siz_lbl_xy},
        # range=[0, 9000],
        secondary_y=True,
        )  # ,type = "log"
    

    fig.update_xaxes(spikemode="toaxis+across") # "toaxis" (will stop at the height of the mouse) / "across" goes for the whole lenght
    fig.update_xaxes(spikesnap="hovered data")
    fig.update_layout(hovermode="x") # "x" lables appear with each colour. "x unified" one unique box that groups all the lable

    # fig.update_xaxes(range=[0, 3000])
    # fig.update_layout(xaxis_range=['2023-11-30','2023-12-03'])

    # fig.update_layout(xaxis_range=[datetime.datetime(2023, 12, 1),
    #                                datetime.datetime(2023, 12, 4)])

    # fig.update_xaxes(rangeslider_visible=True) # This add on the bottom the whole graph where you can see at what point are you if you zoom in
    
    fig.update_layout(yaxis=dict(tickfont=dict(size=txt_size_num_ax)))
    # fig.update_layout(yaxis={'visible': True, 'showticklabels': False})
    fig.update_layout(xaxis=dict(tickfont=dict(size=txt_size_num_ax)))
    fig.update_layout(legend=dict(font=dict(size=txt_siz_leg)))
    # fig.update_layout(
        # legend=dict(
            # orientation="h",
            # yanchor="top",
            # y=1.065,
            # xanchor="left",
            # x=0.01)
            # )

    fig.update_layout(
        title=title,
        font_size=txt_siz_tit,
        # showlegend=False,
        )
    
    fig.update_layout(legend=dict(groupclick="toggleitem"))


#%% THIS SECTION SETS SOME PARAMETERS FOR THE PLOTTING CURVE

op_main_lin = 1 # Set the opacity of the main lines
op_sec_lin = 0.25 # Set the opacity of the secondary lines

lin_typ_1 = "solid"  # Line layout. if we use mode we have to write "lines" in order to have a continuous line
lin_type_2 = "dash"  # Line layout.

T_45 = np.ones(x_val_str_line)*45 # This is a straight line at 45 [°C] to see when we are below the delta T requested from the norm
T_30 = np.ones(x_val_str_line)*30 # This is a straight line at 30 [°C] to see when we are below the delta T requested from the norm

#%% THIS SECTION PLOT THE FIGURES

# tm_ax_microPLAN = all_dict_corr_time["dict_HM45TC_test_G"]["Time_microPLAN"]

# fig = make_subplots(specs=[[{"secondary_y": True}]])

# trace_fig(tm_ax_microPLAN,
#                     2,
#                     "MicroPLAN",
#                     "MicroPLAN",
#                     "Test_G",
#                     #   "darkblue",
#                     False,
#                     op_main_lin,lin_typ_1
#                     )

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

for i in test_num:

    if i[6] == "microPLAN":

        tm_ax_microPLAN = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_microPLAN"]
        tm_ax_microCOM = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_microCOM"]
        # tm_ax_DHW = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_DHW_sens"]
        # # tm_ax_side_T = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_side_T"]
        # tm_ax_PLC = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_PLC"]

        for key,value in all_dict_prm_ax_mPLAN["dict_" + i[2] + "_test_%s" %i[4]].items():
            trace_fig(tm_ax_microPLAN,
                    value,
                    i[2] + "_microPLAN_" + i[4] + "_Algo_" + str(i[5]),
                    i[6] + "_test_" + i[4] + "_Algo_" + str(i[5]),
                    key,
                    #   "darkblue",
                    False,
                    op_main_lin,lin_typ_1
                    )

        for key,value in all_dict_scd_ax_mPLAN["dict_" + i[2] + "_test_%s" %i[4]].items():
            trace_fig(tm_ax_microPLAN,
                    value,
                    i[2] + "_microPLAN_" + i[4] + "_Algo_" + str(i[5]),
                    i[6] + "_test_" + i[4] + "_Algo_" + str(i[5]),
                    key,
                    #   "darkblue",
                    True,
                    op_main_lin,lin_typ_1
                    )
        
    elif i[6] == "SEEB":

        tm_ax_SEEB = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_SEEB"]
        tm_ax_microCOM = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_microCOM"]
        # tm_ax_DHW = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_DHW_sens"]
        # # tm_ax_side_T = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_side_T"]
        # tm_ax_PLC = all_dict_corr_time["dict_" + i[2] + "_test_%s" %i[4]]["Time_PLC"]

        for key,value in all_dict_prm_ax_SEEB["dict_" + i[2] + "_test_%s" %i[4]].items():
            trace_fig(tm_ax_SEEB,
                    value,
                    i[2] + "_SEEB_" + i[4] + "_Algo_" + str(i[5]),
                    "SEEB_test_" + i[4] + "_Algo_" + str(i[5]),
                    key,
                    #   "darkblue",
                    False,
                    op_main_lin,lin_typ_1
                    )
        
        for key,value in all_dict_scd_ax_SEEB["dict_" + i[2] + "_test_%s" %i[4]].items():
            trace_fig(tm_ax_SEEB,
                    value,
                    i[2] + "_SEEB",
                    "SEEB_test_" + i[4] + "_Algo_" + str(i[5]),
                    key,
                    #   "darkblue",
                    True,
                    op_main_lin,lin_typ_1
                    )
    
    for key,value in all_dict_prm_ax_mCOM["dict_" + i[2] + "_test_%s" %i[4]].items():
            trace_fig(tm_ax_microCOM,
                    value,
                    i[2] + "_microCOM_" + i[4] + "_Algo_" + str(i[5]),
                    "microCOM_test_" + i[4] + "_Algo_" + str(i[5]),
                    key,
                    #   "cyan",
                    False,
                    op_main_lin,lin_typ_1
                    )

    # for key,value in  all_dict_DHW_sens["dict_" + i[2] + "_test_%s" %i[4]].items():
    #     trace_fig(tm_ax_DHW,
    #             value,
    #             i[2] + "_DHW_" + i[4] + "_Algo_" + str(i[5]) + "_" + i[6],
    #             "DHW_test_" + i[4] + "_Algo_" + str(i[5]),
    #             key,
    #             #   "cyan",
    #             False,
    #             op_main_lin,lin_typ_1
    #             )
            
    # for key,value in all_dict_side_T["dict_" + i[2] + "_test_%s" %i[4]].items():
    #     trace_fig(tm_ax_side_T,
    #             value,
    #             i[2] + "_Side_T_" + i[4] + "_Algo_" + str(i[5]) + "_" + i[6],
    #             "side_T_test_" + i[4] + "_Algo_" + str(i[5]),
    #             key,
    #             #   "cyan",
    #             False,
    #             op_main_lin,lin_typ_1
    #             )

    # for key,value in all_dict_PLC["dict_" + i[2] + "_test_%s" %i[4]].items():
    #     trace_fig(tm_ax_PLC,
    #             value,
    #             i[2] + "_PLC_T_" + i[4] + "_Algo_" + str(i[5]) + "_" + i[6],
    #             "PLC_test_" + i[4] + "_Algo_" + str(i[5]),
    #             key,
    #             #   "cyan",
    #             False,
    #             op_main_lin,lin_typ_1
    #             )
    
trace_fig(tm_ax_T_45,T_30,"Set","Settings","T = 30 [°C]",False,op_sec_lin,lin_type_2)
trace_fig(tm_ax_T_45,T_45,"Set","Settings","T = 45 [°C]",False,op_sec_lin,lin_type_2)


# Editing layout traces
update_lay_fig(
    "Test time [s]",
    "Temperature °C",
    "Gas Vol (L.)",
    22,
    22,
    16,
    "Comparison Tests",
    18
)
folderName = "Comparaison" + os.sep

def file_name_generation()->str:
    concatenate=""
    for x in test_num:
        concatenate += x[3] +"_" + x[4] + "_"
    return concatenate

plot(fig, filename = folderName + file_name_generation() + "Comparison_Tests.html")
# # plot(fig, filename = path + os.sep + name_test_descp + date_test_dur + ".html")
