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

import CLASS_ext_df_data as df_data
df_dt = df_data.ext_data_dt()

import CLASS_res_timing as adj_t_ax
impt_adj_t_ogj = adj_t_ax.timing_reset()


from tqdm import tqdm # showing how long a for loop usually takes

import plotly.graph_objects as go # importing plotly for plotting figures
from plotly.offline import plot
from plotly.subplots import make_subplots # importing subplots to plot several curves in the same graph

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


# %% THIS SECTION LOADS THE DIFFERENT ARRAYS

test_req_num = "24077" # Test number according to test request. 23146: HM BO 70kW XXL / 24013: MONOTANK BO 70kW XXL / 24022: HM SO 45kW XXL /
test_appl = "HM" # The appliance used for the test: HM or Monotank
pow_appl = "45X" # The power of the appliance in kW: 25, 35, 45, 70, 85, 120
fol_appl = test_appl + os.sep + pow_appl + "kW" + os.sep # The master folder where the different tests for one appliance are stored
test_num = "F" # The test number. It can be A, B, C, D, etc.
alg_typ = "3" # The algorithm type/number we use for the tests



if test_req_num == "23146":
 
    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

    if test_num == "A" or test_num == "B":

        T_DHW = 50 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    
    elif test_num == "C":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E" or test_num == "F" or test_num == "G":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 15 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "H":

        T_DHW = 60 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 45 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "I":

        T_DHW = 60 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 30 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24013":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70_Algo" + alg_typ

    if test_num == "A" or test_num == "B":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 15 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 52 # DHW Setpoint temperature [°C]
        T_ADD = 13 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E" or test_num == "E2":

        T_DHW = 53 # DHW Setpoint temperature [°C]
        T_ADD = 11 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 14 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "F" or test_num == "G":

        T_DHW = 53 # DHW Setpoint temperature [°C]
        T_ADD = 11 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 12 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    
elif test_req_num == "24022":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM45TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    
    elif test_num == "B":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 45 # DHW Setpoint temperature [°C]
        T_ADD = 13 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D" or test_num == "D2" or test_num == "E":

        T_DHW = 50 # DHW Setpoint temperature [°C]
        T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "F":

        T_DHW = 60 # DHW Setpoint temperature [°C]
        T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 16 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "G" or test_num == "H":

        T_DHW = 53 # DHW Setpoint temperature [°C]
        T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "I":

        T_DHW = 49 # DHW Setpoint temperature [°C]
        T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "J" or test_num == "J2" or test_num == "K":

        name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

        T_DHW = 54 # DHW Setpoint temperature [°C]
        T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24041":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

    T_DHW = 54 # DHW Setpoint temperature [°C]
    T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
    T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24042":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 15 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    
    elif test_num == "B":

        T_DHW = 49 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 48 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 2 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 48 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    
    elif test_num == "E":

        T_DHW = 48 # DHW Setpoint temperature [°C]
        T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    
    elif test_num == "F":

        T_DHW = 49 # DHW Setpoint temperature [°C]
        T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    
    elif test_num == "G" or test_num == "H" or test_num == "J" or test_num == "J2":

        T_DHW = 50 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24052":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

    if test_num == "A" or test_num == "B" or test_num == "C":

        T_DHW = 54 # DHW Setpoint temperature [°C]
        T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24058":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM35TC_Algo" + alg_typ

    if test_num == "A" or test_num == "B":

        T_DHW = 53 # DHW Setpoint temperature [°C]
        T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 54 # DHW Setpoint temperature [°C]
        T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 8.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24064":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM120TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 53 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    
    elif test_num == "B":

        T_DHW = 51 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 49 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 48 # DHW Setpoint temperature [°C]
        T_ADD = 12 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24074":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM35TC_Algo" + alg_typ

    if test_num == "C":

        T_DHW = 55 # DHW Setpoint temperature [°C]
        T_ADD = 8.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24077":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM45XTC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 50 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B" or test_num == "C":

        T_DHW = 50 # DHW Setpoint temperature [°C]
        T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 53 # DHW Setpoint temperature [°C]
        T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E" or test_num == "F":

        T_DHW = 53 # DHW Setpoint temperature [°C]
        T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 4 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]


test_descp_miplan = "Microplan_Log" # Microplan test description
test_descp_micom = "Microcom" # Microcom test description
test_descp_DHW = "DHW_Temperature" # DHW test description
test_descp_side_T = "Side_Temperature" # DHW test description
test_descp_PLC = "PLC" # PLC test description
test_descp_SEEB = "SEEB" # SEEB test description

name_test_miplan = name_test_descp + "_" + test_descp_miplan
name_test_micom = name_test_descp + "_" + test_descp_micom
name_test_DHW = name_test_descp + "_" + test_descp_DHW
name_test_side_T = name_test_descp + "_" + test_descp_side_T
name_test_PLC = name_test_descp + "_" + test_descp_PLC
name_test_SEEB = name_test_descp + "_" + test_descp_SEEB

compl_path = fol_appl + fol_test # complete path where we saved the csv file of the tests

# get the start time
st = time.time()

if test_req_num == "23146" and test_num == "C":
    
    dt_microplan = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_miplan,",").dropna() # since the test is broken, there are sone NaN value. When we do the resampling time, pyhton explode
    # dt_SEEB = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_SEEB,"\t")
    dt_microcom = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_micom,",").dropna()
    # dt_DHW = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_DHW,",").dropna()
    # dt_side_T = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_side_T,",").dropna()
    # dt_PLC = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_PLC,",").dropna()

else:

    dt_microplan = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_miplan,",")
    # dt_SEEB = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_SEEB,"\t")
    dt_microcom = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_micom,",")
    # dt_DHW = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_DHW,",")
    # dt_side_T = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_side_T,",")
    # dt_PLC = impt_csv_txt_obj.read_csv_file_v2(compl_path,name_test_PLC,",")

# get the end time
et_rd_df = time.time()

# get the execution time
rd_time = et_rd_df - st

print("Finish reading data in " + str(rd_time) + " seconds")


#%% THIS SECTION READ THE CSV DATA AND STORE THEIR VALUES IN DIFFERENT ARRAYS

rec_time,t_st_rec_miplan,T_in_DHW,T_out_avg,T_out_PT100,T_out_TC1,T_out_TC2,T_out_TC3,T_fume,flow_DHW_kg,flow_DHW_L,Gas_vol,P_valv_in,Pow_cons,Cum_energy = df_dt.read_df_microPLAN(
                                                                    dt_microplan)

# t_st_rec_SEEB,T_in_DHW,T_out_avg,T_fume,flow_valve_1_L,flow_valve_2_L,P_val_in,By_pass_val_ON,Tap_val_ON,Gas_vol,Gas_counter_L = df_dt.read_df_SEEB(dt_SEEB)

T_sup,T_ret,T_DHW_stor,Flame_current,T_fume_mc,Burn_mod = df_dt.read_df_microCOM(dt_microcom) # Storing the MICROCOM

# # T1, T2, T3, T4, T5 = df_dt.read_df_DHW_sens(dt_DHW) # Storing the DHW data
# # T1, T2, T3, T4, T5, T6, T7, T8 = df_dt.read_df_DHW_sens_Monotank(dt_DHW) # Storing the DHW data
# # T1, T2, T3, T4, T5 = df_dt.read_df_DHW_sens_45TC(dt_DHW) # Storing the DHW data
# T1, T2, T3, T4, T5, T6, T7 = df_dt.read_df_DHW_sens_70TCplus(dt_DHW) # Storing the DHW data

# # CH1, CH2, CH3, CH4 = df_dt.read_df_side_T(dt_side_T) # Storing the side temperature data
# CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9 = df_dt.read_df_side_T(dt_side_T) # Storing the side temperature data
# # CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13, CH14, = df_dt.read_df_side_T(dt_side_T) # Storing the side temperature data
# # CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13, CH14, CH15, CH16, = df_dt.read_df_side_T(dt_side_T) # Storing the side temperature data

# pump_onoff,pump_stp,pump_speed = df_dt.read_df_PLC(dt_PLC) # Storing the PLC data

#%% THIS SECTION TIME SCALE THE DHW AND MICROCOM DATASET IN ORDER TO
# PLOT THEM WITH THE CORRECT TIME DELAY AND MATCH THE MICROPLAN DATASET

add_cor_time_miPLAN = impt_adj_t_ogj.res_timing_comparison(dt_microplan,"Timestamp",t_st_rec_miplan)
add_cor_time_miCOM = impt_adj_t_ogj.res_timing_comparison(dt_microcom,"Time DMY",t_st_rec_miplan)
# add_cor_time_DHW = impt_adj_t_ogj.res_timing_comparison(dt_DHW,"Date-Time",t_st_rec_miplan)
# add_cor_time_side_T = impt_adj_t_ogj.res_timing_comparison(dt_side_T,"Date&Time",t_st_rec_miplan)
# add_cor_time_PLC = impt_adj_t_ogj.res_timing_comparison(dt_PLC,"DATE-TIME",t_st_rec_miplan)

# add_cor_time_SEEB = impt_adj_t_ogj.res_timing_comparison(dt_SEEB,"Unnamed: 0",t_st_rec_SEEB)
# add_cor_time_miCOM = impt_adj_t_ogj.res_timing_comparison(dt_microcom,"Time DMY",t_st_rec_SEEB)
# add_cor_time_DHW = impt_adj_t_ogj.res_timing_comparison(dt_DHW,"Date-Time",t_st_rec_SEEB)
# add_cor_time_side_T = impt_adj_t_ogj.res_timing_comparison(dt_side_T,"Date&Time",t_st_rec_SEEB)
# add_cor_time_PLC = impt_adj_t_ogj.res_timing_comparison(dt_PLC,"DATE-TIME",t_st_rec_SEEB)

#%% THIS SECTION GIVES THE TIME ARRAY SPLIT FOR THE DIFFERENT DAYS

day_and_indx_microPLAN,dict_days_arr_microPLAN = impt_adj_t_ogj.res_timing_comparison_same_day(add_cor_time_miPLAN)

day_and_indx_microCOM,dict_days_arr_microCOM = impt_adj_t_ogj.res_tim_comp_same_day_no_midnight(add_cor_time_miCOM)
# day_and_indx_DHW,dict_days_arr_DHW = impt_adj_t_ogj.res_tim_comp_same_day_no_midnight(add_cor_time_DHW)
# day_and_indx_side_T,dict_days_arr_side_T = impt_adj_t_ogj.res_tim_comp_same_day_no_midnight(add_cor_time_side_T)
# day_and_indx_PLC,dict_days_arr_PLC = impt_adj_t_ogj.res_tim_comp_same_day_no_midnight(add_cor_time_PLC)

# dt_time = pd.to_datetime(add_cor_time_DHW,dayfirst="True") # have the date and hour in dataframe
# # sec_array = (dt_time.hour*60+dt_time.minute)*60 + dt_time.second # have all the hours, min and sec in one array with only seconds
# # mid_ind = np.where(sec_array == 0) # find all the indices when we have midnight

# # OBIETTIVO. CONVERTIRE LA DIFFERENZA IN INTEGER. FARE UN LOOP PER VEDERE QUANDO LA
# # DIFFERENZA E' 1 E STORARE QUEL VALORE NELL'ARRAY

# """
# a = dt_time.date - dt_time.date[0]
# a_check = datetime.timedelta(1)
# c = np.zeros(5)
# j=0
# for i in range (0, len(a)-1):

#     if a[i+1] - a[i] == a_check:
#         c[j] = i
#         j = j + 1

# c_no_zeros = c[c != 0]
# a[int(c_no_zeros[0])+1]
# """


# dt_time = pd.to_datetime(add_cor_time_DHW,dayfirst="True") # have the date and hour in dataframe
# days_num = dt_time.date - dt_time.date[0] # compute the number of days we have in the test
# d_check = datetime.timedelta(1)
# indx_chang_day = np.zeros(5)
# j=0
# for i in range (0, len(days_num)-1):

#     if days_num[i+1] - days_num[i] == d_check:
#         indx_chang_day[j] = i+1
#         j = j + 1

# indx_chang_day = indx_chang_day[indx_chang_day != 0] # remove the zero from the list
# ind_list = np.append(indx_chang_day, len(dt_time)-1).astype(int) 
# days = max(dt_time.day - dt_time.day[0]) # check the amount of days we have
# dt_time_new_date = dt_time.map(lambda t: t.replace(month=2, day=23)) # assign the dame month and day to the timing vector
# int_num_day = np.arange(0,days+1) # creating a vector countaining the increasing number of day
# day_and_ind = np.column_stack((int_num_day,ind_list)) # from 1 D array to a 2D countaining days number and the index where the new day start

# counter = 0
# dict_day_arr = {}

# for i in day_and_ind:
#     dict_day_arr["day_" + str(i[0])] = dt_time_new_date[counter:int(i[1])]
#     counter=i[1]

#%% THIS SECTION SPLIT ONE UNIQUE DATAFRAME IN MORE DATAFRAME WHICH ARE STORED IN A DICTIONARY

dict_miPLAN_split = df_dt.split_df(dt_microplan,day_and_indx_microPLAN)
dict_miCOM_split = df_dt.split_df(dt_microcom,day_and_indx_microCOM)
# dict_DHW_split = df_dt.split_df(dt_DHW,day_and_indx_DHW)
# dict_side_T_split = df_dt.split_df(dt_side_T,day_and_indx_side_T)
# dict_PLC_split = df_dt.split_df(dt_PLC,day_and_indx_PLC)


#%% THIS SECTION EXTRACT THE VALUES IN THE DATAFRAME TO STORE IN DICT

microPLAN_data_prm_ax = [
    ["_Test_T_in_DHW","T°in DHW [°C]"], # Inlet temperature coming from the grid [°C]
    ["_Test_T_out_avg","T°out AV.  [°C]"], # Average outlet temperature for the domestic hot water [°C]
    ["_Test_T_fume_mPLAN","T°Fume [°C]"], # Outlet temperature of the smoke exiting the Heat Master [°C]
    ["_Test_flow_DHW_L/min","FLDHW [L/min]"], # Water flow [L/min]
    ["_Test_flow_DHW_kg/min","FLDHW [kg/min]"] # Water flow [kg/min]. This is the flow corrected with the density and Cp. It is not computed if the value is less than 0.5. It will be considered as 0.
] # Vector names of microPLAN to be loaded and plotted on the primary axes

microCOM_data_prm_ax = [
    ["_Test_T_sup","Supply [°C]"], # Temperature on the main tank [°C]
    ["_Test_T_ret","Return [°C]"], # Temperature on the pump pipe to cool down the burner [°C]
    ["_Test_T_DHW_stor_t","DHW stor (°C)"], # Temperature inside the big ballon [°C]
    ["_Test_Flame_current","Flame Curent [uA]"], # Flame current [A] * 10^-6
    ["_Test_T_fume_mCOM","Flue temp [0,01°C]"], # Temperature on the fume [°C]
    ["_Test_Burn_mod","Actual measured load"], # Burner modulation
] # Vector names of microCOM to be loaded and plotted on the primary axes

microPLAN_data_scd_ax = [
    ["_Test_Gas_vol_consp","Cumul. Gaz Vol. Corr.[L]"], # Volume of gas consumption [L]
    ["_Test_P_valv_in","pin DHW [bar]"] # Pressure of the inlet valve [bar]
] # Vector names to be loaded on the secondary axes

SEEB_data_prm_ax = [
    ["_Test_T_in_DHW","TE1"], # Inlet temperature coming from the grid [°C]
    ["_Test_T_out_avg","TE2"], # Average outlet temperature for the domestic hot water [°C]
    ["_Test_T_fume_SEEB","TF1"], # Outlet temperature of the smoke exiting the Heat Master [°C]
    ["_Test_flow_DHW_val1","DE1"], # Water flow [m^3/h] of the first valve
    ["_Test_flow_DHW_val2","DE2"], # Water flow [m^3/h] of the second valve
    ["_Test_By_pass_val_ON","EVE6"], # Counter 0-1 to know when the by-pass valve is on
    ["_Test_Tap_val_ON","EVE7"] # Counter 0-1 to know when the tapping valve is on
] # Vector names to be loaded on the secondary axes

SEEB_data_sdc_ax = [
    ["_Test_Gas_vol","DG1"], # Total amount of gas consumed during the three days [m^3]
    ["_Test_Gas_counter_L","DebitGaz_DG1"], # Counter of amount of gas consumed when burner is on [m^3/h]
    ["_Test_P_val_in","PE1"] # Pressure of the inlet valve [bar]
] # Vector names to be loaded on the secondary axes

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
    ["_Test_T7 [°C]","T7 bas"]
]

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
    # ["_Test_CH15 [°C]","CH15"],
    # ["_Test_CH16 [°C]","CH16"]
]

PLC_data = [
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

for i in tqdm(dict_miPLAN_split, desc="ESTIMATOR LOOP 1"):

    dict_stor_prm_ax_mPLAN = {} # Create an empty dictionary where storing the loading variables
    dict_stor_scd_ax_mPLAN = {} # Create an empty dictionary where storing the loading variables
    dict_stor_prm_ax_SEEB = {} # Create an empty dictionary where storing the loading variables
    dict_stor_scd_ax_SEEB = {} # Create an empty dictionary where storing the loading variables
    dict_stor_prm_ax_mCOM = {} # Create an empty dictionary where storing the loading variables
    dict_stor_DHW_sens = {} # Create an empty dictionary where storing the loading variables
    dict_stor_side_T = {} # Create an empty dictionary where storing the loading variables
    dict_stor_PLC = {} # Create an empty dictionary where storing the loading variables

    for j in tqdm(microPLAN_data_prm_ax, desc="ESTIMATOR LOOP 2"):

        dict_stor_prm_ax_mPLAN[i + j[0]] = dict_miPLAN_split[i][j[1]]
        dict_stor_prm_ax_mPLAN["Delta_T_norm_test_Test_" + i] = dict_miPLAN_split[i]["T°out AV.  [°C]"] - dict_miPLAN_split[i]["T°in DHW [°C]"]

    for l in tqdm(microPLAN_data_scd_ax, desc="ESTIMATOR LOOP 3"):

        dict_stor_scd_ax_mPLAN[i + l[0]] = dict_miPLAN_split[i][l[1]]

    # for p in tqdm(SEEB_data_prm_ax, desc="ESTIMATOR LOOP 4"):

    #     dict_stor_prm_ax_SEEB[i[4] + p[0]] = dt_SEEB[p[1]]
    #     dict_stor_prm_ax_SEEB["Delta_T_norm_test_Test_" + i[4]] = dt_SEEB["TE2"] - dt_SEEB["TE1"]

    # for q in tqdm(SEEB_data_sdc_ax, desc="ESTIMATOR LOOP 5"):

    #     dict_stor_scd_ax_SEEB[i[4] + q[0]] = dt_SEEB[q[1]]

    #     dict_stor_prm_ax_SEEB [i[4] + "_Test_flow_DHW_val1"] = dict_stor_prm_ax_SEEB[i[4] + "_Test_flow_DHW_val1"]*1000/60
    #     dict_stor_prm_ax_SEEB [i[4] + "_Test_flow_DHW_val2"] = dict_stor_prm_ax_SEEB[i[4] + "_Test_flow_DHW_val2"]*1000/60
    #     dict_stor_scd_ax_SEEB [i[4] + "_Test_Gas_vol"] = (dict_stor_scd_ax_SEEB[i[4] + "_Test_Gas_vol"] - dict_stor_scd_ax_SEEB[i[4] + "_Test_Gas_vol"][14000])*1000
    #     dict_stor_scd_ax_SEEB [i[4] + "_Test_Gas_counter_L"] = dict_stor_scd_ax_SEEB[i[4] + "_Test_Gas_counter_L"]*1000/3600
    #     dict_stor_prm_ax_SEEB [i[4] + "_Test_By_pass_val_ON"] = dict_stor_prm_ax_SEEB[i[4] + "_Test_By_pass_val_ON"]*50
    #     dict_stor_prm_ax_SEEB [i[4] + "_Test_Tap_val_ON"] = dict_stor_prm_ax_SEEB[i[4] + "_Test_Tap_val_ON"]*50

    for k in tqdm(microCOM_data_prm_ax, desc="ESTIMATOR LOOP 6"):

        dict_stor_prm_ax_mCOM[i + k[0]] = dict_miCOM_split[i][k[1]]

    # for m in tqdm(DHW_sens_data, desc="ESTIMATOR LOOP 7"):

    #     dict_stor_DHW_sens[i + m[0]] = dict_DHW_split[i][m[1]]

    # for n in tqdm(side_T_data, desc="ESTIMATOR LOOP 8"):

    #     dict_stor_side_T[i + n[0]] = dict_side_T_split[i][n[1]]

    # for o in tqdm(PLC_data, desc="ESTIMATOR LOOP 9"):

    #     dict_stor_PLC[i + o[0]] = dict_PLC_split[i][o[1]]


    all_dict_prm_ax_mPLAN[i] = dict_stor_prm_ax_mPLAN
    all_dict_scd_ax_mPLAN[i] = dict_stor_scd_ax_mPLAN

    # all_dict_prm_ax_SEEB["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_prm_ax_SEEB
    # all_dict_scd_ax_SEEB["dict_" + i[2] + "_test_%s" %i[4]] = dict_stor_scd_ax_SEEB

    all_dict_prm_ax_mCOM[i] = dict_stor_prm_ax_mCOM
    # all_dict_DHW_sens[i] = dict_stor_DHW_sens
    # all_dict_side_T[i] = dict_stor_side_T
    # all_dict_PLC[i] = dict_stor_PLC


#%% THIS SECTION SETS SOME PARAMETERS FOR THE PLOTTING CURVE

op_main_lin = 1 # Set the opacity of the main lines
op_sec_lin = 0.25 # Set the opacity of the secondary lines

lin_typ_1 = "solid"  # Line layout. if we use mode we have to write "lines" in order to have a continuous line
lin_type_2 = "dash"  # Line layout.

T_45 = np.ones(len(dict_days_arr_microPLAN["day_1"]))*45 # This is a straight line at 45 [°C] to see when we are below the delta T requested from the norm
T_30 = np.ones(len(dict_days_arr_microPLAN["day_1"]))*30 # This is a straight line at 30 [°C] to see when we are below the delta T requested from the norm

# dict_days_arr_DHW
# dict_days_arr_side_T
# dict_days_arr_PLC


# #%% THIS SECTION PLOT THE FIGURES

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

for day in all_dict_prm_ax_mPLAN:
    for key,value in all_dict_prm_ax_mPLAN[day].items():
                trace_fig(dict_days_arr_microPLAN[day],
                        value,
                        "MicroPLAN",
                        "MicroPLAN",
                        key,
                        #   "darkblue",
                        False,
                        op_main_lin,lin_typ_1
                        )
                
for day in all_dict_scd_ax_mPLAN:
    for key,value in all_dict_scd_ax_mPLAN[day].items():
                trace_fig(dict_days_arr_microPLAN[day],
                        value,
                        "MicroPLAN",
                        "MicroPLAN",
                        key,
                        #   "darkblue",
                        True,
                        op_main_lin,lin_typ_1
                        )

for day in all_dict_prm_ax_mCOM:
    for key,value in all_dict_prm_ax_mCOM[day].items():
                trace_fig(dict_days_arr_microCOM[day],
                        value,
                        "MicroCOM",
                        "MicroCOM",
                        key,
                        #   "darkblue",
                        True,
                        False,lin_typ_1
                        )


# for day in all_dict_DHW_sens:
#     for key,value in  all_dict_DHW_sens[day].items():
#         trace_fig(dict_days_arr_DHW[day],
#                 value,
#                 "DHW",
#                 "DHW",
#                 key,
#                 #   "cyan",
#                 False,
#                 op_main_lin,lin_typ_1
#                 )

# for day in all_dict_side_T:
#     for key,value in all_dict_side_T[day].items():
#         trace_fig(dict_days_arr_side_T[day],
#                 value,
#                 "Side_T",
#                 "Side_T",
#                 key,
#                 #   "cyan",
#                 False,
#                 op_main_lin,lin_typ_1
#                 )

# for day in all_dict_PLC:
#     for key,value in all_dict_PLC[day].items():
#         trace_fig(dict_days_arr_PLC[day],
#                 value,
#                 "PLC",
#                 "PLC",
#                 key,
#                 #   "cyan",
#                 False,
#                 op_main_lin,lin_typ_1
#                 )


trace_fig(dict_days_arr_microPLAN["day_1"],T_30,"Set","Settings","T = 30 [°C]",False,op_sec_lin,lin_type_2)
trace_fig(dict_days_arr_microPLAN["day_1"],T_45,"Set","Settings","T = 45 [°C]",False,op_sec_lin,lin_type_2)


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

plot(fig, filename = "One_test_one_day.html")
# plot(fig, filename = path + os.sep + name_test_descp + date_test_dur + ".html")
