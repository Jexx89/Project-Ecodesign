"""
Library of all the function to import files.

"""


import csv
import pandas as pd
import os

def read_csv_to_df(path_fol, file_name, dlm=',',sk=0):
    """
    Function in order to read the csv file

    Parameters
    -----------------

    path_fol: string
        The main folde parth where the file is located
    file_name: string
        The file name we want to load. It does not have to include csv
    dlm: sting
        How the data are delimited on the csv file

    Returns
    -----------

    df_csv: dataframe
        A dataframe countaining all the data of the excel sheet
    """
    file_path = f"{path_fol}{os.sep}{file_name}.csv"
    df_csv = pd.read_csv(
        file_path,
        skiprows=sk,
        encoding_errors="ignore",
        low_memory="False",
        delimiter=dlm,
        # header=None, # This option is to have the header as raw stored in the dataframe. In this case we should also activare dtype = "unicode"
        # dtype = "unicode",
        )
    return df_csv


def read_xlsx_to_dict(file_path, sheet_name=0):
    data = []
    try:
        df = pd.read_excel( file_path, sheet_name=sheet_name)
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
        data = df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    return data

def read_txt_to_dict(file_path):
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                row['ID'] = int(row['ID'])
                row['SetpointDHW'] = int(row['SetpointDHW'])
                row['ParamADDER'] = int(row['ParamADDER'])
                row['ParamHysteresis'] = int(row['ParamHysteresis'])
                row['ParamAdderCoef'] = float(row['ParamAdderCoef'])
                row['P_factor'] = int(row['P_factor'])
                row['I_Factor'] = int(row['I_Factor'])
                row['SetPointDeltaPump'] = int(row['SetPointDeltaPump'])
                row['PrePumpPercent'] = int(row['PrePumpPercent'])
                row['PrePumpTime'] = int(row['PrePumpTime'])
                row['PrePumpBurningPercent'] = int(row['PrePumpBurningPercent'])
                row['PostPumpPercent'] = int(row['PostPumpPercent'])
                row['PostPumpTime'] = int(row['PostPumpTime'])
                row['InertiaMBTPercent'] = int(row['InertiaMBTPercent'])
                data.append(row)
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    return data

def read_tsv_to_dict(file_path):
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter='\t')
            for row in csv_reader:
                row['ID'] = int(row['ID'])
                row['SetpointDHW'] = int(row['SetpointDHW'])
                row['ParamADDER'] = int(row['ParamADDER'])
                row['ParamHysteresis'] = int(row['ParamHysteresis'])
                row['ParamAdderCoef'] = float(row['ParamAdderCoef'])
                row['P_factor'] = int(row['P_factor'])
                row['I_Factor'] = int(row['I_Factor'])
                row['SetPointDeltaPump'] = int(row['SetPointDeltaPump'])
                row['PrePumpPercent'] = int(row['PrePumpPercent'])
                row['PrePumpTime'] = int(row['PrePumpTime'])
                row['PrePumpBurningPercent'] = int(row['PrePumpBurningPercent'])
                row['PostPumpPercent'] = int(row['PostPumpPercent'])
                row['PostPumpTime'] = int(row['PostPumpTime'])
                row['InertiaMBTPercent'] = int(row['InertiaMBTPercent'])
                data.append(row)
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    return data



								


def read_file_to_dict(file_path, file_type='xlsx', sheet_name=0):
    if file_type.lower() == 'txt':
        return read_txt_to_dict(file_path)
    elif file_type.lower() == 'csv':
        return read_txt_to_dict(file_path)
    elif file_type.lower() == 'tsv':
        return read_tsv_to_dict(file_path)
    elif file_type.lower() == 'xlsx':
        return read_xlsx_to_dict(file_path, sheet_name)
    else:
        raise ValueError("Type de fichier non pris en charge. Utilisez 'txt', 'csv', 'tsv', ou 'xlsx'.")



# Exemple d'utilisation
if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(script_path)
    file_path_xlsx = f"{script_directory}{os.sep}DataTable_TestParam.xlsx"
    data_dict_xlsx = read_file_to_dict(file_path_xlsx, file_type='xlsx')
    print("Données du fichier Excel:")
    print(data_dict_xlsx)

    # file_path_csv = 'chemin_vers_votre_fichier.csv'
    # data_dict_csv = read_file_to_dict(file_path_csv, file_type='csv')
    # print("Données du fichier CSV:")
    # print(data_dict_csv)

    # file_path_tsv = 'chemin_vers_votre_fichier.tsv'
    # data_dict_tsv = read_file_to_dict(file_path_tsv, file_type='tsv')
    # print("Données du fichier TSV:")
    # print(data_dict_tsv)