'''
Library 
--------------

Enum:
* FILES_LIST : 
    Enum class with all the file type that we use

Structure:
* ConfigFile : 
    Class to store data and configuration from file

Class: 
* InputFile : 
    This class allow us to open a file and import all the data in a dataframe
* Collection_inputFile :
    This class is created to handle on or multiple InputFile
* InputFolder :
    Class to get the folder path with a file dialog window
* FilterFileFromFolder :
    class calling InputFolder and from the folder gather all the file in it and return a collection of file that is filtered by a critéria of type
    
Example
-------------

In this example, we use InputFolder() to gather all the files in a specific folder, and use this list of files to post process de data

>>> from PlotingData import *
>>> from FileManager import *
>>> #listing all the files in the folder
>>> folder = InputFolder(Path_Folder='C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\Schneider\\client zolder').files_in_folder
>>> files_to_plot={}
>>> #creating the ConfigFile dictionary
>>> for x in folder:
    >>> files_to_plot[x['FileName']] = ConfigFile(
                                        name=x['FileName'], 
                                        path=x['Path'],
                                        header_time='DATE-TIME',
                                        delimiter=';',
                                        row_to_ignore=3,
                                        FileType=x['FileType'],
                                        )
>>> #import the data from all the files
>>> files = InputFile(files_to_plot)


TODO:
--------------
* in inputfile
    - add importation, tab file, txt file, log file, and other
* in inputfolder :
    - get all the file present in folder and subfolder
    - output a structure file that give us the name, path, type, date creation, size


Created by JSB(based on Marcello😍🍕 script)
--------------
V1.1 : 
    * add the read_excel function
    * add a var to class ConfigFile: sheet_name to handle the name of the sheet
V1.0 : initial rev
    * open file and put data in dataframe
    * filter and data manipulation
    * open folder and gather all the file in it
'''
# %% import lib
from pandas import read_csv, to_datetime, DataFrame ,read_excel, concat
from dataclasses import dataclass
from time import time
from tkinter import Tk, filedialog
from os import listdir, sep, getcwd, path
from os.path import basename, normpath, isdir, isfile, join
from enum import Enum
from datetime import datetime, timedelta
from sys import exit
from typing import Union
import logging

# %% structural classes
class FILES_LIST(Enum):
    '''
    Enum class with all the file type that we use

    List
    -----

    - fCSV : CSV file  .csv
    - fTSV : CSV file  .csv
    - fEXCEL : EXCEL file  .xls
    - fEXCELX : EXCEL file  .xlsx
    - fTEXT : TEXT file  .txt
    - fLOG : LOG file  .log
    - fENR : CSV file  .enr

    '''
    fCSV = ('CSV file','.csv')
    fTSV = ('CSV file','.csv')
    fEXCEL = ('EXCEL file','.xls')
    fEXCELX = ('EXCEL file','.xlsx')
    fTEXT = ('TEXT file','.txt')
    fLOG = ('LOG file','.log')
    fENR = ('CSV file','.enr')

@dataclass
class ConfigFile:
    '''
    Class to store data and configuration from file
    
    Parameters
    ----------
    
    name: str default value = ''
        Name of the file
    path: str default value = ''
        Absolute path of the file
    header_time: str  default value = ''
        Time Header file for X axis and to convert to time
    data: DataFrame default value = None
        The result dataframe from the data in the file
    delimiter:str default value = ','
        The delimiter used if CSV file selected
    row_to_ignore:int  default value =  0
        The number of row to ignore before gathering the data in a dataframe
    FileType:tuple[str,str] default value = FILES_LIST.fCSV.value
        The file type of the selected file
    value_to_filter:int default value = 0
        The filter to apply on the dataframe, this is to reduce the number of row
    sheet_name:object default value = 0
        a value to defin the sheet name or the sheet int in a workbook

    '''
    name: str=''
    path: str=''
    header_time: str =''
    header_cumul_time:str=''
    data: DataFrame=None
    delimiter:str=','
    row_to_ignore:int = 0
    FileType:tuple[str,str]=FILES_LIST.fCSV.value
    value_to_filter:int=0
    sheet_name : object = 0


# %% READ files and store in Dataframe
class InputFile():
    '''
    This class allow us to open a file and import all the data in a dataframe
    Later the user can post process the dataframe with basic function

    Example :
    --------

    '''
    def __init__(self, FileData:dict[str,ConfigFile], initialDir:str=''):
        '''
        Initialise the class

        Parameter
        ---------

        FileData : dict[str,ConfigFile]
            set of parameter used to open a new file, this is a dictionary of all the files and configuration
            >>> {Name,ConfigFile()}
        initialDir : str = ''
            the initial directory to go, if we don't have any it will take the initial directory of the script
        '''
        logging.basicConfig(filename='log\\trace.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.initialDir = initialDir
        if not self.initialDir:
            self.initialDir= getcwd()
        if FileData is None:
            self.FileData = self.get_File_path([]) # accept anyfiletype
        else:
            self.FileData = FileData

    def get_File_path(self,FileType:list[tuple[str,str]],value_to_filter=0):
        '''
        This function will open a file dialogue window to get the path of one file

        Parameters
        -----------
        currdir : str
            will start the file dialogue in this initial path
        FileType : list[tuple[str,str]], default val = [[FILES_LIST.fCSV]]
            Type of file we need to find

        Output
        ------
        returns a list of config_file for each file selected 
        '''

        def open_file_dialogue():
            '''
            Open a file dialog window and ask the user to select one or more file(s)
            '''
            root = Tk()
            root.withdraw() #use to hide tkinter window
            FileType.append(("All files", "*.*"))
            filez = filedialog.askopenfilenames(
                parent=root, 
                initialdir=self.initialDir, 
                title='Please select files',
                filetypes=FileType)
            if len(filez) > 0:
                list_as_string = '\n'.join(map(str, filez))
                print("You chose :\n%s",list_as_string)
                logging.info("You chose :\n%s",list_as_string)
                return filez
            else:
                print("No file selected!")
                logging.info("No file selected!")
                exit("-_-_-_-_-_-_-_-\n\nBye bye")

        def init_config_file(list_file,value_to_filter=0):
            '''
            Initiate the config file list with all the files selected

            Parameter
            ---------
            liste_file : 
                list of all the file selected'''
            i=0
            file={}
            for l in list_file:
                i+=1
                file[basename(l.split('.')[0])]=ConfigFile(
                            name=basename(l.split('.')[0]),
                            path=l,
                            header_time='',
                            # data=, (empty)
                            # delimiter=, (default val = ',')
                            row_to_ignore= 0,
                            FileType=check_file_type(l),
                            value_to_filter=value_to_filter,
                            sheet_name=0
                            )
            return file
                
        def check_file_type(path):
            '''
            Identify the file type for each file using the extention of the file

            Parameter
            ---------

            Path : 
                fulle path of the file
            '''
            for c in FILES_LIST:
                if c.value[1] in path:
                    return c.value

        return init_config_file(open_file_dialogue(),value_to_filter)

    def get_df_from_file(self):
        '''
        to update, function to call the right function in order to update self.FileData.data
        '''
        def import_data_by_type(p:str='', delimiter:str=',', row_to_ignore:int=0, sheet_name=0)->DataFrame:
            '''
            to update ,Function to select the correct method to get the data from file into a dataframe
            '''
            if FILES_LIST.fCSV.value[1].upper() in p.upper() :
                df = read_csv_to_df(p,delimiter,row_to_ignore)
                print(f"INPUT_FILE - CSV importation")
                logging.info(f"INPUT_FILE - CSV importation")
            elif FILES_LIST.fEXCELX.value[1].upper() in p.upper() :
                df = read_xlsx_to_df(p,sheet_name,row_to_ignore)
                print(f"INPUT_FILE - Excel importation")
                logging.info(f"INPUT_FILE - Excel importation")
            elif FILES_LIST.fENR.value[1].upper() in p.upper() :
                # do stuff
                i=3
                df= None
            elif FILES_LIST.fLOG.value[1].upper() in p.upper() :
                # do stuff
                i=4
                df= None
            else:
                i=5
                #not handle
                df= None
            return df

        def read_csv_to_df(path_File, dlm=',',sk=0)->DataFrame:
            '''
            This function read an CSV file and convert the data correctly to use it later. 
        
            Parameters
            -----------
            path_File:str
                the path of the file we a trying to open
            dlm : str - deault val =','
                the delimiter used to parse data
            sk : int - deault val = 0
                the number of row ignored

            Output
            -------
            The ouput is dataframe with the dataframe of all the data
            '''
            if path_File!='':
                try:
                    df = read_csv(
                        path_File,
                        skiprows=sk,
                        encoding_errors="ignore",
                        low_memory="False",
                        delimiter=dlm,
                        # header=None, # This option is to have the header as raw stored in the dataframe. In this case we should also activare dtype = "unicode"
                        # dtype = "unicode",
                        )
                except FileNotFoundError:
                    print(f"Le fichier {path_File} n'a pas été trouvé.")
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")
                print(f"INPUT_FILE - Opening file : {path_File}")
                logging.info(f"INPUT_FILE - Opening file : {path_File}")
            else:
                print("No path to import data")
                logging.error("No path to import data")
                return None
            return df
        
        def read_xlsx_to_df(path_File, sheet_name=0 ,sk=0)->DataFrame:
            '''
            This function read an excel file and convert the data correctly to use it later. 
        
            Parameters
            -----------
            path_File:str
                the path of the file we a trying to open
            sheet_name : Any - deault val =0
                the name or the number of the excel sheet
            sk : int - deault val = 0
                the number of row ignored

            Output
            -------
            The ouput is dataframe with the dataframe of all the data
            '''
            if path_File!='':
                try:
                    df = read_excel(
                        io=path_File,
                        sheet_name=sheet_name,
                        skiprows=sk,
                        )
                except FileNotFoundError:
                    print(f"Le fichier {path_File} n'a pas été trouvé.")
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")
                print(f"INPUT_FILE - Opening file : {path_File}")
                logging.info(f"INPUT_FILE - Opening file : {path_File}")
            else:
                print("No path to import data")
                logging.error("No path to import data")
                return None
            return df
        
        file:ConfigFile
        for k,file in self.FileData.items():
            file.data = import_data_by_type(file.path, file.delimiter,file.row_to_ignore, file.sheet_name)
    
    def transfrom_data(self):
        '''
        to update, 
        '''
        def down_sample_dataframe(FileData:ConfigFile)->DataFrame:
            '''
            Function for filtering a line on x
            x : self.FileData.value_to_filter
            
            Parameter
            --------
            df:DataFrame
                the data frame to filter
            '''
            x=FileData.value_to_filter
            if len(FileData.data) > 1000 and x > 1:
                stime = time()
                FileData.data =  FileData.data.iloc[::x]
                print(f"INPUT_FILE - Filtering data  from {FileData.name} : {time()-stime:.2f}")
                logging.info(f"INPUT_FILE - Filtering data  from {FileData.name} : {time()-stime:.2f}")

        def parse_column_date(FileData:ConfigFile):
            '''
            Parse the date time column

            Parameter
            --------
            df:DataFrame
                the data frame to filter
            
            '''
            if FileData.header_time !='':
                if FileData.header_time in FileData.data:
                    stime = time()
                    FileData.data[FileData.header_time] = to_datetime(FileData.data[FileData.header_time], dayfirst="True",errors='raise', format='mixed')  # Actual time when we start recording
                    print(f"INPUT_FILE - Parsing date time columns from {FileData.name} : {time()-stime:.2f}")
                    logging.info(f"INPUT_FILE - Parsing date time columns  from {FileData.name} : {time()-stime:.2f}")
                else:
                    print("Parsing date failed : no column found")
                    logging.error("Parsing date failed : no column found")
        
        file:ConfigFile
        for k,file in self.FileData.items():
            down_sample_dataframe(file)
            parse_column_date(file)

    def sync_file_togheter(self, ref_time:datetime, from_file='',criteria=None, header='',rising_edge_num=1, diff_in_second=0):
        '''
        Function to sync ann the data from a criteria defined by the user

        Parameter
        --------
        criteria:Any = None
            select how the sync is done : 
            if None, sync the file from orgine and the reference 21h30m00s from the start of the file of from a specifique critera

        Output
        ------
        Return the dataframe updated with a new date time frame
        '''
        self.stime = time()
        manual_diff_timing = timedelta(seconds = diff_in_second) # in some case the file 
            
        if criteria==None:
            # if no criteria a mention, we set the synchronisation to ref_time as this would be for the ecodisign mode and we estimate that the time frame a sync allready
            self.ref_time = ref_time
            for k, file in self.FileData.items():
                diff_with_ref_time = ref_time - file.data[file.header_time][0]
                file.data[file.header_time] = file.data[file.header_time] + diff_with_ref_time + manual_diff_timing
        else:
            # in this case we considere all the files from different timing/day/test, so we try to find a specific value on with to start the sync
            self.ref_time = ref_time
            for k, file in self.FileData.items():
                if file.name in from_file:
                    file_rising_time, target_index,l=self.finding_rising_edge(file,header,rising_edge_num,criteria)
                    break
            diff_with_ref_time = ref_time-file_rising_time
            for k, file in self.FileData.items():
                file.data[file.header_time] = file.data[file.header_time] + diff_with_ref_time + manual_diff_timing


        print(f"INPUT_FILE - Synchronze data : {time()-self.stime:.2f}")
        logging.info(f"INPUT_FILE - Synchronze data : {time()-self.stime:.2f}")

    def finding_rising_edge(self,file:ConfigFile,header_sync_name:str, n:int=1, criteria=None):
        '''
        This specific function allow us to find the rising edge based on a selective criteria

        Parameters
        -----------
        file:ConfigFile
            the configuration file on which apply the criteria
        header_sync_name:str
            the serie on which apply the criteria
        n:int=1
            Since we can have more than one result, by default we select the first one
        criteria=None
            depending on the input type we apply different criteria
            * -list- : of 2 elements will search the rising edge of a value between the 2 elements
            * -int- : will search the rising edge of a value above or equal the parameter

        '''
        #depending on the input type we apply different criteria
        if type(criteria)==list: #find value between
            conditional :DataFrame = file.data[header_sync_name].between(min(criteria), max(criteria), inclusive='both')
        elif type(criteria)==int: #find value greater or equal
            conditional :DataFrame = file.data[header_sync_name].ge(fill_value=criteria)
        else:
            return 0

        # conditional :DataFrame = df[header_sync_name].between(2.5, 3.5, inclusive='both')
        rising_edge:DataFrame = conditional & (~conditional.shift(fill_value=False))
        rising_edge_indices = file.data.index[rising_edge]

        # Sélectionner le nième front montant (attention : n commence à 1 ici)
        if len(rising_edge_indices) >= n:
            target_index = rising_edge_indices[n - 1]  # n-1 car indexation Python
            rising_time = file.data.loc[target_index, file.header_time]
            print(f"{n}ᵉ front montant détecté à : {rising_time} sur {len(rising_edge_indices)}")
        else:
            print(f"Moins de {n} fronts montants trouvés.")
        return rising_time, target_index, [{'index':x,'time':file.data.loc[x, file.header_time]} for x in rising_edge_indices]


# %% folder class
class InputFolder():
    '''
    Class to get the folder path with a file dialog window
    '''
    def __init__(self, currDir:str='', Path_Folder:str=''):
        '''
        Initialize the folder class

        Parameter
        ---------
        currDir : str - default value = ''
            set the initial directory, if none set, it will automatically select the dir from the script
        Path_Folder:str=''
            if path '' then a windows appeard 
            if all ready initialize, keep the value in class

        '''
        self.currDir:str=currDir
        self.Path_Folder:str= Path_Folder
        logging.basicConfig(filename='log\\trace.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        if not currDir:
            self.currDir:str=f"{getcwd}{sep}HM"
        logging.info(f"INPUT_FOLDER - Initial folder : {self.currDir}")
        if not isdir(Path_Folder):
            self.Path_Folder:str= self.Get_Folder_path(self.currDir)
        self.dict_file_type_in_folder()

    def Get_Folder_path(self,currdir)->str:
        ''' 
        Get the folder path with a file dialog window

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
        folderz = normpath(filedialog.askdirectory(
            parent=root, initialdir=currdir, 
            title='Please select a folder'))
        if len(folderz) > 0:
            print(f"INPUT_FOLDER - You chose : {folderz}")
            logging.info(f"INPUT_FOLDER - You chose : {folderz}")
            return folderz
        else:
            print("INPUT_FOLDER - No folder selected!!")
            logging.error("INPUT_FOLDER - No folder selected!!")
            exit("-_-_-_-_-_-_-_-\n\nBye bye")
            return None

    def dict_file_type_in_folder(self)->list[str]:
        ''' 
        Check if files type in a folder exist and return the list of them

        Returns
        -----------------
            filtered : list[str]
                the list of all the files from a certain type
        '''
        bad_chars = set("%$^¨µ£~§!&")
        self.all_path_only=[]
        for file in listdir(self.Path_Folder):
            if bad_chars.isdisjoint(file) and isfile(join(self.Path_Folder, file)):
                    self.all_path_only.append(file)
        if len(self.all_path_only) == 0:
            print(f"INPUT_FOLDER - No file files found in {self.Path_Folder}")
            logging.info(f"INPUT_FOLDER - No file files found in {self.Path_Folder}")
        else:
            self.files_in_folder=[]
            for item in self.all_path_only:
                    self.files_in_folder.append({"FileName":item,
                                                "Path":join(self.Path_Folder, item),
                                                "FileType":path.splitext(item)[-1]})

 
 # %% main function on how to use it
if __name__ == "__main__":
    file = ConfigFile(
        name='25066L_XXL_HM70TC_SEEB_Enr5.xlsx',
        path='C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\HM\\70kW\\25066L\\25066L_XXL_HM70TC_SEEB_Enr5.xlsx',
        header_time='Timestamp',
        # data=
        delimiter=',',
        row_to_ignore=0,
        FileType= FILES_LIST.fEXCELX.value,
        value_to_filter=0,
        sheet_name='Seeb Data',
    )
    fi = InputFile(file)

