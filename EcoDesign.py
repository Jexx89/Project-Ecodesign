from cl_FileAndInput import *
from cl_EcoParam import *
import sys
from datetime import datetime

# %% Ecodesign classes
class EcoDesign(FilterFileFromFolder):
    '''
    Class specific for ecodesign ploting, incorporating up to 5 differents kind of file to plot in one .html file.
    This class enherit from the class: FilterFileFromFolder -> InputFolder because we a selecting the files first by selecting a folder. 
    '''
    def __init__(self, currDir:str='', Path_Folder:str='', FileType:list[tuple[str,str]]=[FILES_LIST.fCSV.value],Test_request:str='',Test_Num:str='',Appliance_power:str=''):
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
        # if Path_Folder == '' and Test_request!='':
        #         Path_Folder = f"HM\\{Appliance_power}kW\\{Test_request}{Test_Num}\\"

        super().__init__(currDir, Path_Folder, FileType)
        self.test_req_num:str=Test_request
        self.test_letter:str=Test_Num
        self.pow_appl:str=Appliance_power

        #start the script
        if self.test_req_num=='':
            self.getting_input_user()
        if self.test_req_num not in self.Path_Folder: 
            answer=input("Test request num isn't in the file name are you sure you want to continue? [y/n]")
            negativeAnswer = ("NO", "NON", "N", "", "0")
            if answer in negativeAnswer:
                sys.exit("The folder is different from test request num")
            
        try:
            self.paramSet = cl_EcoDesign_Parameter(int(self.test_req_num), self.test_letter)
            self.collection_file = self.detect_file_to_plot(self.CompletePath)
            self.normalizing_datetime()
        #     self.add_parameter()
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
    def detect_file_to_plot(self,listFiles=[str]):
        '''
        Function to filter all the file that we need to plot for ecodesign ploting
        this dictionary is build base on the condition of the naming of the file

        Parameters
        -----------------

        listFiles : list[str]
            list of the avaible file in the folder

        Returns
        -----------------
        fileFoundToPlot : dictionary
            a dictionary with the name as a key and the full path as a value of all the files we found to plot

        '''
        MIP = dict(header_time='Timestamp',name='MICROPLAN',        delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=list('CSV File','*.csv'))
        MIC = dict(header_time='Time DMY',name='MICROCOM',          delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=list('CSV File','*.csv'))
        SEB = dict(header_time='Timestamp',name='SEEB',             delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=list('CSV File','*.csv'))
        DHW = dict(header_time='Date-Time',name='DHW_TEMPERATURE',  delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=list('CSV File','*.csv'))
        SID = dict(header_time='Date&Time',name='SIDE_TEMPERATURE', delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=list('CSV File','*.csv'))
        PLC = dict(header_time='DATE-TIME',name='PLC',              delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=list('CSV File','*.csv'))
        header_list = dict(
                MICROPLAN = MIP,
                SEEB = SEB,
                MICROCOM = MIC,
                DHW_TEMPERATURE = DHW,
                SIDE_TEMPERATURE = SID,
                PLC = PLC,
                )
        File=[ConfigFile]
        for f in listFiles:
            for xf in header_list:
                if header_list[xf]['name'] in f['name'].upper():
                    File.append(ConfigFile(
                        name=xf,
                        path=[f['full_path']],
                        header_time=header_list[xf]['header_time'],
                        delimiter=header_list[xf]['delimiter'],
                        row_to_ignore=header_list[xf]['row_to_ignore'],
                        FileType=header_list[xf]['FileType'],
                        value_to_filter=header_list[xf]['value_to_filter']))
                    break
        if len(File) == 0:
            logging.error("Probleme detecting the files in the list")
            sys.exit("Probleme detecting the files in the list")
        return File_Ecodesign (File)

    def normalizing_datetime(self):
        if 'MICROPLAN' in self.list_of_file_info:
            ref_file:InputFile = self.list_of_file_info['MICROPLAN']
        elif 'SEEB' in self.list_of_file_info:
            ref_file:InputFile = self.list_of_file_info['SEEB']
        else:
            logging.error("No reference file for normalizing date time found")
            sys.exit("No reference file for normalizing date time found")

        st_start= ref_file.file_info[0]['data'][ref_file.file_info[0]['header_time']][0]
        st_year = st_start.year
        st_month = st_start.month
        st_day = st_start.day
        ref_time = datetime(year=st_year, month=st_month, day=st_day, hour=21, minute=30, second=00)  # make a reference time for the tests
        diff_time_to_normalise = ref_time - st_start

        for f in self.list_of_file_info:
             self.list_of_file_info[f].file_info[0]['data'][self.list_of_file_info[f].file_info[0]['header_time']]=self.list_of_file_info[f].file_info[0]['data'][self.list_of_file_info[f].file_info[0]['header_time']]+diff_time_to_normalise
        i=0
    # this function allow us to import the data from the csv files put then in dataframe
    def ploting_files(self,file_info):
        i=0

# %% run main function 
if __name__ == "__main__":
    Traitement = EcoDesign(Test_request='25066',Test_Num='A',Appliance_power='70', Path_Folder="C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\HM\\70kW\\25066A")