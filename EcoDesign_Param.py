'''
Library 
--------------

Class: 
* 'EcoDesign_Parameter' :
    class to handle the parameter section of the ecodesign function
    filter the row with the input critéria
    allow to open multiple type of files, but only Excel file is used in this class
    

TODO:
--------------
* add error handler

Created by JSB(based on Marcello😍🍕 script)
--------------

V1.0 : initial rev
    * Open and import the data from 'DataTable_TestParam.xlsx'
    * filter the row with the input critéria
    * allow to open multiple type of files, but only Excel file is used in this class
'''

# %% import lib
import logging
from pandas import read_excel, DataFrame
from os import getcwd, sep
from time import time


# %% class EcoDesign_Parameter
class EcoDesign_Parameter():
    '''Class to open and gather database of parameter from all the test done in Ecodesign project'''
    def __init__(self, Test_request:int=1,Test_Num:str='A'):
        '''
        Initialize the class by importing the parameter
        
        Parameters
        -----------
        Test_request:int
            Test request number
        Test_Num:str
            Test number (here alphabetic)
        Output
        -------
        Get one line of dataframe with all the parameter
        '''
        logging.basicConfig(filename='log\\trace.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.ALL_DF:DataFrame = []
        self.stime = time()
        self.Test_request = Test_request
        self.Test_Num=Test_Num
        self.test_parameters = self.import_test_param(self.Test_request,self.Test_Num)


        self.BoilerPower = self.test_parameters.at[self.test_parameters.index[0],'BoilerPower']
        self.BoilerStructure = self.test_parameters.at[self.test_parameters.index[0],'BoilerStructure']
        self.SetpointDHW = self.test_parameters.at[self.test_parameters.index[0],'SetpointDHW']
        self.ParamADDER = self.test_parameters.at[self.test_parameters.index[0],'ParamADDER']
        self.ParamHysteresis = self.test_parameters.at[self.test_parameters.index[0],'ParamHysteresis']
        self.ParamAdderCoef = self.test_parameters.at[self.test_parameters.index[0],'ParamAdderCoef']
        self.RangeModulation  = self.test_parameters.at[self.test_parameters.index[0],'RangeModulation ']
        self.SetPointDeltaPump = self.test_parameters.at[self.test_parameters.index[0],'SetPointDeltaPump']

    def status_param(self):
        '''Function to return the stat of the parameter
        
        Output
        -------
        T : test_parameters returns 1 set of parameter
        F : test_parameters returns none or to mush parameter
        '''
        if len(self.test_parameters)>1:
            return {'test':False,'len':len(self.test_parameters)}
        if len(self.test_parameters)==1:
            return {'test':True,'len':len(self.test_parameters)}
        else : 
            return {'test':False,'len':len(self.test_parameters)}

    def import_test_param(self,Test_request:int,Test_Num:str)->DataFrame:
        '''
        This function import the data from the xl file 

        Parameter
        ---------
        Test_request:int
            Test request number
        Test_Num:str
            Test number (here alphabetic)

        Output
        --------
        return a dataframe with all the parameters of the test
        '''
        def read_xlsx_to_dict(file_path:str, sheet_name:0):
            '''
            This function read an excel file and convert the data correctly to use it later. 
        
            Parameters
            -----------
            file_path:str
                the path of the file we a trying to open
            sheet_name:int
                The excel sheet name or number

            Output
            -------
            The ouput is dataframe with the dataframe of all the data in the worksheet
            '''
            data = DataFrame
            try:
                df = read_excel(file_path, sheet_name=sheet_name)
                df['ID'] = df['ID'].astype(int)
                df['SetpointDHW'] = df['SetpointDHW'].astype(int)
                df['ParamADDER'] = df['ParamADDER'].astype(int)
                df['ParamHysteresis'] = df['ParamHysteresis'].astype(int)
                df['ParamAdderCoef'] = df['ParamAdderCoef'].astype(float)
                df['P_factor'] = df['P_factor'].astype(int)
                df['I_Factor'] = df['I_Factor'].astype(int)
                df['SetPointDeltaPump'] = df['SetPointDeltaPump'].astype(int)
                df['PrePumpPercent'] = df['PrePumpPercent'].astype(int)
                df['PrePumpTime'] = df['PrePumpTime'].astype(int)
                df['PrePumpBurningPercent'] = df['PrePumpBurningPercent'].astype(int)
                df['PostPumpPercent'] = df['PostPumpPercent'].astype(int)
                df['PostPumpTime'] = df['PostPumpTime'].astype(int)
                df['InertiaMBTPercent'] = df['InertiaMBTPercent'].astype(int)
                # data = df.to_dict(orient='records')
                data = df
            except FileNotFoundError:
                print(f"Le fichier {file_path} n'a pas été trouvé.")
            except Exception as e:
                print(f"Une erreur s'est produite : {e}")
            return data

        #file path of our parameter table  
        file_path_xlsx = f"{getcwd()}{sep}DataTable_TestParam.xlsx"
        #filtering to get only the good test parameter
        sheet_name = 0
        self.ALL_DF = read_xlsx_to_dict(file_path_xlsx, sheet_name)
        print(f"ECO_PARAM - Reading data from DB : {time() - self.stime:.2f} sec")
        logging.info(f"ECO_PARAM - Reading data from DB : {time() - self.stime:.2f} sec")

        self.stime = time()
        # filter the data with Test_request and Test_Num as criteria
        tp = self.ALL_DF[self.ALL_DF['TestRequest'].apply(lambda x:x==Test_request) & self.ALL_DF['TestNum'].apply(lambda x:x==Test_Num)]
        print(f"ECO_PARAM - Filtering data : {time() - self.stime:.2f} sec")
        logging.info(f"ECO_PARAM - Filtering data : {time() - self.stime:.2f} sec")

        if len(tp) < 1:
            print(f"ECO_PARAM - No parameters found for this test :  '{Test_request}{Test_Num}'")
            logging.error(f"ECO_PARAM - No parameters found for this test :  '{Test_request}{Test_Num}'")
        elif len(tp) > 1:
            print(f"ECO_PARAM - To much parameters found for this test :  '{Test_request}{Test_Num}'")
            logging.error(f"ECO_PARAM - To much parameters found for this test :  '{Test_request}{Test_Num}'")
            for i in tp: print(f"{i} = {tp[i].values}")
            idTest = input("A few parameter set was found please enter the correct 'ID' :")
            tp=tp[tp['ID'].apply(lambda x:x==idTest) ]
        return tp

#%% Example of use
if __name__ == "__main__":
    dataFile = EcoDesign_Parameter(25066,"H").test_parameters
    print("\nDonnées du fichier Excel:")
    for i in dataFile: print(f"{i} = {dataFile[i].values}")
