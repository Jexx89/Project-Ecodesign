# -*- coding: utf-8 -*-
"""Created on Mon Dec 18 13:22:05 2023

@author: Marcello Nitti
"""

#%% CLASS

# class file_parameters:
#     test_req_num:str #Test number as such YYXXX (YY year)(XXXtest number)
#     test_num:str # Test Itereation from A to Z
#     alg_typ:int  # The algo type from 1 to 99
#     T_DHW: int # DHW Setpoint temperature [°C]
#     T_ADD: int # This is the delta T between the T_CH and T_DHW_SP [°C]
#     T_HYS: int # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
    
#     def __init__(self):
#         pass

#     def fol_test()->str:
#         return  test_req_num + test_num
    
#     def name_test_descp()->str:
#         return fol_test() + "_XXL_HM70TC_Algo" + alg_typ

class name_files:

    # def __init__(self, path_fol, file_name):

    #     self.path_fol = path_fol
    #     self.file_name = file_name

    def TR_files(self,test_req_num,test_num,alg_typ):

        """
        Function in order to read the csv file

        Parameters
        -----------------

        test_req_num: string
            Test request number
        test_num: string
            Numer of test executed. Number is a letter (in maiuscle) of the alphabet
        alg_typ: string
            The algorithm type/number we use for the tests
    
        Returns
        -----------

        T_DHW : integer
            Setpoint of DHW for the selected test [°C]
        T_ADD : integer
            Setpoint of delta T (Supply - DHW) for the selected test [°C]
        T_HYS : integer
            Setpoint of the hystesis value for the selected test [°C]
        """


        if test_req_num == "23146":
        
            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

            if test_num == "A" or test_num == "B":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
            
            elif test_num == "C":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "E" or test_num == "F" or test_num == "G":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 15 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "H":

                T_DHW = 60 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 45 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "I":

                T_DHW = 60 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 30 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24013":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM70_Algo" + alg_typ

            if test_num == "A" or test_num == "B":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 15 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "C":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 10 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "D":

                T_DHW = 52 # DHW Setpoint temperature [°C]
                T_ADD = 13 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 10 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "E" or test_num == "E2":

                T_DHW = 53 # DHW Setpoint temperature [°C]
                T_ADD = 11 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 14 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "F" or test_num == "G":

                T_DHW = 53 # DHW Setpoint temperature [°C]
                T_ADD = 11 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 12 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
            
        elif test_req_num == "24022":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM45TC_Algo" + alg_typ

            if test_num == "A":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 10 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
            
            elif test_num == "B":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "C":

                T_DHW = 45 # DHW Setpoint temperature [°C]
                T_ADD = 13 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "D" or test_num == "D2" or test_num == "E":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "F":

                T_DHW = 60 # DHW Setpoint temperature [°C]
                T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 16 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "G" or test_num == "H":

                T_DHW = 53 # DHW Setpoint temperature [°C]
                T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 5 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "I":

                T_DHW = 49 # DHW Setpoint temperature [°C]
                T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "J" or test_num == "J2" or test_num == "K":

                name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

                T_DHW = 54 # DHW Setpoint temperature [°C]
                T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24041":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

            T_DHW = 54 # DHW Setpoint temperature [°C]
            T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
            T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24042":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

            if test_num == "A":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 15 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
            
            elif test_num == "B":

                T_DHW = 49 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "C":

                T_DHW = 48 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 2 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "D":

                T_DHW = 48 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
            
            elif test_num == "E":

                T_DHW = 48 # DHW Setpoint temperature [°C]
                T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
            
            elif test_num == "F":

                T_DHW = 49 # DHW Setpoint temperature [°C]
                T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
            
            elif test_num == "G" or test_num == "H" or test_num == "J" or test_num == "J2":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24052":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM25TC_Algo" + alg_typ

            if test_num == "A" or test_num == "B" or test_num == "C":

                T_DHW = 54 # DHW Setpoint temperature [°C]
                T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "D":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24058":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM35TC_Algo" + alg_typ

            if test_num == "A" or test_num == "B":

                T_DHW = 53 # DHW Setpoint temperature [°C]
                T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 5 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "C":

                T_DHW = 54 # DHW Setpoint temperature [°C]
                T_ADD = 7.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "D":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 8.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24064":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM120TC_Algo" + alg_typ

            if test_num == "A":

                T_DHW = 53 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
            
            elif test_num == "B":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "C":

                T_DHW = 49 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "D":

                T_DHW = 48 # DHW Setpoint temperature [°C]
                T_ADD = 12 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 7 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "E":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 9 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 4 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "F":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 4 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "G":

                T_DHW = 52 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 5 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24074":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM35TC_Algo" + alg_typ

            if test_num == "B" or test_num == "C" or test_num == "D" or test_num == "E" or test_num == "F" or test_num == "G":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 8.5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 5 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24077":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM45XTC_Algo" + alg_typ

            if test_num == "A":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "B" or test_num == "C" or test_num == "I":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "D":

                T_DHW = 53 # DHW Setpoint temperature [°C]
                T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "E" or test_num == "F":

                T_DHW = 53 # DHW Setpoint temperature [°C]
                T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 4 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "G":

                T_DHW = 53 # DHW Setpoint temperature [°C]
                T_ADD = 7 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 3 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "H":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 5 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "J":

                T_DHW = 55 # DHW Setpoint temperature [°C]
                T_ADD = 5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "K":

                T_DHW = 54 # DHW Setpoint temperature [°C]
                T_ADD = 6 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 5 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "L":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24078":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

            if test_num == "A" or test_num == "B" or test_num == "F" or test_num == "G":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "C" or test_num == "D":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 9 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "E":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 11 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 9 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "H":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 9 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 10 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "I":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 9 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 9 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "J":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 9 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "K" or test_num == "L":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "M":

                T_DHW = 52 # DHW Setpoint temperature [°C]
                T_ADD = 8 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "N" or test_num == "O":

                T_DHW = 52 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 8 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        elif test_req_num == "24079":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM25XTC_Algo" + alg_typ

            if test_num == "A":

                T_DHW = 50 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "B":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 9 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "C":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 10 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 6 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]
        
        elif test_req_num == "24122":

            fol_test = test_req_num + test_num
            name_test_descp = fol_test + "_XXL_HM70TC_Algo" + alg_typ

            if test_num == "A":

                T_DHW = 51 # DHW Setpoint temperature [°C]
                T_ADD = 5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 7 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "B":

                T_DHW = 52 # DHW Setpoint temperature [°C]
                T_ADD = 5 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 7 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

            elif test_num == "C":

                T_DHW = 52 # DHW Setpoint temperature [°C]
                T_ADD = 6 # This is the delta T between the T_CH and T_DHW_SP [°C]
                T_HYS = 7 # This is the delta T between the T_DHW_SP and the starting of the burner [°C]

        return T_DHW,T_ADD,T_HYS
    
