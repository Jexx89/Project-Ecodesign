# -*- coding: utf-8 -*-
"""Created on Mon Jan 04 14:18:56 2024

@author: Marcello Nitti
"""

import numpy as np # importing numpy library
import pandas as pd # importing pandas dataframe
import datetime

#%% CLASS


class timing_reset:

    # def __init__(self, dt):

    #     self.dt = dt # Dataframe

    def res_timing(self,dt,col_name_time,t0_miPLAN):

        """
        Function to resample the timing array. It matches the different time
        when the recording started

        Parameters
        -----------------

        dt: datafrane
            The dataframe we want to sincronise
        col_name_time: string
            Name of the column in the dataframe where the time data are stored
        t0_miplan: array
            Time array of microPLAN that is used as reference. Reason is because microPLAN acquire every second.

        Returns
        -----------

        adj_rec_time: series
            An array countaining all the sincronised seconds [s].
        """

        dt_time = pd.to_datetime(dt[col_name_time],dayfirst="True") # have the date and hour in dataframe
        st_year = dt_time.dt.year[0] # Year when we start recording
        st_month = dt_time.dt.month[0] # Month when we start recording
        st_day = dt_time.dt.day[0] # Day when we start recording
        sec_array = (dt_time.dt.hour*60+dt_time.dt.minute)*60 + dt_time.dt.second # have all the hours, min and sec in one array with only seconds
        date_array = dt_time.dt.date # saving only the date
        index_day = date_array - date_array[0] # having index of how many days havcce passed
        ind_arr_days_int = (index_day/np.timedelta64(1, "s")) # array with the number of days passed in seconds
        st_rec_miplan = t0_miPLAN.hour*3600 + t0_miPLAN.minute*60 + t0_miPLAN.second # Staring time of the microplan in seconds
        new_sec_arr = sec_array + ind_arr_days_int - st_rec_miplan # Correct time to be added from the reference date, corrected from the 0 of the microplan
        # ind_arr_days_int = (index_day/np.timedelta64(1, "s"))/86400 # array with the number of days passed. Just number as integer in days and not seconds 
        # new_sec_arr = sec_array + ind_arr_days_int*86400 - (17*3600+22*60+33) # - sec_array[0] # Correct time to be added from the reference date, corrected from the 0 of the microplan
        ref_time = datetime.datetime(year=st_year, month=st_month, day=st_day, hour=21, minute=30, second=00) # make a reference time for the tests
        adj_rec_time = [ref_time + datetime.timedelta(seconds=i) for i in new_sec_arr]

        return adj_rec_time
    

    def res_timing_comparison(self,dt,col_name_time,t0_miPLAN):

        """
        Function to resample the timing array. It matches the different time
        when the recording started

        Parameters
        -----------------

        dt: datafrane
            The dataframe we want to sincronise
        col_name_time: string
            Name of the column in the dataframe where the time data are stored
        t0_miplan: array
            Time array of microPLAN that is used as reference. Reason is because microPLAN acquire every second.

        Returns
        -----------

        adj_rec_time: series
            An array countaining all the sincronised seconds [s].
        """

        st_day_reset = 1
        st_month_reset = 1
        st_year_reset = 2025

        dt_time = pd.to_datetime(dt[col_name_time],dayfirst="True") # have the date and hour in dataframe
        sec_array = (dt_time.dt.hour*60+dt_time.dt.minute)*60 + dt_time.dt.second # have all the hours, min and sec in one array with only seconds
        date_array = dt_time.dt.date # saving only the date
        index_day = date_array - date_array[0] # having index of how many days havcce passed
        ind_arr_days_int = (index_day/np.timedelta64(1, "s")) # array with the number of days passed in seconds
        st_rec_miplan = t0_miPLAN.hour*3600 + t0_miPLAN.minute*60 + t0_miPLAN.second # Staring time of the microplan in seconds
        new_sec_arr = sec_array + ind_arr_days_int - st_rec_miplan # Correct time to be added from the reference date, corrected from the 0 of the microplan
        ref_time = datetime.datetime(year=st_year_reset, month=st_month_reset, day=st_day_reset, hour=21, minute=30, second=00) # make a reference time for the tests
        adj_rec_time = [ref_time + datetime.timedelta(seconds=i) for i in new_sec_arr]

        return adj_rec_time
    

    def res_timing_comparison_bypass(self,dt,col_name_time,t0_miPLAN,bypass_time):

        """
        Function to resample the timing array. It matches the different time
        when the recording started

        Parameters
        -----------------

        dt: datafrane
            The dataframe we want to sincronise
        col_name_time: string
            Name of the column in the dataframe where the time data are stored
        t0_miplan: array
            Time array of microPLAN that is used as reference. Reason is because microPLAN acquire every second.

        Returns
        -----------

        adj_rec_time: series
            An array countaining all the sincronised seconds [s].
        """

        st_day_reset = 1
        st_month_reset = 1
        st_year_reset = 2025

        dt_time = pd.to_datetime(dt[col_name_time],dayfirst="True") # have the date and hour in dataframe
        sec_array = (dt_time.dt.hour*60+dt_time.dt.minute)*60 + dt_time.dt.second # have all the hours, min and sec in one array with only seconds
        date_array = dt_time.dt.date # saving only the date
        index_day = date_array - date_array[0] # having index of how many days havcce passed
        ind_arr_days_int = (index_day/np.timedelta64(1, "s")) # array with the number of days passed in seconds
        st_rec_miplan = t0_miPLAN.hour*3600 + t0_miPLAN.minute*60 + t0_miPLAN.second + bypass_time - 320 # Staring time of the microplan in seconds
        new_sec_arr = sec_array + ind_arr_days_int - st_rec_miplan # Correct time to be added from the reference date, corrected from the 0 of the microplan
        ref_time = datetime.datetime(year=st_year_reset, month=st_month_reset, day=st_day_reset, hour=21, minute=30, second=00) # make a reference time for the tests
        adj_rec_time = [ref_time + datetime.timedelta(seconds=i) for i in new_sec_arr]

        return adj_rec_time
    

    def res_timing_comparison_same_day(self,dt):

        """
        Function to resample the timing array. It matches the different time
        when the recording started

        Parameters
        -----------------

        dt: datafrane
            The dataframe we want to sincronise
        col_name_time: string
            Name of the column in the dataframe where the time data are stored
        t0_miplan: array
            Time array of microPLAN that is used as reference. Reason is because microPLAN acquire every second.

        Returns
        -----------

        adj_rec_time: series
            An array countaining all the sincronised seconds [s].
        """

        """Programma generale"""

        dt_time = pd.to_datetime(dt,dayfirst="True") # have the date and hour in dataframe
        sec_array = (dt_time.hour*60+dt_time.minute)*60 + dt_time.second # have all the hours, min and sec in one array with only seconds
        mid_ind = np.where(sec_array == 0) # find all the indices when we have midnight
        mid_ind_vct = np.asanyarray(mid_ind) # transform the indices in an array
        mid_ind_vct_1D = np.ravel(mid_ind_vct) # make the vector 1D
        days = max(dt_time.day - dt_time.day[0]) # check the amount of days we have
        len(mid_ind[0]) == days # double check to see if the number of days are equal. Maybe microPLAN or SEEB skipped the value (00:00:00)
        ind_list = np.append(mid_ind_vct_1D, len(dt_time)-1) # add the last value to the array in order to have the bounday index for the last day
        dt_time_new_date = dt_time.map(lambda t: t.replace(month=2, day=23)) # assign a fake month and day to the timing vector
        int_num_day = np.arange(0,days+1) # creating a vector countaining the increasing number of day
        day_and_ind = np.column_stack((int_num_day,ind_list)) # from 1 D array to a 2D countaining days number and the index where the new day start

        counter = 0
        dict_day_arr = {}

        for i in day_and_ind:
            dict_day_arr["day_" + str(i[0])] = dt_time_new_date[counter:i[1]]
            counter=i[1]

        return day_and_ind,dict_day_arr


    def res_tim_comp_same_day_no_midnight(self,dt):

        """
        Function to resample the timing array. It matches the different time
        when the recording started

        Parameters
        -----------------

        dt: datafrane
            The dataframe we want to sincronise
        col_name_time: string
            Name of the column in the dataframe where the time data are stored
        t0_miplan: array
            Time array of microPLAN that is used as reference. Reason is because microPLAN acquire every second.

        Returns
        -----------

        adj_rec_time: series
            An array countaining all the sincronised seconds [s].
        """

        """Programma generale"""

        dt_time = pd.to_datetime(dt,dayfirst="True") # have the date and hour in dataframe
        days_num = dt_time.date - dt_time.date[0] # compute the number of days we have in the test
        d_check = datetime.timedelta(1)
        indx_chang_day = np.zeros(5)
        j=0
        for i in range (0, len(days_num)-1):

            if days_num[i+1] - days_num[i] == d_check:
                indx_chang_day[j] = i+1
                j = j + 1

        indx_chang_day = indx_chang_day[indx_chang_day != 0] # remove the zero from the list
        ind_list = np.append(indx_chang_day, len(dt_time)-1).astype(int) # add the last value to the array in order to have the bounday index for the last day. Converting it to integer to not have problem in the for loop
        days = max(dt_time.day - dt_time.day[0]) # check the amount of days we have
        dt_time_new_date = dt_time.map(lambda t: t.replace(month=2, day=23)) # assign a fake month and day to the timing vector
        int_num_day = np.arange(0,days+1) # creating a vector countaining the increasing number of day
        day_and_ind = np.column_stack((int_num_day,ind_list)) # from 1 D array to a 2D countaining days number and the index where the new day start

        counter = 0
        dict_day_arr = {}

        for i in day_and_ind:
            dict_day_arr["day_" + str(i[0])] = dt_time_new_date[counter:int(i[1])]
            counter=i[1]

        return day_and_ind,dict_day_arr


