
#%% plc schneider analysis
'''
This script is used to post processing the data from a PLC scnheider, concatening all the data togheter and print out a plot

'''
from PlotingData import *
from FileManager import *
#listing all the files in the folder
Path='C:\\ACV\\Coding Library\\Python\\Project-Ecodesign\\Schneider\\20250610_rapid test'
folder = InputFolder(Path_Folder=Path).files_in_folder
files_to_plot={}
#creating the ConfigFile dictionary
for x in folder:
    files_to_plot[x['FileName']] = ConfigFile(
                                        name=x['FileName'], 
                                        path=x['Path'],
                                        header_time='DATE-TIME',
                                        delimiter=';',
                                        row_to_ignore=3,
                                        FileType=x['FileType'],
                                        )
#import the data from all the files
files = InputFile(files_to_plot)
#combine all the dataframe's
files.get_df_from_file()
files.transfrom_data()
list_of_df = [file.data for k, file in files.FileData.items()]

combined_df = concat(list_of_df, ignore_index=True)
#sort the data to be sure that they are in the right order
combined_df.sort_values('DATE-TIME')

#generate plot with the data combined
plt = GeneratePlot('DATE-TIME','Test Client Zolder')
plt.creat_figure('Values [°C][%][µA]','Values [bar][volt]')
plt.add_trace_schneider_plc_zolder(combined_df,'DATE-TIME')
plt.add_filtered_trace(plt.fig)

plt.creat_html_figure(Path+'\\2025-06-12_Zoler acquisition.html')
