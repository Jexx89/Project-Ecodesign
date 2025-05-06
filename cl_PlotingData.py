# Plotly import
from plotly import graph_objects as go  # importing plotly for plotting figures
# from plotly.offline import plot
from plotly.subplots import make_subplots  # importing subplots to plot several curves in the same graph

# FileAndInput  import
#from cl_FileAndInput import *
# FileAndInput  import
import random as rd

class ErrorPloting(Exception):
    pass

class GeneratePlot():
    def __init__(self, header_time:str='Timestamp', file_path='C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\Template.html',plot_name='Template'):
        self.header_time = header_time
        self.file_path = file_path
        self.plot_name = plot_name
        self.trace_param = []
        self.lab_x_ax = "Test time [s]"
        self.lab_prim_y_ax_ = "Temperature [°C]/Pressure[bar]/flow[l or kg -/m]"
        self.lab_sec_y_ax_ = "Gas Vol (L.)/Power[watt]"
        self.creat_fig()

    def add_trace_all_columns(self, df):
        liste_unwanted_col = ["Time [h]","Time DMY","Time (h)","Time (dd hh:mm:ss)","Timestamp"]
        for d in df:
            if d not in liste_unwanted_col: #d != self.header_time and 
                self.trace_param.append(dict(
                    x=df[self.header_time] ,
                    y=df[d],
                    legendgroup ="MAIN",
                    legendgrouptitle_text = "MAIN",
                    name = d, 
                    visible=True ,
                    opacity = 1,
                    line=
                        dict(
                            color=self.color_randomized(),
                            width=1.5,
                            dash="solid"
                            ),
                    secondary_y = False))

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
        self.txt_size_num_ax = 20
        self.txt_siz_lbl_xy = 20
        self.txt_siz_leg = 14
        self.txt_siz_tit = 16
        self.fig :go.Figure
        self.fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Editing the layout
        self.fig.update_layout(
            template="simple_white",
            hovermode="x",
            yaxis=dict(tickfont=dict(size=self.txt_size_num_ax)),
            xaxis=dict(tickfont=dict(size=self.txt_size_num_ax)),
            legend=dict(font=dict(size=self.txt_siz_leg),groupclick="toggleitem"),
            title=self.plot_name,
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
    
    def creat_html_file(self):
        self.fig.add_traces(self.trace_param)
        self.fig.show()
        # or 
        # plot(self.fig,filename="C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\test" + ".html")
    
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

    def add_trace_microplan(self,df):
        trace_param = [
            # REPORT series
            dict(x=df[self.header_time],y=df["T°in DHW [°C]"]             ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T in DHW [°C]"      , visible=True ,opacity = 1,line=dict(color="cyan"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°out AV.  [°C]"]           ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T out avg [°C]"     , visible=True ,opacity = 1,line=dict(color="red"           , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Delta T NORM [°C]"]         ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Delta T NORM [°C]"  , visible=True ,opacity = 1,line=dict(color="darkorange"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["FLDHW [kg/min]"]            ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "FLDHW [kg/min]"     , visible=True ,opacity = 1,line=dict(color="darkgreen"     , width=1.5, dash="solid"),secondary_y = False),
            # microplan series - first axes Y
            # dict(x=df[self.header_time],y=df["T°in DHW [°C]"]             ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T in DHW [°C]"            , visible=False ,opacity = 1,line=dict(color="cyan"         , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[self.header_time],y=df["T°out TC  [°C]"]            ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T out avg [°C]"           , visible=False ,opacity = 1,line=dict(color="red"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°Fume [°C]"]               ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T fume MP[°C]"            , visible=False ,opacity = 1,line=dict(color="gray"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°Amb [°C]"]                ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T Amb [°C]"               , visible=False ,opacity = 1,line=dict(color="pink"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Cumul. QDHW  [kWh]"]        ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Cum ener [kWh]"           , visible=False ,opacity = 1,line=dict(color="yellow"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["pin DHW [bar]"]             ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "P in [bar]"               , visible=False ,opacity = 1,line=dict(color="maroon"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[self.header_time],y=df["T°out PT100  [°C]"]         ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T PT100  [°C]"            , visible=False ,opacity = 1,line=dict(color="peachpuff"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[self.header_time],y=df["T°out TC1  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC1  [°C]"              , visible=False ,opacity = 1,line=dict(color="rosybrown"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[self.header_time],y=df["T°out TC2  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC2  [°C]"              , visible=False ,opacity = 1,line=dict(color="peru"       , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[self.header_time],y=df["T°out TC3  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC3  [°C]"              , visible=False ,opacity = 1,line=dict(color="papayawhip"       , width=1.5, dash="solid"),secondary_y = False)
            # Microplan series - second axes Y
            dict(x=df[self.header_time],y=df["Cumul. Gaz Vol. Corr.[L]"]  ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Total Gas consumed [L]"   , visible=False ,opacity = 1,line=dict(color="orange"       , width=1.5, dash="solid"),secondary_y = True),
            dict(x=df[self.header_time],y=df["Power Absorbed [W]"]        ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Pow consumption [W]"      , visible=False ,opacity = 1,line=dict(color="tomato"       , width=1.5, dash="solid"),secondary_y = True),
            ]
        self.trace_param.append(trace_param)

    def add_trace_seeb(self,df):
        trace_param = [
            # REPORT series
            dict(x=df[self.header_time],y=df["T°in DHW [°C]"]             ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T in DHW [°C]"      , visible=True ,opacity = 1,line=dict(color="cyan"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°out TC  [°C]"]            ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T out avg [°C]"     , visible=True ,opacity = 1,line=dict(color="red"           , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Delta T NORM [°C]"]         ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Delta T NORM [°C]"  , visible=True ,opacity = 1,line=dict(color="darkorange"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["FLDHW [kg/min]"]            ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "FLDHW [kg/min]"     , visible=True ,opacity = 1,line=dict(color="darkgreen"     , width=1.5, dash="solid"),secondary_y = False),
            # SEEB series - first axes Y
            # dict(x=df[self.header_time],y=df["T°in DHW [°C]"]             ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T in DHW [°C]"            , visible=False ,opacity = 1,line=dict(color="cyan"         , width=1.5, dash="solid"),secondary_y = False),
            # dict(x=df[self.header_time],y=df["T°out TC  [°C]"]            ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T out avg [°C]"           , visible=False ,opacity = 1,line=dict(color="red"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°Fume [°C]"]               ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T fume MP[°C]"            , visible=False ,opacity = 1,line=dict(color="gray"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°Amb [°C]"]                ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "T°Amb [°C]"               , visible=False ,opacity = 1,line=dict(color="pink"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Cumul. QDHW  [kWh]"]        ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "Cum ener [kWh]"           , visible=False ,opacity = 1,line=dict(color="yellow"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["pin DHW [bar]"]             ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "P in [bar]"               , visible=False ,opacity = 1,line=dict(color="maroon"       , width=1.5, dash="solid"),secondary_y = False),
            # SEEB series - second axes Y
            dict(x=df[self.header_time],y=df["Cumul. Gaz Vol. Corr.[L]"]  ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "Total Gas consumed [L]"   , visible=False ,opacity = 1,line=dict(color="orange"       , width=1.5, dash="solid"),secondary_y = True),
            dict(x=df[self.header_time],y=df["Power Absorbed [W]"]        ,legendgroup = "SEEB",legendgrouptitle_text = "SEEB" ,name = "Pow consumption [W]"      , visible=False ,opacity = 1,line=dict(color="tomato"       , width=1.5, dash="solid"),secondary_y = True),
            ]
        self.trace_param.append(trace_param)

    def add_trace_microcom(self, df):
        trace_param = [
            # REPORT series
            dict(x=df[self.header_time],y=df["Supply [°C]"]               ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T sup [°C]"         , visible=True ,opacity = 1,line=dict(color="darksalmon"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["DHW stor (°C)"]             ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "T DHW [°C]"         , visible=True ,opacity = 1,line=dict(color="mediumblue"    , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Actual measured load"]      ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Flame curr [micr A]", visible=True ,opacity = 1,line=dict(color="peru"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Flame Curent [uA]"]         ,legendgroup = "Report",legendgrouptitle_text = "Report" ,name = "Burner mod[%]"      , visible=True ,opacity = 1,line=dict(color="violet"        , width=1.5, dash="solid"),secondary_y = False),
            # microcom series - first axes Y
            dict(x=df[self.header_time],y=df["T return [°C]"]             ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T in DHW [°C]"            , visible=False ,opacity = 1,line=dict(color="cyan"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T fume MC[°C]"]            ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T out avg [°C]"           , visible=False ,opacity = 1,line=dict(color="red"          , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Delta T boiler [°C]"]               ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T fume MP[°C]"            , visible=False ,opacity = 1,line=dict(color="gray"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Pump modulation [%]"]                ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T Amb [°C]"               , visible=False ,opacity = 1,line=dict(color="pink"         , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Pump power consumed [W]"]        ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "Cum ener [kWh]"           , visible=False ,opacity = 1,line=dict(color="yellow"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["Burner status"]             ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "P in [bar]"               , visible=False ,opacity = 1,line=dict(color="maroon"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°out PT100  [°C]"]         ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T PT100  [°C]"            , visible=False ,opacity = 1,line=dict(color="peachpuff"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°out TC1  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC1  [°C]"              , visible=False ,opacity = 1,line=dict(color="rosybrown"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°out TC2  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC2  [°C]"              , visible=False ,opacity = 1,line=dict(color="peru"       , width=1.5, dash="solid"),secondary_y = False),
            dict(x=df[self.header_time],y=df["T°out TC3  [°C]"]           ,legendgroup = "Microplan",legendgrouptitle_text = "Microplan" ,name = "T TC3  [°C]"              , visible=False ,opacity = 1,line=dict(color="papayawhip"       , width=1.5, dash="solid"),secondary_y = False),
           ]
        self.trace_param.append(trace_param)


# %% run main function 
if __name__ == "__main__":
    i=0
    #file=InputFile()
    #GP=GeneratePlot(file.df,"first attempte","Timestamp")
    #GP.add_all_columns()
    # Traitement = EcoDesign(Test_request="25066",Test_Num="A",Appliance_power="70")