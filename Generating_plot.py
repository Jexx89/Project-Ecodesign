import pandas 
from time import time as ti
from os import listdir, sep
from os.path import isfile, join , abspath, dirname
from CLASS_ImportData import read_file_to_dict
from sys import exit
#negativeAnswer = ("NO", "NON", "N", "", "0")

class FindingFile(Exception):
    pass

# %% THIS SECTION SET THE INPUT PARAMETERS
class Ecodesign():
    def __init__(self, Test_request:str='',Test_Num:str='',Appliance_power:str='', Appliance_Type:str='HM'):
        self.test_req_num:str=Test_request
        self.test_letter:str=Test_Num
        self.test_appl:str=Appliance_Type
        self.pow_appl:str=Appliance_power
        self.folder_appl:str= self.updateFolderAppl()
        self.folder_test:str= self.updateFolderTest()


        #start the script
        if self.test_req_num=='':
            self.getting_input_user()
        try:
            self.folder_all = self.check_folder_name(self.folder_appl,self.folder_test)
            self.listCSVFile = self.dict_file_type_in_folder(self.folder_all)
            self.dictFileToPlot = self.dict_file_to_plot(self.listCSVFile)
            self.test_parameters = self.import_test_param(self.test_req_num,self.test_letter)
            print(self.test_parameters)
        except FindingFile as error:
            print(f"\nOpening files interupted : {error}")
        # set startTime

        startTimer = ti()

        ####importing file


        # get the end time
        endTimer = ti()
        # get the execution time and print it
        print(f"Finish reading data in {endTimer - startTimer:.3f} seconds")

    def align_input_user(self,s: str) -> str:
        spacementForAnswer = 65
        x = 0
        if len(s) < spacementForAnswer:
            x = spacementForAnswer - len(s)
        return s + (" " * x)
    def updateFolderAppl(self)->str:
        return f"{self.test_appl}{sep}{self.pow_appl}kW"
    def updateFolderTest(self)->str:
        return f"{self.test_req_num}{self.test_letter}"
    # getting input from user
    def getting_input_user(self):
        self.test_req_num = input(self.align_input_user("Enter the test request number(yyxxx): "))  # Test number according to test request. 23146: HM BO 70kW XXL / 24013: MONOTANK BO 70kW XXL / 24022: HM SO 45kW XXL /
        self.test_letter = input(self.align_input_user("Enter the test letter: ")).upper()  # The test number. It can be A, B, C, D, etc.
        self.pow_appl = input(self.align_input_user("Enter the power type (25, 35, 45, 60, 70, 85, 120, 45X, 25X): "))  # The power of the appliance in kW: 25, 35, 45, 60, 70, 85, 120, 45X, 25X
        self.folder_appl = self.updateFolderAppl()
        self.folder_test = self.updateFolderTest()

    # intializing path and checking if exist
    def check_folder_name(self, base_older:str='',to_find:str=''):
        if base_older=='' or to_find=='':
            raise FindingFile("\nThe function as been called without parameters")
        if to_find not in listdir(base_older):
            raise FindingFile(f"\nThe folder '{to_find}' wasn't found in '{base_older}'.")
        return f"{base_older}{sep}{to_find}"

    # checking if file exist
    def dict_file_type_in_folder(self,folder:str,type:str='.csv'):
        filtered=[f for f in listdir(folder) if isfile(join(folder,f)) and f.lower().endswith(type)]
        if len(filtered) == 0:
            raise FindingFile(f"No file '.csv' files found in {folder}")
        return filtered

    # check all files to be plot
    def dict_file_to_plot(self,listFiles=[str])->dict:
        file_description = [str]
        file_description = ("MICROPLAN",
            "MICROCOM",
            "DHW_TEMPERATURE",
            "SIDE_TEMPERATURE",
            "PLC",
            "SEEB",)
        fileFoundToPlot = dict()
        for f in listFiles:
            for xf in file_description : 
                if xf in f.upper():
                    fileFoundToPlot[xf]=f"{self.folder_all}{sep}{f}"
                    break
        if len(fileFoundToPlot) == 0:
            raise FindingFile(f"No file '.csv' files found in '{self.folder_all}'")
        return fileFoundToPlot

    #import parameter from test
    def import_test_param(self,test_req_num:str,test_letter:str)->list:
        #file path of our parameter table  
        script_path = abspath(__file__)
        script_directory = dirname(script_path)
        file_path_xlsx = f"{script_directory}{sep}DataTable_TestParam.xlsx"
        #filtering to get only the good test parameter
        # print(read_file_to_dict(file_path_xlsx, file_type='xlsx'))
        test_parameters = list(filter(lambda data: data['TestRequest'] == int(test_req_num) and data['TestNum'] == test_letter, read_file_to_dict(file_path_xlsx, file_type='xlsx')))
        
        if len(test_parameters) < 1:
            raise FindingFile(f"No parameters found for this test :  '{test_req_num}{test_letter}'")
        elif len(test_parameters) > 1:
            for i in test_parameters: print(i)
            idTest = input(self.align_input_user("A few parameter set was found please enter the correct 'ID' :"))
            test_parameters = list(filter(lambda data: data['ID'] == int(idTest) , test_parameters))
        return test_parameters
    
    







# %% run main function 
if __name__ == "__main__": 
    Traitement = Ecodesign("25066","A","70")
    
    