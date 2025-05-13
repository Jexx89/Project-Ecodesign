from pandas import read_csv, to_datetime, DataFrame #read_excel, 
from dataclasses import dataclass
# from time import time as ti
from tkinter import Tk, filedialog
from os import listdir, sep, getcwd
from os.path import isfile, join, basename, normpath
from enum import Enum
import logging

# %% Enum

class FILES_LIST(Enum):
    fCSV = ('CSV file','.csv')
    fTSV = ('CSV file','.csv')
    fEXCEL = ('EXCEL file','.xls')
    fEXCELX = ('EXCEL file','.xlsx')
    fTEXT = ('TEXT file','.txt')
    fLOG = ('LOG file','.log')
    fENR = ('CSV file','.enr')

@dataclass
class ConfigFile:
    name: str=''
    path: str=''
    header_time: str =''
    data: DataFrame=None
    delimiter:str=','
    row_to_ignore:int = 0
    FileType:tuple[str,str]=FILES_LIST.fCSV.value
    value_to_filter:int=0
# %%

# %% READ files and store in Dataframe
class InputFile():
    # init for the class
    def __init__(self, FileData=ConfigFile):
        logging.basicConfig(filename='log\\InputFile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Starting file opening")
        self.FileData:ConfigFile = FileData
        self.Get_file_to_df()
    
    def Get_file_to_df(self):
        logging.info("Import file")
        self.FileData.data = self.import_data_by_type(self.FileData.path)

    def import_data_by_type(self, p:str)->DataFrame:
            if FILES_LIST.fCSV.value[1] in p:
                return self.read_csv_to_df(p,self.FileData.delimiter,self.FileData.row_to_ignore)
            elif FILES_LIST.fCSV.value[1] in p:
                # do stuff
                i=2
                return None
            elif FILES_LIST.fCSV.value[1] in p:
                # do stuff
                i=3
                return None
            elif FILES_LIST.fCSV.value[1] in p:
                # do stuff
                i=4
                return None
            else:
                i=5
                #not handle
                return None

    def read_csv_to_df(self,path_File, dlm=',',sk=0)->DataFrame:
        if path_File!='':
            logging.info("Import data from .csv")
            df = read_csv(
                path_File,
                skiprows=sk,
                encoding_errors="ignore",
                low_memory="False",
                delimiter=dlm,
                # header=None, # This option is to have the header as raw stored in the dataframe. In this case we should also activare dtype = "unicode"
                # dtype = "unicode",
                )
        else:
            logging.error("No path to import data")
            df=None
        df=self.down_sample_dataframe(df)
        df=self.parse_column_date(df)
        return df

    def down_sample_dataframe(self,df)->DataFrame:
        if len(df)*10 > self.FileData.value_to_filter and self.FileData.value_to_filter > 1:
            df =  df.iloc[::self.FileData.value_to_filter]
        return df

    def parse_column_date(self, df):
        if self.FileData.header_time !='':
            if self.FileData.header_time in df:
                df[self.FileData.header_time] = to_datetime(df[self.FileData.header_time], dayfirst="True",errors='raise', format='mixed')  # Actual time when we start recording
            else:
                logging.info("Parsing date failed : no column found")
        return df
    
    def normalize_date_time(self, diff_time_to_normalise):
        self.FileData.data[self.FileData.header_time] = self.FileData.data[self.FileData.header_time] + diff_time_to_normalise

class Collection_inputFile():
    def __init__(self,initialDir:str='', files_config:list[ConfigFile]=None):

        self.initialDir = initialDir
        if not self.initialDir:
            self.initialDir= getcwd()
        
        self.files_config=files_config
        if self.files_config is None:
            self.files_config = self.get_File_path([])
        if len(self.files_config)>1:
            self.Files = [InputFile(f) for f in self.files_config]
        else:
            self.File = InputFile(self.files_config[0]) 

    
    def get_File_path(self,FileType:list[tuple[str,str]]):
        '''
        This function will open a file dialogue window to get the path of one file

        Parameters:
        -----------

        currdir : str
            will start the file dialogue in this initial path
        FileType : list[tuple[str,str]], default val = [[FILES_LIST.fCSV]]
            Type of file we need to find
        '''
        def open_file_dialogue():
            root = Tk()
            root.withdraw() #use to hide tkinter window
            FileType.append(("All files", "*.*"))
            logging.info("Selecting the files")
            filez = filedialog.askopenfilenames(
                parent=root, 
                initialdir=self.initialDir, 
                title='Please select files',
                filetypes=FileType)
            if len(filez) > 0:
                list_as_string = '\n'.join(map(str, filez))
                logging.info("You chose :\n%s",list_as_string)
                return filez
            else:
                logging.info("No file selected!")


        def init_config_file(liste_file):
            i=0
            file=[]
            for l in liste_file:
                i+=1
                file.append(ConfigFile(
                            name=basename(l.split('.')[0]),
                            path=l,
                            header_time='',
                            # data=,
                            # delimiter=,
                            # row_to_ignore=,
                            FileType=check_file_type(l),
                            # value_to_filter=,
                            ))
            return file
                
        def check_file_type(path):
                for c in FILES_LIST:
                    if c.value[1] in path:
                        return c.value

        return init_config_file(open_file_dialogue())


# %% folder class
class InputFolder():
    def __init__(self, currDir:str='', Path_Folder:str=''):
        self.currDir:str=currDir
        self.Path_Folder:str= Path_Folder
        logging.info("Start module")
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
        logging.info("Selecting the folder")
        folderz = normpath(filedialog.askdirectory(
            parent=root, initialdir=currdir, 
            title='Please select a folder'))
        if len(folderz) > 0:
            logging.info("You chose : %s",folderz)
            return folderz
        else:
             logging.error("No folder selected!!")



class FilterFileFromFolder(InputFolder):

    def __init__(self, currDir:str='', Path_Folder:str='', FileType:list[tuple[str,str]]=[FILES_LIST.fCSV.value]):
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
            logging.info(f"No file ({b}() files found in {folder}")
        return filtered

 # %% main function
if __name__ == "__main__":
    file = ConfigFile(
        #  name=''
        #  path=''
        # header_time=
        # data=
        # delimiter=
        # row_to_ignore=
        # FileType=
        # value_to_filter=
    )
    fi = Collection_inputFile()
    print(fi.files_config)
    # fl = InputFolder()
    # ff = FilterFileFromFolder()
    # print(ff.Path_Folder)
    # print(ff.FilterdFile)
    # print(fl.Path_Folder)
