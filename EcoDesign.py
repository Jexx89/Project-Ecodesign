'''
Library Ecodesign project

Class: 
* 'EcoDesign' :
    Class specific for ecodesign ploting, incorporating up to 5 differents kind of file to plot in one .html file.

TODO:
--------------
* add a comparaison of each day

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
from datetime import datetime, timedelta


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
    Files_path: #list[dict['FileName':'','path':'','FileType':'']]
        list of the filename, they path and they type
    collection_file: InputFile
        this is a collection of all the file with the data 
    Time_correction : int
        is used to synchronise the data when we compare 2 or more tests, this value will delay the time of the time vector
    '''
    Test_request:str=''
    Test_Num:str=''
    Appliance_power:str=''
    ParamSet: EcoDesign_Parameter = None
    Files_path:InputFolder = None #list[dict['FileName':'','path':'','FileType':'']] = None #{'FileName':'','path':'','FileType':''}
    collection_file:InputFile=None
    Time_correction:int=0



# %% Ecodesign classes
class EcoDesign():
    '''
    Class specific for ecodesign ploting, incorporating up to 2 differents kind of file(Seeb;microcom or microplan;microcom) to plot in a .html file.
    This class allow us also to compare different test to comapre result
    '''
    def __init__(self, test_parameters:dict[str,ConfigTest]=None,initialDir:str=''):
        '''
        Initialize whent he class is called

        Parameter
        -----------------
        test_parameters : dict[str,ConfigTest]=None
            This dictionnary is to initialise the class with a set of parameter ( test request, test num, ...), we can add any number of test to compare.
        initialDir : str, default val = ''
            Set the first path to look into when the file dialogue is called

        Returns
        -----------------
        return in output a HTML file that help us to analyse the data from all the ecodesign tests
        '''

        # initializing the varaible
        self.initialDir = initialDir
        self.test_param_sets = test_parameters
        test_param_set : ConfigTest
        self.now = datetime.now() # this to help us to synchronize the date
        # check variable if none, initialise them
        if not self.initialDir:
            self.initialDir= getcwd()# simply get the actual folder of the script
        if self.test_param_sets == None:
            self.test_param_sets = {'newTest':ConfigTest()} # initialize a configuration test class

        self.test_count = len(self.test_param_sets)
        value_to_filter = self.test_count * 1 # this variable is use to filter data 
        try:
            for k,test_param_set in self.test_param_sets.items():
                self.verifying_input_user(test_param_set) # check and ask the user input on the test (for plot and title name)
                tempory_path =f"HM\\{test_param_set.Appliance_power}kW\\{test_param_set.Test_request}{test_param_set.Test_Num}"

                # get all the files in the folder selected(will search for 'SEEB''MICROPLAN''MICROCOM' in the file name)
                test_param_set.Files_path = InputFolder(self.initialDir,tempory_path)
                #check if the test parameters are present in the database
                test_param_set.ParamSet = EcoDesign_Parameter(int(test_param_set.Test_request), test_param_set.Test_Num)
                # import the data from all the files found in folder and keep them in dataframe
                test_param_set.collection_file = self.get_file_to_plot(test_param_set.Files_path,value_to_filter)
                test_param_set.collection_file.get_df_from_file()
                test_param_set.collection_file.transfrom_data()
                #defining our reference time (here actual date at 7h00m00s, ==> first tapping at 3l/min (see profile XXL Ecodesign))
                ref_time = datetime(year=self.now.year,month=self.now.month,day=self.now.day,hour=7,minute=0, second=0)
                #synchronise test and files togheter
                test_param_set.collection_file.sync_file_togheter(
                    ref_time=ref_time, # our reference time to synchronize
                    from_file=['SEEB','MICROPLAN'], # select what file to used as a reference 
                    criteria=[2.5,3.5], #what is the criteria, here the first edge between 2.5 and 3.5
                    header='FLDHW [kg/min]', # the serie on which apply the filter : 'FLDHW [kg/min]'
                    rising_edge_num=1, # we can find multiple rising edge, so we will use the first one
                    diff_in_second=test_param_set.Time_correction) # this is to add a delay if the rising edge isn't sync well
                # adding parameter to the file if needed
                self.adding_parameters(test_param_set)
        except errorEcodesign as error :
            print(f"\nError will post processing the file : \n\n{error}")
            input("Press Enter to exit...")

    def verifying_input_user(self, test_param_set:ConfigTest):
        '''
        Getting input from the user :
        - the test request number
        - the test index ( letter here )
        - the power of the appliance in kw

        Parameters
        -----------------
        test_param_set:ConfigTest
            Parameter set of a test

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
        print("-"*60)
        #Check if we have all the infos
        if not test_param_set.Test_request: 
            # Test number according to test request. 23146: HM BO 70kW XXL / 24013: MONOTANK BO 70kW XXL / 24022: HM SO 45kW XXL /
            test_param_set.Test_request = input(align_input_user("Enter the test request number(yyxxx): "))  
        if not test_param_set.Test_Num: 
            # The test number. It can be A, B, C, D, etc.
            test_param_set.Test_Num = input(align_input_user("Enter the test letter: ")).upper()  
        if not test_param_set.Appliance_power: 
            # The power of the appliance in kW: 25, 35, 45, 60, 70, 85, 120, 45X, 25X
            test_param_set.Appliance_power = input(align_input_user("Enter the power type (25, 35, 45, 60, 70, 85, 120, 45X, 25X): "))  

    def get_file_to_plot(self,Files_path:InputFolder,value_to_filter=0)->InputFile:
        '''
        Function to filter all the file that we need to plot for ecodesign ploting
        this dictionary is build base on the condition of the naming of the file

        Parameters
        -----------------

        Files_path:InputFolder
            class InputFolder with all the available file in the folder
        value_to_filter=0
            parameter to filter the data. 0 = no filter; 1 = no filter; 2 = one line from 2 filter

        Returns
        -----------------
        Files : InputFile
            a class InputFile with all the file from the test.

        '''
        def file_database(value_to_filter=0):
            '''
            This function return a complete dataset of configfile that we can found in the folder
            We initialize all the file with there parameters

            Parameters
            -----------------

            value_to_filter=0
                parameter to filter the data. 0 = no filter; 1 = no filter; 2 = one line from 2 filter
            Returns
            -----------------
                returns a dictionary with all the known file used for the project Ecodesign
            '''
            MIP = ConfigFile(header_time='Timestamp',name='MICROPLAN',        delimiter=',',row_to_ignore=0, value_to_filter=value_to_filter,FileType=FILES_LIST.fEXCELX, sheet_name = 'McrLine Data',header_cumul_time='TT-sec')
            MIC = ConfigFile(header_time='Time DMY' ,name='MICROCOM',         delimiter=',',row_to_ignore=2, value_to_filter=value_to_filter,FileType=FILES_LIST.fEXCELX, sheet_name = 'McrCom Data')
            SEB = ConfigFile(header_time='Timestamp',name='SEEB',             delimiter=',',row_to_ignore=0, value_to_filter=value_to_filter,FileType=FILES_LIST.fEXCELX, sheet_name = 'Seeb Data',header_cumul_time='Cumul Time(ms)')
            DHW = ConfigFile(header_time='Date-Time',name='DHW_TEMPERATURE',  delimiter=',',row_to_ignore=0, value_to_filter=value_to_filter,FileType=FILES_LIST.fCSV, sheet_name = 0)
            SID = ConfigFile(header_time='Date&Time',name='SIDE_TEMPERATURE', delimiter=',',row_to_ignore=0, value_to_filter=value_to_filter,FileType=FILES_LIST.fCSV, sheet_name = 0)
            PLC = ConfigFile(header_time='DATE-TIME',name='PLC',              delimiter=',',row_to_ignore=0, value_to_filter=value_to_filter,FileType=FILES_LIST.fCSV, sheet_name = 0)
            hl = dict(
                    MICROPLAN = MIP,
                    SEEB = SEB,
                    MICROCOM = MIC,
                    DHW_TEMPERATURE = DHW,
                    SIDE_TEMPERATURE = SID,
                    PLC = PLC,
                    )
            return hl

        files_to_plot={} # initialize
        header_list = file_database(value_to_filter) 
        #This for loop go through all the files in the folder and check if one file match with one present in the file data set
        for file in Files_path.files_in_folder: 
            for xfile in header_list:
                if header_list[xfile].name in file['FileName'].upper() and file['FileType'] in header_list[xfile].FileType.value:
                    header_list[xfile].path = file['Path']
                    files_to_plot[file['FileName']]= header_list[xfile]
                    break
        # no file detect end of the script
        if len(files_to_plot) == 0: 
            print("Probleme detecting the files in the list")
            logging.error("Probleme detecting the files in the list")
            exit("-_-_-_-_-_-_-_-\n\nBye bye")

        print(f"ECO_DESIGN - {len(files_to_plot)} file(s) found")
        logging.info(f"ECO_DESIGN - {len(files_to_plot)} file(s) found")

        #return a dictionary of ConfigFile and creat a InputFile class
        return InputFile(files_to_plot) 

    def adding_parameters(self, test_param_set:ConfigTest):
        '''
        This function is there to creat new trace from the parameter section that help us to analyse the data

        Parameters
        -----------------
        test_param_set:ConfigTest
            Parameter set of a test
        '''
        if test_param_set.ParamSet.status_param()['test']: # this condition to check if we found the parameter set for this test in the database
            #Getting info from database
            t_DHW_setPoint = test_param_set.ParamSet.SetpointDHW
            t_adder = test_param_set.ParamSet.ParamADDER
            t_adder_coef = test_param_set.ParamSet.ParamAdderCoef
            t_hysteresys = test_param_set.ParamSet.ParamHysteresis

            # calculating setpoint
            BurnerON = t_DHW_setPoint - t_hysteresys
            BurnerOFF = t_DHW_setPoint - (t_adder * t_adder_coef)
            t_ch_setPoint = t_DHW_setPoint + t_adder
            v:ConfigFile=None

            #for each file in the InputFile class, add the correct lines
            for v in test_param_set.collection_file.FileData.items():

                if v[1].name in ['SEEB','MICROPLAN']:#check if we using the ecodesign files
                    v[1].data['T = 30 [°C]'] = 30 * ones(len(v[1].data['T°in DHW [°C]'])) #creat a vector the same size as the dataframe
                    v[1].data['T = 45 [°C]'] = 45 * ones(len(v[1].data['T°in DHW [°C]'])) 
                    v[1].data['T = 55 [°C]'] = 55 * ones(len(v[1].data['T°in DHW [°C]'])) 
                    v[1].data['T = 30 [°C]'] = 30 * ones(len(v[1].data['T°in DHW [°C]'])) 

                    t_out_name = 'T°out AV.  [°C]' if 'MICROPLAN' == v[1].name else 'T°out TC  [°C]' #specific name for Tout
                    v[1].data['Delta T NORM [°C]'] = v[1].data[t_out_name] - v[1].data['T°in DHW [°C]']

                if 'MICROCOM' in v[1].name:
                    v[1].data['Delta T boiler [°C]'] = v[1].data['Supply [°C]'] - v[1].data['Return [°C]']
                    v[1].data['T BURN ON [°C]'] =  BurnerON * ones(len(v[1].data['Return [°C]'])) #creat a vector the same size as the dataframe
                    v[1].data['T BURN OFF [°C]'] = BurnerOFF * ones(len(v[1].data['Return [°C]'])) 
                    v[1].data['T CH STP [°C]'] = t_ch_setPoint * ones(len(v[1].data['Return [°C]'])) 
                    v[1].data['T DHW Setpoint [°C]'] = t_DHW_setPoint * ones(len(v[1].data['Return [°C]']))

    def plot_initiate_figure(self, PlotTitle:str=''):
        '''
        This function calls the GeneratePlot class to creat and configure a plot ECO-DESIGN

        Parameters :
        ---------------
        PlotTitle:str
            plot title to use
        '''
        # PlotTitle = f"HM{self.pow_appl}kW - {self.test_req_num}{self.test_letter} - {datetime.today().strftime('%Y-%m-%d')}"
        if PlotTitle=='':
            PlotTitle = self.creatPlotName()
        self.plotter = GeneratePlot(plot_name=PlotTitle)
        self.plotter.creat_figure()

    def plot_generate_html(self, File_name:str=''):
        '''
        This function call the generation of the html figure and set the name of the file

        Parameters
        ----------------
        File_name:str=''
            the file name used to creat the HTML file
        '''
        if File_name=='':
            File_name = f"{self.creatPlotName()}.html"
            if self.test_count==1:
                for k, v in self.test_param_sets.items():
                    p = v.Files_path.Path_Folder + '\\' + File_name
            else:
                p=f"{getcwd()}\\Comparaison\\{File_name}"
                print(p)
        self.plotter.creat_html_figure(p)

    def creatPlotName(self):
        '''
        for all the test in test_param_sets self.test_param_sets we generate a name automatically

        Example :
        -------------
        - "25066H_HM70kW_25066M_HM70kW_25066Q_HM70kW_2025-05-26"
        - "25071D_HM45kW_24086D_HM45kW_2025-05-28"
        - "25071E_HM45kW_2025-06-02"
        '''
        date_created = f"{datetime.today().strftime('%Y-%m-%d')}"
        PlotTitle="".join([f"{v[1].Test_request}{v[1].Test_Num}_HM{v[1].Appliance_power}kW_" for v in self.test_param_sets.items()])
        # example : 25066H_HM70kW_25066M_HM70kW_25066Q_HM70kW_2025-05-26 ; 25071D_HM45kW_24086D_HM45kW_2025-05-28; 25071E_HM45kW_2025-06-02
        return PlotTitle + date_created

    def plot_files_eco_design(self, per_day=False):
        '''
        This function calls all the trtace creator for each indivual files and add them to the figure
        '''
        grouping_text=''
        for k, v in self.test_param_sets.items(): # each test 
            grouping_text ='' if self.test_count==1 else f"{v.Test_request}{v.Test_Num}" # to seperate the trace in group of test
            for kx,vx in v.collection_file.FileData.items(): # each file in test (SEEB, microplan, microcom, ...)
                if not ('Day_' not in kx and per_day) :
                    if 'MICROPLAN' in vx.name:
                        self.plotter.add_trace_microplan(vx.data,vx.header_time,grouping_text)
                    elif 'SEEB' in vx.name:
                        self.plotter.add_trace_seeb(vx.data,vx.header_time,grouping_text)
                    elif 'MICROCOM' in vx.name:
                        self.plotter.add_trace_microcom(vx.data,vx.header_time,grouping_text)
            self.plotter.darken_named_color(0.8) #darken the colors for each new test added to the figure
        self.plotter.add_filtered_trace(self.plotter.fig)

    def separating_days(self):
        '''
        in preparation 
        '''
        for k,test_param_set in self.test_param_sets.items():
            for k, file in test_param_set.collection_file.FileData.items():
                if file.name in ['SEEB','MICROPLAN'] :
                    first_time = file.data[file.header_time].min()
                    file.data['time_test_diff'] = file.data[file.header_cumul_time].diff()
                    file.data['cycle'] = (file.data['time_test_diff'] < 0).cumsum()
                    grouped = file.data.groupby('cycle')
                    dataframes = [group for _, group in grouped]
                    grouped = file.data.groupby('cycle')
                    min_max = [[dt[file.header_time].min(),dt[file.header_time].max(),dt[file.header_time].min()-first_time,dt[file.header_time].max()-dt[file.header_time].min()] for dt in dataframes]
                    break

        print(*min_max,sep='\n')
        delta_time = timedelta(hours=20,minutes=0, seconds=0)
        temp_param_sets={}
        # update test parameters
        i=1
        for k,test_param_set in self.test_param_sets.items():
            for limits in min_max:
                if delta_time < limits[3]:
                    temporary_dict={}
                    for k, f in test_param_set.collection_file.FileData.items():
                        template_df = f.data[f.data[f.header_time].between(limits[0],limits[1])]
                        template_df[f.header_time] = template_df[f.header_time]-limits[2]
                        temporary_dict[f"Day_{i}_{f.name}"] = ConfigFile(
                                                name  = f.name,
                                                header_time = f.header_time,
                                                header_cumul_time = f.header_cumul_time,
                                                data = template_df,
                                                delimiter = f.delimiter,
                                                row_to_ignore = f.row_to_ignore,
                                                FileType = f.FileType,
                                                value_to_filter = f.value_to_filter,
                                                sheet_name = f.sheet_name
                                                )
                    temp_param_sets[f"{test_param_set.Test_request}{test_param_set.Test_Num}_day_{i}"] = ConfigTest(
                        Test_request=test_param_set.Test_request,
                        Test_Num=f"{test_param_set.Test_Num}_day_{i}",
                        Appliance_power=test_param_set.Appliance_power,
                        ParamSet=test_param_set.ParamSet,
                        Files_path=test_param_set.Files_path,
                        collection_file=InputFile(temporary_dict),
                        Time_correction=test_param_set.Time_correction
                        )
                    i+=1
            print(*test_param_set.collection_file.FileData.keys(),sep='\n')

        self.test_param_sets.clear()
        self.test_param_sets = temp_param_sets.copy()
        self.test_count = len(self.test_param_sets)

        ref_time = datetime(year=self.now.year,month=self.now.month,day=self.now.day,hour=7,minute=0, second=0)
        for k,test_param_set in self.test_param_sets.items():
                #synchronise test and files togheter
                test_param_set.collection_file.sync_file_togheter(
                    ref_time=ref_time, # our reference time to synchronize
                    from_file=['SEEB','MICROPLAN'], # select what file to used as a reference 
                    criteria=[2.5,3.5], #what is the criteria, here the first edge between 2.5 and 3.5
                    header='FLDHW [kg/min]', # the serie on which apply the filter : 'FLDHW [kg/min]'
                    rising_edge_num=1, # we can find multiple rising edge, so we will use the first one
                    diff_in_second=test_param_set.Time_correction) # this is to add a delay if the rising edge isn't sync well

        print(f'Number of days : {i}')




# %% run main function
if __name__ == "__main__":
    # to test the function
    Solo_config = ConfigTest(
        Test_request ='25072',
        Test_Num ='C',
        Appliance_power ='120',
    )
    test={f"{Solo_config.Test_request}{Solo_config.Test_Num}": Solo_config}
    Traitement = EcoDesign(test)
    Traitement.plot_initiate_figure()
    Traitement.plot_files_eco_design()
    Traitement.plot_generate_html()