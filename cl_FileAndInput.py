from pandas import read_csv, to_datetime, DataFrame #read_excel, 
# from time import time as ti
from tkinter import Tk, filedialog
from os import listdir, sep, getcwd
from os.path import isfile, join, dirname, normpath
from enum import Enum
import logging

# Configuration du logging


# %% Enum

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
    def __init__(self, currDir:str='', Path_File:list[str]=None, FileType:list[tuple[str,str]]=[FILES_LIST.fCSV.value], delimiter:str=',', row_to_ignore:int=0):
        logging.basicConfig(filename='log\\InputFile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Starting file opening")
        self.currDir = currDir
        self.Path_File = Path_File
        self.FileType = FileType
        self.delimiter = delimiter
        self.row_to_ignore = row_to_ignore
        if not self.currDir:
            self.currDir:str     = getcwd()
        if not self.Path_File:
            Path_File       = self.get_File_path(self.currDir,self.FileType)

    def get_file_to_df(self):
        logging.info("Loop trough all files selected")
        nbr = len(self.Path_File)
        if nbr==1:
            logging.info("Import one file")
            self.df = self.check_data_type(self.Path_File[0])
        if nbr>1:
            self.df=[]
            logging.info(f"Loop and import {nbr} files")
            for p in self.Path_File:
                self.df.append(self.check_data_type(p))
        else:
            logging.info("No file input")

    def import_data_by_type(self, p:str)->DataFrame:
            if FILES_LIST.fCSV.value[1] in p:
                data = self.read_csv_to_df(p,self.delimiter,self.row_to_ignore)
            elif FILES_LIST.fCSV.value[1] in p:
                # do stuff
                i=2
            elif FILES_LIST.fCSV.value[1] in p:
                # do stuff
                i=3
            elif FILES_LIST.fCSV.value[1] in p:
                # do stuff
                i=4
            else:
                i=5
                #not handle
            return data

    def get_File_path(self,currdir:str,FileType:list[tuple[str,str]]=[FILES_LIST.fCSV.value])->str:
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
        FileType.append(("All files", "*.*"))
        logging.info("Selecting the files")
        filez = filedialog.askopenfilenames(
            parent=root, 
            initialdir=currdir, 
            title='Please select files',
            filetypes=FileType)
        if len(filez) > 0:
            list_as_string = '\n'.join(map(str, filez))
            logging.info("You chose :\n%s",list_as_string)
            return filez
        else:
             logging.info("No file selected!")
    
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
        return df


class File_Ecodesign(InputFile):
    def __Init__(self, currDir:str='', Eco_File:list[dict[str,str]]=None, FileType:list[tuple[str,str]]=[FILES_LIST.fCSV.value], delimiter:str=',', row_to_ignore:int=0):
        super.__init__(currDir,[x['File'] for x in Eco_File],FileType,delimiter,row_to_ignore)
        self.number_file = len(Eco_File)
        if self.number_file == 1:
            self.header_time        = Eco_File[0]['header_time']
            self.file_info          = None
        elif self.number_file > 1:
            self.header_time        = [x['header_time'] for x in Eco_File]
            self.file_info          = []


    def Get_file_to_df(self):
        logging.info("Loop trough all files selected")
        for p in self.Path_File:
            if FILES_LIST.fCSV.value[1] in p:
                self.df.append[self.read_csv_to_df(p,self.delimiter,self.row_to_ignore)]
                if header_time !='':
                    df = self.convert_col_date(df,header_time)
                self.file_info.append(dict(
                    file_type       = FILES_LIST.fCSV, 
                    file_path       = p, 
                    file_directory  = dirname(p), 
                    data            = df,
                    header_time     = header_time
                    ))
            elif FILES_LIST.fCSV.value[1] in p:
                # do stuff
                i=2
            elif FILES_LIST.fCSV.value[1] in p:
                # do stuff
                i=3
            elif FILES_LIST.fCSV.value[1] in p:
                # do stuff
                i=4
            else:
                i=5
                #not handle

    def parse_column_date(self):
        df: DataFrame
        ht: str
        if type(self.df) == 'list':

            for df in self.df:
                conv_col_to_date(df,self.header_time)
        elif type(self.df) == 'dataframe':
            df = self.df
            conv_col_to_date(self.df,self.header_time)

        def conv_col_to_date()->DataFrame:
            nonlocal df
            nonlocal ht
            logging.info("Convert the date columns from string to datetime")
            if ht in df:
                df[ht] = to_datetime(df[ht], dayfirst="True",errors='raise', format='mixed')  # Actual time when we start recording
            else:
                logging.info("Parsing date failed : no column found")
            return df

    def down_sample_dataframe(self,value_to_filter:int=1):
        if df is None:
            df=self.file_info[0]['data']
        return df.iloc[::value_to_filter]




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

if __name__ == "__main__":
    fi = InputFile()
    fl = InputFolder()
    ff = FilterFileFromFolder()
    print(ff.Path_Folder)
    print(ff.FilterdFile)
    print(fl.Path_Folder)
