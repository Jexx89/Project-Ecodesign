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
from pandas import read_csv, to_datetime, DataFrame ,read_excel
from dataclasses import dataclass
from time import time
from tkinter import Tk, filedialog
from os import listdir, sep, getcwd
from os.path import isfile, join, basename, normpath
from enum import Enum
from datetime import datetime
from sys import exit
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
    '''
    def __init__(self, FileData=ConfigFile):
        '''
        Initialise the class

        Parameter
        ---------

        FileData : ConfigFile
            set of parameter used to open a new file
        '''
        logging.basicConfig(filename='log\\trace.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.FileData:ConfigFile = FileData
        self.stime = time()
        self.Get_file_to_df()
    
    def Get_file_to_df(self):
        '''
        to update, function to call the right function in order to update self.FileData.data
        '''
        df = self.import_data_by_type(self.FileData.path)
        df = self.down_sample_dataframe(df)
        df = self.parse_column_date(df)
        self.FileData.data = df

    def import_data_by_type(self, p:str)->DataFrame:
        '''
        to update ,Function to select the correct method to get the data from file into a dataframe
        '''
        if FILES_LIST.fCSV.value[1] in p:
            df = self.read_csv_to_df(p,self.FileData.delimiter,self.FileData.row_to_ignore)
            print(f"INPUT_FILE - CSV importation")
            logging.info(f"INPUT_FILE - CSV importation")
        elif FILES_LIST.fEXCELX.value[1] in p:
            df = self.read_xlsx_to_df(p,self.FileData.sheet_name,self.FileData.row_to_ignore)
            print(f"INPUT_FILE - Excel importation")
            logging.info(f"INPUT_FILE - Excel importation")
        elif FILES_LIST.fENR.value[1] in p:
            # do stuff
            i=3
            df= None
        elif FILES_LIST.fLOG.value[1] in p:
            # do stuff
            i=4
            df= None
        else:
            i=5
            #not handle
            df= None
        return df

    def read_csv_to_df(self,path_File, dlm=',',sk=0)->DataFrame:
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
    
    def read_xlsx_to_df(self,path_File, sheet_name=0 ,sk=0)->DataFrame:
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

    def down_sample_dataframe(self,df:DataFrame)->DataFrame:
        '''
        Function for filtering a line on x
        x : self.FileData.value_to_filter
        
        Parameter
        --------
        df:DataFrame
            the data frame to filter
        '''
        x=self.FileData.value_to_filter
        if len(df)*10 > x and x > 1:
            self.stime = time()
            df =  df.iloc[::x]
            print(f"INPUT_FILE - Filtering data  from {self.FileData.name} : {time()-self.stime:.2f}")
            logging.info(f"INPUT_FILE - Filtering data  from {self.FileData.name} : {time()-self.stime:.2f}")
        return df

    def parse_column_date(self, df):
        '''
        Parse the date time column

        Parameter
        --------
        df:DataFrame
            the data frame to filter
        
        '''
        if self.FileData.header_time !='':
            if self.FileData.header_time in df:
                self.stime = time()
                df[self.FileData.header_time] = to_datetime(df[self.FileData.header_time], dayfirst="True",errors='raise', format='mixed')  # Actual time when we start recording
                print(f"INPUT_FILE - Parsing date time columns from {self.FileData.name} : {time()-self.stime:.2f}")
                logging.info(f"INPUT_FILE - Parsing date time columns  from {self.FileData.name} : {time()-self.stime:.2f}")
            else:
                print("Parsing date failed : no column found")
                logging.error("Parsing date failed : no column found")
        return df
    
    def diff_standard_time_normalize(self):
        '''
        Allow us to found the différente between the standard normalize hour from the EN15502 : 
        test start at 21h30m00s

        Output
        -------
        return the difference between the reference time and the starting time from the test
        '''
        st_start= self.FileData.data[self.FileData.header_time][0]
        st_year = st_start.year
        st_month = st_start.month
        st_day = st_start.day
        ref_time = datetime(year=st_year, month=st_month, day=st_day, hour=21, minute=30, second=00)  # make a reference time for the tests
        return ref_time - st_start

    def normalize_date_time(self, diff_time_to_normalise):
        '''
        Function to modify the date time columns by adding a define time to it.
        This is usefull when we need to synchronize different file
        
        Parameter
        --------
        diff_time_to_normalise:int
            value in datatime format to add to the datatime column

        Output
        ------
        Return the dataframe updated with a new date time frame
        '''
        self.stime = time()
        self.FileData.data[self.FileData.header_time] = self.FileData.data[self.FileData.header_time] + diff_time_to_normalise
        print(f"INPUT_FILE - Normalizing date time from {self.FileData.name} : {time()-self.stime:.2f}")
        logging.info(f"INPUT_FILE - Normalizing date time from {self.FileData.name} : {time()-self.stime:.2f}")

class Collection_inputFile():
    '''This class is created to handle on or multiple InputFile'''
    def __init__(self,initialDir:str='', files_config:dict[str,ConfigFile]=None):
        '''
        Initialize the class

        Parameters
        ----------
        initialDir : str - default value = ''
            set the initial directory, if none set, it will automatically select the dir from the script
        files_config :list[ConfigFile] - default value = None
            a list of all the input files
        '''
        self.initialDir = initialDir
        if not self.initialDir:
            self.initialDir= getcwd()
        
        self.files_config=files_config
        if self.files_config is None:
            self.files_config = self.get_File_path([])
        if len(self.files_config)>1:
            self.Files = {k:InputFile(v) for k,v in self.files_config.items()}
        else:
            self.File = {self.files_config[0].name:InputFile(self.files_config[0])}

    def get_File_path(self,FileType:list[tuple[str,str]]):
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

        def init_config_file(list_file):
            '''
            Initiate the config file list with all the files selected

            Parameter
            ---------
            liste_file : 
                list of all the file selected'''
            i=0
            file=[]
            for l in list_file:
                i+=1
                file.append(ConfigFile(
                            name=basename(l.split('.')[0]),
                            path=l,
                            header_time='',
                            # data=, (empty)
                            # delimiter=, (default val = ',')
                            # row_to_ignore= (),
                            FileType=check_file_type(l),
                            # value_to_filter=,
                            ))
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

        return init_config_file(open_file_dialogue())

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
        if not Path_Folder:
            self.Path_Folder:str= self.Get_Folder_path(self.currDir)

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
            print("INPUT_FOLDER - You chose : %s",folderz)
            logging.info("INPUT_FOLDER - You chose : %s",folderz)
            return folderz
        else:
            print("INPUT_FOLDER - No folder selected!!")
            logging.error("INPUT_FOLDER - No folder selected!!")
            exit("-_-_-_-_-_-_-_-\n\nBye bye")
            return None
            

class FilterFileFromFolder(InputFolder):
    '''
    class calling InputFolder and from the folder gather all the file in it and return a collection of file that is filtered by a critéria of type
    '''
    def __init__(self, currDir:str='', Path_Folder:str='', FileType:list[tuple[str,str]]=[FILES_LIST.fCSV.value]):
        '''
        Initialize the class

        Parameter
        ---------
        currDir : str - default value = ''
            set the initial directory, if none set, it will automatically select the dir from the script
        Path_Folder:str=''
            if path '' then a windows appeard 
            if all ready initialize, keep the value in class
        FileType:list[tuple[str,str]]=[FILES_LIST.fCSV.value]
            the criteria based on the file type 
        '''
        super().__init__(currDir,Path_Folder)
        self.FilterdFile = self.dict_file_type_in_folder(self.Path_Folder,FileType)
        self.CompletePath = [dict(full_path=f"{self.Path_Folder}\\{item}",name=item) for item in self.FilterdFile]

    def dict_file_type_in_folder(self,folder:str,FileType:list[tuple[str,str]]=[FILES_LIST.fCSV.value])->list[str]:
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
        b = FileType[0]
        filtered=[f for f in listdir(folder) if isfile(join(folder,f)) and f.lower().endswith(b)]
        if len(filtered) == 0:
            print(f"INPUT_FOLDER - No file ({b}) files found in {folder}")
            logging.info(f"INPUT_FOLDER - No file ({b}) files found in {folder}")
        return filtered

 
 # %% main function on how to use it
if __name__ == "__main__":
    # file = ConfigFile(
    #     #  name=''
    #     #  path=''
    #     # header_time=
    #     # data=
    #     # delimiter=
    #     # row_to_ignore=
    #     # FileType=
    #     # value_to_filter=
    # )
    fi = Collection_inputFile()
    print(fi.files_config)

