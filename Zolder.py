
#%% plc schneider analysis
from PlotingData import *
from FileManager import *
folder = InputFolder(Path_Folder='C:\ACV\Coding Library\Python\Project-Ecodesign\Schneider\client zolder').files_in_folder
files_to_plot={}
for x in folder:
    files_to_plot[x['FileName']] = ConfigFile(
                                        name=x['FileName'], 
                                        path=x['Path'],
                                        header_time='DATE-TIME',
                                        delimiter=';',
                                        row_to_ignore=3,
                                        FileType=x['FileType'],
                                        )
files = InputFile(files_to_plot)
plt = GeneratePlot('DATE-TIME','Test Client Zolder')
plt.creat_figure('Values [°C][%][µA]','Values [bar][volt]')

list_of_df = [file.data for k, file in files.FileData.items()]
combined_df = concat(list_of_df, ignore_index=True)
plt.add_trace_schneider_plc_zolder(combined_df,'DATE-TIME')
plt.add_filtered_trace(plt.fig)

plt.show_html_figure()
