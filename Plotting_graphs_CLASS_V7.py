# -*- coding: utf-8 -*-
"""
Created on Wed Dec 6 09:45:02 2023

@author: Marcello Nitti
"""

#%% THIS SECTION IS FOR IMPORTING SEVERAL PACKAGES

import numpy as np # importing numpy library
import os # importing the correct separator between folder and files depending on the operating system
# import plotly as pl
import pandas as pd # importing pandas dataframe
import time
import datetime

import CLASS_import_csv_txt as rd_csv
impt_csv_txt_obj = rd_csv.impt_files()

import CLASS_ext_df_data as df_data
df_dt = df_data.ext_data_dt()

import CLASS_res_timing as corr_time
adj_time = corr_time.timing_reset()

import CLASS_fig_settings as figures
plot_fig = figures.fig_set()

import plotly.graph_objects as go # importing plotly for plotting figures
from plotly.offline import plot
from plotly.subplots import make_subplots # importing subplots to plot several curves in the same graph


#%% THIS SECTION SET THE INPUT PARAMETERS FOR READING CSV FILES

# 23146_STRATEGIE_PID_LOG_FILT_DAY1      filter data day 1 - Use Scattergl
# 23146_STRATEGIE_PID_LOG                no filter data day 1 - Use Scatter

# A 1 30/11 04/12 - T_DHW = 50, T_ADD = 10, T_HYS = 3, T_FUM_MAX = NA
# B 2 04/12 07/12 - T_DHW = 50, T_ADD = 10, T_HYS = 3, T_FUM_MAX = NA
# C 3 07/12 11/12 - T_DHW = 55, T_ADD = 5, T_HYS = 3, T_FUM_MAX = NA
# D2 4 13/12 15/12 - T_DHW = 50, T_ADD = 10, T_HYS = 3, T_FUM_MAX = 28
# E 5 15/12 18/12 - T_DHW = 55, T_ADD = 10, T_HYS = 15, T_FUM_MAX = NA
# F 6 18/12 21/12 - T_DHW = 55, T_ADD = 10, T_HYS = 15, T_FUM_MAX = 30

test_num ="F" # The test number. It can be A, B, C, D, etc.
alg_typ = "6" # The algorithm type/number we use for the tests
test_descp_miplan = "Microplan_Log" # Microplan test description
test_descp_micom = "Microcom" # Microcom test description
test_descp_DHW = "DHW_Temperature" # DHW test description
test_descp_side_T = "Side_Temperature" # DHW test description
test_descp_PLC = "PLC" # PLC test description

path = "23146" + test_num
name_test_descp = path + "_XXL_HM70TC_Algo" + alg_typ
name_test_miplan = name_test_descp + "_" + test_descp_miplan
name_test_micom = name_test_descp + "_" + test_descp_micom
name_test_DHW = name_test_descp + "_" + test_descp_DHW
name_test_side_T = name_test_descp + "_" + test_descp_side_T
name_test_PLC = name_test_descp + "_" + test_descp_PLC

# get the start time
st = time.time()

if test_num == "C":
    
    dt_microplan = impt_csv_txt_obj.read_csv_file(path,name_test_miplan).dropna() # since the test is broken, there are sone NaN value. When we do the resampling time, pyhton explode
    dt_microcom = impt_csv_txt_obj.read_csv_file(path,name_test_micom).dropna()
    dt_DHW = impt_csv_txt_obj.read_csv_file(path,name_test_DHW).dropna()
    dt_side_T = impt_csv_txt_obj.read_csv_file(path,name_test_side_T).dropna()
    # dt_PLC = impt_csv_txt_obj.read_csv_file(path,name_test_PLC).dropna()

else:

    dt_microplan = impt_csv_txt_obj.read_csv_file(path,name_test_miplan)
    dt_microcom = impt_csv_txt_obj.read_csv_file(path,name_test_micom)
    dt_DHW = impt_csv_txt_obj.read_csv_file(path,name_test_DHW)
    dt_side_T = impt_csv_txt_obj.read_csv_file(path,name_test_side_T)
    # dt_PLC = impt_csv_txt_obj.read_csv_file(path,name_test_PLC)

# get the end time
et_rd_df = time.time()

# get the execution time
rd_time = et_rd_df - st

print("Finish reading data in " + str(rd_time) + " seconds")


#%% STORING DATAFRAME DATA IN SEVERAL VARIABLES

# get the start time
st_stor = time.time()

rec_time,t_st_rec_miplan,T_in_DHW,T_out_avg,T_out_PT100,T_out_TC1,T_out_TC3,T_fume,flow_DHW_kg,flow_DHW_L,Gas_vol,P_valv_in,Pow_cons,Cum_energy = df_dt.read_df_microPLAN(
                                                                    dt_microplan)

T_sup,T_ret,T_DHW_stor,Flame_current,T_fume_mc,Burn_mod = df_dt.read_df_microCOM(dt_microcom) # Storing the MICROCOM

T1, T2, T3, T4, T5 = df_dt.read_df_DHW_sens(dt_DHW) # Storing the DHW data

CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9 = df_dt.read_df_side_T(dt_side_T) # Storing the side temperature data

# pump_onoff,pump_stp,pump_speed = df_dt.read_df_PLC(dt_PLC) # Storing the PLC data

# get the end time
et_stor = time.time()

# get the execution time
stor_time = et_stor - st_stor

print("Finish storing data in " + str(stor_time) + " seconds")

#%% ADJUSTING TIMING VECTOR. PLOT THE DATA WITH THE CORRECT TIME DELAY AND MATCH THE MICROPLAN DATASET

add_cor_time_miPLAN = adj_time.res_timing(dt_microplan,"Timestamp",t_st_rec_miplan)
add_cor_time_miCOM = adj_time.res_timing(dt_microcom,"Time DMY",t_st_rec_miplan)
add_cor_time_DHW = adj_time.res_timing(dt_DHW,"Date-Time",t_st_rec_miplan)
add_cor_time_side_T = adj_time.res_timing(dt_side_T,"Date&Time",t_st_rec_miplan)
# add_cor_time_PLC = adj_time.res_timing(dt_PLC,"DATE-TIME",t_st_rec_miplan)

#%% EXTRACTING THE STARTING AND ENDING DATE OF THE TESTS

rec_time_dt = pd.to_datetime(dt_microplan["Timestamp"],dayfirst="True") # Recording time array
st_y = str(rec_time_dt.dt.year[0]) # Year when we start recording
st_m = str(rec_time_dt.dt.month[0]) # Month when we start recording
st_day = str(rec_time_dt.dt.day[0]) # Day when we start recording
end_y = str(rec_time_dt.dt.year[len(rec_time_dt)-1]) # Year when we end recording
end_m = str(rec_time_dt.dt.month[len(rec_time_dt)-1]) # Month when we end recording
end_day = str(rec_time_dt.dt.day[len(rec_time_dt)-1]) # Day when we end recording
date_test_dur = "_" + st_y + "_" + st_m + "_" + st_day + "_" + end_y + "_" + end_m + "_" + end_day

#%% THIS SECTION HAS THE SETTED CONDITIONS FOR THE TESTS

T_DHW_SP = np.ones(len(T_out_avg))*55  # This is temperature setpoint for DHW [°C]
T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
T_CH = T_DHW_SP + T_ADD # This is the temperature setpoint for CH or primary water or supply temperature [°C]

Hyst = 15  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
Burn_ON = np.ones(len(T_out_avg))*(T_DHW_SP - Hyst)

T_45 = np.ones(len(T_out_avg))*45 # This is a straight line at 45 [°C] to see when we are below the delta T requested from the norm
T_30 = np.ones(len(T_out_avg))*30 # This is a straight line at 30 [°C] to see when we are below the delta T requested from the norm

delta_T_req = T_out_avg - T_in_DHW # Delta T required by the norm between T DHW out and T DHW [°C]
delta_T_boil = T_sup - T_ret # Delta T between T supply and T of the pump [°C]

#%% THIS SECTION SETS SOME PARAMETERS FOR THE PLOTTING CURVE

op_main_lin = 1 # Set the opacity of the main lines
op_sec_lin = 0.25 # Set the opacity of the secondary lines

lin_typ_1 = "solid"  # Line layout. if we use mode we have to write "lines" in order to have a continuous line
lin_type_2 = "dash"  # Line layout.


#%% THIS SECTION PLOT THE FIGURES

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
plot_fig.trace_fig(add_cor_time_miPLAN,T_in_DHW,"T in DHW [°C]","cyan",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,T_out_avg,"T out avg [°C]","red",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,T_out_PT100,"T out PT100 [°C]","maroon",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,T_out_TC1,"T out TC1 [°C]","olivedrab",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,T_out_TC3,"T out TC3 [°C]","fuchsia",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,T_fume,"T fume MP[°C]","gray",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,flow_DHW_L,"FLDHW [L/min]","lightgreen",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,flow_DHW_kg,"FLDHW [kg/min]","darkgreen",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,Gas_vol,"Cumul. Gaz Vol. Corr. [L]","orange",True,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,P_valv_in,"P in [bar]","maroon",True,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,Pow_cons,"Pow consumption [W]","tomato",True,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miPLAN,delta_T_req,"Delta T NORM [°C]","darkorange",False,op_main_lin,lin_typ_1)
# plot_fig.trace_fig(add_cor_time_miPLAN,Cum_energy,"Cum ener [kWh]","maroon",False,op_main_lin,lin_typ_1)

plot_fig.trace_fig(add_cor_time_miPLAN,T_CH,"T CH STP [°C]","red",False,op_sec_lin,lin_type_2)
plot_fig.trace_fig(add_cor_time_miPLAN,Burn_ON,"T BURN ON [°C]","purple",False,op_sec_lin,lin_type_2)
plot_fig.trace_fig(add_cor_time_miPLAN,T_30,"T = 30 [°C]","black",False,op_sec_lin,lin_type_2)
plot_fig.trace_fig(add_cor_time_miPLAN,T_45,"T = 45 [°C]","black",False,op_sec_lin,lin_type_2)

plot_fig.trace_fig(add_cor_time_miCOM,T_sup,"T sup [°C]","darksalmon",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miCOM,T_ret,"T return [°C]","deeppink",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miCOM,T_DHW_stor,"T DHW storage [°C]","mediumblue",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miCOM,Flame_current,"Flame current [micr A]","peru",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miCOM,T_fume_mc,"T fume MC[°C]","darkblue",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miCOM,Burn_mod,"Burner mod[%]","violet",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_miCOM,delta_T_boil,"Delta T boiler [°C]","olivedrab",False,op_main_lin,lin_typ_1)

# plot_fig.trace_fig(add_cor_time_PLC,pump_onoff,"ON/OFF Pump","mediumpurple",False,op_main_lin,lin_typ_1)
# plot_fig.trace_fig(add_cor_time_PLC,pump_stp,"Pump setpoint [°C]","mediumslateblue",False,op_main_lin,lin_typ_1)
# plot_fig.trace_fig(add_cor_time_PLC,pump_speed,"Pump speed [%]","mediumvioletred",False,op_main_lin,lin_typ_1)

plot_fig.trace_fig(add_cor_time_DHW,T1,"T1 [°C]","black",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_DHW,T2,"T2 [°C]","blue",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_DHW,T3,"T3 [°C]","yellow",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_DHW,T4,"T4 [°C]","pink",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_DHW,T5,"T5 [°C]","purple",False,op_main_lin,lin_typ_1)

plot_fig.trace_fig(add_cor_time_side_T,CH1,"CH1 [°C]","red",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_side_T,CH2,"CH2 [°C]","rebeccapurple",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_side_T,CH3,"CH3 [°C]","palegreen",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_side_T,CH4,"CH4 [°C]","salmon",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_side_T,CH5,"CH5 [°C]","lightskyblue",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_side_T,CH6,"CH6 [°C]","darkviolet",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_side_T,CH7,"CH7 [°C]","darkcyan",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_side_T,CH8,"CH8 [°C]","brown",False,op_main_lin,lin_typ_1)
plot_fig.trace_fig(add_cor_time_side_T,CH9,"CH9 [°C]","blueviolet",False,op_main_lin,lin_typ_1)

#TODO fig.add_vline(x=add_cor_time_side_T[5000])

# Editing layout traces
plot_fig.update_lay_fig(
    "Test time [s]",
    "Temperature °C",
    "Gas Vol (L.)",
    20,
    20,
    14,
    name_test_descp,
    16
)


plot(fig, filename = "BONGA.html")
# plot(fig, filename = path + os.sep + name_test_descp + date_test_dur + ".html")
    
# plot(fig, filename = path_fig + "HTML" + os.sep + add_path + date + "_" + vel + rpm + tape + test_name + "Evenlope_spectrum_signal_" + name + ".html")
