# -*- coding: utf-8 -*-
"""Created on Mon Dec 18 13:22:05 2023

@author: Marcello Nitti
"""

import os
import pandas as pd # importing pandas dataframe

#%% CLASS


class impt_files:

    # def __init__(self, path_fol, file_name):

    #     self.path_fol = path_fol
    #     self.file_name = file_name

    def read_csv_file(self,path_fol,file_name):

        """
        Function in order to read the csv file

        Parameters
        -----------------

        path_fol: string
            The main folde parth where the file is located
        file_name: string
            The file name we want to load. It does not have to include csv
    
        Returns
        -----------

        df_csv: dataframe
            A dataframe countaining all the data of the excel sheet
        """

        df_csv = pd.read_csv(
        path_fol +
        os.sep +
        file_name + ".csv",
        # skiprows=1,
        encoding_errors="ignore",
        low_memory="False",
        delimiter=",",
        # header=None, # This option is to have the header as raw stored in the dataframe. In this case we should also activare dtype = "unicode"
        # dtype = "unicode",
        )

        return df_csv
    
    def read_csv_file_v2(self,path_fol,file_name,dlm):

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

        df_csv = pd.read_csv(
        path_fol +
        os.sep +
        file_name + ".csv",
        # skiprows=1,
        encoding_errors="ignore",
        low_memory="False",
        delimiter=dlm,
        # header=None, # This option is to have the header as raw stored in the dataframe. In this case we should also activare dtype = "unicode"
        # dtype = "unicode",
        )

        return df_csv
