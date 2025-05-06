from pandas import read_excel, read_csv, to_datetime, to_numeric, DataFrame
# from time import time as ti
from tkinter import Tk, filedialog
from os import listdir, sep, getcwd
from os.path import isfile, join, dirname, normpath
from enum import Enum

# %% error handling
class ErrorFile(Exception):
    pass
class ErrorConverting(Exception):
        # try:
        # except ErrorConverting as error:
        #     print(f"\nConverting files interupted : {error}")
    pass



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
        self.df:DataFrame=DataFrame

        if not currDir:
            currDir:str=f"{getcwd()}"
        if not Path_File:
            self.Path_File:str= self.Get_File_path(currDir,FileType)
            self.Path_Folder:str= dirname(self.Path_File)

        if FileType[0] == FILES_LIST.fCSV:
            self.df = self.read_csv_to_df(',',0)
        elif FileType[0] == FILES_LIST.fEXCELX:
            # do stuff
            i=1
        elif FileType[0] == FILES_LIST.fLOG:
            # do stuff
            i=1
        elif FileType[0] == FILES_LIST.fTSV:
            # do stuff
            i=1
        
    def Get_File_path(self,currdir,FileType:list[tuple[str,str]]=[FILES_LIST.fCSV])->str:
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
            parent=root, 
            initialdir=currdir, 
            title='Please select one files',
            filetypes={FileType[0].value})
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
    
        return df


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

    def __init__(self, currDir:str='', Path_Folder:str='', FileType:list[tuple[str,str]]=[FILES_LIST.fCSV.value]):
        super().__init__(currDir,Path_Folder)
        self.FilterdFile = self.dict_file_type_in_folder(self.Path_Folder,FileType)
    
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
            raise ErrorFile(f"No file ({b}() files found in {folder}")
        return filtered