'''
Library Ecodesign project

Class: 
* 'EcoDesign' :
    Class specific for ecodesign ploting, incorporating up to 5 differents kind of file to plot in one .html file.

TODO:
--------------
* add a comparaison file 
* add a comparaison of each day
* generate file into HTML offline

Created by JSB(based on Marcello😍🍕 script)
--------------
V1.1 : 
    * add the possibility to read excel file's
V1.0 : initial rev
    * open files based on test req num and alphabetic test
    * open files with the folder
    * ask info to user if we don't have all the info

'''
#%% import library
from FileManager import *
from PlotingData import *
from EcoDesign_Param import *

from numpy import ones # to creat single vector
from sys import exit
from datetime import datetime


class errorEcodesign(Exception):
    pass
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
        return in output a HTML file that help us to analyse the data from all the ecodesign tests

        '''
        negativeAnswer = ("NO", "NON", "N", "", "0")
        self.getting_input_user(Test_request,Test_Num,Appliance_power)
        if Path_Folder !='':
            Path_Folder = f"HM\\{self.pow_appl}kW\\{self.test_req_num}{self.test_letter}\\"
        super().__init__(currDir, Path_Folder, FileType)

        if self.test_req_num not in self.Path_Folder : 
            answer = input("Test request num isn't in the file name are you sure you want to continue? [y/n]")
            if answer.upper() in negativeAnswer:
                exit("The folder is different from test request num")
            
        try:
            self.paramSet = EcoDesign_Parameter(int( self.test_req_num), self.test_letter)
            self.collection_file = self.get_file_to_plot(self.CompletePath)
            self.normalizing_datetime()
            self.adding_parameters()
            self.ploting_files_eco_design()
        except errorEcodesign as error :
            print(f"\nError will post processing the file : \n\n{error}")

    def getting_input_user(self,Test_request:str='',Test_Num:str='',Appliance_power:str=''):
        '''
        Getting input from the user :
        - the test request number
        - the test index ( letter here )
        - the power of the appliance in kw

        Parameters
        -----------------
        Test_request : str, default val = ''
            the test request number 
        Test_Num : str, default val = ''
            the test index, here a letter
        Appliance_power : str, default val = ''
            the power of the appliance (boiler)
        
        Returns
        -----------------
            void

        '''
        def align_input_user(s: str) -> str:
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

    def get_file_to_plot(self,listFiles=[str]):
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
            '''
            This function return a complete set of configfile that we can found in the folder
            We initialize all the file with there parameters
            '''
            MIP = ConfigFile(header_time='Timestamp',name='MICROPLAN',        delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fEXCELX, sheet_name = 'McrLine Data')
            MIC = ConfigFile(header_time='Time DMY' ,name='MICROCOM',         delimiter=',',row_to_ignore=2, value_to_filter=0,FileType=FILES_LIST.fEXCELX, sheet_name = 'McrCom Data')
            SEB = ConfigFile(header_time='Timestamp',name='SEEB',             delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fEXCELX, sheet_name = 'Seeb Data')
            DHW = ConfigFile(header_time='Date-Time',name='DHW_TEMPERATURE',  delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fCSV, sheet_name = 0)
            SID = ConfigFile(header_time='Date&Time',name='SIDE_TEMPERATURE', delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fCSV, sheet_name = 0)
            PLC = ConfigFile(header_time='DATE-TIME',name='PLC',              delimiter=',',row_to_ignore=0, value_to_filter=0,FileType=FILES_LIST.fCSV, sheet_name = 0)
            hl = dict(
                    MICROPLAN = MIP,
                    SEEB = SEB,
                    MICROCOM = MIC,
                    DHW_TEMPERATURE = DHW,
                    SIDE_TEMPERATURE = SID,
                    PLC = PLC,
                    )
            return hl

        files_to_plot={}
        header_list = file_database()
        for f in listFiles:
            for xf in header_list:
                if header_list[xf].name in f['name'].upper():
                    header_list[xf].path = f['full_path']
                    if header_list[xf].name == 'MICROPLAN' or header_list[xf].name == 'SEEB':
                        files_to_plot['reference']= header_list[xf]
                    else:
                        files_to_plot[header_list[xf].name]= header_list[xf]
                    break
        if len(files_to_plot) == 0:
            print("Probleme detecting the files in the list")
            logging.error("Probleme detecting the files in the list")
            exit("-_-_-_-_-_-_-_-\n\nBye bye")

        print(f"ECO_DESIGN - {len(files_to_plot)} file(s) found")
        logging.info(f"ECO_DESIGN - {len(files_to_plot)} file(s) found")
        return Collection_inputFile(files_config=files_to_plot)

    def normalizing_datetime(self):
        '''
        This function help us to normalize the date and time for each files an start all the file at 21h30m00s as defined in standard 
        '''
        diff_time_to_normalise = self.collection_file.Files['reference'].diff_standard_time_normalize()
        if diff_time_to_normalise is None :
            print("No reference file for normalizing date time found")
            logging.error("No reference file for normalizing date time found")
        else:
            for f in self.collection_file.Files:
                self.collection_file.Files[f].normalize_date_time(diff_time_to_normalise)

    def adding_parameters(self):
        '''
        This function is there to creat new trace from the parameter section taht help the used for analysing the data
        '''
        t_DHW_setPoint = self.paramSet.test_parameters.at[self.paramSet.test_parameters.index[0],'SetpointDHW']
        t_adder = self.paramSet.test_parameters.at[self.paramSet.test_parameters.index[0],'ParamADDER']
        t_adder_coef = self.paramSet.test_parameters.at[self.paramSet.test_parameters.index[0],'ParamAdderCoef']
        t_hysteresys = self.paramSet.test_parameters.at[self.paramSet.test_parameters.index[0],'ParamHysteresis']

        BurnerON = t_DHW_setPoint - t_hysteresys
        BurnerOFF = t_DHW_setPoint - (t_adder * t_adder_coef)
        t_ch_setPoint = t_DHW_setPoint + t_adder
        
        if 'reference' in self.collection_file.Files.keys():
            self.collection_file.Files['reference'].FileData.data['T = 30 [°C]'] = 30 * ones(len(self.collection_file.Files['reference'].FileData.data['T°in DHW [°C]'])) 
            self.collection_file.Files['reference'].FileData.data['T = 45 [°C]'] = 45 * ones(len(self.collection_file.Files['reference'].FileData.data['T°in DHW [°C]'])) 
            self.collection_file.Files['reference'].FileData.data['T = 55 [°C]'] = 55 * ones(len(self.collection_file.Files['reference'].FileData.data['T°in DHW [°C]'])) 
            self.collection_file.Files['reference'].FileData.data['T = 30 [°C]'] = 30 * ones(len(self.collection_file.Files['reference'].FileData.data['T°in DHW [°C]'])) 
            if 'MICROPLAN' == self.collection_file.Files['reference'].FileData.name:
                t_out_name = 'T°out AV.  [°C]'
            if 'SEEB' == self.collection_file.Files['reference'].FileData.name:
                t_out_name = 'T°out TC  [°C]'
            self.collection_file.Files['reference'].FileData.data['Delta T NORM [°C]'] = self.collection_file.Files['reference'].FileData.data[t_out_name] - self.collection_file.Files['reference'].FileData.data['T°in DHW [°C]']
        if 'MICROCOM' in self.collection_file.Files.keys():
            self.collection_file.Files['MICROCOM'].FileData.data['Delta T boiler [°C]'] = self.collection_file.Files['MICROCOM'].FileData.data['Supply [°C]'] - self.collection_file.Files['MICROCOM'].FileData.data['Return [°C]']
            self.collection_file.Files['MICROCOM'].FileData.data['T BURN ON [°C]'] =  BurnerON * ones(len(self.collection_file.Files['MICROCOM'].FileData.data['Return [°C]'])) 
            self.collection_file.Files['MICROCOM'].FileData.data['T BURN OFF [°C]'] = BurnerOFF * ones(len(self.collection_file.Files['MICROCOM'].FileData.data['Return [°C]'])) 
            self.collection_file.Files['MICROCOM'].FileData.data['T CH STP [°C]'] = t_ch_setPoint * ones(len(self.collection_file.Files['MICROCOM'].FileData.data['Return [°C]'])) 
            self.collection_file.Files['MICROCOM'].FileData.data['T DHW Setpoint [°C]'] = t_DHW_setPoint * ones(len(self.collection_file.Files['MICROCOM'].FileData.data['Return [°C]']))

    # this function allow us to import the data from the csv files put then in dataframe
    def ploting_files_eco_design(self):
        '''
        This function calls the GeneratePlot class to creat and configure a plot ECO-DESIGN
        '''
        plotter = GeneratePlot(plot_name=f"HM{self.pow_appl}kW - {self.test_req_num}{self.test_letter} - {datetime.today().strftime('%Y-%m-%d')}")
        plotter.creat_figure()
        if 'reference' in self.collection_file.Files.keys():
            if 'MICROPLAN' == self.collection_file.Files['reference'].FileData.name:
                plotter.add_trace_microplan(self.collection_file.Files['reference'].FileData.data,self.collection_file.Files['reference'].FileData.header_time)
            if 'SEEB' == self.collection_file.Files['reference'].FileData.name:
                plotter.add_trace_seeb(self.collection_file.Files['reference'].FileData.data,self.collection_file.Files['reference'].FileData.header_time)
        if 'MICROCOM' in self.collection_file.Files.keys():
            plotter.add_trace_microcom(self.collection_file.Files['MICROCOM'].FileData.data,self.collection_file.Files['MICROCOM'].FileData.header_time)

        plotter.add_filtered_trace()
        # plotter.show_html_figure()
        plotter.creat_html_figure(f"{self.Path_Folder}\\{self.test_req_num}{self.test_letter}_XXL_HM{self.pow_appl}TC_PLOT.html")

# %% run main function 
if __name__ == "__main__":
    
    Traitement = EcoDesign(
        FileType=[FILES_LIST.fEXCELX.value],
        Path_Folder='C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\HM\\70kW\\25066L',
        Test_Num='M',
        Test_request='25066',
        Appliance_power='70')
    # Traitement = EcoDesign(
    #     FileType=[FILES_LIST.fEXCELX.value],
    #     Path_Folder='C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\HM\\35kW\\25063L',
    #     Test_Num='L',
    #     Test_request='25063',
    #     Appliance_power='35')