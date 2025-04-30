
# Library to import datafile for ecodesign table


import csv
from pandas import read_excel, DataFrame
from os import getcwd, sep

# %% error handling
class ErrorFile(Exception):
    pass

#class to handle the parameter section of the ecodesign function
class cl_EcoDesign_Parameter():
    def __init__(self, Test_request:int=1,Test_Num:str='A'):
        self.ALL_DF:DataFrame = []
        self.test_parameters = self.import_test_param(Test_request,Test_Num)
        

    #import parameter from test
    def import_test_param(self,test_req_num:int,test_letter:str)->DataFrame:
        #file path of our parameter table  
        file_path_xlsx = f"{getcwd()}{sep}DataTable_TestParam.xlsx"
        #filtering to get only the good test parameter
        # print(read_file_to_dict(file_path_xlsx, file_type='xlsx'))
        #test_parameters = list(filter(lambda data: data['TestRequest'] == test_req_num and data['TestNum'] == test_letter, self.read_file_to_dict(file_path_xlsx)))
        self.ALL_DF = self.read_file_to_dict(file_path_xlsx)
        tp = self.ALL_DF[self.ALL_DF['TestRequest'].apply(lambda x:x==test_req_num) & self.ALL_DF['TestNum'].apply(lambda x:x==test_letter)]

        if len(tp) < 1:
            raise ErrorFile(f"No parameters found for this test :  '{test_req_num}{test_letter}'")
        elif len(tp) > 1:
            for i in tp: print(f"{i} = {tp[i].values}")
            idTest = input("A few parameter set was found please enter the correct 'ID' :")
            tp=tp[tp['ID'].apply(lambda x:x==idTest) ]
            #tp = list(filter(lambda data: data['ID'] == int(idTest) , test_parameters))
        return tp

    #function used to read the xlsx database of all the parameters
    def read_xlsx_to_dict(self,file_path, sheet_name=0):
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




    def read_txt_to_dict(self,file_path):
        data = DataFrame
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
            data = list(csv_reader)
            df = DataFrame(data)
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

    def read_tsv_to_dict(self,file_path):
        data = DataFrame
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file, delimiter='\t')
            data = list(csv_reader)
            df = DataFrame(data)
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

    def read_file_to_dict(self,file_path, file_type='xlsx', sheet_name=0)->DataFrame:
        if file_type.lower() == 'txt':
            return self.read_txt_to_dict(file_path)
        elif file_type.lower() == 'csv':
            return self.read_txt_to_dict(file_path)
        elif file_type.lower() == 'tsv':
            return self.read_tsv_to_dict(file_path)
        elif file_type.lower() == 'xlsx':
            return self.read_xlsx_to_dict(file_path, sheet_name)
        else:
            raise ValueError("Type de fichier non pris en charge. Utilisez 'txt', 'csv', 'tsv', ou 'xlsx'.")

# Exemple d'utilisation
if __name__ == "__main__":
    dataFile = cl_EcoDesign_Parameter(25063,"G").test_parameters
    print("\nDonnées du fichier Excel:")
    for i in dataFile: print(f"{i} = {dataFile[i].values}")
    

    # file_path_csv = 'chemin_vers_votre_fichier.csv'
    # data_dict_csv = read_file_to_dict(file_path_csv, file_type='csv')
    # print("Données du fichier CSV:")
    # print(data_dict_csv)

    # file_path_tsv = 'chemin_vers_votre_fichier.tsv'
    # data_dict_tsv = read_file_to_dict(file_path_tsv, file_type='tsv')
    # print("Données du fichier TSV:")
    # print(data_dict_tsv)