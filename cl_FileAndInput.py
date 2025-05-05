from pandas import read_excel, read_csv, to_datetime, to_numeric, DataFrame
from time import time as ti
from tkinter import Tk, filedialog
import numpy as np  # importing numpy library
from os import listdir, sep, getcwd
from os.path import isfile, join, dirname, normpath
from cl_EcoParam import *
from plotly import graph_objects as go  # importing plotly for plotting figures
from plotly.offline import plot
from plotly.subplots import (make_subplots)  # importing subplots to plot several curves in the same graph
# from CLASS_ImportData import read_file_to_dict
# from sys import exit
from enum import Enum
#negativeAnswer = ("NO", "NON", "N", "", "0")

# %% error handling
class ErrorFile(Exception):
    pass
class ErrorConverting(Exception):
        # try:
        # except ErrorConverting as error:
        #     print(f"\nConverting files interupted : {error}")
    pass
class ErrorPloting(Exception):
    pass


# %% enum classes
class FILE_NAME(Enum):
    MICROPLAN = 1
    MICROCOM = 2
    DHW_TEMPERATURE = 3
    SIDE_TEMPERATURE = 4
    PLC = 5
    SEEB = 6

class FILES_LIST(Enum):
    fCSV = ('CSV file','.csv')
    fTSV = ('CSV file','.csv')
    fEXCEL = ('EXCEL file','.xls')
    fEXCELX = ('EXCEL file','.xlsx')
    fTEXT = ('TEXT file','.txt')
    fLOG = ('LOG file','.log')
    fENR = ('CSV file','.enr')


# %% READ files and store in Dataframe
class InputFile():
    # init for the class
    def __init__(self, currDir:str='', Path_File:str='', FileType:list[tuple[str,str]]=[FILES_LIST.fCSV], header_time:str='Timestamp'):
        self.Path_File:str= Path_File
        self.header_time = header_time
        self.Path_Folder:str= dirname(Path_File)
        if not currDir:
            currDir:str=f"{getcwd}"
        if not Path_File:
            self.Path_File:str= self.Get_File_path(currDir,FileType)
            self.Path_Folder:str= dirname(self.Path_File)
        if FileType[0] == FILES_LIST.fCSV:
            self.df, self.time_start, self.time_end = self.read_csv_to_df(Path_File)
        elif FileType[0] == FILES_LIST.fEXCELX:
            # do stuff
            i=1
        elif FileType[0] == FILES_LIST.fLOG:
            # do stuff
            i=1
        elif FileType[0] == FILES_LIST.fTSV:
            # do stuff
            i=1

    def Get_File_path(self,currdir,FileType:list[tuple[str,str]]=[[FILES_LIST.fCSV]])->str:
        '''
        This function will open a file dialogue window to get the path of one file

        Parameters:
        -----------

        currdir : str
            will start the file dialogue in this initial path
        FileType : list[tuple[str,str]], default val = [[FILES_LIST.fCSV]]
            Type of file we need to find
        '''
        root = Tk()
        root.withdraw() #use to hide tkinter window
        print("Getting the file to process...")
        filez = filedialog.askopenfilenames(
            parent=root, initialdir=currdir, 
            title='Please select one files',
            filetypes=FileType)
        if len(filez) > 0:
            print(f"You chose : '{filez[0]}'")
            return filez[0]#take first file selected
        else:
            raise ErrorFile("No file selected!")
    
    def read_csv_to_df(self, dlm=',',sk=0)->DataFrame:
        df = read_csv(
            self.Path_File,
            skiprows=sk,
            encoding_errors="ignore",
            low_memory="False",
            delimiter=dlm,
            # header=None, # This option is to have the header as raw stored in the dataframe. In this case we should also activare dtype = "unicode"
            # dtype = "unicode",
            )
        df[self.header_time] = to_datetime(df[self.header_time], dayfirst="True")  # Actual time when we start recording

        return df , df[self.header_time][0], df[self.header_time][-1]

    def res_timing(self,dt, col_name_time, t0_miplan):
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

        dt_time = pd.to_datetime(dt[col_name_time], dayfirst="True")  # have the date and hour in dataframe
        st_year = dt_time.dt.year[0]  # Year when we start recording
        st_month = dt_time.dt.month[0]  # Month when we start recording
        st_day = dt_time.dt.day[0]  # Day when we start recording
        sec_array = (dt_time.dt.hour * 60 + dt_time.dt.minute) * 60 + dt_time.dt.second  # have all the hours, min and sec in one array with only seconds
        date_array = dt_time.dt.date  # saving only the date
        index_day = (date_array - date_array[0])  # having index of how many days havcce passed
        ind_arr_days_int = index_day / np.timedelta64(1, "s")  # array with the number of days passed in seconds
        st_rec_miplan = (t0_miplan.hour * 3600 + t0_miplan.minute * 60 + t0_miplan.second)  # Staring time of the microplan in seconds
        new_sec_arr = (sec_array + ind_arr_days_int - st_rec_miplan)  # Correct time to be added from the reference date, corrected from the 0 of the microplan
        # ind_arr_days_int = (index_day/np.timedelta64(1, "s"))/86400 # array with the number of days passed. Just number as integer in days and not seconds
        # new_sec_arr = sec_array + ind_arr_days_int*86400 - (17*3600+22*60+33) # - sec_array[0] # Correct time to be added from the reference date, corrected from the 0 of the microplan
        ref_time = datetime.datetime(year=st_year, month=st_month, day=st_day, hour=21, minute=30, second=00)  # make a reference time for the tests
        adj_rec_time = [ref_time + datetime.timedelta(seconds=i) for i in new_sec_arr]

        return adj_rec_time

# %% differente type of classes to run the files
class MicromFile(InputFile):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)

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


class MicroplanFile(InputFile):

    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)
        self.read_csv_to_df()




class Seebfile(InputFile):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)
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
        t_str_rec = to_datetime(dt["Timestamp"][0], dayfirst="True")  # Actual time when we start recording
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



# %% will check later to sync with previous files
class DhwTemperatureFile(InputFile):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)
        
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

class SideTemperatureFile(InputFile):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)

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

class PlcFile(InputFile):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)
    
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
            pump_stp = dt["PUMP SP"]  # Setpoint of the pump. Delta T between T supply and T return [°C]
            pump_speed = dt["PUMP SPEED %"]  # Pump speed [%]
            # volt_burn = dt["VoltageInput"] # Voltage of the XXX [V]
            return pump_onoff, pump_stp, pump_speed
        if complete == "Yes":
            pump_onoff = dt["PUMP"]  # Array of 0 and 1 to see if pump is ON or OFF [-]
            pump_stp = dt["PUMP SP"]  # Setpoint of the pump. Delta T between T supply and T return [°C]
            pump_speed = dt["PUMP SPEED %"]  # Pump speed [%]
            T_sup = dt["SUPPLY DEG"]  # Temperature on the main tank [°C]
            T_ret = dt["RETURN DEG"]  # Temperature on the pump pipe to cool down the burner [°C]
            T_DHW_stor = dt["DHW DEG"]  # Temperature inside the big ballon [°C]
            Flame_current = dt["FLAME µA"]  # Flame current [A] * 10^-6
            T_fume_mc = dt["FLUE DEG"]  # Temperature on the fume [°C]
            Burn_mod = dt["MICROCOM Mod."]  # Burner modulation
            return (T_sup,T_ret,T_DHW_stor,Flame_current,T_fume_mc,Burn_mod,pump_onoff,pump_stp,pump_speed,)


# %% library to do to be able to plot any kind of file
class ExcelFile(InputFile):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)

class CsvFile(InputFile):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)

class TxtFile(InputFile):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)





# %% folder class
class InputFolder():
    def __init__(self, currDir:str='', Path_Folder:str=''):
        self.currDir:str=currDir
        self.Path_Folder:str= Path_Folder

        if not currDir:
            self.currDir:str=f"{getcwd}{sep}HM"
        if not Path_Folder:
            self.Path_Folder:str= self.Get_Folder_path(self.currDir)

    def Get_Folder_path(self,currdir)->str:
        ''' 
        Check if files type in a folder exist and return the list of them

        Parameter
        -----------------

        currDir : str
            Set the first path to look into when the file dialogue is called
        
        Returns
        -----------------
            Folder : str
                return the folder path

        '''
        root = Tk()
        root.withdraw() #use to hide tkinter window
        print("Getting the file to process...")
        folderz = normpath(filedialog.askdirectory(
            parent=root, initialdir=currdir, 
            title='Please select a folder'))
        if len(folderz) > 0:
            print(f"You chose : '{folderz}'")
            return folderz
        else:
            raise ErrorFile("No folder selected!!")

class FilterFileFromFolder(InputFolder):

    def __init__(self, currDir:str='', Path_Folder:str='', FileType:list[tuple[str,str]]=[[FILES_LIST.fCSV]]):
        super().__init__(currDir,Path_Folder)
        self.FilterdFile = self.dict_file_type_in_folder(self.Path_Folder,FileType)
    def dict_file_type_in_folder(self,folder:str,FileType:list[tuple[str,str]]=[[FILES_LIST.fCSV]])->list[str]:
        ''' 
        Check if files type in a folder exist and return the list of them

        Parameter
        -----------------

        folder : str, default val = ''
            set the path of the folder
        FileType : list[tuple[str,str]], default val = [[FILES_LIST.fCSV]]
            Type of file we need to find
        
        Returns
        -----------------
            filtered : list[str]
                the list of all the files from a certain type

        '''
        a,b = FileType[0]
        filtered=[f for f in listdir(folder) if isfile(join(folder,f)) and f.lower().endswith(b)]
        if len(filtered) == 0:
            raise ErrorFile(f"No file ({a}() files found in {folder}")
        return filtered

# %% Ecodesign classes
class EcoDesign(FilterFileFromFolder):
    '''
    Class specific for ecodesign ploting, incorporating up to 5 differents kind of file to plot in one .html file.
    This class enherit from the class: FilterFileFromFolder -> InputFolder because we a selecting the files first by selecting a folder. 
    '''
    def __init__(self, currDir:str='', Path_Folder:str='', FileType:list[tuple[str,str]]=[[FILES_LIST.fCSV]],Test_request:str='',Test_Num:str='',Appliance_power:str=''):
        '''
        Initialize whent he class is called

        Parameter
        -----------------

        currDir : str, default val = ''
            Set the first path to look into when the file dialogue is called
        Path_Folder : str, default val = ''
            set the path of the folder
        FileType : list[tuple[str,str]], default val = [[FILES_LIST.fCSV]]
            Type of file we need to find
        Test_request : str, default val = ''
            the test request number 
        Test_Num : str, default val = ''
            the test index, here a letter
        Appliance_power : str, default val = ''
            the power of the appliance (boiler)
        
        Returns
        -----------------
        Initialize the class

        '''
        super().__init__(currDir, Path_Folder, FileType)
        self.test_req_num:str=Test_request
        self.test_letter:str=Test_Num
        self.pow_appl:str=Appliance_power

        #start the script
        if self.test_req_num=='':
            self.getting_input_user()
        try:
            self.paramSet = cl_EcoDesign_Parameter(int(self.test_req_num), self.test_letter)
            self.dictFileToPlot = self.dict_file_to_plot(self.FilterdFile,self.Path_Folder)
            self.FilesDataFrame = self.import_all_ploting_data(self.dictFileToPlot)
        except ErrorFile as error:
            print(f"\nOpening files interupted : {error}")

    #allow to align the input in the terminal
    def align_input_user(self,s: str) -> str:
        '''
        Function align the user input command

        Parameter
        -----------------

        s : str
            The string to align
        
        Returns
        -----------------
        string
            a string with blank space to align in the terminal

        '''
        spacementForAnswer = 65
        x = 0
        if len(s) < spacementForAnswer:
            x = spacementForAnswer - len(s)
        return s + (" " * x)

    # getting input from user
    def getting_input_user(self):
        '''
        Getting input from the user :
        - the test request number
        - the test index ( letter here )
        - the power of the appliance in kw

        Parameters
        -----------------

            none
        
        Returns
        -----------------
            void

        '''
        self.test_req_num = input(self.align_input_user("Enter the test request number(yyxxx): "))  # Test number according to test request. 23146: HM BO 70kW XXL / 24013: MONOTANK BO 70kW XXL / 24022: HM SO 45kW XXL /
        self.test_letter = input(self.align_input_user("Enter the test letter: ")).upper()  # The test number. It can be A, B, C, D, etc.
        self.pow_appl = input(self.align_input_user("Enter the power type (25, 35, 45, 60, 70, 85, 120, 45X, 25X): "))  # The power of the appliance in kW: 25, 35, 45, 60, 70, 85, 120, 45X, 25X

    # check all files to be plot
    def dict_file_to_plot(self,listFiles=[str], Path_Folder:str='')->dict:
        '''
        Function to filter all the file that we need to plot for ecodesign ploting
        this dictionary is build base on the condition of the naming of the file

        Parameters
        -----------------

        listFiles : list[str]
            list of the avaible file in the folder
        Path_Folder : str
            The path of the folder to reconstruct the complete path of the file
        
        Returns
        -----------------
        fileFoundToPlot : dictionary
            a dictionary with the name as a key and the full path as a value of all the files we found to plot

        '''
        fileFoundToPlot = dict()
        for f in listFiles:
            for xf in FILE_NAME : 
                if xf.name in f.upper():
                    fileFoundToPlot[xf]=join(Path_Folder,f)
                    break
        if len(fileFoundToPlot) == 0:
            raise ErrorFile(f"No file '.csv' files found in '{Path_Folder}'")
        return fileFoundToPlot

    # this function allow us to import the data from the csv files put then in dataframe
    def import_all_ploting_data(self,dictFileToPlot)->dict:
        '''
        Function to go trough all the files in the dictionary and launch :
            - reading 
            - ploting

        Parameter
        -----------------

        dictFileToPlot : dictionary
            Dictionary with the file path of all the files to plot
        
        Returns
        -----------------
            void
        '''
        for d in dictFileToPlot:
            if d == FILE_NAME.MICROPLAN:
                print(f"fileName :{dictFileToPlot[d]}")

                #do the stuuuuf
            elif d == FILE_NAME.MICROCOM:
                print(f"fileName :{dictFileToPlot[d]}")
                #do the stuuuuf
            elif d == FILE_NAME.SEEB:
                print(f"fileName :{dictFileToPlot[d]}")
                #do the stuuuuf
            break
        return 0




# %% run main function 
if __name__ == "__main__":
    Traitement = EcoDesign(Test_request="25066",Test_Num="A",Appliance_power="70")