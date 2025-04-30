from pandas import read_excel, read_csv
from time import time as ti
from tkinter import Tk, filedialog
from os import listdir, sep, getcwd
from os.path import isfile, join , abspath, dirname
# from CLASS_ImportData import read_file_to_dict
from sys import exit
from enum import Enum
#negativeAnswer = ("NO", "NON", "N", "", "0")

class ErrorFile(Exception):
    pass
class ErrorConverting(Exception):
    pass
class ErrorPloting(Exception):
    pass

class FILE_NAME(Enum):
    MICROPLAN = 1
    MICROCOM = 2
    DHW_TEMPERATURE = 3
    SIDE_TEMPERATURE = 4
    PLC = 5
    SEEB = 6



# %% THIS SECTION SET THE INPUT PARAMETERS

class MicromcomFile():
    pass

class MicroplanFile():
    pass

class DhwTemperatureFile():
    pass

class SideTemperatureFile():
    pass

class PlcFile():
    pass

class ExcelFile():
    pass

class CsvFile():
    pass

class TxtFile():
    pass

class Seebfile():
    pass

class EcoDesign():
    pass


def read_csv_to_df(path_fol, file_name, dlm=',',sk=0):
    """
    Function in order to read the csv file

    Parameters
    -----------------

    path_fol: string
        The main folde parth where the file is located
    file_name: string
        The file name we want to load. It does not have to include csv
    dlm: sting
        How the data are delimited on the csv file

    Returns
    -----------

    df_csv: dataframe
        A dataframe countaining all the data of the excel sheet
    """
    file_path = f"{path_fol}{sep}{file_name}.csv"
    df_csv = read_csv(
        file_path,
        skiprows=sk,
        encoding_errors="ignore",
        low_memory="False",
        delimiter=dlm,
        # header=None, # This option is to have the header as raw stored in the dataframe. In this case we should also activare dtype = "unicode"
        # dtype = "unicode",
        )
    return df_csv



class InputFile():
    # init for the class
    def __init__(self, currDir:str='', Path_File:str='', Type:list[tuple[str,str]]=[]): 
        self.Path_File:str= Path_File
        self.Path_Folder:str= dirname(Path_File)

        if not currDir:
            currDir:str=f"{getcwd}"
        if not Path_File:
            self.Path_File:str= self.Get_File_path(currDir,Type)
            self.Path_Folder:str= dirname(self.Path_File)

    def Get_File_path(currdir,Type:list[tuple[str,str]]=[])->str:
        root = Tk()
        root.withdraw() #use to hide tkinter window
        print("Getting the file to process...")
        Type.append(("All Files", "*.*"))
        filez = filedialog.askopenfilenames(
            parent=root, initialdir=currdir, 
            title='Please select one files',
            filetypes=Type)
        if len(filez) > 0:
            print(f"You chose {filez[0]}")
            return filez[0]#take first file selected
        else:
            raise ErrorFile("No file selected!!")


class InputFolder():
    def __init__(self, currDir:str='', Path_Folder:str=''):
        self.currDir:str=currDir
        self.Path_Folder:str= Path_Folder

        if not currDir:
            self.currDir:str=f"{getcwd}{sep}HM"
        if not Path_Folder:
            self.Path_Folder:str= self.Get_Folder_path(self.currDir)
        
        self.listCSVFile = self.dict_file_type_in_folder(self.Path_Folder,'.csv')


    def Get_Folder_path(self,currdir)->str:
        root = Tk()
        root.withdraw() #use to hide tkinter window
        print("Getting the file to process...")
        folderz = filedialog.askdirectory(
            parent=root, initialdir=currdir, 
            title='Please select a folder')
        if len(folderz) > 0:
            print(f"You chose {folderz[0]}")
            return folderz[0]#take first folder selected
        else:
            raise ErrorFile("No folder selected!!")

    # checking if file exist
    def dict_file_type_in_folder(self,folder:str,type:str='.csv'):
        filtered=[f for f in listdir(folder) if isfile(join(folder,f)) and f.lower().endswith(type)]
        if len(filtered) == 0:
            raise ErrorFile(f"No file '.csv' files found in {folder}")
        return filtered

    # check all files to be plot
    def dict_file_to_plot(self,listFiles=[str])->dict:
        fileFoundToPlot = dict()
        for f in listFiles:
            for xf in FILE_NAME : 
                if xf.name in f.upper():
                    fileFoundToPlot[xf]=f"{self.folder_all}{sep}{f}"
                    break
        if len(fileFoundToPlot) == 0:
            raise ErrorFile(f"No file '.csv' files found in '{self.folder_all}'")
        return fileFoundToPlot



#class to handle input from user specific to Ecodesign module
class cl_EcoInput(InputFolder):
    # init for the class
    def __init__(self,currDir, Path_File, Path_Folder, Test_request:str='',Test_Num:str='',Appliance_power:str='', Appliance_Type:str='HM'):
        super().__init__(currDir, Path_File, Path_Folder)
        self.test_req_num:str=Test_request
        self.test_letter:str=Test_Num
        self.test_appl:str=Appliance_Type
        self.pow_appl:str=Appliance_power
        self.folder_appl:str= self.updateFolderAppl()
        self.folder_test:str= self.updateFolderTest()

        #start the script
        if self.test_req_num=='':
            self.getting_input_user()
        try:
            self.folder_all = self.check_folder_name(self.folder_appl,self.folder_test)
            self.listCSVFile = self.dict_file_type_in_folder(self.folder_all)
            self.dictFileToPlot = self.dict_file_to_plot(self.listCSVFile)
            
            self.FilesDataFrame = self.import_all_ploting_data(self.dictFileToPlot)
            # print(self.test_parameters)
            print(self.dictFileToPlot)
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
        self.folder_appl = self.updateFolderAppl()
        self.folder_test = self.updateFolderTest()

    # this function allow us to import the data from the csv files put then in dataframe
    def import_all_ploting_data(self,dictFileToPlot)->dict:
        for d in dictFileToPlot:
            if d == FILE_NAME.MICROPLAN:
                print(dictFileToPlot[d])

                #do the stuuuuf
            elif d == FILE_NAME.MICROCOM:
                print(dictFileToPlot[d])
                #do the stuuuuf
            elif d == FILE_NAME.SEEB:
                print(dictFileToPlot[d])
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
        file_path_xlsx = f"{getcwd}{sep}DataTable_TestParam.xlsx"
        #filtering to get only the good test parameter
        # print(read_file_to_dict(file_path_xlsx, file_type='xlsx'))
        test_parameters = list(filter(lambda data: data['TestRequest'] == test_req_num and data['TestNum'] == test_letter, self.read_file_to_dict(file_path_xlsx, file_type='xlsx')))
        
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
            df = read_excel( file_path, sheet_name=sheet_name)
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
    
    Traitement = cl_FileAndInput("25066","A","70")
    