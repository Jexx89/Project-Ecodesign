# -*- coding: utf-8 -*-
"""
Created on Wed Dec 6 09:45:02 2023

@author: Marcello Nitti
"""

#%% THIS SECTION IS FOR IMPORTING SEVERAL PACKAGES

import numpy as np # importing numpy library
import os # importing the correct separator between folder and files depending on the operating system
import pandas as pd # importing pandas dataframe
import time # to get how long different secion of the code requires to run
import datetime

import plotly.graph_objects as go # importing plotly for plotting figures
from plotly.offline import plot
from plotly.subplots import make_subplots # importing subplots to plot several curves in the same graph

from scipy.integrate import odeint

#%% THIS SECTION HAS ALL THE FUNCTIONS THAT ARE USED LATER IN THE SCRIPT

def trace_fig(x_axis,y_axis,group,gourp_ttl,name,col,secd_y_ax,opac,typ_line):

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
                   line = dict(color=col, width=1.5, dash=typ_line)),
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
        secondary_y=False,
        # tickmode = "sync",
        )  # ,type = "log"
    
    fig.update_yaxes(
        title=lab_sec_y_ax_,
        title_font={"size": txt_siz_lbl_xy},
        range=[0, 80],
        secondary_y=True,
        # tickmode = "sync",
        anchor="y",
        # rangemode="tozero",
        # overlaying="y",
        # matches="y",
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


#%% THIS SECTION HAS ALL TECHNICAL INFORMATION OF THE PRODUCTS

Power = 25                                      # [kW] - Possible values: 25, 35, 45, 60, 70, 85, 120, NOTE: all the powers are in KILOWATT.
Size = "SO"                                     # [tipe of appliance we are using] - Possible value "SO" or "BO"
T_DHW_tube_lenght = 500/1000                         # [m] - Tube lenght on the T DHW
T_DHW_sensor_height = T_DHW_tube_lenght - 50/1000    # [m] - Sensonr height in the tank. 50 mm is necessary for the fitting of the tube
Burner_modulation = 100                         # [%] - Power of the burning modulation
Q = Power*1000*Burner_modulation/100            # [W] - [Total amount of power put in the product]

if Size == "SO":
    Volume = 77.5                                # [L] - Total volume of the big ballon

    d_in_int = 183/1000                                # [m] - Interal diameter of the inner circle
    d_ext_int = 213/1000                               # [m] - External diameter of the inner circle
    d_m_in = (d_in_int + d_ext_int) / 2           # [m] - Medium diameter of the inner circle

    d_in_ext = 404.8/1000                             # [m] - Interal diameter of the external circle
    d_ext_ext = 436.7/1000                            # [m] - External diameter of the external circle
    d_m_ext = (d_in_ext + d_ext_ext) / 2         # [m] - Medium diameter of the external circle
    
    h_col = 546.5/1000                                         # [m] - height of the cylinder until the attachment with the plates
    h_rec_bas = 20/1000                                            # [m] - height of the rectable below the spherical cap
    h_rec_top = 90/1000                                             # [m] - height of the top rectanle
    Vol_cil_base = np.pi*h_rec_bas*(d_ext_ext**2-d_ext_int**2)/4   # [m^3] - cylindrical volume on the bottom part
    Vol_cil_top = np.pi*h_rec_top*((d_ext_ext-0.059)**2-d_ext_int**2)/4    # [m^3] - cylindrical volume on the middle part
    Dome = Vol_cil_base + Vol_cil_top           # [m^3] - Volume of the dome above/below the cylindrical body.

elif Size == "BO":
    Volume = 173                                # [L] - Total volume of the big ballon

    d_in_int = 274/1000                                # [m] - Interal diameter of the inner circle
    d_ext_int = 300/1000                               # [m] - External diameter of the inner circle
    d_m_in = (d_in_int + d_ext_int) / 2           # [m] - Medium diameter of the inner circle

    d_in_ext = 513/1000                             # [m] - Interal diameter of the external circle
    d_ext_ext = 540/1000                            # [m] - External diameter of the external circle
    d_m_ext = (d_in_ext + d_ext_ext) / 2         # [m] - Medium diameter of the external circle
    
    h_col = 886.8/1000                                         # [m] - height of the cylinder until the attachment with the plates
    h_rec_bas = 20/1000                                            # [m] - height of the rectable below the spherical cap
    h_rec_top = 90/1000                                             # [m] - height of the top rectanle
    Vol_cil_base = np.pi*h_rec_bas*(d_ext_ext**2-d_ext_int**2)/4   # [m^3] - cylindrical volume on the bottom part
    Vol_cil_top = np.pi*h_rec_top*(d_ext_ext**2-d_ext_int**2)/4    # [m^3] - cylindrical volume on the middle part
    Dome = Vol_cil_base + Vol_cil_top           # [m^3] - Volume of the dome above/below the cylindrical body.

V_theory_m3 = (np.pi*h_col*(d_m_ext**2-d_m_in**2)/4) + 2*Dome # [m^3] - Theoretical volume of the donats. The / 1000 is to convert millimeters into meters
V_theory_L = V_theory_m3*1000                      # [L] - Theoretical volume of the donats.
V_theory_L_r = np.round(V_theory_L,1)              # [L] - Theoretical volume of the donats rounded to the 1 decimal point

V_above_T_DHW_m3 = (np.pi*T_DHW_sensor_height*(d_m_ext**2-d_m_in**2)/4) + Dome # [m^3] - Theoretical volume above T DHW sensor
V_above_T_DHW_L = V_above_T_DHW_m3*1000                                             # [L] - Theoretical volume above T DHW sensor


#%% THIS SECTION COMPUTES THE CURVE OF T OUT - NO BURNER ON

sim_time = 1                                          # [h] - hours we want to simulate for T DHW
stop_time = sim_time*60*60                            # [s] - hours we want to simulate for T DHW
t_arr_tot = np.arange(0,stop_time,0.1)                # [s] - time array in seconds

T_st_HM = 80            # [°C] - starting temperature of the tank
T_in = 10               # [°C] - Inlet water temperature
cp = 4.1861             # [kJ/Kg*K] - average cp of water from 10 °C to 80 °C

input_mode = "Temperature"     # [sting: Mass, Temperature, Time] - This defines the input we want for the model, and so the relative output

if input_mode == "Mass":

    m = 10                  # [L/min] - tapped mass from the tank in liters per minute
    m_sec = m/60            # [L/s] - tapped mass from the tank in liters per seconds
    m_kg_sec = m_sec        # [kg/s] - tapped mass from the tank in kg per seconds

    t_emp_HM_stop = V_theory_L_r/m_sec                 # [s] - time to empty the boiler without the burner being active in seconds
    t_emp_HM = np.arange(0,t_emp_HM_stop,0.1)          # [s] - time array to empty the tank in seconds
    T_out_st = np.ones(len(t_emp_HM))*T_st_HM          # [°C] - Array output temperature to empty the tank

    t_arr = np.arange(t_emp_HM_stop,stop_time,0.1)          # [s] - time array in seconds after the transient
    T_out = Q/(m_kg_sec*cp*1000) + np.ones(len(t_arr_tot)-len(t_emp_HM))*T_in

elif input_mode == "Temperature":

    T_out = 40                                          # [°C] - Wanted output temperature

    m_kg_sec = Q/(cp*1000*(T_out-T_in))                 # [kg/s] - tapped mass from the tank in kg per seconds
    m = m_kg_sec*60                                     # [L/min] - tapped mass from the tank in liters per minute

    t_emp_HM_stop = V_theory_L_r/m_kg_sec              # [s] - time to empty the boiler without the burner being active in seconds
    t_emp_HM = np.arange(0,t_emp_HM_stop,0.1)          # [s] - time array to empty the tank in seconds
    T_out_st = np.ones(len(t_emp_HM))*T_st_HM          # [°C] - Array output temperature to empty the tank

    t_arr = np.arange(t_emp_HM_stop,stop_time,0.1)          # [s] - time array in seconds after the transient
    T_out = np.ones(len(t_arr_tot)-len(t_emp_HM))*T_out

elif input_mode == "Time":

    t_emp_HM_stop = 635                                 # [s] - time to empty the boiler without the burner being active in seconds

    m_kg_sec = V_theory_L_r/t_emp_HM_stop                 # [kg/s] - tapped mass from the tank in kg per seconds
    m = m_kg_sec*60                                       # [L/min] - tapped mass from the tank in liters per minute

    t_emp_HM = np.arange(0,t_emp_HM_stop,0.1)          # [s] - time array to empty the tank in seconds
    T_out_st = np.ones(len(t_emp_HM))*T_st_HM          # [°C] - Array output temperature to empty the tank

    t_arr = np.arange(t_emp_HM_stop,stop_time,0.1)          # [s] - time array in seconds after the transient
    T_out = Q/(m_kg_sec*cp*1000) + np.ones(len(t_arr_tot)-len(t_emp_HM))*T_in

#TODO Work on the mix --> water mix temperature (eg. 40) --> then we want the mass flow rate hot + cold in order to have 40
# Base on mass and T out computed we need to compute the mix of water we want

######## THE FOLLOWING PART HAS THE OBJECTIVE OF COMPUTING DIFFERENT AMOUNT OF MASS TO EMPTY THE TANK AND THEN ADJUST TO THE WANTED
######## TEMPERATURE AND SO MASS WE CAN EXTRACT



T_in_tot = np.ones(len(t_arr_tot))*T_in         # [°C] - Array of inlet temperature for the whole simulation

T_out_tot = np.concatenate([T_out_st, T_out])
m_out = np.ones(len(t_arr_tot))*m_kg_sec        # [L/s] - Array of tapped mass for the whole simulation
m_L_min = m_out*60                              # [L/min] - Array of tapped mass for the whole simulation. THIS IS NOT IN LINE WITH THE SECONDS OF THE ARRAY. IT IS JUST TO HAVE A SIMPLER VISUAL THING

T_90 = np.ones(len(T_out_tot))*90               # This is a straight line at a fixed number


"""
The formula we are about to use for the water ratio is based the mixing relation for Richman's law
"""

Hot_water_ratio = (T_out[1]-T_in)/(T_st_HM-T_in)            # [-] - Mix ratio of hot water in order to achieve the wanted temperature
m_out_mix = m_kg_sec/Hot_water_ratio                        # [L/s] - Total amount of water it is beeing used
m_out_tot = np.ones(len(t_arr_tot))*m_out_mix               # [L/s] - Total amount of water it is beeing used
m_out_tot_min = m_out_tot*60                                # [L/min] - Total amount of water it is beeing used

#%% THIS SECTION SOLVES THE ODE AND COMPUTE T OUT AND T DHW OVER TIME

fraction_vol = 0

# We can have a change in the volume fraction

def HM_T_evolution(t):

    T_DHW = T_st_HM


    return T_DHW

# for i in range (0,lent(t_arr_tot)):
    
#     y = odeint(HM_T_evolution,T_in_cond,t_arr_tot,args=inputs)

#     store all the values


#%% THIS SECTION SETS SOME PARAMETERS FOR THE PLOTTING CURVE

op_main_lin = 1 # Set the opacity of the main lines
op_sec_lin = 0.25 # Set the opacity of the secondary lines

lin_typ_1 = "solid"  # Line layout. if we use mode we have to write "lines" in order to have a continuous line
lin_type_2 = "dash"  # Line layout.

#%% THIS SECTION PLOT THE FIGURES

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
# trace_fig(t_emp_HM,T_out_st,"Simulation","First trial","T out start [°C]","red",False,op_main_lin,lin_typ_1)
# trace_fig(t_arr,T_out,"Simulation","First trial","T out [°C]","orange",False,op_main_lin,lin_typ_1)
trace_fig(t_arr_tot,T_out_tot,"Simulation","First trial","T out [°C]","red",False,op_main_lin,lin_typ_1)
trace_fig(t_arr_tot,T_in_tot,"Simulation","First trial","T in [°C]","cyan",False,op_main_lin,lin_typ_1)
trace_fig(t_arr_tot,m_out,"Mass","Tapped mass","m_HM [L/s]","green",True,op_main_lin,lin_typ_1)
trace_fig(t_arr_tot,m_L_min,"Mass","Tapped mass","m_HM [L/min]","darkgreen",True,op_main_lin,lin_typ_1)
trace_fig(t_arr_tot,m_out_tot,"Mass","Total amount of mass used","m tot [L/s]","darkviolet",True,op_main_lin,lin_typ_1)
trace_fig(t_arr_tot,m_out_tot_min,"Mass","Total amount of mass used","m tot [L/min]","mediumslateblue",True,op_main_lin,lin_typ_1)
trace_fig(t_arr_tot,T_90,"Set","Settings","T = 90 [°C]","black",False,op_sec_lin,lin_type_2) # add_cor_time_miPLAN or add_cor_time_SEEB


# Editing layout traces
update_lay_fig(
    "Test time [s]",
    "Temperature [°C]",
    "Mass [kg/s]",
    20,
    20,
    14,
    "Simulation",
    16
)

plot(fig, "Test.html")
# plot(fig, filename = fol_appl + fol_test + os.sep + name_test_descp + date_test_dur + ".html")
