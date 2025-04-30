from pandas import read_excel, read_csv, to_datetime, to_numeric, DataFrame
from time import time as ti
from tkinter import Tk, filedialog
from os import listdir, sep, getcwd
from os.path import isfile, join, dirname, normpath
# from CLASS_ImportData import read_file_to_dict
# from sys import exit
from enum import Enum
#negativeAnswer = ("NO", "NON", "N", "", "0")

# %% error handling
class ErrorFile(Exception):
    pass
class ErrorConverting(Exception):
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
    def __init__(self, currDir:str='', Path_File:str='', FileType:list[tuple[str,str]]=[FILES_LIST.fCSV]):
        self.Path_File:str= Path_File
        self.Path_Folder:str= dirname(Path_File)
        if not currDir:
            currDir:str=f"{getcwd}"
        if not Path_File:
            self.Path_File:str= self.Get_File_path(currDir,FileType)
            self.Path_Folder:str= dirname(self.Path_File)
        if FileType[0] == FILES_LIST.fCSV:
            self.df = self.read_csv_to_df(self.Path_File)
        elif FileType[0] == FILES_LIST.fEXCELX:
            # do stuff
            i=1
        elif FileType[0] == FILES_LIST.fLOG:
            # do stuff
            i=1
        elif FileType[0] == FILES_LIST.fTSV:
            # do stuff
            i=1

    def Get_File_path(currdir,FileType:list[tuple[str,str]]=[[FILES_LIST.fCSV]])->str:
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

    def read_csv_to_df(Path_File:str, dlm=',',sk=0)->DataFrame:
        df = read_csv(
            Path_File,
            skiprows=sk,
            encoding_errors="ignore",
            low_memory="False",
            delimiter=dlm,
            # header=None, # This option is to have the header as raw stored in the dataframe. In this case we should also activare dtype = "unicode"
            # dtype = "unicode",
            )
        return df


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

class MicroplanFile(InputFile):

    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)
        self.read_df_microplan()

    def read_df_microplan(self):
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
            # df['InertiaMBTPercent'] = df['InertiaMBTPercent'].astype(int)
            # data = df.to_dict(orient='records')
        T_in_DHW = self.df["T°in DHW [°C]"].astype(int)  # Inlet temperature coming from the grid [°C]
        T_out_avg = self.df["T°out AV.  [°C]"]  # Average outlet temperature for the domestic hot water [°C]
        T_out_PT100 = self.df["T°out PT100  [°C]"]  # Outlet temperature for the domestic hot water - sensor PT100 [°C]
        T_out_TC1 = self.df["T°out TC1  [°C]"]  # Outlet temperature for the domestic hot water - sensor TC1 [°C]
        T_out_TC2 = self.df["T°out TC2  [°C]"]  # Outlet temperature for the domestic hot water - sensor TC2 [°C]
        T_out_TC3 = self.df["T°out TC3  [°C]"]  # Outlet temperature for the domestic hot water - sensor TC3 [°C]
        T_fume = self.df["T°Fume [°C]"]  # Outlet temperature of the smoke exiting the Heat Master [°C]
        flow_DHW_kg = self.df["FLDHW [kg/min]"]  # Water flow [kg/min]
        flow_DHW_L = self.df["FLDHW [L/min]"]  # Water flow [L/min]
        Gas_vol = self.df["Cumul. Gaz Vol. Corr.[L]"]  # Volume of gas consumption [L]
        P_val_in = self.df["pin DHW [bar]"]  # Pressure of the inlet valve [bar]
        Pow_cons = self.df["Power Absorbed [W]"]  # Energy consumption of the whole electronic: fan, pump and boards [W]
        Cum_energy = self.df["Cumul. QDHW  [kWh]"]  # Cumulative consunmption of energy [kWh]
        T_amb = self.df["T°Amb [°C]"]  # Cumulative consunmption of energy [kWh]
        t_str_rec = to_datetime( self.df["Timestamp"][0], dayfirst="True")  # Actual time when we start recording

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


# %% Ecodesign classes
class Ecodesign_folder(InputFolder):

    def __init__(self, currDir:str='', Path_Folder:str='', FileType:list[tuple[str,str]]=[[FILES_LIST.fCSV]]):
        super().__init__(currDir,Path_Folder)
        self.FilterdFile = self.dict_file_type_in_folder(self.Path_Folder,FileType)
    # checking if file exist
    def dict_file_type_in_folder(self,folder:str,FileType:list[tuple[str,str]]=[[FILES_LIST.fCSV]]):
        a,b = FileType[0]
        filtered=[f for f in listdir(folder) if isfile(join(folder,f)) and f.lower().endswith(b)]
        if len(filtered) == 0:
            raise ErrorFile(f"No file ({a}() files found in {folder}")
        return filtered

class EcoDesign(Ecodesign_folder):
    def __init__(self, currDir:str='', Path_Folder:str='', FileType:list[tuple[str,str]]=[[FILES_LIST.fCSV]],Test_request:str='',Test_Num:str='',Appliance_power:str='', Appliance_Type:str='HM'):
        super().__init__(currDir, Path_Folder, FileType)
        self.test_req_num:str=Test_request
        self.test_letter:str=Test_Num
        self.test_appl:str=Appliance_Type
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
        spacementForAnswer = 65
        x = 0
        if len(s) < spacementForAnswer:
            x = spacementForAnswer - len(s)
        return s + (" " * x)

    # getting input from user
    def getting_input_user(self):
        self.test_req_num = input(self.align_input_user("Enter the test request number(yyxxx): "))  # Test number according to test request. 23146: HM BO 70kW XXL / 24013: MONOTANK BO 70kW XXL / 24022: HM SO 45kW XXL /
        self.test_letter = input(self.align_input_user("Enter the test letter: ")).upper()  # The test number. It can be A, B, C, D, etc.
        self.pow_appl = input(self.align_input_user("Enter the power type (25, 35, 45, 60, 70, 85, 120, 45X, 25X): "))  # The power of the appliance in kW: 25, 35, 45, 60, 70, 85, 120, 45X, 25X

    # check all files to be plot
    def dict_file_to_plot(self,listFiles=[str], Path_Folder:str='')->dict:
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
        return dict()

#class to handle the parameter section of the ecodesign function
class cl_EcoDesign_Parameter():
    def __init__(self, Test_request:int=1,Test_Num:str='A'):
        self.test_parameters = self.import_test_param(Test_request,Test_Num)

    #import parameter from test
    def import_test_param(self,test_req_num:int,test_letter:str)->list:
        #file path of our parameter table  
        file_path_xlsx = f"{getcwd()}{sep}DataTable_TestParam.xlsx"
        #filtering to get only the good test parameter
        # print(read_file_to_dict(file_path_xlsx, file_type='xlsx'))
        test_parameters = list(filter(lambda data: data['TestRequest'] == test_req_num and data['TestNum'] == test_letter, self.read_xlsx_to_dict(file_path_xlsx, 0)))
        
        if len(test_parameters) < 1:
            raise ErrorFile(f"No parameters found for this test :  '{test_req_num}{test_letter}'")
        elif len(test_parameters) > 1:
            for i in test_parameters: print(i)
            idTest = input("A few parameter set was found please enter the correct 'ID' :")
            test_parameters = list(filter(lambda data: data['ID'] == int(idTest) , test_parameters))
        return test_parameters

    #function used to read the xlsx database of all the parameters
    def read_xlsx_to_dict(self,file_path, sheet_name=0):
        data = []
        try:
            df = read_excel(file_path, sheet_name=sheet_name)
            df['ID'] = df['ID'].astype(int)
            df['SetpointDHW'] = df['SetpointDHW'].astype(int)
            df['ParamADDER'] = df['ParamADDER'].astype(int)
            df['ParamHysteresis'] = df['ParamHysteresis'].astype(int)
            df['ParamAdderCoef'] = df['ParamAdderCoef'].astype(float)
            df['P_factor'] = df['P_factor'].astype(int)
            df['I_Factor'] = df['I_Factor'].astype(int)
            df['SetPointDeltaPump'] = df['SetPointDeltaPump'].astype(int)
            df['PrePumpPercent'] = df['PrePumpPercent'].astype(int)
            df['PrePumpTime'] = df['PrePumpTime'].astype(int)
            df['PrePumpBurningPercent'] = df['PrePumpBurningPercent'].astype(int)
            df['PostPumpPercent'] = df['PostPumpPercent'].astype(int)
            df['PostPumpTime'] = df['PostPumpTime'].astype(int)
            df['InertiaMBTPercent'] = df['InertiaMBTPercent'].astype(int)
            data = df.to_dict(orient='records')
        except FileNotFoundError:
            print(f"Le fichier {file_path} n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        return data


# %% run main function 
if __name__ == "__main__":
    
    Traitement = EcoDesign(Test_request="25066",Test_Num="A",Appliance_power="70")
    