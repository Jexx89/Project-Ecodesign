from cl_FileAndInput import *
from cl_PlotingData import *
from cl_EcoParam import *
from numpy import ones 
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
        self.getting_input_user(Test_request,Test_Num,Appliance_power)
        if Path_Folder !='':
            Path_Folder = f"HM\\{self.pow_appl}kW\\{self.test_req_num}{self.test_letter}\\"
        super().__init__(currDir, Path_Folder, FileType)

        # if self.paramSet.status_param()['test']:
        # #start the script
        # if self.test_req_num not in self.Path_Folder : 
        #     answer=input("Test request num isn't in the file name are you sure you want to continue? [y/n]")
        #     negativeAnswer = ("NO", "NON", "N", "", "0")
        #     if answer in negativeAnswer:
        #         sys.exit("The folder is different from test request num")
            
        try:
            self.paramSet = cl_EcoDesign_Parameter(int( self.test_req_num), self.test_letter)
            self.collection_file = self.detect_file_to_plot(self.CompletePath)
            self.normalizing_datetime()
            self.adding_parameters()
            self.ploting_files()
        except ErrorFile as error:
            print(f"\nOpening files interupted : {error}")



    # getting input from user
    def getting_input_user(self,Test_request:str='',Test_Num:str='',Appliance_power:str=''):
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
        if not Test_request: 
            self.test_req_num = input(align_input_user("Enter the test request number(yyxxx): "))  # Test number according to test request. 23146: HM BO 70kW XXL / 24013: MONOTANK BO 70kW XXL / 24022: HM SO 45kW XXL /
        else:
            self.test_req_num = Test_request
        if not Test_Num:
            self.test_letter = input(align_input_user("Enter the test letter: ")).upper()  # The test number. It can be A, B, C, D, etc.
        else:
            self.test_letter = Test_Num
        if not Appliance_power:
            self.pow_appl = input(align_input_user("Enter the power type (25, 35, 45, 60, 70, 85, 120, 45X, 25X): "))  # The power of the appliance in kW: 25, 35, 45, 60, 70, 85, 120, 45X, 25X
        else:
            self.pow_appl = Appliance_power

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
        def file_database():
            MIP = ConfigFile(header_time='Timestamp',name='MICROPLAN',        delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fCSV)
            MIC = ConfigFile(header_time='Time DMY' ,name='MICROCOM',         delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fCSV)
            SEB = ConfigFile(header_time='Timestamp',name='SEEB',             delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fCSV)
            DHW = ConfigFile(header_time='Date-Time',name='DHW_TEMPERATURE',  delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fCSV)
            SID = ConfigFile(header_time='Date&Time',name='SIDE_TEMPERATURE', delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fCSV)
            PLC = ConfigFile(header_time='DATE-TIME',name='PLC',              delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fCSV)
            hl = dict(
                    MICROPLAN = MIP,
                    SEEB = SEB,
                    MICROCOM = MIC,
                    DHW_TEMPERATURE = DHW,
                    SIDE_TEMPERATURE = SID,
                    PLC = PLC,
                    )
            return hl

        files_to_plot=[]
        header_list = file_database()
        for f in listFiles:
            for xf in header_list:
                if header_list[xf].name in f['name'].upper():
                    header_list[xf].path = f['full_path']
                    files_to_plot.append(header_list[xf])
                    break
        
        if len(files_to_plot) == 0:
            logging.error("Probleme detecting the files in the list")
            sys.exit("Probleme detecting the files in the list")
        return Collection_inputFile(files_config=files_to_plot)

    def normalizing_datetime(self):
        ref_file = InputFile|None
        for x in self.collection_file.Files:
            if x.FileData.name == 'MICROPLAN':
                ref_file = x
            if x.FileData.name == 'SEEB':
                ref_file = x
        if ref_file is None :
            logging.error("No reference file for normalizing date time found")
            sys.exit("No reference file for normalizing date time found")

        st_start= ref_file.FileData.data[ref_file.FileData.header_time][0]
        st_year = st_start.year
        st_month = st_start.month
        st_day = st_start.day
        ref_time = datetime(year=st_year, month=st_month, day=st_day, hour=21, minute=30, second=00)  # make a reference time for the tests
        diff_time_to_normalise = ref_time - st_start

        for f in self.collection_file.Files:
             f.normalize_date_time(diff_time_to_normalise)

    def adding_parameters(self):
        t_DHW_setPoint = self.paramSet.test_parameters.at[self.paramSet.test_parameters.index[0],'SetpointDHW']
        t_adder = self.paramSet.test_parameters.at[self.paramSet.test_parameters.index[0],'ParamADDER']
        t_adder_coef = self.paramSet.test_parameters.at[self.paramSet.test_parameters.index[0],'ParamAdderCoef']
        t_hysteresys = self.paramSet.test_parameters.at[self.paramSet.test_parameters.index[0],'ParamHysteresis']

        BurnerON = t_DHW_setPoint - t_hysteresys
        BurnerOFF = t_DHW_setPoint - (t_adder * t_adder_coef)
        t_ch_setPoint = t_DHW_setPoint + t_adder
        

        for x in self.collection_file.Files:
            if x.FileData.name == 'MICROPLAN':
                x.FileData.data['Delta T NORM [°C]'] = x.FileData.data['T°out AV.  [°C]'] - x.FileData.data['T°in DHW [°C]']
                x.FileData.data['T = 30 [°C]'] = 30 * ones(len(x.FileData.data['T°in DHW [°C]'])) 
                x.FileData.data['T = 45 [°C]'] = 45 * ones(len(x.FileData.data['T°in DHW [°C]'])) 
                x.FileData.data['T = 55 [°C]'] = 55 * ones(len(x.FileData.data['T°in DHW [°C]'])) 
            if x.FileData.name == 'SEEB':
                x.FileData.data['Delta T NORM [°C]'] = x.FileData.data['T°out TC  [°C]'] - x.FileData.data['T°in DHW [°C]']
                x.FileData.data['T = 30 [°C]'] = 30 * ones(len(x.FileData.data['T°in DHW [°C]'])) 
                x.FileData.data['T = 45 [°C]'] = 45 * ones(len(x.FileData.data['T°in DHW [°C]'])) 
                x.FileData.data['T = 55 [°C]'] = 55 * ones(len(x.FileData.data['T°in DHW [°C]'])) 
            if x.FileData.name == 'MICROCOM':
                x.FileData.data['Delta T boiler [°C]'] = x.FileData.data['Supply [°C]'] - x.FileData.data['Return [°C]']
                x.FileData.data['T BURN ON [°C]'] =  BurnerON * ones(len(x.FileData.data['Return [°C]'])) 
                x.FileData.data['T BURN OFF [°C]'] = BurnerOFF * ones(len(x.FileData.data['Return [°C]'])) 
                x.FileData.data['T CH STP [°C]'] = t_ch_setPoint * ones(len(x.FileData.data['Return [°C]'])) 
                x.FileData.data['T DHW Setpoint [°C]'] = t_DHW_setPoint * ones(len(x.FileData.data['Return [°C]']))

    # this function allow us to import the data from the csv files put then in dataframe
    def ploting_files(self):
        plotter = GeneratePlot(plot_name=f"HM{self.pow_appl}kW - {self.test_req_num}{self.test_letter} - {datetime.today().strftime('%Y-%m-%d')}")
        plotter.creat_fig()

        for f in self.collection_file.Files:
            if f.FileData.name == 'MICROPLAN':
                plotter.add_trace_microplan(f.FileData.data,f.FileData.header_time)
            if f.FileData.name == 'MICROCOM':
                plotter.add_trace_microcom(f.FileData.data,f.FileData.header_time)
            if f.FileData.name == 'SEEB':
                plotter.add_trace_seeb(f.FileData.data,f.FileData.header_time)
        plotter.add_filtered_trace()
        plotter.creat_html_file()

# %% run main function 
if __name__ == "__main__":
    Traitement = EcoDesign(Test_request='25066',Test_Num='F',Appliance_power='70', Path_Folder="C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\HM\\70kW\\25066F")