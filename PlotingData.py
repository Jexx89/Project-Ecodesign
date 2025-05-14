'''
Library 
--------------

Class: 
* 'GeneratePlot' :
    This library allow the user to generate a plot based on a dataframe for the lab in dworp
    We can add a lot of parameter and modify as we wish by adding new function based on : add_trace------

TODO:
--------------
* go to dash instead of plotly to have better functionnalities
* add more trace library to handle more dataframes
* add error handler

Created by JSB(based on Marcello😍🍕 script)
--------------

V1.0 : initial rev
    * creat and initialise figure
    * Creat and add trace with random color
    * creat and add trace for Ecodesign project with Microplan; Seeb; Microcom DataFrame
    * Show and creat html file output
'''


#%% Import Lib
from plotly import graph_objects as go  # importing plotly for plotting figures
from plotly.subplots import make_subplots  # importing subplots to plot several curves in the same graph
from plotly.offline import plot
from pandas import DataFrame
import random as rd
import logging

#%% to delete if we clean the class
from FileManager import InputFile # used to read file ( to test the class)
from time import time # used to measure the performance of the class


#%% GeneratePlot
class GeneratePlot():
    '''Class to generate and plot from dataframe'''
    def __init__(self, header_time:str='Timestamp',plot_name='Template'):
        '''
        This class allow us to creat a plot from plotly library. we can trace all columns from file of filter the columns from a dataframe. 
        
        Parameters
        -----------
        header_time:str
            the columns name from the dataframe to use as X axis
        plot_name:str
            Name of the plot that will be shown
        Output
        -------
        The ouput is a plot as a form of .html file.
        '''
        logging.basicConfig(filename='log\\trace.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        self.header_time = header_time
        self.plot_name = plot_name
        self.trace_param = []
        self.stime = time()

    def add_trace_all_columns(self, df:DataFrame):
        '''
        This Function is used to plot all the data, from a dataframe?
        This function adds all the trace to the plot initially created.
        List of columns ignored : 
        "Time [h]","Time DMY","Time (h)","Time (dd hh:mm:ss)","Timestamp", "Cumul Time(ms)", "Time record(ms)"

        Parameter
        ---------
        df:DataFrame
            the dataframe with all the data to plot

        Output
        ------
        This function 
        '''
        self.stime = time()
        liste_unwanted_col = ["Time [h]","Time DMY","Time (h)","Time (dd hh:mm:ss)","Timestamp", "Cumul Time(ms)", "Time record(ms)"]
        print("Creat each trace from file")
        for d in df:
            if d not in liste_unwanted_col: #d != self.header_time and 
                secondary_axe:bool = df[d].max() > 120
                self.fig.add_trace(
                    go.Scatter(
                    x=df[self.header_time],
                    y=df[d],
                    legendgroup ="sec" if secondary_axe else"prim",
                    legendgrouptitle_text = "Secondary" if secondary_axe else"Primary",
                    name = d, 
                    # visible=True ,
                    # opacity = 1,
                    line=
                        dict(
                            color=self.color_randomized(),
                            width=1.5,
                            dash="solid"
                            )
                    ),secondary_y = secondary_axe)
        print(f"PLOT - Adding trace for each columns : {time() - self.stime:.2f} sec")
        logging.info(f"PLOT - Adding trace for each columns : {time() - self.stime:.2f} sec")

    def creat_figure(self):
        """
        Function to creat and edit the layout of the figure
        """
        self.stime = time()
        self.lab_x_axe = "Time"
        self.lab_prim_y_axe = "Values [°C][bar][l/m][kg/m][%][µA]"
        self.lab_sec_y_axe = "Values [l][Watt][mbar]"
        self.txt_size_num_ax = 20
        self.txt_siz_lbl_xy = 20
        self.txt_siz_leg = 14
        self.txt_siz_tit = 16
        self.fig =go.Figure()
        self.fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Editing the layout
        # Configure axes
        self.fig.update_layout(
            template="simple_white",
            clickmode='event+select',
            title=self.plot_name,
            font_size=self.txt_siz_tit,
            legend=dict(font=dict(size=self.txt_siz_leg),groupclick="toggleitem",x=1.0, y=1.0, xanchor="left", yanchor="top", orientation="v"),
            xaxis=dict(title=self.lab_x_axe,title_font={"size": self.txt_siz_lbl_xy},spikesnap="hovered data",spikemode="toaxis+across", domain=[0.0, 0.95]),
            yaxis=dict(title=self.lab_prim_y_axe, title_font={"size": self.txt_siz_lbl_xy}),
            yaxis2=dict(title=self.lab_sec_y_axe, overlaying="y", side="right", title_font={"size": self.txt_siz_lbl_xy},anchor="y"),
            hovermode="x unified",  # "x" lables appear with each colour. "x unified" one unique box that groups all the lable
            margin=dict(l=60, r=120, t=50, b=50)
        )
        print(f"PLOT - Creating figure and initialisasing layout : {time() - self.stime:.2f} sec")
        logging.info(f"PLOT - Creating figure and initialising layout : {time() - self.stime:.2f} sec")

    def creat_html_figure(self, new_file_path:str='C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\Template.html'):
        '''
        Function to generate file and show the figure in browser

        Parameter
        --------
        new_file_path:str
            this varaible is to set a name for the file created
        '''
        self.stime = time()
        plot(self.fig,filename=new_file_path)
        print(f"PLOT - Generating plot : {time() - self.stime:.2f} sec")
        logging.info(f"PLOT - Generating plot : {time() - self.stime:.2f} sec")
    
    def show_html_figure(self):
        '''
        Function to show the figure in browser
        '''
        self.stime = time()
        self.fig.show()
        print(f"PLOT - Generating plot : {time() - self.stime:.2f} sec")
        logging.info(f"PLOT - Generating plot : {time() - self.stime:.2f} sec")

    def add_filtered_trace(self):
        '''
        This function add trace for each item in trace_param.
        '''
        self.stime = time()
        for t in self.trace_param :
                self.fig.add_trace(
                    go.Scatter(
                    x                       = t['x'],
                    y                       = t['y'],
                    legendgroup             = t['legendgroup'],
                    legendgrouptitle_text   = t['legendgrouptitle_text'],
                    name                    = t['name'], 
                    visible                 = t['visible'], 
                    opacity                 = t['opacity'], 
                    line                    = t['line'], 
                    ),
                    secondary_y             = t['secondary_y'], )
        print(f"PLOT - Adding trace from dictionary : {time() - self.stime:.2f} sec")
        logging.info(f"PLOT - Adding trace from dictionary : {time() - self.stime:.2f} sec")

    def add_trace_microplan(self,df:DataFrame,header_time:str):
        '''This function compile all the data to creat a collection of trace for Microplan'''
        self.stime = time()
        trace_param = [
            # REPORT series
            dict(x=df[header_time],y=df["T°in DHW [°C]"]             ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T in DHW [°C]"      , visible=True ,opacity = 1,line=dict(color="cyan"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°out AV.  [°C]"]           ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T out avg [°C]"     , visible=True ,opacity = 1,line=dict(color="red"           , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Delta T NORM [°C]"]         ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Delta T NORM [°C]"  , visible=True ,opacity = 1,line=dict(color="darkorange"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["FLDHW [kg/min]"]            ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "FLDHW [kg/min]"     , visible=True ,opacity = 1,line=dict(color="darkgreen"     , width=1.5, dash="solid"),secondary_y = False),
            # microplan series - first axes Y
            # dict(x=df[header_time],y=df["T°in DHW [°C]"]             ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T in DHW [°C]"            , visible=False ,opacity = 1,line=dict(color="cyan"         , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC  [°C]"]            ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T out avg [°C]"           , visible=False ,opacity = 1,line=dict(color="red"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°Fume [°C]"]               ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T fume MP[°C]"            , visible='legendonly' ,opacity = 1,line=dict(color="gray"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°Amb [°C]"]                ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T Amb [°C]"               , visible='legendonly' ,opacity = 1,line=dict(color="pink"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Cumul. QDHW  [kWh]"]        ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Cum ener [kWh]"           , visible='legendonly' ,opacity = 1,line=dict(color="yellow"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["pin DHW [bar]"]             ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "P in [bar]"               , visible='legendonly' ,opacity = 1,line=dict(color="maroon"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out PT100  [°C]"]         ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T PT100  [°C]"            , visible=False ,opacity = 1,line=dict(color="peachpuff"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC1  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC1  [°C]"              , visible=False ,opacity = 1,line=dict(color="rosybrown"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC2  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC2  [°C]"              , visible=False ,opacity = 1,line=dict(color="peru"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC3  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC3  [°C]"              , visible=False ,opacity = 1,line=dict(color="papayawhip"       , width=1.5, dash="solid"),secondary_y = False)
            # Microplan series - second axes Y
            dict(x=df[header_time],y=df["Cumul. Gaz Vol. Corr.[L]"]  ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Total Gas consumed [L]"   , visible='legendonly' ,opacity = 1,line=dict(color="orange"       , width=1.5, dash="solid"),secondary_y = True),
            dict(x=df[header_time],y=df["Power Absorbed [W]"]        ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Pow consumption [W]"      , visible='legendonly' ,opacity = 1,line=dict(color="tomato"       , width=1.5, dash="solid"),secondary_y = True),
            # Microplan parameter serie 
            dict(x=df[header_time],y=df["T = 30 [°C]"]               ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T = 30 [°C]"              , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T = 45 [°C]"]               ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T = 45 [°C]"              , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T = 55 [°C]"]               ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T = 55 [°C]"              , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
            ]
        self.trace_param.extend(trace_param)
        print(f"PLOT - Adding microplan trace to the dictonary : {time() - self.stime:.2f} sec")
        logging.info(f"PLOT - Adding microplan trace to the dictonary : {time() - self.stime:.2f} sec")

    def add_trace_seeb(self,df:DataFrame,header_time:str):
        '''This function compile all the data to creat a collection of trace for Seeb'''
        self.stime = time()
        trace_param = [
            # REPORT series
            dict(x=df[header_time],y=df["T°in DHW [°C]"]             ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T in DHW [°C]"      , visible=True ,opacity = 1,line=dict(color="cyan"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°out TC  [°C]"]            ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T out avg [°C]"     , visible=True ,opacity = 1,line=dict(color="red"           , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Delta T NORM [°C]"]         ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Delta T NORM [°C]"  , visible=True ,opacity = 1,line=dict(color="darkorange"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["FLDHW [kg/min]"]            ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "FLDHW [kg/min]"     , visible=True ,opacity = 1,line=dict(color="darkgreen"     , width=1.5, dash="solid"),secondary_y = False),
            # SEEB series - first axes Y
            # dict(x=df[header_time],y=df["T°in DHW [°C]"]             ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T in DHW [°C]"            , visible=False ,opacity = 1,line=dict(color="cyan"         , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC  [°C]"]            ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T out avg [°C]"           , visible=False ,opacity = 1,line=dict(color="red"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°Fume [°C]"]               ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T fume MP[°C]"            , visible='legendonly' ,opacity = 1,line=dict(color="gray"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°Amb [°C]"]                ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T°Amb [°C]"               , visible='legendonly' ,opacity = 1,line=dict(color="pink"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Cumul. QDHW  [kWh]"]        ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "Cum ener [kWh]"           , visible='legendonly' ,opacity = 1,line=dict(color="yellow"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["pin DHW [bar]"]             ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "P in [bar]"               , visible='legendonly' ,opacity = 1,line=dict(color="maroon"       , width=1.5, dash="solid"),secondary_y = False),
            # SEEB series - second axes Y
            dict(x=df[header_time],y=df["Cumul. Gaz Vol. Corr.[L]"]  ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "Total Gas consumed [L]"   , visible='legendonly' ,opacity = 1,line=dict(color="orange"       , width=1.5, dash="solid"),secondary_y = True),
            dict(x=df[header_time],y=df["Power Absorbed [W]"]        ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "Power consum. [Watt]"     , visible='legendonly' ,opacity = 1,line=dict(color="tomato"       , width=1.5, dash="solid"),secondary_y = True),
            # SEEB paramter serie 
            dict(x=df[header_time],y=df["T = 30 [°C]"]               ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T = 30 [°C]"              , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T = 45 [°C]"]               ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T = 45 [°C]"              , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T = 55 [°C]"]               ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T = 55 [°C]"              , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
            
            ]
        self.trace_param.extend(trace_param)
        print(f"PLOT - Adding SEEB trace to the dictonary : {time() - self.stime:.2f} sec")
        logging.info(f"PLOT - Adding SEEB trace to the dictonary : {time() - self.stime:.2f} sec")

    def add_trace_microcom(self,df:DataFrame,header_time:str):
        '''This function compile all the data to creat a collection of trace for Microcom'''
        self.stime = time()
        trace_param = [
            # REPORT series
            dict(x=df[header_time],y=df["Supply [°C]"]               ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T sup [°C]"         , visible=True ,opacity = 1,line=dict(color="darksalmon"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["DHW stor (°C)"]             ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T DHW [°C]"         , visible=True ,opacity = 1,line=dict(color="mediumblue"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Flame Curent [uA]"]         ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Flame curr [µA]"    , visible=True ,opacity = 1,line=dict(color="peru"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Actual measured load"]      ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Burner mod[%]"      , visible=True ,opacity = 1,line=dict(color="violet"        , width=1.5, dash="solid"),secondary_y = False),
            # microcom series - first axes Y
            dict(x=df[header_time],y=df["Return [°C]"]               ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "T ret [°C]"         , visible='legendonly' ,opacity = 1,line=dict(color="deeppink"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Flue temp [0,01°C]"]        ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "T fume MC[°C]"      , visible='legendonly' ,opacity = 1,line=dict(color="darkblue"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Delta T boiler [°C]"]       ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "Delta T boiler [°C]", visible='legendonly' ,opacity = 1,line=dict(color="olivedrab"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Pump PWM %(111F)"]          ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "Pump mod. [%]"      , visible='legendonly' ,opacity = 1,line=dict(color="mediumslateblue"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Pump Power W(65F2)"]        ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "Pump power [Watt]"  , visible='legendonly' ,opacity = 1,line=dict(color="mediumspringgreen"       , width=1.5, dash="solid"),secondary_y = False),
            #dict(x=df[header_time],y=df["Burner State"]              ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "Burner status"      , visible=False ,opacity = 1,line=dict(color="tomato"       , width=1.5, dash="solid"),secondary_y = False),
            # microcom serie for parameter line
            dict(x=df[header_time],y=df["T BURN ON [°C]"]            ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "T BURN ON [°C]"     , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark')       , width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T BURN OFF [°C]"]           ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "T BURN OFF [°C]"    , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark')       , width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T CH STP [°C]"]             ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "T CH STP [°C]"      , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark')       , width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T DHW Setpoint [°C]"]       ,legendgroup = "Microcom",legendgrouptitle_text = "Microcom" ,name = "T DHW Setpoint [°C]", visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark')       , width=0.25, dash="dash"),secondary_y = False),
           ]

        self.trace_param.extend(trace_param)
        print(f"PLOT - Adding microcom trace to the dictonary : {time() - self.stime:.2f} sec")
        logging.info(f"PLOT - Adding microcom trace to the dictonary : {time() - self.stime:.2f} sec")

    def color_randomized(self, collection:str='all')->str:
        '''
        This function allow to randomly select a color

        Parameter
        ---------
        collection : str defautl value = 'all' 
            all|dark|ligth|red|blue|gray
        '''
        all = ["aliceblue"," antiquewhite"," aqua"," aquamarine"," azure",
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
        dark = [x for x in all if 'dark' in x]
        light = [x for x in all if 'light' in x]
        classic = [" black"," blue"," red"," yellow"," green"," brown", "orange", "turquoise"]
        red = [x for x in all if 'red' in x].extend([" firebrick"," salmon"," tomato"," darksalmon","maroon","brown","coral"])
        blue = [x for x in all if 'blue' in x].extend([" turquoise"," teal"," paleturquoise"," mediumturquoise","cyan","darkcyan","aqua"])
        green = [x for x in all if 'green' in x].extend(["chartreuse","lime","olive","olivedrab"])


        if collection =='all':
            colorCollection=all
        elif collection =='dark': 
            colorCollection=dark
        elif collection =='classic': 
            colorCollection=classic
        elif collection =='light': 
            colorCollection=light
        elif collection =='blue': 
            colorCollection=blue
        elif collection =='red': 
            colorCollection=red
        elif collection =='green': 
            colorCollection=green
        else:
            colorCollection=all

        return rd.choice(colorCollection)


# %% run main function 
if __name__ == "__main__":
    i=0
    init = time()
    s_mc = "C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\HM\\85kW\\25021W\\25021W_XXL_HM85TC_Algo16_Microcom.csv"
    s_sb = "C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\HM\\85kW\\25021W\\25021W_XXL_HM85TC_Algo16_Seeb_Enr5 - Copy.csv"
    seeb=InputFile(Path_File=[s_sb], header_time='Timestamp')  #header_time='Timestamp'
    mc=InputFile(Path_File=[s_mc], header_time='Time DMY')  #header_time='Time DMY'
    plotingfile=GeneratePlot(plot_name="first attempt")

    print(f"Time to file : {(time()-init):.2f} s")
    init=time()

    plotingfile.creat_figure()
    print(f"Time to update layout: {(time()-init):.2f} s")
    init=time()
    #plotingfile.add_trace_all_columns(Microplan.down_sample_dataframe(Microplan.file_info[0]['data']))
    plotingfile.add_trace_microplan(seeb.down_sample_dataframe(value_to_filter=10),seeb.file_info[0]['header_time'])
    plotingfile.add_trace_microcom(mc.down_sample_dataframe(value_to_filter=3),mc.file_info[0]['header_time'])
    plotingfile.add_filtered_trace()
    print(f"Time to add trace: {(time()-init):.2f} s")
    init=time()
    plotingfile.show_html_figure()

    print(f"Time to show plot : {(time()-init):.2f} s")
    init=time()
