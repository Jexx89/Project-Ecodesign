# -*- coding: utf-8 -*-
"""Created on Mon Jan 04 14:18:56 2024

@author: Marcello Nitti
"""

import numpy as np # importing numpy library
import pandas as pd # importing pandas dataframe
import datetime

#%% CLASS


class ext_data_dt:

    # def __init__(self, dt):

    #     self.dt = dt # Dataframe

    def read_df_microPLAN(self,dt):

        """
        Function to read some columns of the dataframe and store them in a series
        (Series is a one-dimensional labeled array capable of holding data of
        any type (integer, string, float, python objects, etc.). The axis
        labels are collectively called index)

        Parameters
        -----------------

        dt: dataframe
            The dataframe with all the stored values
        st_m: string
            Month when the test started
        st_day: string
            Day when the test started
        end_m: string
            Month when the test finished
        end_day: string
            Day when the test ended

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
        T_out_TC3: series
            An array countaining all the values of the outlet temperature for the domestic hot water - sensor TC1 [°C]
        T_fume: series
            An array countaining all the values of the outlet temperature of the smoke exiting the Heat Master [°C]
        flow_DHW_kg: series
            An array countaining all the values of the water flow [kg/min] corrected with water density and Cp.
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

        """

        T_in_DHW = dt["T°in DHW [°C]"] # Inlet temperature coming from the grid [°C]
        T_out_avg = dt["T°out AV.  [°C]"] # Average outlet temperature for the domestic hot water [°C]
        T_out_PT100 = dt["T°out PT100  [°C]"] # Outlet temperature for the domestic hot water - sensor PT100 [°C]
        T_out_TC1 = dt["T°out TC1  [°C]"] # Outlet temperature for the domestic hot water - sensor TC1 [°C]
        T_out_TC2 = dt["T°out TC2  [°C]"] # Outlet temperature for the domestic hot water - sensor TC2 [°C]
        T_out_TC3 = dt["T°out TC3  [°C]"] # Outlet temperature for the domestic hot water - sensor TC1 [°C]
        T_fume = dt["T°Fume [°C]"] # Outlet temperature of the smoke exiting the Heat Master [°C]
        flow_DHW_kg = dt["FLDHW [kg/min]"] # Water flow [kg/min]. This is the flow corrected with the density and Cp. It is not computed if the value is less than 0.5. It will be considered as 0.
        flow_DHW_L = dt["FLDHW [L/min]"] # Water flow [L/min].
        Gas_vol = dt["Cumul. Gaz Vol. Corr.[L]"] # Volume of gas consumption [L]
        P_val_in = dt["pin DHW [bar]"] # Pressure of the inlet valve [bar]
        Pow_cons = dt["Power Absorbed [W]"] # Energy consumption of the whole electronic: fan, pump and boards [W]
        Cum_energy = dt["Cumul. QDHW  [kWh]"] # Cumulative consunmption of energy [kWh]

        t_str_rec = pd.to_datetime(dt["Timestamp"][0],dayfirst="True") # Actual time when we start recording
        time_arr = pd.to_datetime(dt["Timestamp"],dayfirst="True") # Recording time array

        return t_str_rec,T_in_DHW,T_out_avg,T_out_PT100,T_out_TC1,T_out_TC2,T_out_TC3,T_fume,flow_DHW_kg,flow_DHW_L,Gas_vol,P_val_in,Pow_cons,Cum_energy
        
    
    def read_df_SEEB(self,dt):

        """
        Function to read some columns of the dataframe and store them in a series
        (Series is a one-dimensional labeled array capable of holding data of
        any type (integer, string, float, python objects, etc.). The axis
        labels are collectively called index)

        Parameters
        -----------------

        dt: dataframe
            The dataframe with all the stored values
        st_m: string
            Month when the test started
        st_day: string
            Day when the test started
        end_m: string
            Month when the test finished
        end_day: string
            Day when the test ended

        Returns
        -----------

        T_in_DHW: series
            An array countaining all the values of the inlet temperature coming from the grid [°C]
        T_out_avg: series
            An array countaining all the values of the average outlet temperature for the domestic hot water [°C]
        T_fume: series
            An array countaining all the values of the outlet temperature of the smoke exiting the Heat Master [°C]
        flow_DHW_kg: series
            An array countaining all the values of the water flow [kg/min] corrected with water density and Cp.
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
        Rec_time: series
            An array countaining the time step every second for the whole duration of the test [s]         

        """

        T_in_DHW = dt["TE1"] # Inlet temperature coming from the grid [°C]
        T_out_avg = dt["TE2"] # Average outlet temperature for the domestic hot water [°C]
        # T_out_PT100 = dt["T°out PT100  [°C]"] # Outlet temperature for the domestic hot water - sensor PT100 [°C]
        # T_out_TC1 = dt["T°out TC1  [°C]"] # Outlet temperature for the domestic hot water - sensor TC1 [°C]
        # T_out_TC2 = dt["T°out TC2  [°C]"] # Outlet temperature for the domestic hot water - sensor TC2 [°C]
        # T_out_TC3 = dt["T°out TC3  [°C]"] # Outlet temperature for the domestic hot water - sensor TC3 [°C]
        T_fume = dt["TF1"] # Outlet temperature of the smoke exiting the Heat Master [°C]
        flow_valve_1 = dt["DE1"] # Water flow [m^3/h] of the first valve
        flow_valve_1_L = flow_valve_1*1000/60 # Water flow [L/min] of the first valve (1 m^3 = 1000 L and 1/h = 1/60 min)
        flow_valve_2 = dt["DE2"] # Water flow [m^3/h] of the second valve
        flow_valve_2_L = flow_valve_2*1000/60 # Water flow [L/min] of the first valve
        By_pass_val_ON = dt["EVE6"] # Counter 0-1 to know when the by-pass valve is on
        Tap_val_ON = dt["EVE7"] # Counter 0-1 to know when the tapping valve is on
        P_val_in = dt["PE1"] # Pressure of the inlet valve [bar]
        Tot_gas_vol = dt["DG1"] # Total amount of gas consumed during the three days [m^3]
        Gas_vol = (Tot_gas_vol - Tot_gas_vol[14000])*1000 # Total amount of gas consumed during the three days [L] OSS: We are correcting the Gas with the value after the first night
        Gas_counter = dt["DebitGaz_DG1"] # Counter of amount of gas consumed when burner is on [m^3/h]
        Gas_counter_L = Gas_counter*1000/3600 #  Counter of amount of gas consumed when burner is on [L/s]
        t_str_rec = pd.to_datetime(dt["Unnamed: 0"][0],dayfirst="True") # Actual time when we start recording
        

        return t_str_rec,T_in_DHW,T_out_avg,T_fume,flow_valve_1_L,flow_valve_2_L,P_val_in,By_pass_val_ON,Tap_val_ON,Gas_vol,Gas_counter_L


    def read_df_microCOM(self,dt):

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
        
        """

        T_sup = dt["Supply [°C]"] # Temperature on the main tank [°C]
        T_ret = dt["Return [°C]"] # Temperature on the pump pipe to cool down the burner [°C]
        T_DHW_stor = dt["DHW stor (°C)"] # Temperature inside the big ballon [°C]
        Flame_current = dt["Flame Curent [uA]"] # Flame current [A] * 10^-6
        T_fume_mc = dt["Flue temp [0,01°C]"] # Temperature on the fume [°C]
        Burn_mod = dt["Actual measured load"] # Burner modulation

        return T_sup,T_ret,T_DHW_stor,Flame_current,T_fume_mc, Burn_mod


    def read_df_DHW_sens(self,dt):

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
        
        """

        T_1_bas = dt["T1 bas"] # Temperature of the sensor in position 1 [°C]
        T_2 = dt["T2"] # Temperature of the sensor in position 2 [°C]
        T_3 = dt["T3"] # Temperature of the sensor in position 3 [°C]
        T_4 = dt["T4"] # Temperature of the sensor in position 4 [°C]
        T_5_haut = dt["T5 haut"] # Temperature of the sensor in position 5 [°C]

        return T_1_bas,T_2,T_3,T_4,T_5_haut


    def read_df_DHW_sens_Monotank(self,dt):

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

        T_1_bas: series
            An array countaining all the values of the temperature sensor on the fith position 
        T_2: series
            An array countaining all the values of the temperature sensor on the second position
        T_3: series
            An array countaining all the values of the temperature sensor on the third position
        T_4: series
            An array countaining all the values of the temperature sensor on the fourth position
        T_5_haut: series
            An array countaining all the values of the temperature sensor on the highest position
        T_6_bas: series
            An array countaining all the values of the temperature sensor on the sixth position
        T_7_bas: series
            An array countaining all the values of the temperature sensor on the seventh position     
        T_8_bas_deep: series
            An array countaining all the values of the temperature sensor on the lowest position

        """

        T_1_bas = dt["T1 bas"] # Temperature of the sensor in position 1 [°C]
        T_2 = dt["T2"] # Temperature of the sensor in position 2 [°C]
        T_3 = dt["T3"] # Temperature of the sensor in position 3 [°C]
        T_4 = dt["T4"] # Temperature of the sensor in position 4 [°C]
        T_5_haut = dt["T5 haut"] # Temperature of the sensor in position 5 [°C]
        T_6_bas = dt["T6 bas"] # Temperature of the sensor in position 6 [°C]
        T_7_bas = dt["T7 bas"] # Temperature of the sensor in position 7 [°C]
        T_8_bas_deep = dt["T8 bas deep"] # Temperature of the sensor in position 8 [°C]

        return T_1_bas,T_2,T_3,T_4,T_5_haut,T_6_bas,T_7_bas,T_8_bas_deep

    def read_df_DHW_sens_45TC(self,dt):

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
        
        """

        T_1 = dt["T1 Top"] # Temperature of the sensor in position 1 [°C]
        T_2 = dt["T2"] # Temperature of the sensor in position 2 [°C]
        T_3 = dt["T3"] # Temperature of the sensor in position 3 [°C]
        T_4 = dt["T4"] # Temperature of the sensor in position 4 [°C]
        T_5 = dt["T5 Bottom"] # Temperature of the sensor in position 5 [°C]

        return T_1,T_2,T_3,T_4,T_5


    def read_df_DHW_sens_70TCplus(self,dt):

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

        T_1_top: series
            An array countaining all the values of the temperature sensor on the fith position 
        T_2: series
            An array countaining all the values of the temperature sensor on the second position
        T_3: series
            An array countaining all the values of the temperature sensor on the third position
        T_4: series
            An array countaining all the values of the temperature sensor on the fourth position
        T_5: series
            An array countaining all the values of the temperature sensor on the highest position
        T_6: series
            An array countaining all the values of the temperature sensor on the sixth position
        T_7_bas: series
            An array countaining all the values of the temperature sensor on the seventh position     

        """

        T_1_top = dt["T1 Top"] # Temperature of the sensor in position 1 [°C]
        T_2 = dt["T2"] # Temperature of the sensor in position 2 [°C]
        T_3 = dt["T3"] # Temperature of the sensor in position 3 [°C]
        T_4 = dt["T4"] # Temperature of the sensor in position 4 [°C]
        T_5 = dt["T5"] # Temperature of the sensor in position 5 [°C]
        T_6 = dt["T6"] # Temperature of the sensor in position 6 [°C]
        T_7_bas = dt["T7 bas"] # Temperature of the sensor in position 7 [°C]

        return T_1_top,T_2,T_3,T_4,T_5,T_6,T_7_bas

    def read_df_side_T(self,dt):

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
            An array countaining all the values of the temperature sensor on the higest position (hottest temperature. Values in [°C])
        CH2: series
            An array countaining all the values of the temperature sensor on the second position
        CH3: series
            An array countaining all the values of the temperature sensor on the third position
        CH4: series
            An array countaining all the values of the temperature sensor on the lowest position (coldest temperature. Values in [°C])    
        CH5: series
            An array countaining all the values of the temperature sensor on
        CH6: series
            An array countaining all the values of the temperature sensor on
        CH7: series
            An array countaining all the values of the temperature sensor on 
        CH8: series
            An array countaining all the values of the temperature sensor on     
        CH9: series
            An array countaining all the values of the temperature sensor on     

        """

        CH1 = dt["CH1"] # Temperature of the sensor in position 1 [°C]
        CH2 = dt["CH2"] # Temperature of the sensor in position 2 [°C]
        CH3 = dt["CH3"] # Temperature of the sensor in position 3 [°C]
        CH4 = dt["CH4"] # Temperature of the sensor in position 4 [°C]
        CH5 = dt["CH5"] # Temperature of the sensor in position 5 [°C]
        CH6 = dt["CH6"] # Temperature of the sensor in position 6 [°C]
        CH7 = dt["CH7"] # Temperature of the sensor in position 7 [°C]
        CH8 = dt["CH8"] # Temperature of the sensor in position 8 [°C]
        CH9 = dt["CH9"] # Temperature of the sensor in position 9 [°C]
        # CH10 = dt["CH10"] # Temperature of the sensor in position 10 [°C]
        # CH11 = dt["CH11"] # Temperature of the sensor in position 11 [°C]
        # CH12 = dt["CH12"] # Temperature of the sensor in position 12 [°C]
        # CH13 = dt["CH13"] # Temperature of the sensor in position 13 [°C]
        # CH14 = dt["CH14"] # Temperature of the sensor in position 14 [°C]
        # CH15 = dt["CH15"] # Temperature of the sensor in position 15 [°C]
        # CH16 = dt["CH16"] # Temperature of the sensor in position 16 [°C]

        # return CH1,CH2,CH3,CH4
        return CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9
        # return CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9,CH10,CH11,CH12,CH13,CH14
        # return CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9,CH10,CH11,CH12,CH13,CH14,CH15,CH16


    def read_df_PLC(self,dt):

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

        PUMP: series
            An array indicating when the pump is on or off. 0 = pump off. 1 = pump on
        PUMP SP: series
            An array countaining all the values of the pump setpoint [°C]. Setpoint between T supply and T return [°C]. It will modulate the pump speed to get closer to this setpoint.
        PUMP SPEED %: series
            An array countaining the pwm signal send to the pump. Namely the speed in %  

        """

        pump_onoff = dt["PUMP"] # Array of 0 and 1 to see if pump is ON or OFF [-]
        pump_stp = dt["PUMP SP"] # Setpoint of the pump. Delta T between T supply and T return [°C]
        pump_speed = dt["PUMP SPEED %"] # Pump speed [%]
        
        return pump_onoff,pump_stp,pump_speed
    
    def split_df(self,dt,arr_day_and_indx):

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

        dict_days: dictionary
            Dictionary countaining the dataframe separated in different days

        """
        dict_days = {}
        counter = 0

        for i in arr_day_and_indx:
            dict_days["day_" + str(i[0])] = dt.iloc[counter:i[1],:]
            counter = i[1]

        return dict_days
