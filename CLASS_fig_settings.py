# -*- coding: utf-8 -*-
"""Created on Mon Jan 04 14:18:56 2024

@author: Marcello Nitti
"""

import os

import numpy as np # importing numpy library
import pandas as pd # importing pandas dataframe
import datetime

import plotly.graph_objects as go # importing plotly for plotting figures
from plotly.offline import plot
from plotly.subplots import make_subplots # importing subplots to plot several curves in the same graph

#%% CLASS


class fig_set:

    # def __init__(self, fig):

    #     self.fig = fig # figure setting

    def trace_fig(self,x_axis,y_axis,name,col,secd_y_ax,opac,typ_line):

        """
        Function to add the trace on the graphs

        Parameters
        -----------------

        x: array
            Array with values to be plotted on the x axis
        y: array
            Array with values to be plotted on the y axis
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

        The trace that can be added to the main figure plot

        """

        # Adding the trace
        self.fig.add_trace(go.Scatter
                    (x = x_axis,
                    y = y_axis,
                    name = name,
                    opacity = opac,
                    #    mode = typ_line,
                    #    marker = {"color" : col}),
                    line = dict(color=col, width=1.5, dash=typ_line)),
                    secondary_y=secd_y_ax,
                    )
    

    def update_lay_fig(
            self,
            lab_x_ax,
            lab_prim_y_ax_,
            lab_sec_y_ax_,
            txt_size_num_ax,
            txt_siz_lbl_xy,
            txt_siz_leg,
            title,
            txt_siz_tit):

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

        # Editing the layout
        self.fig.update_layout(template="simple_white")
        
        self.fig.update_xaxes(
            title=lab_x_ax,
            title_font={"size": txt_siz_lbl_xy}
            )
        
        self.fig.update_yaxes(
            title=lab_prim_y_ax_,
            title_font={"size": txt_siz_lbl_xy},
            secondary_y=False
            )  # ,type = "log"
        
        self.fig.update_yaxes(
            title=lab_sec_y_ax_,
            title_font={"size": txt_siz_lbl_xy},
            # range=[0, 9000],
            secondary_y=True,
            )  # ,type = "log"
        
        self.fig.update_xaxes(spikemode="toaxis+across") # "toaxis" (will stop at the height of the mouse) / "across" goes for the whole lenght
        self.fig.update_xaxes(spikesnap="hovered data")
        self.fig.update_layout(hovermode="x") # "x" lables appear with each colour. "x unified" one unique box that groups all the lable
        
        # fig.update_xaxes(range=[0, 3000])
        # fig.update_layout(xaxis_range=['2023-11-30','2023-12-03'])

        # fig.update_layout(xaxis_range=[datetime.datetime(2023, 12, 1),
        #                                datetime.datetime(2023, 12, 4)])

        # fig.update_xaxes(rangeslider_visible=True) # This add on the bottom the whole graph where you can see at what point are you if you zoom in
        
        self.fig.update_layout(yaxis=dict(tickfont=dict(size=txt_size_num_ax)))
        # fig.update_layout(yaxis={'visible': True, 'showticklabels': False})
        self.fig.update_layout(xaxis=dict(tickfont=dict(size=txt_size_num_ax)))
        self.fig.update_layout(legend=dict(font=dict(size=txt_siz_leg)))
        # fig.update_layout(
            # legend=dict(
                # orientation="h",
                # yanchor="top",
                # y=1.065,
                # xanchor="left",
                # x=0.01)
                # )

        self.fig.update_layout(
            title=title,
            font_size=txt_siz_tit,
            # showlegend=False,
            )