from cl_FileAndInput import *
from cl_EcoParam import *


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
        if Path_Folder == '' and Test_request!='':
                Path_Folder = f"HM\\{Appliance_power}kW\\{Test_request}{Test_Num}\\"

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
            self.add_parameter()
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
        header_list = dict(
                MICROPLAN = 'Timestamp',
                MICROCOM = 'Time DMY',
                DHW_TEMPERATURE = 'Date-Time',
                SIDE_TEMPERATURE = 'Date&Time',
                PLC = 'DATE-TIME',
                SEEB = 'Timestamp')

        fileFoundToPlot=[]
        for f in listFiles:
            for xf in header_list:
                if xf in f.upper():
                    fileFoundToPlot.append({
                        "type": xf, 
                        "path":join(Path_Folder,f), 
                        "header_time":header_list[xf]})
                    break
        if len(fileFoundToPlot) == 0:
            raise ErrorFile(f"No file '.csv' files found in '{Path_Folder}'")
        return fileFoundToPlot

    # this function allow us to import the data from the csv files put then in dataframe
    def import_all_ploting_data(self,dictFileToPlot)->dict:
        '''
        Function to go trough all the files in the dictionary and launch :
            - reading

        Parameter
        -----------------

        dictFileToPlot : dictionary
            Dictionary with the file path of all the files to plot
        
        Returns
        -----------------
            void
        '''
        self.files=[]
        if "MICROPLAN" in dictFileToPlot:
            fl = InputFile(Path_File=dictFileToPlot["MICROPLAN"].get(),header_time=FILE_NAME.MICROPLAN.value,FileType=FILES_LIST.fCSV)

        elif "SEEB" in dictFileToPlot:
            fl = InputFile(Path_File=dictFileToPlot[FILE_NAME.SEEB],header_time=FILE_NAME.SEEB.value,FileType=FILES_LIST.fCSV)
        else:
            raise ErrorFile(f"No main file found in '{self.Path_Folder}'")
        st_start= fl.df[FILE_NAME.MICROPLAN.value][0]
        st_year = st_start.dt.year
        st_month = st_start.dt.month
        st_day = st_start.dt.day
        ref_time = to_datetime(year=st_year, month=st_month, day=st_day, hour=21, minute=30, second=00)  # make a reference time for the tests
        diff_time_to_normalise = ref_time - st_start
        fl.df[FILE_NAME.MICROPLAN.value]  = fl.df[FILE_NAME.MICROPLAN.value] - diff_time_to_normalise
        self.files.append(fl)




        self.files.append([InputFile(Path_File=dictFileToPlot[d],header_time=d.value,FileType=FILES_LIST.fCSV) for d in dictFileToPlot if d != FILE_NAME.SEEB & d != FILE_NAME.MICROPLAN])

    def add_parameter(self):
        w=1

# %% run main function 
if __name__ == "__main__":
    Traitement = EcoDesign(Test_request="25066",Test_Num="A",Appliance_power="70")