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
import matplotlib.colors as mcolors

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
        self.colorDatabase()# allow us to initialize de db color, so if we compare file we can update de basic colors to darker rev
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
            hovermode="x",  # "x" lables appear with each colour. "x unified" one unique box that groups all the lable
            margin=dict(l=60, r=120, t=50, b=50), 
            updatemenus=[dict(
                                type="buttons",
                                direction="right",
                                buttons=list([
                                    dict(label="Hover: x",
                                        method="relayout",
                                        args=[{"hovermode": "x"}]),
                                    dict(label="Hover: x unified",
                                        method="relayout",
                                        args=[{"hovermode": "x unified"}]),
                                    dict(label="Hover: Closest",
                                        method="relayout",
                                        args=[{"hovermode": "closest"}]),
                                    # dict(label="Hover: y unified",
                                    #     method="relayout",
                                    #     args=[{"hovermode": "y unified"}]),
                                ]),
                                x=1,
                                y=1.1,
                            )
                        ],

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

    def add_filtered_trace(self,fig:go.Figure, Text2Identify:str=''):
        '''
        This function add trace for each item in trace_param.

        Parameter
        -------------
        Text2Identify:str = ''
            this parameter is use to add a specifique text in front of the legend groups and names of the serie, 
            it is used when we are comparing files from a same test in order to différenciate them
        '''
        self.stime = time()
        for t in self.trace_param :
                fig.add_trace(
                    go.Scatter(
                    x                       = t['x'],
                    y                       = t['y'],
                    legendgroup             = Text2Identify + t['legendgroup'],
                    legendgrouptitle_text   = Text2Identify + t['legendgrouptitle_text'],
                    name                    = Text2Identify + t['name'], 
                    visible                 = t['visible'], 
                    opacity                 = t['opacity'], 
                    line                    = t['line'], 
                    ),
                    secondary_y             = t['secondary_y'], )
        print(f"PLOT - Adding trace from dictionary : {time() - self.stime:.2f} sec")
        logging.info(f"PLOT - Adding trace from dictionary : {time() - self.stime:.2f} sec")

    def add_trace_microplan(self,df:DataFrame,header_time:str,groupName:str=''):
        '''This function compile all the data to creat a collection of trace for Microplan'''
        if groupName !='':
            groupName=groupName + '_'
        report_name = f"{groupName}Report"
        microplan_name = f"{groupName}MicroPlan"

        self.stime = time()
        trace_param = [
            # REPORT series
            dict(x=df[header_time],y=df["T°in DHW [°C]"]             ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "T in DHW [°C]"                  , visible=True ,opacity = 1,line=dict(color=self.colorDB["T in DHW [°C]"]              , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°out AV.  [°C]"]           ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "T out avg [°C]"                 , visible=True ,opacity = 1,line=dict(color=self.colorDB["T out avg [°C]"]             , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Delta T NORM [°C]"]         ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "Delta T NORM [°C]"              , visible=True ,opacity = 1,line=dict(color=self.colorDB["Delta T NORM [°C]"]          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["FLDHW [kg/min]"]            ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "FLDHW [kg/min]"                 , visible=True ,opacity = 1,line=dict(color=self.colorDB["FLDHW [kg/min]"]             , width=1.5, dash="solid"),secondary_y = False),
            # microplan series - first axes Y
            # dict(x=df[header_time],y=df["T°in DHW [°C]"]             ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T in DHW [°C]"            , visible=False ,opacity = 1,line=dict(color="cyan"         , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC  [°C]"]            ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T out avg [°C]"           , visible=False ,opacity = 1,line=dict(color="red"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°Fume [°C]"]               ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T fume MP[°C]"            , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["T fume MP[°C]"]      , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°Amb [°C]"]                ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T Amb [°C]"               , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["T Amb [°C]"]         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Cumul. QDHW  [kWh]"]        ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "Cum ener [kWh]"           , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["Cum ener [kWh]"]     , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["pin DHW [bar]"]             ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "P in [bar]"               , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["P in [bar]"]         , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out PT100  [°C]"]         ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T PT100  [°C]"            , visible=False ,opacity = 1,line=dict(color="peachpuff"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC1  [°C]"]           ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T TC1  [°C]"              , visible=False ,opacity = 1,line=dict(color="rosybrown"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC2  [°C]"]           ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T TC2  [°C]"              , visible=False ,opacity = 1,line=dict(color="peru"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC3  [°C]"]           ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T TC3  [°C]"              , visible=False ,opacity = 1,line=dict(color="papayawhip"       , width=1.5, dash="solid"),secondary_y = False)
            # Microplan series - second axes Y
            dict(x=df[header_time],y=df["Cumul. Gaz Vol. Corr.[L]"]  ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "Total Gas consumed [L]"   , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["Total Gas consumed [L]"], width=1.5, dash="solid"),secondary_y = True),
            dict(x=df[header_time],y=df["Power Absorbed [W]"]        ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "Pow consumption [W]"      , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["Pow consumption [W]"] , width=1.5, dash="solid"),secondary_y = True),
            ]
            # Microplan parameter serie 
        if microplan_name == 'MicroPlan' :
            trace_param.extend([
                dict(x=df[header_time],y=df["T = 30 [°C]"]               ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T = 30 [°C]"          , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
                dict(x=df[header_time],y=df["T = 45 [°C]"]               ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T = 45 [°C]"          , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
                dict(x=df[header_time],y=df["T = 55 [°C]"]               ,legendgroup = microplan_name,legendgrouptitle_text = microplan_name ,name = "T = 55 [°C]"          , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
                ])
        self.trace_param.extend(trace_param)
        print(f"PLOT - Adding microplan trace to the dictonary")
        logging.info(f"PLOT - Adding microplan trace to the dictonary")

    def add_trace_seeb(self,df:DataFrame,header_time:str,groupName:str=''):
        '''This function compile all the data to creat a collection of trace for Seeb'''
        if groupName !='':
            groupName=groupName + '_'
        report_name = f"{groupName}Report"
        SEEB_name = f"{groupName}SEEB"

        self.stime = time()
        trace_param = [
            # REPORT series
            dict(x=df[header_time],y=df["T°in DHW [°C]"]             ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "T in DHW [°C]"      , visible=True ,opacity = 1,line=dict(color=self.colorDB["T in DHW [°C]"]          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°out TC  [°C]"]            ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "T out avg [°C]"     , visible=True ,opacity = 1,line=dict(color=self.colorDB["T out avg [°C]"]           , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Delta T NORM [°C]"]         ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "Delta T NORM [°C]"  , visible=True ,opacity = 1,line=dict(color=self.colorDB["Delta T NORM [°C]"]    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["FLDHW [kg/min]"]            ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "FLDHW [kg/min]"     , visible=True ,opacity = 1,line=dict(color=self.colorDB["FLDHW [kg/min]"]     , width=1.5, dash="solid"),secondary_y = False),
            # SEEB series - first axes Y
            # dict(x=df[header_time],y=df["T°in DHW [°C]"]             ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "T in DHW [°C]"            , visible=False ,opacity = 1,line=dict(color="cyan"         , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[header_time],y=df["T°out TC  [°C]"]            ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "T out avg [°C]"           , visible=False ,opacity = 1,line=dict(color="red"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°Fume [°C]"]               ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "T fume MP[°C]"            , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["T fume MP[°C]"]         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["T°Amb [°C]"]                ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "T°Amb [°C]"               , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["T Amb [°C]"]         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Cumul. QDHW  [kWh]"]        ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "Cum ener [kWh]"           , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["Cum ener [kWh]"]       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["pin DHW [bar]"]             ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "P in [bar]"               , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["P in [bar]"]       , width=1.5, dash="solid"),secondary_y = False),
            # SEEB series - second axes Y
            dict(x=df[header_time],y=df["Cumul. Gaz Vol. Corr.[L]"]  ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "Total Gas consumed [L]"   , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["Total Gas consumed [L]"]       , width=1.5, dash="solid"),secondary_y = True),
            dict(x=df[header_time],y=df["Power Absorbed [W]"]        ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "Power consum. [Watt]"     , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["Pow consumption [W]"]       , width=1.5, dash="solid"),secondary_y = True),
            # SEEB paramter serie 
            ]
            # Microplan parameter serie 
        if SEEB_name == 'SEEB' :
            trace_param.extend([
                dict(x=df[header_time],y=df["T = 30 [°C]"]               ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "T = 30 [°C]"              , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
                dict(x=df[header_time],y=df["T = 45 [°C]"]               ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "T = 45 [°C]"              , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
                dict(x=df[header_time],y=df["T = 55 [°C]"]               ,legendgroup = SEEB_name,legendgrouptitle_text = SEEB_name ,name = "T = 55 [°C]"              , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark'), width=0.25, dash="dash"),secondary_y = False),
            ])
        
        self.trace_param.extend(trace_param)
        print(f"PLOT - Adding SEEB trace to the dictonary")
        logging.info(f"PLOT - Adding SEEB trace to the dictonary")

    def add_trace_microcom(self,df:DataFrame,header_time:str,groupName:str=''):
        '''This function compile all the data to creat a collection of trace for Microcom'''

        if groupName !='':
            groupName=groupName + '_'
        report_name = f"{groupName}Report"
        Microcom_name = f"{groupName}Microcom"


        self.stime = time()
        trace_param = [
            # REPORT series
            dict(x=df[header_time],y=df["Supply [°C]"]               ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "T sup [°C]"         , visible=True ,opacity = 1,line=dict(color=self.colorDB["T sup [°C]"]    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["DHW stor (°C)"]             ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "T DHW [°C]"         , visible=True ,opacity = 1,line=dict(color=self.colorDB["T DHW [°C]"]    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Flame Curent [uA]"]         ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "Flame curr [µA]"    , visible=True ,opacity = 1,line=dict(color=self.colorDB["Flame curr [µA]"]          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Actual measured load"]      ,legendgroup = report_name,legendgrouptitle_text = report_name ,name = "Burner mod[%]"      , visible=True ,opacity = 1,line=dict(color=self.colorDB["Burner mod[%]"]        , width=1.5, dash="solid"),secondary_y = False),
            # microcom series - first axes Y
            dict(x=df[header_time],y=df["Return [°C]"]               ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "T ret [°C]"         , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["T ret [°C]"]         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Flue temp [0,01°C]"]        ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "T fume MC[°C]"      , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["T fume MC[°C]"]          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Delta T boiler [°C]"]       ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "Delta T boiler [°C]", visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["Delta T boiler [°C]"]         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Pump PWM %(111F)"]          ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "Pump mod. [%]"      , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["Pump mod. [%]"]         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[header_time],y=df["Pump Power W(65F2)"]        ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "Pump power [Watt]"  , visible='legendonly' ,opacity = 1,line=dict(color=self.colorDB["Pump power [Watt]"]       , width=1.5, dash="solid"),secondary_y = False),
            #dict(x=df[header_time],y=df["Burner State"]              ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "Burner status"      , visible=False ,opacity = 1,line=dict(color="tomato"       , width=1.5, dash="solid"),secondary_y = False),
            ]
            # microcom serie for parameter line
        if Microcom_name == 'Microcom' :
            trace_param.extend([
            dict(x=df[header_time],y=df["T BURN ON [°C]"]            ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "T BURN ON [°C]"     , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark')       , width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T BURN OFF [°C]"]           ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "T BURN OFF [°C]"    , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark')       , width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T CH STP [°C]"]             ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "T CH STP [°C]"      , visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark')       , width=0.25, dash="dash"),secondary_y = False),
            dict(x=df[header_time],y=df["T DHW Setpoint [°C]"]       ,legendgroup = Microcom_name,legendgrouptitle_text = Microcom_name ,name = "T DHW Setpoint [°C]", visible=True ,opacity = 1,line=dict(color=self.color_randomized('dark')       , width=0.25, dash="dash"),secondary_y = False),
           ])

        self.trace_param.extend(trace_param)
        print(f"PLOT - Adding microcom trace to the dictonary")
        logging.info(f"PLOT - Adding microcom trace to the dictonary")

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

    def colorDatabase(self):
        self.colorDB={
            "T in DHW [°C]":"cyan",
            "T out avg [°C]":"red",
            "Delta T NORM [°C]":"orangered",
            "FLDHW [kg/min]":"burlywood",
            "T fume MP[°C]":"gray",
            "T Amb [°C]":"pink",
            "Cum ener [kWh]":"yellow",
            "P in [bar]":"maroon",
            "Total Gas consumed [L]":"orange",
            "Pow consumption [W]":"tomato",
            "T sup [°C]":"salmon",
            "T DHW [°C]":"mediumblue",
            "Flame curr [µA]":"peru",
            "Burner mod[%]":"violet",
            "T ret [°C]":"deeppink",
            "T fume MC[°C]":"moccasin",
            "Delta T boiler [°C]":"olivedrab",
            "Pump mod. [%]":"mediumslateblue",
            "Pump power [Watt]":"mediumspringgreen"
        }
        for k,color in self.colorDB.items():
            self.colorDB[k]=mcolors.to_hex(mcolors.to_rgb(color))
        
    def darken_named_color(self, factor=0.7):
        """Darken a named color by converting to RGB, scaling, and returning HEX."""
        for k,hexColor in self.colorDB.items():
            rgb = mcolors.to_rgb(hexColor)
            self.colorDB[k]= mcolors.to_hex(tuple(max(0, min(1, c * factor)) for c in rgb))


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
