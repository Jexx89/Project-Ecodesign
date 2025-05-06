# Plotly import
from plotly import graph_objects as go  # importing plotly for plotting figures
# from plotly.offline import plot
from plotly.subplots import make_subplots  # importing subplots to plot several curves in the same graph

# FileAndInput  import
from cl_FileAndInput import *
# FileAndInput  import
import random as rd

class ErrorPloting(Exception):
    pass

class GeneratePlot(InputFile):
    def __init__(self, currDir:str='', Path_File:str='', FileType:list[tuple[str,str]]=[FILES_LIST.fCSV], header_time:str='Timestamp'):
        super().__init__(currDir,Path_File,FileType,header_time)
        if self.df is None:
            exit
        self.name_test_descp = self.Path_File
        self.txt_size_num_ax = 20
        self.txt_siz_lbl_xy = 20
        self.txt_siz_leg = 14
        self.txt_siz_tit = 16
        # self.offline_html_path = self.name_test_descp
        self.header_time = header_time
        self.lab_x_ax = "Test time [s]"
        self.lab_prim_y_ax_ = "Temperature [°C]/Pressure[bar]/flow[l or kg -/m]"
        self.lab_sec_y_ax_ = "Gas Vol (L.)/Power[watt]"

        self.fig :go.Figure
        self.creat_fig()

    def add_all_columns(self):
        for d in self.df:
            if d != self.header_time:
                self.trace_fig(self.df[self.header_time] ,self.df[d],"MAIN","MAIN",d,self.color_randomized(),False,1,"solid")
        self.fig.show()
        # plot(self.fig,filename="C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\test" + ".html")

    def trace_fig(self,x_axis, y_axis, group, gourp_ttl, name, col, secd_y_ax, opac, typ_line):
        """
        Function to add the trace on the graphs

        Parameters
        -----------------

        x_axis: array
            Array with values to be plotted on the x axis
        y_axis: array
            Array with values to be plotted on the y axis
        group: string
            Name of the group where to gather the courves
        gourp_ttl: string
            Name of the group to show on graph
        name: string
            Name of the curve to plot
        col: string
            Colour of the curve on the graph
        secd_y_ax: Boolean
            True or False. True: plotting on the secondary y axins. False: plot on the primary
        opac: integer
            Value from 0 to 1 to set the opacity of the line
        typ_line: string
            Set the line layout

        Returns
        -----------

        The trace of the figure be added to the main graph

        """

        # Adding the trace
        self.fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=y_axis,
                yaxis="y",
                legendgroup=group,
                legendgrouptitle_text=gourp_ttl,
                name=name,
                opacity=opac,
                #    mode = typ_line,
                #    marker = {"color" : col}),
                line=dict(color=col, width=1.5, dash=typ_line)),
            secondary_y=secd_y_ax)

    def creat_fig(self):


        """
        Function to edit the layout of the figure

        Parameters
        -----------------

        lab_x_ax: string
            Lable of the x axis
        lab_prim_y_ax_: string
            Lable of the primary y axis
        lab_sec_y_ax_: string
            Lable of the seconday y axis
        txt_size_num_ax: int
            Size of the x and y values
        txt_siz_lbl_xy: int
            Size of the x and y axis lable
        txt_siz_leg: int
            Size of legend
        title: string
            Title of the graph
        txt_siz_tit: string
            Size of the title

        Returns
        -----------

        The editated trace of the graph

        """
        self.fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Editing the layout
        self.fig.update_layout(
            template="simple_white",
            hovermode="x",
            yaxis=dict(tickfont=dict(size=self.txt_size_num_ax)),
            xaxis=dict(tickfont=dict(size=self.txt_size_num_ax)),
            legend=dict(font=dict(size=self.txt_siz_leg),groupclick="toggleitem"),
            title=self.name_test_descp,
            font_size=self.txt_siz_tit)
        self.fig.update_xaxes(
            title=self.lab_x_ax, 
            title_font={"size": self.txt_siz_lbl_xy},
            spikemode="toaxis+across",spikesnap="hovered data")
        self.fig.update_yaxes(
            title=self.lab_prim_y_ax_,
            title_font={"size": self.txt_siz_lbl_xy},
            secondary_y=False)
        self.fig.update_yaxes(
            title=self.lab_sec_y_ax_,
            title_font={"size": self.txt_siz_lbl_xy},
            secondary_y=True,
            anchor="y")

    def color_randomized(self)->str:
        color = ["aliceblue"," antiquewhite"," aqua"," aquamarine"," azure",
                "beige"," bisque"," black"," blanchedalmond"," blue",
                "blueviolet"," brown"," burlywood"," cadetblue",
                "chartreuse"," chocolate"," coral"," cornflowerblue",
                "cornsilk"," crimson"," cyan"," darkblue"," darkcyan",
                "darkgoldenrod"," darkgray"," darkgrey"," darkgreen",
                "darkkhaki"," darkmagenta"," darkolivegreen"," darkorange",
                "darkorchid"," darkred"," darksalmon"," darkseagreen",
                "darkslateblue"," darkslategray"," darkslategrey",
                "darkturquoise"," darkviolet"," deeppink"," deepskyblue",
                "dimgray"," dimgrey"," dodgerblue"," firebrick",
                "floralwhite"," forestgreen"," fuchsia"," gainsboro",
                "ghostwhite"," gold"," goldenrod"," gray"," grey"," green",
                "greenyellow"," honeydew"," hotpink"," indianred"," indigo",
                "ivory"," khaki"," lavender"," lavenderblush"," lawngreen",
                "lemonchiffon"," lightblue"," lightcoral"," lightcyan",
                "lightgoldenrodyellow"," lightgray"," lightgrey",
                "lightgreen"," lightpink"," lightsalmon"," lightseagreen",
                "lightskyblue"," lightslategray"," lightslategrey",
                "lightsteelblue"," lightyellow"," lime"," limegreen",
                "linen"," magenta"," maroon"," mediumaquamarine",
                "mediumblue"," mediumorchid"," mediumpurple",
                "mediumseagreen"," mediumslateblue"," mediumspringgreen",
                "mediumturquoise"," mediumvioletred"," midnightblue",
                "mintcream"," mistyrose"," moccasin"," navajowhite"," navy",
                "oldlace"," olive"," olivedrab"," orange"," orangered",
                "orchid"," palegoldenrod"," palegreen"," paleturquoise",
                "palevioletred"," papayawhip"," peachpuff"," peru"," pink",
                "plum"," powderblue"," purple"," red"," rosybrown",
                "royalblue"," saddlebrown"," salmon"," sandybrown",
                "seagreen"," seashell"," sienna"," silver"," skyblue",
                "slateblue"," slategray"," slategrey"," snow"," springgreen",
                "steelblue"," tan"," teal"," thistle"," tomato"," turquoise",
                "violet"," wheat"," white"," whitesmoke"," yellow",
                "yellowgreen"]
        return rd.choice(color)




# %% differente type of classes to run the files
class MicromFile(GeneratePlot):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)

        # T_sup = dt["Supply [°C]"]  # Temperature on the main tank [°C]
        # T_ret = dt["Return [°C]"]  # Temperature on the pump pipe to cool down the burner [°C]
        # T_DHW_stor = dt["DHW stor (°C)"]  # Temperature inside the big ballon [°C]
        # Flame_current = dt["Flame Curent [uA]"]  # Flame current [A] * 10^-6
        # T_fume_mc = dt["Flue temp [0,01°C]"]  # Temperature on the fume [°C]
        # Burn_mod = dt["Actual measured load"]  # Burner modulation [%]
        #     pump_spd_MicroCOM = dt["Pump PWM %(111F)"]  # Pump modulation power [%] (Range:0 - 100 %)
        #     pump_pwr_MicroCOM = dt["Pump Power W(65F2)"]  # Pump power consumed [W] (Range: 0 - 70 W)
        #     burner_status = dt["Burner State"]  # Status of the burner

    


    # def res_timing(self, t0_miplan):
    #     """
    #     Function to resample the timing array. It matches the different time
    #     when the recording started

    #     Parameters
    #     -----------------

    #     dt: datafrane
    #         The dataframe we want to sincronise
    #     col_name_time : string
    #         Column name in the dataframe where the time vector is stored
    #     t0_miplan : date-type
    #         The date and time taken as reference for sincronizating the data

    #     Returns
    #     -----------

    #     adj_rec_time: series
    #         An array countaining all the sincronised seconds [s]
    #     """

    #     dt_time = self.df[self.header_time]  # have the date and hour in dataframe
    #     st_year = dt_time.dt.year[0]  # Year when we start recording
    #     st_month = dt_time.dt.month[0]  # Month when we start recording
    #     st_day = dt_time.dt.day[0]  # Day when we start recording
    #     sec_array = (dt_time.dt.hour * 60 + dt_time.dt.minute) * 60 + dt_time.dt.second  # have all the hours, min and sec in one array with only seconds
    #     date_array = dt_time.dt.date  # saving only the date
    #     index_day = (date_array - date_array[0])  # having index of how many days havcce passed
    #     ind_arr_days_int = index_day / np.timedelta64(1, "s")  # array with the number of days passed in seconds
    #     st_rec_miplan = (t0_miplan.hour * 3600 + t0_miplan.minute * 60 + t0_miplan.second)  # Staring time of the microplan in seconds
    #     new_sec_arr = (sec_array + ind_arr_days_int - st_rec_miplan)  # Correct time to be added from the reference date, corrected from the 0 of the microplan
    #     # ind_arr_days_int = (index_day/np.timedelta64(1, "s"))/86400 # array with the number of days passed. Just number as integer in days and not seconds
    #     # new_sec_arr = sec_array + ind_arr_days_int*86400 - (17*3600+22*60+33) # - sec_array[0] # Correct time to be added from the reference date, corrected from the 0 of the microplan
    #     # ref_time = datetime.datetime(year=st_year, month=st_month, day=st_day, hour=21, minute=30, second=00)  # make a reference time for the tests
    #     # adj_rec_time = [ref_time + datetime.timedelta(seconds=i) for i in new_sec_arr]

    #     return adj_rec_time


class MicroplanFile(GeneratePlot):
    def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
        super().__init__(currDir, Path_File, FileType)
        self.df["Delta T NORM [°C]"] = self.df["T°out TC  [°C]"]-self.df["T°in DHW [°C]"]

    def add_microplan_trace(self):
        trace_param = [
            # REPORT series
            dict(x=self.df[self.header_time],y=self.df["T°in DHW [°C]"]             ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T in DHW [°C]"      , visible=True ,opacity = 1,line=dict(color="cyan"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["T°out AV.  [°C]"]           ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T out avg [°C]"     , visible=True ,opacity = 1,line=dict(color="red"           , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["Delta T NORM [°C]"]         ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Delta T NORM [°C]"  , visible=True ,opacity = 1,line=dict(color="darkorange"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["FLDHW [kg/min]"]            ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "FLDHW [kg/min]"     , visible=True ,opacity = 1,line=dict(color="darkgreen"     , width=1.5, dash="solid"),secondary_y = False),
            # SEEB series - first axes Y
            # dict(x=self.df[self.header_time],y=self.df["T°in DHW [°C]"]             ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T in DHW [°C]"            , visible=False ,opacity = 1,line=dict(color="cyan"         , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=self.df[self.header_time],y=self.df["T°out TC  [°C]"]            ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T out avg [°C]"           , visible=False ,opacity = 1,line=dict(color="red"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["T°Fume [°C]"]               ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T fume MP[°C]"            , visible=False ,opacity = 1,line=dict(color="gray"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["T°Amb [°C]"]                ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T Amb [°C]"               , visible=False ,opacity = 1,line=dict(color="pink"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["Cumul. QDHW  [kWh]"]        ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Cum ener [kWh]"           , visible=False ,opacity = 1,line=dict(color="yellow"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["pin DHW [bar]"]             ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "P in [bar]"               , visible=False ,opacity = 1,line=dict(color="maroon"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=self.df[self.header_time],y=self.df["T°out PT100  [°C]"]         ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T PT100  [°C]"            , visible=False ,opacity = 1,line=dict(color="peachpuff"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=self.df[self.header_time],y=self.df["T°out TC1  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC1  [°C]"              , visible=False ,opacity = 1,line=dict(color="rosybrown"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=self.df[self.header_time],y=self.df["T°out TC2  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC2  [°C]"              , visible=False ,opacity = 1,line=dict(color="peru"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=self.df[self.header_time],y=self.df["T°out TC3  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC3  [°C]"              , visible=False ,opacity = 1,line=dict(color="papayawhip"       , width=1.5, dash="solid"),secondary_y = False),

            # Microplan series - second axes Y
            dict(x=self.df[self.header_time],y=self.df["Cumul. Gaz Vol. Corr.[L]"]  ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Total Gas consumed [L]"   , visible=False ,opacity = 1,line=dict(color="orange"       , width=1.5, dash="solid"),secondary_y = True),
            dict(x=self.df[self.header_time],y=self.df["Power Absorbed [W]"]        ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Pow consumption [W]"      , visible=False ,opacity = 1,line=dict(color="tomato"       , width=1.5, dash="solid"),secondary_y = True),
            ]
        self.fig.add_traces(trace_param)
        self.fig.show()
        # or 
        # plot(self.fig,filename="C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\test" + ".html")

class Seebfile(GeneratePlot):
    def __init__(self, df:DataFrame, name_test_descp:str, header_time:str="time_stamp"):
        super().__init__(df, name_test_descp, header_time)
        self.df["Delta T NORM [°C]"] = self.df["T°out TC  [°C]"]-self.df["T°in DHW [°C]"]
    def add_seeb_trace(self):
        trace_param = [
            # REPORT series
            dict(x=self.df[self.header_time],y=self.df["T°in DHW [°C]"]             ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T in DHW [°C]"      , visible=True ,opacity = 1,line=dict(color="cyan"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["T°out TC  [°C]"]            ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T out avg [°C]"     , visible=True ,opacity = 1,line=dict(color="red"           , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["Delta T NORM [°C]"]         ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Delta T NORM [°C]"  , visible=True ,opacity = 1,line=dict(color="darkorange"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["FLDHW [kg/min]"]            ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "FLDHW [kg/min]"     , visible=True ,opacity = 1,line=dict(color="darkgreen"     , width=1.5, dash="solid"),secondary_y = False),
            # SEEB series - first axes Y
            # dict(x=self.df[self.header_time],y=self.df["T°in DHW [°C]"]             ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T in DHW [°C]"            , visible=False ,opacity = 1,line=dict(color="cyan"         , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=self.df[self.header_time],y=self.df["T°out TC  [°C]"]            ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T out avg [°C]"           , visible=False ,opacity = 1,line=dict(color="red"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["T°Fume [°C]"]               ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T fume MP[°C]"            , visible=False ,opacity = 1,line=dict(color="gray"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["T°Amb [°C]"]                ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T°Amb [°C]"               , visible=False ,opacity = 1,line=dict(color="pink"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["Cumul. QDHW  [kWh]"]        ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "Cum ener [kWh]"           , visible=False ,opacity = 1,line=dict(color="yellow"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=self.df[self.header_time],y=self.df["pin DHW [bar]"]             ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "P in [bar]"               , visible=False ,opacity = 1,line=dict(color="maroon"       , width=1.5, dash="solid"),secondary_y = False),
            # SEEB series - second axes Y
            dict(x=self.df[self.header_time],y=self.df["Cumul. Gaz Vol. Corr.[L]"]  ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "Total Gas consumed [L]"   , visible=False ,opacity = 1,line=dict(color="orange"       , width=1.5, dash="solid"),secondary_y = True),
            dict(x=self.df[self.header_time],y=self.df["Power Absorbed [W]"]        ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "Pow consumption [W]"      , visible=False ,opacity = 1,line=dict(color="tomato"       , width=1.5, dash="solid"),secondary_y = True),
            ]
        self.fig.add_traces(trace_param)
        self.fig.show()


# %% will check later to sync with previous files
# class DhwTemperatureFile(InputFile):
#     def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
#         super().__init__(currDir, Path_File, FileType)
        
#     def read_df_DHW_sens(dt, appliance):
#         """
#         Function to read some columns of the dataframe and store them in a series
#         (Series is a one-dimensional labeled array capable of holding data of
#         any type (integer, string, float, python objects, etc.). The axis
#         labels are collectively called index)

#         Parameters
#         -----------------

#         dt: dataframe
#             The dataframe with all the stored values
#         appliance: sting
#             Appliance type on which the sensors are located

#         Returns
#         -----------

#         T_1_bas: series
#             An array countaining all the values of the temperature sensor on the lowest position
#         T_2: series
#             An array countaining all the values of the temperature sensor on the second position
#         T_3: series
#             An array countaining all the values of the temperature sensor on the third position
#         T_4: series
#             An array countaining all the values of the temperature sensor on the fourth position
#         T_5_haut: series
#             An array countaining all the values of the temperature sensor on the highest position
#         T_6_bas: series
#             An array Temperature of the sensor in position 6
#         T_7_bas: series
#             An array Temperature of the sensor in position 7
#         T_8_bas_deep: series
#             An array Temperature of the sensor in position 8
#         T_1: series
#             An array Temperature of the sensor in position XXXX
#         T_5: series
#             An array Temperature of the sensor in position XXXX
#         T_1_top: series
#             An array Temperature of the sensor in position XXXX

#         """
#         if appliance == "Normal":

#             T_1_bas = dt["T1 bas"]  # Temperature of the sensor in position 1 [°C]
#             T_2 = dt["T2"]  # Temperature of the sensor in position 2 [°C]
#             T_3 = dt["T3"]  # Temperature of the sensor in position 3 [°C]
#             T_4 = dt["T4"]  # Temperature of the sensor in position 4 [°C]
#             T_5_haut = dt["T5 haut"]  # Temperature of the sensor in position 5 [°C]

#             return T_1_bas, T_2, T_3, T_4, T_5_haut

#         elif appliance == "Monotank":

#             T_1_bas = dt["T1 bas"]  # Temperature of the sensor in position 1 [°C]
#             T_2 = dt["T2"]  # Temperature of the sensor in position 2 [°C]
#             T_3 = dt["T3"]  # Temperature of the sensor in position 3 [°C]
#             T_4 = dt["T4"]  # Temperature of the sensor in position 4 [°C]
#             T_5_haut = dt["T5 haut"]  # Temperature of the sensor in position 5 [°C]
#             T_6_bas = dt["T6 bas"]  # Temperature of the sensor in position 6 [°C]
#             T_7_bas = dt["T7 bas"]  # Temperature of the sensor in position 7 [°C]
#             T_8_bas_deep = dt["T8 bas deep"]  # Temperature of the sensor in position 8 [°C]

#             return T_1_bas, T_2, T_3, T_4, T_5_haut, T_6_bas, T_7_bas, T_8_bas_deep

#         elif appliance == "45TC":

#             T_1 = dt["T1 Top"]  # Temperature of the sensor in position 1 [°C]
#             T_2 = dt["T2"]  # Temperature of the sensor in position 2 [°C]
#             T_3 = dt["T3"]  # Temperature of the sensor in position 3 [°C]
#             T_4 = dt["T4"]  # Temperature of the sensor in position 4 [°C]
#             T_5 = dt["T5 Bottom"]  # Temperature of the sensor in position 5 [°C]

#             return T_1, T_2, T_3, T_4, T_5

#         elif appliance == "70TC":

#             T_1_top = dt["T1 Top"]  # Temperature of the sensor in position 1 [°C]
#             T_2 = dt["T2"]  # Temperature of the sensor in position 2 [°C]
#             T_3 = dt["T3"]  # Temperature of the sensor in position 3 [°C]
#             T_4 = dt["T4"]  # Temperature of the sensor in position 4 [°C]
#             T_5 = dt["T5"]  # Temperature of the sensor in position 5 [°C]
#             T_6 = dt["T6"]  # Temperature of the sensor in position 6 [°C]
#             T_7_bas = dt["T7 bas"]  # Temperature of the sensor in position 7 [°C]

#             return T_1_top, T_2, T_3, T_4, T_5, T_6, T_7_bas

# class SideTemperatureFile(InputFile):
#     def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
#         super().__init__(currDir, Path_File, FileType)

#     def read_df_side_T(dt):
#         """
#         Function to read some columns of the dataframe and store them in a series
#         (Series is a one-dimensional labeled array capable of holding data of
#         any type (integer, string, float, python objects, etc.). The axis
#         labels are collectively called index)

#         Parameters
#         -----------------

#         dt: dataframe
#             The dataframe with all the stored values

#         Returns
#         -----------

#         CH1: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 1 [°C]
#         CH2: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 2 [°C]
#         CH3: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 3 [°C]
#         CH4: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 4 [°C]
#         CH5: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 5 [°C]
#         CH6: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 6 [°C]
#         CH7: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 7 [°C]
#         CH8: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 8 [°C]
#         CH9: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 9 [°C]
#         CH10: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 10 [°C]
#         CH11: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 11 [°C]
#         CH12: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 12 [°C]
#         CH13: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 13 [°C]
#         CH14: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 14 [°C]
#         CH15: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 15 [°C]
#         CH16: series
#             An array countaining all the values of the temperature sensor of thermocouple in position n. 16 [°C]

#         """

#         CH1 = dt["CH1"]  # Temperature of the sensor in position 1 [°C]
#         CH2 = dt["CH2"]  # Temperature of the sensor in position 2 [°C]
#         CH3 = dt["CH3"]  # Temperature of the sensor in position 3 [°C]
#         CH4 = dt["CH4"]  # Temperature of the sensor in position 4 [°C]
#         CH5 = dt["CH5"]  # Temperature of the sensor in position 5 [°C]
#         CH6 = dt["CH6"]  # Temperature of the sensor in position 6 [°C]
#         CH7 = dt["CH7"]  # Temperature of the sensor in position 7 [°C]
#         CH8 = dt["CH8"]  # Temperature of the sensor in position 8 [°C]
#         CH9 = dt["CH9"]  # Temperature of the sensor in position 9 [°C]
#         # CH10 = dt["CH10"] # Temperature of the sensor in position 10 [°C]
#         # CH11 = dt["CH11"] # Temperature of the sensor in position 11 [°C]
#         # CH12 = dt["CH12"] # Temperature of the sensor in position 12 [°C]
#         # CH13 = dt["CH13"] # Temperature of the sensor in position 13 [°C]
#         # CH14 = dt["CH14"] # Temperature of the sensor in position 14 [°C]
#         # CH15 = dt["CH15"] # Temperature of the sensor in position 15 [°C]
#         # CH16 = dt["CH16"] # Temperature of the sensor in position 16 [°C]

#         # return CH1,CH2,CH3,CH4
#         return CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9
#         # return CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9,CH10,CH11,CH12,CH13,CH14
#         # return CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9,CH10,CH11,CH12,CH13,CH14,CH15,CH16

# class PlcFile(InputFile):
#     def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
#         super().__init__(currDir, Path_File, FileType)
    
#     def read_df_PLC(dt, complete):
#         """
#         Function to read some columns of the dataframe and store them in a series
#         (Series is a one-dimensional labeled array capable of holding data of
#         any type (integer, string, float, python objects, etc.). The axis
#         labels are collectively called index)

#         Parameters
#         -----------------

#         dt: dataframe
#             The dataframe with all the stored values
#         complete : string
#             "Yes" or "No". This variable allows to load more data of the dataframe or not

#         Returns
#         -----------

#         PUMP: series
#             An array indicating when the pump is on or off. 0 = pump off. 1 = pump on
#         PUMP SP: series
#             An array countaining all the values of the pump setpoint [°C]. Setpoint between T supply and T return [°C]. It will modulate the pump speed to get closer to this setpoint.
#         PUMP SPEED %: series
#             An array countaining the pwm signal send to the pump. Namely the speed in %

#         """

#         if complete == "No":
#             pump_onoff = dt["PUMP"]  # Array of 0 and 1 to see if pump is ON or OFF [-]
#             pump_stp = dt["PUMP SP"]  # Setpoint of the pump. Delta T between T supply and T return [°C]
#             pump_speed = dt["PUMP SPEED %"]  # Pump speed [%]
#             # volt_burn = dt["VoltageInput"] # Voltage of the XXX [V]
#             return pump_onoff, pump_stp, pump_speed
#         if complete == "Yes":
#             pump_onoff = dt["PUMP"]  # Array of 0 and 1 to see if pump is ON or OFF [-]
#             pump_stp = dt["PUMP SP"]  # Setpoint of the pump. Delta T between T supply and T return [°C]
#             pump_speed = dt["PUMP SPEED %"]  # Pump speed [%]
#             T_sup = dt["SUPPLY DEG"]  # Temperature on the main tank [°C]
#             T_ret = dt["RETURN DEG"]  # Temperature on the pump pipe to cool down the burner [°C]
#             T_DHW_stor = dt["DHW DEG"]  # Temperature inside the big ballon [°C]
#             Flame_current = dt["FLAME µA"]  # Flame current [A] * 10^-6
#             T_fume_mc = dt["FLUE DEG"]  # Temperature on the fume [°C]
#             Burn_mod = dt["MICROCOM Mod."]  # Burner modulation
#             return (T_sup,T_ret,T_DHW_stor,Flame_current,T_fume_mc,Burn_mod,pump_onoff,pump_stp,pump_speed,)




# %% library to do to be able to plot any kind of file
# class ExcelFile(InputFile):
#     def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
#         super().__init__(currDir, Path_File, FileType)

# class CsvFile(InputFile):
#     def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
#         super().__init__(currDir, Path_File, FileType)

# class TxtFile(InputFile):
#     def __init__(self, currDir = '', Path_File = '', FileType = [FILES_LIST.fCSV]):
#         super().__init__(currDir, Path_File, FileType)






# %% run main function 
if __name__ == "__main__":
    file=InputFile()
    GP=GeneratePlot(file.df,"first attempte","Timestamp")
    GP.add_all_columns()
    # Traitement = EcoDesign(Test_request="25066",Test_Num="A",Appliance_power="70")