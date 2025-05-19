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

@dataclass
class ConfigTest:
    '''
    Class to store the configuration of the test
    
    Parameters
    ----------
    
    path: str default value = ''
        Absolute path of the file
    FileType : list[tuple[str,str]], default val = [[FILES_LIST.fCSV]]
        Type of file we need to find
    Test_request : str, default val = ''
        the test request number 
    Test_Num : str, default val = ''
        the test index, here a letter
    Appliance_power : str, default val = ''
        the power of the appliance (boiler)
    ParamSet: EcoDesign_Parameter
        class with all the parameter from the test found in the database file
    '''
    Test_request:str=''
    Test_Num:str=''
    Appliance_power:str=''
    Path: str='' #where to search the data
    ParamSet: EcoDesign_Parameter = None
    Files_path:list = None #list[dict['FileName':'','path':'','FileType':'']] = None #{'FileName':'','path':'','FileType':''}
    collection_file:InputFile=None



# %% Ecodesign classes
class EcoDesign():
    '''
    Class specific for ecodesign ploting, incorporating up to 5 differents kind of file to plot in one .html file.
    This class enherit from the class: FilterFileFromFolder -> InputFolder because we a selecting the files first by selecting a folder. 
    '''
    def __init__(self, test_parameters:Union[dict[str,ConfigTest],list[dict[str,ConfigTest]]]=None,initialDir:str=''):
        '''
        Initialize whent he class is called

        Parameter
        -----------------

        initialDir : str, default val = ''
            Set the first path to look into when the file dialogue is called

        Returns
        -----------------
        return in output a HTML file that help us to analyse the data from all the ecodesign tests
        '''
        self.initialDir = initialDir
        if not self.initialDir:
            self.initialDir= getcwd()
        self.test_param_sets  =test_parameters
        self.verifying_input_user()
        try:
            test_param_set:ConfigTest
            for k,test_param_set in self.test_param_sets.items():
                if test_param_set.Path =='':
                    test_param_set.Path = f"HM\\{test_param_set.Appliance_power}kW\\{test_param_set.Test_request}{test_param_set.Test_Num}"
                test_param_set.Files_path = InputFolder(self.initialDir,test_param_set.Path)
                test_param_set.ParamSet = EcoDesign_Parameter(int(test_param_set.Test_request), test_param_set.Test_Num)
                test_param_set.collection_file = self.get_file_to_plot(test_param_set.Files_path)
                if len(self.test_param_sets)>1:
                    test_param_set.collection_file.sync_file_togheter([2.5,3.5],'FLDHW [kg/min]',1)
                elif len(self.test_param_sets)==1:
                    test_param_set.collection_file.sync_file_togheter()
                    self.adding_parameters(test_param_set)
                else:
                    exit("-_-_-_-_-_-_-_-\n\nBye bye")
                

        except errorEcodesign as error :
            print(f"\nError will post processing the file : \n\n{error}")

    def verifying_input_user(self):
        '''
        Getting input from the user :
        - the test request number
        - the test index ( letter here )
        - the power of the appliance in kw

        Returns
        -----------------
            update self.test_param_sets

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
        
        if len(self.test_param_sets)>0:
            for t in self.test_param_sets:
                #Check if we have all the infos
                if not self.test_param_sets[t].Test_request: 
                    self.test_param_sets[t].Test_request = input(align_input_user("Enter the test request number(yyxxx): "))  # Test number according to test request. 23146: HM BO 70kW XXL / 24013: MONOTANK BO 70kW XXL / 24022: HM SO 45kW XXL /
                if not self.test_param_sets[t].Test_Num: 
                    self.test_param_sets[t].Test_Num = input(align_input_user("Enter the test letter: ")).upper()  # The test number. It can be A, B, C, D, etc.
                if not self.test_param_sets[t].Appliance_power: 
                    self.test_param_sets[t].Appliance_power = input(align_input_user("Enter the power type (25, 35, 45, 60, 70, 85, 120, 45X, 25X): "))  # The power of the appliance in kW: 25, 35, 45, 60, 70, 85, 120, 45X, 25X
        else:
            newTest:ConfigTest=None
             #Check if we have all the infos
            newTest.Test_request = input(align_input_user("Enter the test request number(yyxxx): "))  # Test number according to test request. 23146: HM BO 70kW XXL / 24013: MONOTANK BO 70kW XXL / 24022: HM SO 45kW XXL /
            newTest.Test_Num = input(align_input_user("Enter the test letter: ")).upper()  # The test number. It can be A, B, C, D, etc.
            newTest.Appliance_power = input(align_input_user("Enter the power type (25, 35, 45, 60, 70, 85, 120, 45X, 25X): "))  # The power of the appliance in kW: 25, 35, 45, 60, 70, 85, 120, 45X, 25X
            self.test_param_sets = [{f"{newTest.Test_request}{newTest.Test_Num}": newTest}] #creating ONE test configuration 

    def get_file_to_plot(self,Files_path:InputFolder)->InputFile:
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
        for file in Files_path.files_in_folder:
            for xfile in header_list:
                if header_list[xfile].name in file['FileName'].upper() and file['FileType'] in header_list[xfile].FileType.value:
                    header_list[xfile].path = file['Path']
                    files_to_plot[file['FileName']]= header_list[xfile]
                    break
        if len(files_to_plot) == 0:
            print("Probleme detecting the files in the list")
            logging.error("Probleme detecting the files in the list")
            exit("-_-_-_-_-_-_-_-\n\nBye bye")

        print(f"ECO_DESIGN - {len(files_to_plot)} file(s) found")
        logging.info(f"ECO_DESIGN - {len(files_to_plot)} file(s) found")
        return InputFile(files_to_plot)

    # def normalizing_datetime(self):
    #     '''
    #     This function help us to normalize the date and time for each files an start all the file at 21h30m00s as defined in standard 
    #     '''
    #     self.diff_time_to_normalise = self.collection_file.Files['reference'].diff_standard_time_normalize()
    #     if self.diff_time_to_normalise is None :
    #         print("No reference file for normalizing date time found")
    #         logging.error("No reference file for normalizing date time found")
    #     else:
    #         for f in self.collection_file.Files:
    #             self.collection_file.Files[f].normalize_date_time(self.diff_time_to_normalise)


    def adding_parameters(self, test_param_set:ConfigTest):
        '''
        This function is there to creat new trace from the parameter section taht help the used for analysing the data
        '''
        t_DHW_setPoint = test_param_set.ParamSet.test_parameters.at[test_param_set.ParamSet.test_parameters.index[0],'SetpointDHW']
        t_adder = test_param_set.ParamSet.test_parameters.at[test_param_set.ParamSet.test_parameters.index[0],'ParamADDER']
        t_adder_coef = test_param_set.ParamSet.test_parameters.at[test_param_set.ParamSet.test_parameters.index[0],'ParamAdderCoef']
        t_hysteresys = test_param_set.ParamSet.test_parameters.at[test_param_set.ParamSet.test_parameters.index[0],'ParamHysteresis']

        BurnerON = t_DHW_setPoint - t_hysteresys
        BurnerOFF = t_DHW_setPoint - (t_adder * t_adder_coef)
        t_ch_setPoint = t_DHW_setPoint + t_adder
        v:ConfigFile=None

        for v in test_param_set.collection_file.FileData.items():

            if 'MICROPLAN' in v[1].name or 'SEEB' in v[1].name:
                v[1].data['T = 30 [°C]'] = 30 * ones(len(v[1].data['T°in DHW [°C]'])) 
                v[1].data['T = 45 [°C]'] = 45 * ones(len(v[1].data['T°in DHW [°C]'])) 
                v[1].data['T = 55 [°C]'] = 55 * ones(len(v[1].data['T°in DHW [°C]'])) 
                v[1].data['T = 30 [°C]'] = 30 * ones(len(v[1].data['T°in DHW [°C]'])) 
                if 'MICROPLAN' == v[1].name:
                    t_out_name = 'T°out AV.  [°C]'
                if 'SEEB' == v[1].name:
                    t_out_name = 'T°out TC  [°C]'
                v[1].data['Delta T NORM [°C]'] = v[1].data[t_out_name] - v[1].data['T°in DHW [°C]']

            if 'MICROCOM' in v[1].name:
                v[1].data['Delta T boiler [°C]'] = v[1].data['Supply [°C]'] - v[1].data['Return [°C]']
                v[1].data['T BURN ON [°C]'] =  BurnerON * ones(len(v[1].data['Return [°C]'])) 
                v[1].data['T BURN OFF [°C]'] = BurnerOFF * ones(len(v[1].data['Return [°C]'])) 
                v[1].data['T CH STP [°C]'] = t_ch_setPoint * ones(len(v[1].data['Return [°C]'])) 
                v[1].data['T DHW Setpoint [°C]'] = t_DHW_setPoint * ones(len(v[1].data['Return [°C]']))

    def plot_initiate_figure(self, PlotTitle:str=''):
        '''
        This function calls the GeneratePlot class to creat and configure a plot ECO-DESIGN
        '''
        if PlotTitle=='':
            PlotTitle = f"HM{self.pow_appl}kW - {self.test_req_num}{self.test_letter} - {datetime.today().strftime('%Y-%m-%d')}"
        self.plotter = GeneratePlot(plot_name=PlotTitle)
        self.plotter.creat_figure()

    def plot_files_eco_design(self,  test_param_set:ConfigTest):
        '''
        This function calls the GeneratePlot class to creat and configure a plot ECO-DESIGN
        '''
        for v in test_param_set.collection_file.FileData.items():
            if 'MICROPLAN' in v[1].name:
                self.plotter.add_trace_microplan(v[1].data,v[1].header_time)
            elif 'SEEB' in v[1].name:
                self.plotter.add_trace_seeb(v[1].data,v[1].header_time)
            elif 'MICROCOM' in v[1].name:
                self.plotter.add_trace_microcom(v[1].data,v[1].header_time)

        self.plotter.add_filtered_trace(self.plotter.fig)

    def plot_generate_html(self, File_name:str=''):
        if File_name=='':
            File_name = f"{self.Path_Folder}\\{self.test_req_num}{self.test_letter}_XXL_HM{self.pow_appl}TC_PLOT.html"
        self.plotter.creat_html_figure(File_name)

# class CompareTests(EcoDesign):
#     def __init__(self,comparelist:list[dict[str, any]]):
#         flag=False
#         self.FullName = f"Compare{[ f"_{x['Test_request']}{x['Test_Num']}" for x in comparelist]}"
#         self.plot_initiate_figure(self.FullName)
#         collection={}
#         for t in comparelist:
#             if 'Test_Num' in t and 'Test_request' in t and 'Appliance_power' in t:
#                 EcoTest = EcoDesign(
#                                 FileType=t['FileType'],
#                                 #Path_Folder='C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\HM\\70kW\\25066L',
#                                 Test_Num=t['Test_Num'],
#                                 Test_request=t['Test_request'],
#                                 Appliance_power=t['Appliance_power'])
#                 EcoTest.normalizing_datetime()
#                 EcoTest.adding_parameters()
#                 if not flag:
#                     flag=True
#                     self.timeSync, self.indexSync, self.listRisingEdge = EcoTest.collection_file.Files['reference'].list_of_rising_edge('FLDHW [kg/min]',1,[2.5,3.5])
#                 else:
#                     self.sync_time_between_test(EcoTest)
#                 collection[[f"{t['Test_request']}{t['Test_Num']}"]] = EcoTest
                
#     def plot_files_eco_design(self):
#         '''
#         This function calls the GeneratePlot class to creat and configure a plot ECO-DESIGN
#         '''
#         if 'reference' in self.collection_file.Files.keys():
#             if 'MICROPLAN' == self.collection_file.Files['reference'].FileData.name:
#                 self.plotter.add_trace_microplan(self.collection_file.Files['reference'].FileData.data,self.collection_file.Files['reference'].FileData.header_time)
#             if 'SEEB' == self.collection_file.Files['reference'].FileData.name:
#                 self.plotter.add_trace_seeb(self.collection_file.Files['reference'].FileData.data,self.collection_file.Files['reference'].FileData.header_time)
#         if 'MICROCOM' in self.collection_file.Files.keys():
#             self.plotter.add_trace_microcom(self.collection_file.Files['MICROCOM'].FileData.data,self.collection_file.Files['MICROCOM'].FileData.header_time)

#         self.plotter.add_filtered_trace(self.plotter.fig)

#     def sync_time_between_test(self, EcoTest:EcoDesign):
#         for f in EcoTest.collection_file.Files:
#             followingSync, i, listRisingEdge = EcoTest.collection_file.Files['reference'].small_water_flow_rising_edge('FLDHW [kg/min]')
#             EcoTest.collection_file.Files[f].normalize_date_time(self.timeSync-followingSync)

            
# %% run main function 
if __name__ == "__main__":

    single_config = ConfigTest(
        Test_request ='25066',
        Test_Num ='M',
        Appliance_power ='70',
    )


    test={f"{single_config.Test_request}{single_config.Test_Num}": single_config}
#defining test to process :


#sequence :: 
    Traitement = EcoDesign(test)
    Traitement.adding_parameters()

    Traitement.plot_initiate_figure()
    Traitement.plot_files_eco_design()
    Traitement.plot_generate_html()
