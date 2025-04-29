# -*- coding: utf-8 -*-


"""
Created on Wed Dec 6 09:45:02 2023

@author: Marcello Nitti
"""

# %% THIS SECTION IS FOR IMPORTING SEVERAL PACKAGES

import numpy as np  # importing numpy library
import os  # importing the correct separator between folder and files depending on the operating system
import sys

# import plotly as pl
import pandas as pd  # importing pandas dataframe
import time  # to get how long different secion of the code requires to run
import datetime

import plotly.graph_objects as go  # importing plotly for plotting figures
from plotly.offline import plot
from plotly.subplots import (make_subplots)  # importing subplots to plot several curves in the same graph

# import tkinter as tk  # importing the GUI toolkit interface
# from tkinter import messagebox

# %% THIS SECTION HAS ALL THE FUNCTIONS THAT ARE USED LATER IN THE SCRIPT


def read_csv_file(path_fol, file_name, dlm):
    """
    Function in order to read the csv file

    Parameters
    -----------------

    path_fol: string
        The main folder parth where the file is located
    file_name: string
        The file name we want to load. It does not have to include csv in it
    dlm: sting
        How the data are delimited on the csv file

    Returns
    -----------

    df_csv: dataframe
        A dataframe countaining all the data of the excel sheet

    """
    if os.path.exists(path_fol + os.sep + file_name + ".csv"):
        df_csv = pd.read_csv(
            path_fol + os.sep + file_name + ".csv",
            # skiprows=1, # This option allows to skip and NOT read some lines of the file
            encoding_errors="ignore",
            low_memory="False",
            delimiter=dlm,
            # header=None, # This option is to have the header as raw stored in the dataframe. In this case we should also activare dtype = "unicode"
            # dtype = "unicode",
        )
    else:
        sys.exit("File not found : " + path_fol + os.sep + file_name + ".csv")

    return df_csv


def read_df_microplan(dt):
    """
    Function to read some columns of the dataframe and store them in a series
    (Series is a one-dimensional labeled array capable of holding data of
    any type (integer, string, float, python objects, etc.). The axis
    labels are collectively called index)

    Parameters
    -----------------

    dt: dataframe
        The dataframe with all the stored values

    Returns
    -----------

    T_in_DHW: series
        An array countaining all the values of the inlet temperature coming from the grid [°C]
    T_out_avg: series
         An array countaining all the values of the average outlet temperature for the domestic hot water [°C]
    T_out_PT100: series
         An array countaining all the values of the outlet temperature for the domestic hot water - sensor PT100 [°C]
    T_out_TC1: series
         An array countaining all the values of the outlet temperature for the domestic hot water - sensor TC1 [°C]
    T_out_TC2: series
         An array countaining all the values of the outlet temperature for the domestic hot water - sensor TC2 [°C]
    T_out_TC3: series
         An array countaining all the values of the outlet temperature for the domestic hot water - sensor TC3 [°C]
    T_fume: series
         An array countaining all the values of the outlet temperature of the smoke exiting the Heat Master or Water Master [°C]
    flow_DHW_kg: series
         An array countaining all the values of the water flow [kg/min]
    flow_DHW_L: series
         An array countaining all the values of the water flow [L/min]
    Gas_vol: series
         An array countaining all the values of the volume of gas consumption [L]
    P_val_in: series
         An array countaining all the values of the inlet pressure [bar]
    Pow_cons: series
         An array countaining all the values of the energy consumption of the whole electronic: fan, pumo and elec board [W]
    Cum_energy: series
         An array countaining the cumulative consumption of energy [kWh]
    t_str_rec: series
         A value indicating the date when the test actually started
    T_amb: series
        An array countaining all the values of the ambiente temperature - T°Amb [°C]

    """

    T_in_DHW = dt["T°in DHW [°C]"]  # Inlet temperature coming from the grid [°C]
    T_out_avg = dt["T°out AV.  [°C]"]  # Average outlet temperature for the domestic hot water [°C]
    T_out_PT100 = dt["T°out PT100  [°C]"]  # Outlet temperature for the domestic hot water - sensor PT100 [°C]
    T_out_TC1 = dt["T°out TC1  [°C]"]  # Outlet temperature for the domestic hot water - sensor TC1 [°C]
    T_out_TC2 = dt["T°out TC2  [°C]"]  # Outlet temperature for the domestic hot water - sensor TC2 [°C]
    T_out_TC3 = dt["T°out TC3  [°C]"]  # Outlet temperature for the domestic hot water - sensor TC3 [°C]
    T_fume = dt["T°Fume [°C]"]  # Outlet temperature of the smoke exiting the Heat Master [°C]
    flow_DHW_kg = dt["FLDHW [kg/min]"]  # Water flow [kg/min]
    flow_DHW_L = dt["FLDHW [L/min]"]  # Water flow [L/min]
    Gas_vol = dt["Cumul. Gaz Vol. Corr.[L]"]  # Volume of gas consumption [L]
    P_val_in = dt["pin DHW [bar]"]  # Pressure of the inlet valve [bar]
    Pow_cons = dt["Power Absorbed [W]"]  # Energy consumption of the whole electronic: fan, pump and boards [W]
    Cum_energy = dt["Cumul. QDHW  [kWh]"]  # Cumulative consunmption of energy [kWh]
    T_amb = dt["T°Amb [°C]"]  # Cumulative consunmption of energy [kWh]
    t_str_rec = pd.to_datetime(dt["Timestamp"][0], dayfirst="True")  # Actual time when we start recording

    return (
        t_str_rec,
        T_in_DHW,
        T_out_avg,
        T_out_PT100,
        T_out_TC1,
        T_out_TC2,
        T_out_TC3,
        T_fume,
        flow_DHW_kg,
        flow_DHW_L,
        Gas_vol,
        P_val_in,
        Pow_cons,
        Cum_energy,
        T_amb
    )


def read_df_SEEB(dt):
    """
    Function to read some columns of the dataframe and store them in a series
    (Series is a one-dimensional labeled array capable of holding data of
    any type (integer, string, float, python objects, etc.). The axis
    labels are collectively called index)

    Parameters
    -----------------

    dt: dataframe
        The dataframe with all the stored values

    Returns
    -----------

    T_in_DHW: series
        An array countaining all the values of the inlet temperature coming from the grid [°C]
    T_out_avg: series
         An array countaining all the values of the average outlet temperature for the domestic hot water [°C]
    T_out_PT100: series
         An array countaining all the values of the outlet temperature for the domestic hot water - sensor PT100 [°C]
    T_out_TC1: series
         An array countaining all the values of the outlet temperature for the domestic hot water - sensor TC1 [°C]
    T_out_TC2: series
         An array countaining all the values of the outlet temperature for the domestic hot water - sensor TC2 [°C]
    T_out_TC3: series
         An array countaining all the values of the outlet temperature for the domestic hot water - sensor TC3 [°C]
    T_fume: series
         An array countaining all the values of the outlet temperature of the smoke exiting the Heat Master or Water Master [°C]
    flow_valve_1_L: series
         An array countaining all the values of the water flow [L/min] in the first valve
    flow_valve_2_L: series
         An array countaining all the values of the water flow [L/min] in the second valve
    By_pass_val_ON : series
         Counter 0-1 to know when the by-pass valve is on
    Tap_val_ON : series
         Counter 0-1 to know when the tapping valve is on
    P_val_in: series
         An array countaining all the values of the inlet pressure [bar]
    Gas_vol: series
         Total amount of gas consumed during the three days [L]
    Gas_counter_L: series
         An array countaining all the values of the volume of gas consumption [L/s]
    t_str_rec: series
         A value indicating the date and time when the test actually started

    """

    T_in_DHW = dt["TE1"]  # Inlet temperature coming from the grid [°C]
    T_out_avg = dt["TE2"]  # Average outlet temperature for the domestic hot water [°C]
    # T_out_PT100 = dt["T°out PT100  [°C]"] # Outlet temperature for the domestic hot water - sensor PT100 [°C]
    # T_out_TC1 = dt["T°out TC1  [°C]"] # Outlet temperature for the domestic hot water - sensor TC1 [°C]
    # T_out_TC2 = dt["T°out TC2  [°C]"] # Outlet temperature for the domestic hot water - sensor TC2 [°C]
    # T_out_TC3 = dt["T°out TC3  [°C]"] # Outlet temperature for the domestic hot water - sensor TC3 [°C]
    T_fume = dt["TF1"]  # Outlet temperature of the smoke exiting the Heat Master [°C]
    flow_valve_1 = dt["DE1"]  # Water flow [m^3/h] of the first valve
    flow_valve_1_L = (
        flow_valve_1 * 1000 / 60
    )  # Water flow [L/min] of the first valve (1 m^3 = 1000 L and 1/h = 1/60 min)
    flow_valve_2 = dt["DE2"]  # Water flow [m^3/h] of the second valve
    flow_valve_2_L = flow_valve_2 * 1000 / 60  # Water flow [L/min] of the first valve
    By_pass_val_ON = dt["EVE6"]  # Counter 0-1 to know when the by-pass valve is on
    Tap_val_ON = dt["EVE7"]  # Counter 0-1 to know when the tapping valve is on
    P_val_in = dt["PE1"]  # Pressure of the inlet valve [bar]
    Tot_gas_vol = dt["DG1"]  # Total amount of gas consumed during the three days [m^3]
    Gas_vol = (
        Tot_gas_vol - Tot_gas_vol[14000]
    ) * 1000  # Total amount of gas consumed during the three days [L] OSS: We are correcting the Gas with the value after the first night
    Gas_counter = dt[
        "DebitGaz_DG1"
    ]  # Counter of amount of gas consumed when burner is on [m^3/h]
    Gas_counter_L = (
        Gas_counter * 1000 / 3600
    )  #  Counter of amount of gas consumed when burner is on [L/s]
    t_str_rec = pd.to_datetime(
        dt["Unnamed: 0"][0], dayfirst="True"
    )  # Actual time when we start recording

    return (
        t_str_rec,
        T_in_DHW,
        T_out_avg,
        T_fume,
        flow_valve_1_L,
        flow_valve_2_L,
        P_val_in,
        By_pass_val_ON,
        Tap_val_ON,
        Gas_vol,
        Gas_counter_L,
    )


def read_df_SEEB_Enr5(dt):
    """
    Function to read some columns of the dataframe and store them in a series
    (Series is a one-dimensional labeled array capable of holding data of
    any type (integer, string, float, python objects, etc.). The axis
    labels are collectively called index)

    Parameters
    -----------------

    dt: dataframe
        The dataframe with all the stored values

    Returns
    -----------

    T_in_DHW: series
        An array countaining all the values of the inlet temperature coming from the grid [°C]
    T_out_avg: series
         An array countaining all the values of the average outlet temperature for the domestic hot water [°C]
    T_fume: series
         An array countaining all the values of the outlet temperature of the smoke exiting the Heat Master or Water Master [°C]
    flow_DHW_kg: series
         An array countaining all the values of the water flow [kg/min]
    Gas_vol: series
         An array countaining all the values of the volume of gas consumption [L]
    P_val_in: series
         An array countaining all the values of the inlet pressure [bar]
    Pow_cons: series
         An array countaining all the values of the energy consumption of the whole electronic: fan, pumo and elec board [W]
    Cum_energy: series
         An array countaining the cumulative consumption of energy [kWh]
    t_str_rec: series
         A value indicating the date and time when the test actually started
    T_amb: series
        An array countaining all the values of the ambiente temperature - T°Amb [°C]
    """

    # t_str_rec = pd.to_datetime(dt["Date Time"][0],dayfirst="True") # Actual time when we start recording
    t_str_rec = pd.to_datetime(dt["Timestamp"][0], dayfirst="True")  # Actual time when we start recording
    T_in_DHW = dt["T°in DHW [°C]"]  # Inlet temperature coming from the grid [°C]
    T_out_avg = dt["T°out TC  [°C]"]  # Average outlet temperature for the domestic hot water [°C]
    T_fume = dt["T°Fume [°C]"]  # Outlet temperature of the smoke exiting the Heat Master [°C]
    flow_DHW_kg = dt["FLDHW [kg/min]"]  # Water flow [kg/min]. This is the flow corrected with the density and Cp. It is not computed if the value is less than 0.5. It will be considered as 0.
    Gas_vol = dt["Cumul. Gaz Vol. Corr.[L]"]  # Volume of gas consumption [L]
    P_val_in = dt["pin DHW [bar]"]  # Pressure of the inlet valve [bar]
    Pow_cons = dt["Power Absorbed [W]"]  # Energy consumption of the whole electronic: fan, pump and boards [W]
    T_amb = dt["T°Amb [°C]"]  # Cumulative consunmption of energy [kWh]
    Cum_energy = dt["Cumul. QDHW  [kWh]"]  # Cumulative consunmption of energy [kWh]

    return (
        t_str_rec,
        T_in_DHW,
        T_out_avg,
        T_fume,
        flow_DHW_kg,
        Gas_vol,
        P_val_in,
        Pow_cons,
        Cum_energy,
        T_amb
    )


def read_df_microcom(dt, pump):
    """
    Function to read some columns of the dataframe and store them in a series
    (Series is a one-dimensional labeled array capable of holding data of
    any type (integer, string, float, python objects, etc.). The axis
    labels are collectively called index)

    Parameters
    -----------------

    dt: dataframe
        The dataframe with all the stored values

    Returns
    -----------

    T_sup: series
        An array countaining all the values of the supply temperature [°C]. Sensor between the two big ballons.
    T_ret: series
         An array countaining all the values of the temperature in order to cool down the boiler [°C]. Tube connected to the pump.
    T_DHW_stor: series
         An array countaining all the values of the temperature inside the big ballon [°C]
    Flame_current: series
         An array countaining all the values of the current [A] * 10^-6
    T_fume_mc: series
         An array countaining all the values of the outlet temperature of the smoke exiting the Heat Master or Water Master [°C]
    Burn_mod: series
         An array countaining all the values of the the burning modulation [%]
    pump: string
         An array with "yes" or "no" deciding if loading the pump power/speed of MicroCOM
    """

    T_sup = dt["Supply [°C]"]  # Temperature on the main tank [°C]
    T_ret = dt["Return [°C]"]  # Temperature on the pump pipe to cool down the burner [°C]
    T_DHW_stor = dt["DHW stor (°C)"]  # Temperature inside the big ballon [°C]
    Flame_current = dt["Flame Curent [uA]"]  # Flame current [A] * 10^-6
    T_fume_mc = dt["Flue temp [0,01°C]"]  # Temperature on the fume [°C]
    Burn_mod = dt["Actual measured load"]  # Burner modulation [%]

    if pump == "no":

        return T_sup, T_ret, T_DHW_stor, Flame_current, T_fume_mc, Burn_mod

    elif pump == "yes":

        pump_spd_MicroCOM = dt["Pump PWM %(111F)"]  # Pump modulation power [%] (Range:0 - 100 %)
        pump_pwr_MicroCOM = dt["Pump Power W(65F2)"]  # Pump power consumed [W] (Range: 0 - 70 W)
        burner_status = dt["Burner State"]  # Status of the burner

        return (
            T_sup,
            T_ret,
            T_DHW_stor,
            Flame_current,
            T_fume_mc,
            Burn_mod,
            pump_spd_MicroCOM,
            pump_pwr_MicroCOM,
            burner_status,
        )


def read_df_DHW_sens(dt, appliance):
    """
    Function to read some columns of the dataframe and store them in a series
    (Series is a one-dimensional labeled array capable of holding data of
    any type (integer, string, float, python objects, etc.). The axis
    labels are collectively called index)

    Parameters
    -----------------

    dt: dataframe
        The dataframe with all the stored values
    appliance: sting
        Appliance type on which the sensors are located

    Returns
    -----------

    T_1_bas: series
         An array countaining all the values of the temperature sensor on the lowest position
    T_2: series
         An array countaining all the values of the temperature sensor on the second position
    T_3: series
         An array countaining all the values of the temperature sensor on the third position
    T_4: series
         An array countaining all the values of the temperature sensor on the fourth position
    T_5_haut: series
         An array countaining all the values of the temperature sensor on the highest position
    T_6_bas: series
        An array Temperature of the sensor in position 6
    T_7_bas: series
        An array Temperature of the sensor in position 7
    T_8_bas_deep: series
        An array Temperature of the sensor in position 8
    T_1: series
        An array Temperature of the sensor in position XXXX
    T_5: series
        An array Temperature of the sensor in position XXXX
    T_1_top: series
        An array Temperature of the sensor in position XXXX

    """
    if appliance == "Normal":

        T_1_bas = dt["T1 bas"]  # Temperature of the sensor in position 1 [°C]
        T_2 = dt["T2"]  # Temperature of the sensor in position 2 [°C]
        T_3 = dt["T3"]  # Temperature of the sensor in position 3 [°C]
        T_4 = dt["T4"]  # Temperature of the sensor in position 4 [°C]
        T_5_haut = dt["T5 haut"]  # Temperature of the sensor in position 5 [°C]

        return T_1_bas, T_2, T_3, T_4, T_5_haut

    elif appliance == "Monotank":

        T_1_bas = dt["T1 bas"]  # Temperature of the sensor in position 1 [°C]
        T_2 = dt["T2"]  # Temperature of the sensor in position 2 [°C]
        T_3 = dt["T3"]  # Temperature of the sensor in position 3 [°C]
        T_4 = dt["T4"]  # Temperature of the sensor in position 4 [°C]
        T_5_haut = dt["T5 haut"]  # Temperature of the sensor in position 5 [°C]
        T_6_bas = dt["T6 bas"]  # Temperature of the sensor in position 6 [°C]
        T_7_bas = dt["T7 bas"]  # Temperature of the sensor in position 7 [°C]
        T_8_bas_deep = dt["T8 bas deep"]  # Temperature of the sensor in position 8 [°C]

        return T_1_bas, T_2, T_3, T_4, T_5_haut, T_6_bas, T_7_bas, T_8_bas_deep

    elif appliance == "45TC":

        T_1 = dt["T1 Top"]  # Temperature of the sensor in position 1 [°C]
        T_2 = dt["T2"]  # Temperature of the sensor in position 2 [°C]
        T_3 = dt["T3"]  # Temperature of the sensor in position 3 [°C]
        T_4 = dt["T4"]  # Temperature of the sensor in position 4 [°C]
        T_5 = dt["T5 Bottom"]  # Temperature of the sensor in position 5 [°C]

        return T_1, T_2, T_3, T_4, T_5

    elif appliance == "70TC":

        T_1_top = dt["T1 Top"]  # Temperature of the sensor in position 1 [°C]
        T_2 = dt["T2"]  # Temperature of the sensor in position 2 [°C]
        T_3 = dt["T3"]  # Temperature of the sensor in position 3 [°C]
        T_4 = dt["T4"]  # Temperature of the sensor in position 4 [°C]
        T_5 = dt["T5"]  # Temperature of the sensor in position 5 [°C]
        T_6 = dt["T6"]  # Temperature of the sensor in position 6 [°C]
        T_7_bas = dt["T7 bas"]  # Temperature of the sensor in position 7 [°C]

        return T_1_top, T_2, T_3, T_4, T_5, T_6, T_7_bas


def read_df_side_T(dt):
    """
    Function to read some columns of the dataframe and store them in a series
    (Series is a one-dimensional labeled array capable of holding data of
    any type (integer, string, float, python objects, etc.). The axis
    labels are collectively called index)

    Parameters
    -----------------

    dt: dataframe
        The dataframe with all the stored values

    Returns
    -----------

    CH1: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 1 [°C]
    CH2: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 2 [°C]
    CH3: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 3 [°C]
    CH4: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 4 [°C]
    CH5: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 5 [°C]
    CH6: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 6 [°C]
    CH7: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 7 [°C]
    CH8: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 8 [°C]
    CH9: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 9 [°C]
    CH10: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 10 [°C]
    CH11: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 11 [°C]
    CH12: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 12 [°C]
    CH13: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 13 [°C]
    CH14: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 14 [°C]
    CH15: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 15 [°C]
    CH16: series
         An array countaining all the values of the temperature sensor of thermocouple in position n. 16 [°C]

    """

    CH1 = dt["CH1"]  # Temperature of the sensor in position 1 [°C]
    CH2 = dt["CH2"]  # Temperature of the sensor in position 2 [°C]
    CH3 = dt["CH3"]  # Temperature of the sensor in position 3 [°C]
    CH4 = dt["CH4"]  # Temperature of the sensor in position 4 [°C]
    CH5 = dt["CH5"]  # Temperature of the sensor in position 5 [°C]
    CH6 = dt["CH6"]  # Temperature of the sensor in position 6 [°C]
    CH7 = dt["CH7"]  # Temperature of the sensor in position 7 [°C]
    CH8 = dt["CH8"]  # Temperature of the sensor in position 8 [°C]
    CH9 = dt["CH9"]  # Temperature of the sensor in position 9 [°C]
    # CH10 = dt["CH10"] # Temperature of the sensor in position 10 [°C]
    # CH11 = dt["CH11"] # Temperature of the sensor in position 11 [°C]
    # CH12 = dt["CH12"] # Temperature of the sensor in position 12 [°C]
    # CH13 = dt["CH13"] # Temperature of the sensor in position 13 [°C]
    # CH14 = dt["CH14"] # Temperature of the sensor in position 14 [°C]
    # CH15 = dt["CH15"] # Temperature of the sensor in position 15 [°C]
    # CH16 = dt["CH16"] # Temperature of the sensor in position 16 [°C]

    # return CH1,CH2,CH3,CH4
    return CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9
    # return CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9,CH10,CH11,CH12,CH13,CH14
    # return CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9,CH10,CH11,CH12,CH13,CH14,CH15,CH16


def read_df_PLC(dt, complete):
    """
    Function to read some columns of the dataframe and store them in a series
    (Series is a one-dimensional labeled array capable of holding data of
    any type (integer, string, float, python objects, etc.). The axis
    labels are collectively called index)

    Parameters
    -----------------

    dt: dataframe
        The dataframe with all the stored values
    complete : string
        "Yes" or "No". This variable allows to load more data of the dataframe or not

    Returns
    -----------

    PUMP: series
         An array indicating when the pump is on or off. 0 = pump off. 1 = pump on
    PUMP SP: series
         An array countaining all the values of the pump setpoint [°C]. Setpoint between T supply and T return [°C]. It will modulate the pump speed to get closer to this setpoint.
    PUMP SPEED %: series
         An array countaining the pwm signal send to the pump. Namely the speed in %

    """

    if complete == "No":

        pump_onoff = dt["PUMP"]  # Array of 0 and 1 to see if pump is ON or OFF [-]
        pump_stp = dt[
            "PUMP SP"
        ]  # Setpoint of the pump. Delta T between T supply and T return [°C]
        pump_speed = dt["PUMP SPEED %"]  # Pump speed [%]
        # volt_burn = dt["VoltageInput"] # Voltage of the XXX [V]

        return pump_onoff, pump_stp, pump_speed

    if complete == "Yes":

        pump_onoff = dt["PUMP"]  # Array of 0 and 1 to see if pump is ON or OFF [-]
        pump_stp = dt[
            "PUMP SP"
        ]  # Setpoint of the pump. Delta T between T supply and T return [°C]
        pump_speed = dt["PUMP SPEED %"]  # Pump speed [%]
        T_sup = dt["SUPPLY DEG"]  # Temperature on the main tank [°C]
        T_ret = dt[
            "RETURN DEG"
        ]  # Temperature on the pump pipe to cool down the burner [°C]
        T_DHW_stor = dt["DHW DEG"]  # Temperature inside the big ballon [°C]
        Flame_current = dt["FLAME µA"]  # Flame current [A] * 10^-6
        T_fume_mc = dt["FLUE DEG"]  # Temperature on the fume [°C]
        Burn_mod = dt["MICROCOM Mod."]  # Burner modulation

        return (
            T_sup,
            T_ret,
            T_DHW_stor,
            Flame_current,
            T_fume_mc,
            Burn_mod,
            pump_onoff,
            pump_stp,
            pump_speed,
        )


def res_timing(dt, col_name_time, t0_miplan):
    """
    Function to resample the timing array. It matches the different time
    when the recording started

    Parameters
    -----------------

    dt: datafrane
        The dataframe we want to sincronise
    col_name_time : string
        Column name in the dataframe where the time vector is stored
    t0_miplan : date-type
        The date and time taken as reference for sincronizating the data

    Returns
    -----------

    adj_rec_time: series
        An array countaining all the sincronised seconds [s]
    """

    dt_time = pd.to_datetime(
        dt[col_name_time], dayfirst="True"
    )  # have the date and hour in dataframe
    st_year = dt_time.dt.year[0]  # Year when we start recording
    st_month = dt_time.dt.month[0]  # Month when we start recording
    st_day = dt_time.dt.day[0]  # Day when we start recording
    sec_array = (
        dt_time.dt.hour * 60 + dt_time.dt.minute
    ) * 60 + dt_time.dt.second  # have all the hours, min and sec in one array with only seconds
    date_array = dt_time.dt.date  # saving only the date
    index_day = (
        date_array - date_array[0]
    )  # having index of how many days havcce passed
    ind_arr_days_int = index_day / np.timedelta64(
        1, "s"
    )  # array with the number of days passed in seconds
    st_rec_miplan = (
        t0_miplan.hour * 3600 + t0_miplan.minute * 60 + t0_miplan.second
    )  # Staring time of the microplan in seconds
    new_sec_arr = (
        sec_array + ind_arr_days_int - st_rec_miplan
    )  # Correct time to be added from the reference date, corrected from the 0 of the microplan
    # ind_arr_days_int = (index_day/np.timedelta64(1, "s"))/86400 # array with the number of days passed. Just number as integer in days and not seconds
    # new_sec_arr = sec_array + ind_arr_days_int*86400 - (17*3600+22*60+33) # - sec_array[0] # Correct time to be added from the reference date, corrected from the 0 of the microplan
    ref_time = datetime.datetime(
        year=st_year, month=st_month, day=st_day, hour=21, minute=30, second=00
    )  # make a reference time for the tests
    adj_rec_time = [ref_time + datetime.timedelta(seconds=i) for i in new_sec_arr]

    return adj_rec_time


def trace_fig(x_axis, y_axis, group, gourp_ttl, name, col, secd_y_ax, opac, typ_line):
    """
    Function to add the trace on the graphs

    Parameters
    -----------------

    x_axis: array
        Array with values to be plotted on the x axis
    y_axis: array
        Array with values to be plotted on the y axis
    group: string
        Name of the group where to gather the courves
    gourp_ttl: string
        Name of the group to show on graph
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

    The trace of the figure be added to the main graph

    """

    # Adding the trace
    fig.add_trace(
        go.Scatter(
            x=x_axis,
            y=y_axis,
            yaxis="y",
            legendgroup=group,
            legendgrouptitle_text=gourp_ttl,
            name=name,
            opacity=opac,
            #    mode = typ_line,
            #    marker = {"color" : col}),
            line=dict(color=col, width=1.5, dash=typ_line),
        ),
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
    txt_siz_tit,
):
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

    fig.update_xaxes(title=lab_x_ax, title_font={"size": txt_siz_lbl_xy})

    fig.update_yaxes(
        title=lab_prim_y_ax_,
        title_font={"size": txt_siz_lbl_xy},
        secondary_y=False,
        # tickmode = "sync",
    )  # ,type = "log"

    fig.update_yaxes(
        title=lab_sec_y_ax_,
        title_font={"size": txt_siz_lbl_xy},
        # range=[0, 9000],
        secondary_y=True,
        # tickmode = "sync",
        anchor="y",
        # rangemode="tozero",
        # overlaying="y",
        # matches="y",
    )  # ,type = "log"

    fig.update_xaxes(
        spikemode="toaxis+across"
    )  # "toaxis" (will stop at the height of the mouse) / "across" goes for the whole lenght
    fig.update_xaxes(spikesnap="hovered data")
    fig.update_layout(
        hovermode="x"
    )  # "x" lables appear with each colour. "x unified" one unique box that groups all the lable

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


def align_input_user(s: str) -> str:
    spacementForAnswer = 65
    x = 0
    if len(s) < spacementForAnswer:
        x = spacementForAnswer - len(s)
    return s + (" " * x)


# %% THIS SECTION SET THE INPUT PARAMETERS FOR READING CSV FILES

# filter data day 1 - Use Scattergl
# no filter data day 1 - Use Scatter

negativeAnswer = ("NO", "NON", "N", "", "0")

test_req_num = input(align_input_user("Enter the test request number(yyxxx): "))  # Test number according to test request. 23146: HM BO 70kW XXL / 24013: MONOTANK BO 70kW XXL / 24022: HM SO 45kW XXL /
test_appl = input(align_input_user("Enter the test appliance type (HM or Monotank):"))  # The appliance used for the test: HM or Monotank
pow_appl = input(align_input_user("Enter the power type (25, 35, 45, 60, 70, 85, 120, 45X, 25X): "))  # The power of the appliance in kW: 25, 35, 45, 60, 70, 85, 120, 45X, 25X
fol_appl = (test_appl + os.sep + pow_appl + "kW" + os.sep)  # The master folder where the different tests for one appliance are stored
test_num = input(align_input_user("Enter the test letter: "))  # The test number. It can be A, B, C, D, etc.
alg_typ =''
# alg_typ = input(
#     align_input_user("Enter the alorithm number:")
# )  # The algorithm type/number we use for the tests
Plt_MiPLAN = input(align_input_user("Plot MicroPLAN data?       Yes or No:")).upper() not in negativeAnswer  # [Yes or No] - Sting type. Variable to define if we have to load MicroPLAN data and plot them

Plt_SEEB = input(align_input_user("Plot SEEB data?            Yes or No:")).upper()  not in negativeAnswer   # [Yes or No] - Sting type. Variable to define if we have to load SEEB data and plot them
Plt_MiCOM = input(align_input_user("Plot MicroCOM data?        Yes or No:")).upper()  not in negativeAnswer   # [Yes or No] - Sting type. Variable to define if we have to load MicroCOM data and plot them
Plt_DHW = input(align_input_user("Plot FieldLogger data?     Yes or No:")).upper()  not in negativeAnswer   # [Yes or No] - Sting type. Variable to define if we have to load FieldLogger data and plot them
Plt_Side_T = input(align_input_user("Side temperature data?     Yes or No:")).upper()  not in negativeAnswer   # [Yes or No] - Sting type. Variable to define if we have to load thermocouples data and plot them
Plt_PLC = input(align_input_user("Plot PLC data?             Yes or No:")).upper()  not in negativeAnswer   # [Yes or No] - Sting type. Variable to define if we have to load PLC data and plot them

if test_req_num == "23146":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

    if test_num == "A" or test_num == "B":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E" or test_num == "F" or test_num == "G":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 15  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "H":

        T_DHW = 60  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 45  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "I":

        T_DHW = 60  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 30  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24013":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70_Algo" + alg_typ

    if test_num == "A" or test_num == "B":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 15  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 13  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E" or test_num == "E2":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 11  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 14  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "F" or test_num == "G":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 11  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 12  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24022":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM45TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 45  # DHW Setpoint temperature [°C]
        T_ADD = 13  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D" or test_num == "D2" or test_num == "E":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "F":

        T_DHW = 60  # DHW Setpoint temperature [°C]
        T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 16  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "G" or test_num == "H":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "I":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "J" or test_num == "J2" or test_num == "K":

        name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24041":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

    T_DHW = 54  # DHW Setpoint temperature [°C]
    T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
    T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24042":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 15  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 48  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 2  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 48  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E":

        T_DHW = 48  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "F":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "G" or test_num == "H" or test_num == "J" or test_num == "J2":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24052":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

    if test_num == "A" or test_num == "B" or test_num == "C":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24058":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM35TC_Algo" + alg_typ

    if test_num == "A" or test_num == "B":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 7.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 8.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24064":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM120TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 48  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 9  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 4  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "F":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 4  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "G":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24074":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM35TC_Algo" + alg_typ

    if (
        test_num == "B"
        or test_num == "C"
        or test_num == "D"
        or test_num == "E"
        or test_num == "F"
        or test_num == "G"
        or test_num == "H"
    ):

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 8.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24077":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM45XTC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B" or test_num == "C" or test_num == "I":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E" or test_num == "F":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 4  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "G":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 7  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 3  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "H":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "J":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "K":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 6  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "L":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24078":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

    if test_num == "A" or test_num == "B" or test_num == "F" or test_num == "G":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C" or test_num == "D":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 11  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "H":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 9  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "I":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 9  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "J":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 9  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "K" or test_num == "L":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "M":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "N" or test_num == "O":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24079":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM25XTC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 9  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24122":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 6  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E":

        T_DHW = 53  # DHW Setpoint temperature [°C]
        T_ADD = 6  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "F":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "G" or test_num == "H":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "I":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "J":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 9  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "K" or test_num == "O" or test_num == "P" or test_num == "Q":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "M" or test_num == "N":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24123":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM35TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 5.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 4  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B" or test_num == "C":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 5.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24091":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

    if test_num == "A" or test_num == "B":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 5.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 4.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 4.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24086":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM45TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 6.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 11  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 6.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 11  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 5.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 5.5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 12  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24108":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM120TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 11  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D":

        T_DHW = 52  # DHW Setpoint temperature [°C]
        T_ADD = 11  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 19  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and24108 the starting of the burner [°C]

    elif test_num == "F":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 19  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "G":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 18  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    # elif test_num == "H": # Day 1

    #     T_DHW = 49 # DHW Setpoint temperature [°C]
    #     T_ADD = 18 # This is the delta T between the T_CH and T_DHW_SP [°C]
    #     T_HYS = 7 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "H":  # Day 2 and 3

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 17  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "I":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "J" or test_num == "K":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 21  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "L" or test_num == "M":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 21  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "N":

        T_DHW = 48  # DHW Setpoint temperature [°C]
        T_ADD = 20  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "O":

        T_DHW = 48  # DHW Setpoint temperature [°C]
        T_ADD = 18  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "P":

        T_DHW = 48  # DHW Setpoint temperature [°C]
        T_ADD = 16  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24082":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM45XTC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B" or test_num == "C" or test_num == "D":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "24092":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM25XTC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B" or test_num == "C":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D" or test_num == "E":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "25017":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM120TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 21  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "25021":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM85TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "B" or test_num == "D":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 15  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "C":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 13  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "E":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 15  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "F":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 16  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "G" or test_num == "H" or test_num == "M" or test_num == "N":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 14  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "I":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "J":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "K":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 10  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "L":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 9  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 14  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "O" or test_num == "P" or test_num == "Q":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 15  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 10  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "R" or test_num == "S":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 15  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "T" or test_num == "U" or test_num == "V":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 15  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    elif test_num == "W":

        T_DHW = 49  # DHW Setpoint temperature [°C]
        T_ADD = 16  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "25027":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "25063":


    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM35TC" #_Algo" + alg_typ"
    # name_test_descp = fol_test + "_XXL_HM35TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    if test_num == "B":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    if test_num == "C":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    if test_num == "D":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    if test_num == "E":

        T_DHW = 55  # DHW Setpoint temperature [°C]
        T_ADD = 5  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    if test_num == "F":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 6  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    if test_num == "H":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 5  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    if test_num == "G":

        T_DHW = 54  # DHW Setpoint temperature [°C]
        T_ADD = 8  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 6  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "25066":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM70TC" #_Algo" + alg_typ"
    # name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    if test_num == "B":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 7  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    if test_num == "C":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    if test_num == "D":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    if test_num == "E":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    if test_num == "F":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    if test_num == "G":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

elif test_req_num == "25013":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM60TC"#_Algo" + alg_typ
    # name_test_descp = fol_test + "_XXL_HM60TC_Algo" + alg_typ

    if test_num == "A":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 13  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    if test_num == "B":
        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 13  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]


elif test_req_num == "25028":

    fol_test = test_req_num + test_num
    name_test_descp = fol_test + "_XXL_HM60TC_Algo" + alg_typ

    if test_num == "A" or test_num == "B" or test_num == "C":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 12  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "D" or test_num == "E" or test_num == "F":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 13  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 9  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "G":

        T_DHW = 51  # DHW Setpoint temperature [°C]
        T_ADD = 13  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

    elif test_num == "H" or test_num == "I":

        T_DHW = 50  # DHW Setpoint temperature [°C]
        T_ADD = 13  # This is the delta T between the T_CH and T_DHW_SP [°C]
        T_HYS = 8  # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

test_descp_miplan = "Microplan_Log"  # Microplan test description
test_descp_micom = "Microcom"  # Microcom test description
test_descp_DHW = "DHW_Temperature"  # DHW test description
test_descp_side_T = "Side_Temperature"  # DHW test description
test_descp_PLC = "PLC"  # PLC test description
test_descp_SEEB = "SEEB"  # SEEB test description
test_descp_SEEB_Enr5 = "SEEB_Enr5"  # SEEB test description

name_test_miplan = name_test_descp + "_" + test_descp_miplan
name_test_micom = name_test_descp + "_" + test_descp_micom
name_test_DHW = name_test_descp + "_" + test_descp_DHW
name_test_side_T = name_test_descp + "_" + test_descp_side_T
name_test_PLC = name_test_descp + "_" + test_descp_PLC
name_test_SEEB = name_test_descp + "_" + test_descp_SEEB
name_test_SEEB_Enr5 = name_test_descp + "_" + test_descp_SEEB_Enr5

compl_path = (fol_appl + fol_test)  # complete path where we saved the csv file of the tests

# get the start time
st = time.time()


if Plt_MiPLAN:

    dt_microplan = read_csv_file(compl_path, name_test_miplan, ",")

if Plt_SEEB:

    # dt_SEEB = read_csv_file(compl_path,name_test_SEEB,"\t")
    dt_SEEB_Enr5 = read_csv_file(compl_path, name_test_SEEB_Enr5, ",")

if Plt_MiCOM:

    dt_microcom = read_csv_file(compl_path, name_test_micom, ",")

if Plt_DHW:

    dt_DHW = read_csv_file(compl_path, name_test_DHW, ",")

if Plt_Side_T:

    dt_side_T = read_csv_file(compl_path, name_test_side_T, ",")

if Plt_PLC:

    dt_PLC = read_csv_file(compl_path, name_test_PLC, ",")

# get the end time
et_rd_df = time.time()

# get the execution time
rd_time = et_rd_df - st

print(f"Finish reading data in {rd_time:.3f} seconds")

# %% THIS SECTION READ THE CSV DATA AND STORE THEIR VALUES IN DIFFERENT ARRAYS

if Plt_MiPLAN:

    (
        t_st_rec_miplan,
        T_in_DHW,
        T_out_avg,
        T_out_PT100,
        T_out_TC1,
        T_out_TC2,
        T_out_TC3,
        T_fume,
        flow_DHW_kg,
        flow_DHW_L,
        Gas_vol,
        P_valv_in,
        Pow_cons,
        Cum_energy,
        T_amb
    ) = read_df_microplan(dt_microplan)

if Plt_SEEB:

    # t_st_rec_SEEB,T_in_DHW,T_out_avg,T_fume,flow_valve_1_L,flow_valve_2_L,P_val_in,By_pass_val_ON,Tap_val_ON,Gas_vol,Gas_counter_L = read_df_SEEB(dt_SEEB)
    (
        t_st_rec_SEEB,
        T_in_DHW,
        T_out_avg,
        T_fume,
        flow_kg,
        Gas_vol,
        P_val_in,
        Pow_cons,
        Cum_energy,
        T_amb
        
    ) = read_df_SEEB_Enr5(dt_SEEB_Enr5)

if Plt_MiCOM:

    # T_sup,T_ret,T_DHW_stor,Flame_current,T_fume_mc,Burn_mod = read_df_microcom(dt_microcom,"no") # Storing the MICROCOM
    (
        T_sup,
        T_ret,
        T_DHW_stor,
        Flame_current,
        T_fume_mc,
        Burn_mod,
        pump_speed_mCOM,
        pump_pwr_MicroCOM,
        burner_status,
    ) = read_df_microcom(
        dt_microcom, "yes"
    )  # Storing the MICROCOM

if Plt_DHW:

    # T1, T2, T3, T4, T5 = read_df_DHW_sens(dt_DHW,"Normal") # Storing the DHW data
    # T1, T2, T3, T4, T5, T6, T7, T8 = read_df_DHW_sens(dt_DHW,"Monotank") # Storing the DHW data
    # T1, T2, T3, T4, T5 = read_df_DHW_sens(dt_DHW,"45TC") # Storing the DHW data
    T1, T2, T3, T4, T5, T6, T7 = read_df_DHW_sens( dt_DHW, "70TC")  # Storing the DHW data

if Plt_Side_T:

    # CH1, CH2, CH3, CH4 = read_df_side_T(dt_side_T) # Storing the side temperature data
    CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9 = read_df_side_T(
        dt_side_T
    )  # Storing the side temperature data
    # CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13, CH14, = read_df_side_T(dt_side_T) # Storing the side temperature data
    # CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13, CH14, CH15, CH16, = read_df_side_T(dt_side_T) # Storing the side temperature data

if Plt_PLC:

    # pump_onoff,pump_stp,pump_speed = read_df_PLC(dt_PLC,"No") # Storing the PLC data
    (
        T_sup_PLC,
        T_ret_PLC,
        T_DHW_stor_PLC,
        Flame_current_PLC,
        T_fume_mc_PLC,
        Burn_mod_PLC,
        pump_onoff,
        pump_stp,
        pump_speed,
    ) = read_df_PLC(
        dt_PLC, "Yes"
    )  # Storing the PLC data

# %% THIS SECTION TIME SCALE THE DHW AND MICROCOM DATASET IN ORDER TO
# PLOT THEM WITH THE CORRECT TIME DELAY AND MATCH THE MICROPLAN DATASET


if Plt_MiPLAN:

    add_cor_time_miPLAN = res_timing(dt_microplan, "Timestamp", t_st_rec_miplan)

    if Plt_MiCOM:

        add_cor_time_miCOM = res_timing(dt_microcom, "Time DMY", t_st_rec_miplan)

    if Plt_DHW:

        add_cor_time_DHW = res_timing(dt_DHW, "Date-Time", t_st_rec_miplan)

    if Plt_Side_T:

        add_cor_time_side_T = res_timing(dt_side_T, "Date&Time", t_st_rec_miplan)

    if Plt_PLC:

        add_cor_time_PLC = res_timing(dt_PLC, "DATE-TIME", t_st_rec_miplan)


if Plt_SEEB:

    # # add_cor_time_SEEB = res_timing(dt_SEEB,"Unnamed: 0",t_st_rec_SEEB)
    # add_cor_time_SEEB = res_timing(dt_SEEB_Enr5,"Date Time",t_st_rec_SEEB)
    add_cor_time_SEEB = res_timing(dt_SEEB_Enr5, "Timestamp", t_st_rec_SEEB)

    if Plt_MiCOM:

        add_cor_time_miCOM = res_timing(dt_microcom, "Time DMY", t_st_rec_SEEB)

    if Plt_DHW:

        add_cor_time_DHW = res_timing(dt_DHW, "Date-Time", t_st_rec_SEEB)

    if Plt_Side_T:

        add_cor_time_side_T = res_timing(dt_side_T, "Date&Time", t_st_rec_SEEB)

    if Plt_PLC:

        add_cor_time_PLC = res_timing(dt_PLC, "DATE-TIME", t_st_rec_SEEB)


# %% THIS SECTION DIVIDE THE TIME VECTOR IN THE DIFFERENT DAYS

"""

# a = rec_time_dt
# a.dt.day
# a2 = a.apply(lambda dt: dt.replace(day=25))    # this is to change day if we have a dt

a = pd.to_datetime(add_cor_time_miPLAN,dayfirst="True") # convert list to DatetimeIndex

""" "Programma generale" """
a1 = (a.hour*60+a.minute)*60 + a.second
a2 = np.where(a1 == 0) # controllo a che positione si trova mezzanotte
a3 = np.asanyarray(a2) # make a2 a vector
a4 = a3.ravel # make the vector 1D
days = max(a.day - a.day[0]) # numero di giorni totali
len(a2[0]) == days # check per controllare che non abbaimo perso valori. Magari 00:00:00 non è stato registrato
# len(a4) == days # check per controllare che non abbaimo perso valori. Magari 00:00:00 non è stato registrato
ind_list = np.append(a4, len(a)-1)
# zero_el = np.zeros(1,dtype="int64")
# fin_ind_list = np.append(zero_el, ind_list)
a_new = a.map(lambda t: t.replace(month=2, day=23))

ii = 0
dict_arr = {}
for t in ind_list:
    dict_arr["day"] = a[ii:t]
    ii=t


""
Programma che funziona solo per i test che hanno giorni in 1 mese. Non funziona
fra mesi differenti
""

st_day = a.day[0]
fn_day = max(a.day)
indx_spli_day = np.arange(st_day,fn_day+1)
# days = a.day - a.day[0]
# days_num = max(days)
# np.arange(0,max(days)+1) # creating a vector countaing the number of days passed as integer. Adding +1 because np.arange does not take into account the last value

a_new_date = a.map(lambda t: t.replace(year=2013, month=2, day=1)) # change values to a DatetimeIndex
a_new = a.map(lambda t: t.replace(day=25))
final_arr = a_new.tolist() # convert the DatetimeIndex to list

"""

"""
Working general program

a = pd.to_datetime(add_cor_time_miPLAN,dayfirst="True") # convert list to DatetimeIndex
a1 = (a.hour*60+a.minute)*60 + a.second # convert the time array in seconds
a2 = np.where(a1 == 0) # controllo a che positione si trova mezzanotte
a3 = np.asanyarray(a2) # make a2 a vector
a4 = np.ravel(a3) # make the vector 1D
days = max(a.day - a.day[0]) # numero di giorni totali
len(a2[0]) == days # check per controllare che non abbaimo perso valori. Magari 00:00:00 non è stato registrato
# len(a4) == days # check per controllare che non abbaimo perso valori. Magari 00:00:00 non è stato registrato
ind_list = np.append(a4, len(a)-1)
# zero_el = np.zeros(1,dtype="int64")
# fin_ind_list = np.append(zero_el, ind_list)
a_new = a.map(lambda t: t.replace(month=2, day=23))


num_days = np.arange(0,days+1)

day_and_ind = np.column_stack((num_days,ind_list)) # from 1 D array to a 2D countaining all of them


ii = 0
dict_arr = {}

for t in day_and_ind:
    dict_arr["day_" + str(t[0])] = a_new[ii:t[1]]
    ii=t[1]
"""

# %% EXTRACTING THE STARTING AND ENDING DATE OF THE TESTS

if Plt_MiPLAN:

    rec_time_dt = pd.to_datetime(
        dt_microplan["Timestamp"], dayfirst="True"
    )  # Recording time array

if Plt_SEEB:

    # # rec_time_dt = pd.to_datetime(dt_SEEB["Unnamed: 0"],dayfirst="True") # Recording time array
    # rec_time_dt = pd.to_datetime(dt_SEEB_Enr5["Date Time"],dayfirst="True") # Recording time array
    rec_time_dt = pd.to_datetime(
        dt_SEEB_Enr5["Timestamp"], dayfirst="True"
    )  # Recording time array


st_y = str(rec_time_dt.dt.year[0])  # Year when we start recording
st_m = str(rec_time_dt.dt.month[0])  # Month when we start recording
st_day = str(rec_time_dt.dt.day[0])  # Day when we start recording
end_y = str(rec_time_dt.dt.year[len(rec_time_dt) - 1])  # Year when we end recording
end_m = str(rec_time_dt.dt.month[len(rec_time_dt) - 1])  # Month when we end recording
end_day = str(rec_time_dt.dt.day[len(rec_time_dt) - 1])  # Day when we end recording
date_test_dur = ("_" + st_y + "_" + st_m + "_" + st_day + "_" + end_y + "_" + end_m + "_" + end_day)

# %% THIS SECTION HAS THE SETTED CONDITIONS FOR THE TESTS

T_DHW_SP = np.ones(len(T_out_avg)) * T_DHW  # This is temperature setpoint for DHW [°C]
T_CH = (T_DHW_SP + T_ADD)  # This is the temperature setpoint for CH or primary water or supply temperature [°C]

Burn_ON = np.ones(len(T_out_avg)) * (T_DHW_SP - T_HYS)

T_30 = (np.ones(len(T_out_avg)) * 30)  # This is a straight line at 30 [°C] to see when we are below the delta T requested from the norm
T_45 = (np.ones(len(T_out_avg)) * 45)  # This is a straight line at 45 [°C] to see when we are below the delta T requested from the norm
T_55 = (np.ones(len(T_out_avg)) * 55)  # This is a straight line at 55 [°C] to see if T OUT is above or below this treshold

if Plt_MiPLAN or Plt_SEEB:
    delta_T_req = (T_out_avg - T_in_DHW)  # Delta T required by the norm between T DHW out and T DHW [°C]

if Plt_MiCOM:
    delta_T_boil = T_sup - T_ret  # Delta T between T supply and T of the pump [°C]

if Plt_PLC:
    delta_T_boil_PLC = (T_sup_PLC - T_ret_PLC)  # Delta T between T supply and T of the pump [°C]

# %% THIS SECTION SETS SOME PARAMETERS FOR THE PLOTTING CURVE

op_main_lin = 1  # Set the opacity of the main lines
op_sec_lin = 0.25  # Set the opacity of the secondary lines

lin_typ_1 = "solid"  # Line layout. if we use mode we have to write "lines" in order to have a continuous line
lin_type_2 = "dash"  # Line layout.

# %% THIS SECTION PLOT THE FIGURES

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces

if Plt_MiPLAN:
    add_time_set = add_cor_time_miPLAN

if Plt_SEEB:
    add_time_set = add_cor_time_SEEB


if Plt_MiPLAN:

    trace_fig(
        add_cor_time_miPLAN,
        T_in_DHW,
        "Rep_plot",
        "Report_plot",
        "T in DHW [°C]",
        "cyan",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        T_out_avg,
        "Rep_plot",
        "Report_plot",
        "T out avg [°C]",
        "red",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        flow_DHW_kg,
        "Rep_plot",
        "Report_plot",
        "FLDHW [kg/min]",
        "darkgreen",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        delta_T_req,
        "Rep_plot",
        "Report_plot",
        "Delta T NORM [°C]",
        "darkorange",
        False,
        op_main_lin,
        lin_typ_1,
    )

if Plt_SEEB:

    trace_fig(
        add_cor_time_SEEB,
        T_in_DHW,
        "Rep_plot",
        "Report_plot",
        "T in DHW [°C]",
        "cyan",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_SEEB,
        T_out_avg,
        "Rep_plot",
        "Report_plot",
        "T out avg [°C]",
        "red",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_SEEB,
        flow_kg,
        "Rep_plot",
        "Report_plot",
        "FLDHW [kg/min]",
        "darkgreen",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_SEEB,
        delta_T_req,
        "Rep_plot",
        "Report_plot",
        "Delta T NORM [°C]",
        "darkorange",
        False,
        op_main_lin,
        lin_typ_1,
    )

if Plt_MiCOM:

    trace_fig(
        add_cor_time_miCOM,
        T_sup,
        "Rep_plot",
        "Report_plot",
        "T sup [°C]",
        "darksalmon",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        T_DHW_stor,
        "Rep_plot",
        "Report_plot",
        "T DHW storage [°C]",
        "mediumblue",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        Flame_current,
        "Rep_plot",
        "Report_plot",
        "Flame current [micr A]",
        "peru",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        Burn_mod,
        "Rep_plot",
        "Report_plot",
        "Burner mod[%]",
        "violet",
        False,
        op_main_lin,
        lin_typ_1,
    )

if Plt_MiPLAN:

    trace_fig(
        add_cor_time_miPLAN,
        T_in_DHW,
        "miPLAN",
        "microPLAN",
        "T in DHW [°C]",
        "cyan",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        T_out_avg,
        "miPLAN",
        "microPLAN",
        "T out avg [°C]",
        "red",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        T_out_PT100,
        "miPLAN",
        "microPLAN",
        "T out PT100 [°C]",
        "maroon",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        T_amb,
        "miPLAN",
        "microPLAN",
        "T°Amb [°C]",
        "pink",
        False,
        op_main_lin,
        lin_typ_1,
    )
    
    trace_fig(
        add_cor_time_miPLAN,
        T_out_TC1,
        "miPLAN",
        "microPLAN",
        "T out TC1 [°C]",
        "olivedrab",
        False,
        op_main_lin,
        lin_typ_1,
    )
    # trace_fig(add_cor_time_miPLAN,T_out_TC2,"miPLAN","microPLAN","T out TC2 [°C]","bisque",False,op_main_lin,lin_typ_1)
    trace_fig(
        add_cor_time_miPLAN,
        T_out_TC3,
        "miPLAN",
        "microPLAN",
        "T out TC3 [°C]",
        "fuchsia",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        T_fume,
        "miPLAN",
        "microPLAN",
        "T fume MP[°C]",
        "gray",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        flow_DHW_L,
        "miPLAN",
        "microPLAN",
        "FLDHW [L/min]",
        "lightgreen",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        flow_DHW_kg,
        "miPLAN",
        "microPLAN",
        "FLDHW [kg/min]",
        "darkgreen",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        Gas_vol,
        "miPLAN",
        "microPLAN",
        "Cumul. Gaz Vol. Corr. [L]",
        "orange",
        True,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        P_valv_in,
        "miPLAN",
        "microPLAN",
        "P in [bar]",
        "maroon",
        True,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        Pow_cons,
        "miPLAN",
        "microPLAN",
        "Pow consumption [W]",
        "tomato",
        True,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miPLAN,
        delta_T_req,
        "miPLAN",
        "microPLAN",
        "Delta T NORM [°C]",
        "darkorange",
        False,
        op_main_lin,
        lin_typ_1,
    )
    # trace_fig(add_cor_time_miPLAN,Cum_energy,"Cum ener [kWh]","maroon",False,op_main_lin,lin_typ_1)

if Plt_SEEB:

    trace_fig(
        add_cor_time_SEEB,
        T_in_DHW,
        "SEEB",
        "SEEB",
        "T in DHW [°C]",
        "cyan",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_SEEB,
        T_out_avg,
        "SEEB",
        "SEEB",
        "T out avg [°C]",
        "red",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_SEEB,
        T_fume,
        "SEEB",
        "SEEB",
        "T fume MP[°C]",
        "gray",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_SEEB,
        flow_kg,
        "SEEB",
        "SEEB",
        "FLDHW [kg/min]",
        "darkgreen",
        False,
        op_main_lin,
        lin_typ_1,
    )
    # trace_fig(add_cor_time_SEEB,flow_valve_1_L,"SEEB","SEEB","FLDHW [L/min] valve 1","lightgreen",False,op_main_lin,lin_typ_1)
    # trace_fig(add_cor_time_SEEB,flow_valve_2_L,"SEEB","SEEB","FLDHW [L/min] valve 2","darkgreen",False,op_main_lin,lin_typ_1)
    # trace_fig(add_cor_time_SEEB,Tap_val_ON,"SEEB","SEEB","Flow valve ON","darkblue",False,op_main_lin,lin_typ_1)
    trace_fig(
        add_cor_time_SEEB,
        Gas_vol,
        "SEEB",
        "SEEB",
        "Total Gas consumed [L]",
        "orange",
        True,
        op_main_lin,
        lin_typ_1,
    )
    # trace_fig(add_cor_time_SEEB,Gas_counter_L,"SEEB","SEEB","Gas counter [L/min]","tomato",True,op_main_lin,lin_typ_1)
    trace_fig(
        add_cor_time_SEEB,
        P_val_in,
        "SEEB",
        "SEEB",
        "P in [bar]",
        "maroon",
        True,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_SEEB,
        Pow_cons,
        "SEEB",
        "SEEB",
        "Pow consumption [W]",
        "tomato",
        True,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_SEEB,
        delta_T_req,
        "SEEB",
        "SEEB",
        "Delta T NORM [°C]",
        "darkorange",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_SEEB,
        T_amb,
        "SEEB",
        "SEEB",
        "T°Amb [°C]",
        "pink",
        False,
        op_main_lin,
        lin_typ_1,
    )
    # # trace_fig(add_cor_time_SEEB,Cum_energy,"Cum ener [kWh]","maroon",False,op_main_lin,lin_typ_1)

if Plt_MiCOM:

    trace_fig(
        add_cor_time_miCOM,
        T_sup,
        "miCOM",
        "microCOM",
        "T sup [°C]",
        "darksalmon",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        T_ret,
        "miCOM",
        "microCOM",
        "T return [°C]",
        "deeppink",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        T_DHW_stor,
        "miCOM",
        "microCOM",
        "T DHW storage [°C]",
        "mediumblue",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        Flame_current,
        "miCOM",
        "microCOM",
        "Flame current [micr A]",
        "peru",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        T_fume_mc,
        "miCOM",
        "microCOM",
        "T fume MC[°C]",
        "darkblue",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        Burn_mod,
        "miCOM",
        "microCOM",
        "Burner mod[%]",
        "violet",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        delta_T_boil,
        "miCOM",
        "microCOM",
        "Delta T boiler [°C]",
        "olivedrab",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        pump_speed_mCOM,
        "miCOM",
        "microCOM",
        "Pump modulation [%]",
        "mediumslateblue",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        pump_pwr_MicroCOM,
        "miCOM",
        "microCOM",
        "Pump power consumed [W]",
        "mediumspringgreen",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_miCOM,
        burner_status,
        "miCOM",
        "microCOM",
        "Burner status",
        "tomato",
        False,
        op_main_lin,
        lin_typ_1,
    )

    burner_status

trace_fig(
    add_time_set,
    T_CH,
    "Set",
    "Settings",
    "T CH STP [°C]",
    "orange",
    False,
    op_sec_lin,
    lin_type_2,
)
trace_fig(
    add_time_set,
    Burn_ON,
    "Set",
    "Settings",
    "T BURN ON [°C]",
    "purple",
    False,
    op_sec_lin,
    lin_type_2,
)
trace_fig(
    add_time_set,
    T_DHW_SP,
    "Set",
    "Settings",
    "T DHW Setpoint [°C]",
    "red",
    False,
    op_sec_lin,
    lin_type_2,
)
trace_fig(
    add_time_set,
    T_30,
    "Set",
    "Settings",
    "T = 30 [°C]",
    "black",
    False,
    op_sec_lin,
    lin_type_2,
)
trace_fig(
    add_time_set,
    T_45,
    "Set",
    "Settings",
    "T = 45 [°C]",
    "black",
    False,
    op_sec_lin,
    lin_type_2,
)
trace_fig(
    add_time_set,
    T_55,
    "Set",
    "Settings",
    "T = 55 [°C]",
    "black",
    False,
    op_sec_lin,
    lin_type_2,
)

if Plt_PLC:

    trace_fig(
        add_cor_time_PLC,
        pump_onoff,
        "PLC",
        "PLC",
        "ON/OFF Pump",
        "mediumpurple",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_PLC,
        pump_stp,
        "PLC",
        "PLC",
        "Pump setpoint [°C]",
        "mediumslateblue",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_PLC,
        pump_speed,
        "PLC",
        "PLC",
        "Pump speed [%]",
        "mediumvioletred",
        False,
        op_main_lin,
        lin_typ_1,
    )
    # trace_fig(add_cor_time_PLC,volt_flame_burn,"PLC","PLC","Voltage PLC [V]","rosybrown",False,op_main_lin,lin_typ_1)
    trace_fig(
        add_cor_time_PLC,
        T_sup_PLC,
        "PLC",
        "PLC",
        "T sup [°C]",
        "darksalmon",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_PLC,
        T_ret_PLC,
        "PLC",
        "PLC",
        "T return [°C]",
        "deeppink",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_PLC,
        T_DHW_stor_PLC,
        "PLC",
        "PLC",
        "T DHW storage [°C]",
        "mediumblue",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_PLC,
        Flame_current_PLC,
        "PLC",
        "PLC",
        "Flame current [micr A]",
        "peru",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_PLC,
        T_fume_mc_PLC,
        "PLC",
        "PLC",
        "T fume MC[°C]",
        "darkblue",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_PLC,
        Burn_mod_PLC,
        "PLC",
        "PLC",
        "Burner mod[%]",
        "violet",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_PLC,
        delta_T_boil_PLC,
        "PLC",
        "PLC",
        "Delta T boiler [°C]",
        "olivedrab",
        False,
        op_main_lin,
        lin_typ_1,
    )

if Plt_DHW:

    trace_fig(
        add_cor_time_DHW,
        T1,
        "DHW",
        "DHW",
        "T1 [°C]",
        "black",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_DHW,
        T2,
        "DHW",
        "DHW",
        "T2 [°C]",
        "blue",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_DHW,
        T3,
        "DHW",
        "DHW",
        "T3 [°C]",
        "coral",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_DHW,
        T4,
        "DHW",
        "DHW",
        "T4 [°C]",
        "pink",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_DHW,
        T5,
        "DHW",
        "DHW",
        "T5 [°C]",
        "purple",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_DHW,
        T6,
        "DHW",
        "DHW",
        "T6 [°C]",
        "moccasin",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_DHW,
        T7,
        "DHW",
        "DHW",
        "T7 [°C]",
        "navy",
        False,
        op_main_lin,
        lin_typ_1,
    )
    # trace_fig(add_cor_time_DHW,T8,"DHW","DHW","T8 [°C]","khaki",False,op_main_lin,lin_typ_1)

if Plt_Side_T:

    trace_fig(
        add_cor_time_side_T,
        CH1,
        "Side",
        "Side Temperature",
        "CH1 [°C]",
        "red",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_side_T,
        CH2,
        "Side",
        "Side Temperature",
        "CH2 [°C]",
        "rebeccapurple",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_side_T,
        CH3,
        "Side",
        "Side Temperature",
        "CH3 [°C]",
        "palegreen",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_side_T,
        CH4,
        "Side",
        "Side Temperature",
        "CH4 [°C]",
        "salmon",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_side_T,
        CH5,
        "Side",
        "Side Temperature",
        "CH5 [°C]",
        "lightskyblue",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_side_T,
        CH6,
        "Side",
        "Side Temperature",
        "CH6 [°C]",
        "darkviolet",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_side_T,
        CH7,
        "Side",
        "Side Temperature",
        "CH7 [°C]",
        "darkcyan",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_side_T,
        CH8,
        "Side",
        "Side Temperature",
        "CH8 [°C]",
        "brown",
        False,
        op_main_lin,
        lin_typ_1,
    )
    trace_fig(
        add_cor_time_side_T,
        CH9,
        "Side",
        "Side Temperature",
        "CH9 [°C]",
        "blueviolet",
        False,
        op_main_lin,
        lin_typ_1,
    )
    # trace_fig(add_cor_time_side_T,CH10,"Side","Side Temperature","CH10 [°C]","plum",False,op_main_lin,lin_typ_1)
    # trace_fig(add_cor_time_side_T,CH11,"Side","Side Temperature","CH11 [°C]","orchid",False,op_main_lin,lin_typ_1)
    # trace_fig(add_cor_time_side_T,CH12,"Side","Side Temperature","CH12 [°C]","olive",False,op_main_lin,lin_typ_1)
    # trace_fig(add_cor_time_side_T,CH13,"Side","Side Temperature","CH13 [°C]","mediumspringgreen",False,op_main_lin,lin_typ_1)
    # trace_fig(add_cor_time_side_T,CH14,"Side","Side Temperature","CH14 [°C]","mediumvioletred",False,op_main_lin,lin_typ_1)
    # trace_fig(add_cor_time_side_T,CH15,"Side","Side Temperature","CH15 [°C]","rosybrown",False,op_main_lin,lin_typ_1)
    # # trace_fig(add_cor_time_side_T,CH16,"Side","Side Temperature","CH16 [°C]","orange",False,op_main_lin,lin_typ_1)

# TODO fig.add_vline(x=add_cor_time_side_T[5000])

# Editing layout traces
update_lay_fig("Test time [s]", "Temperature °C", "Gas Vol (L.)", 20, 20, 14, name_test_descp, 16)

plot(fig,filename=fol_appl + fol_test + os.sep + name_test_descp + date_test_dur + ".html")

# plot(fig, filename = path_fig + "HTML" + os.sep + add_path + date + "_" + vel + rpm + tape + test_name + "Evenlope_spectrum_signal_" + name + ".html")
# fig.write_image("Test_1.png", scale=1, width=1920, height=1080)

# %% THIS SECTION SAVES THE DIFFERENT ARRAYS

# save_array = "no"

# if save_array == "yes":

#     path_arr = "Saved_array" + os.sep + "23146" + test_num + os.sep
#     add_cor_time_arr = np.array(add_cor_time_miCOM) # convertin the list into an array

#     np.save(path_arr + "T_in_DHW_test_" + test_num, T_in_DHW)
#     np.save(path_arr + "T_out_avg_test_" + test_num, T_out_avg)
#     np.save(path_arr + "T_fume_mPLAN_test_" + test_num, T_fume)
#     np.save(path_arr + "flow_DHW_L_test_" + test_num, flow_DHW_L)
#     np.save(path_arr + "Gas_vol_test_" + test_num, Gas_vol)
#     np.save(path_arr + "P_valv_in_test_" + test_num, P_valv_in)
#     np.save(path_arr + "Pow_cons_test_" + test_num, Pow_cons)
#     np.save(path_arr + "delta_T_test_" + test_num, delta_T_req)
#     np.save(path_arr + "T_sup_test_" + test_num, T_sup)
#     np.save(path_arr + "T_ret_test_" + test_num, T_ret)
#     np.save(path_arr + "T_DHW_stor_test_" + test_num, T_DHW_stor)
#     np.save(path_arr + "Flame_current_test_" + test_num, Flame_current)
#     np.save(path_arr + "T_fume_mCOM_test_" + test_num, T_fume_mc)
#     np.save(path_arr + "Burn_mod_test_" + test_num, Burn_mod)
#     np.save(path_arr + "rec_time_mPLAN_test_" + test_num, add_cor_time_miPLAN)
#     np.save(path_arr + "rec_time_mCOM_test_" + test_num, add_cor_time_arr)
#     np.save(path_arr + "rec_time_PLC_test_" + test_num, add_cor_time_PLC)

"""
import pathlib
pathlib.Path().resolve() ---- have the path of the current working folder (where the python program is located)

path = pathlib.Path().resolve() --- assign the path to this variable

files = os.listdir(path) --- read all the files and put them in a list. NOTE: the file are read with the extension as well
"""
