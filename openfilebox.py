import tkinter
from tkinter import filedialog,Tk
import os

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

currdir = os.getcwd()


# def Get_File_path(currdir,Type:list[tuple[str,str]])->str:
#     root = Tk()
#     root.withdraw() #use to hide tkinter window
#     print("Getting the file to process...")
#     Type.append(("All Files", "*.*"))
#     print(Type)
#     filez = filedialog.askopenfilenames(
#         parent=root, initialdir=currdir, 
#         title='Please select one files',
#         filetypes=Type)
#     if len(filez) > 0:
#         print(f"You chose {filez[0]}")
    
#     return filez[0]#take first file selected



# tempdir = Get_File_path(currdir,[("csv files",".csv")])
# if len(tempdir) > 0:
#     print(f"You chose {tempdir[0]}")
#     print(f"You chose {currdir}{os.sep}HM")


# test=[('CSV file','.csv')]
# print(test[0])
# a,b = test[0]
# print(a)
# print(b)


s = 'frist'
l=['1','2','3','4','5','6']

m=s.join(map(str,l))

print(m,sep='\n')

g=50
yaxis = "y" if g> 49 else"y2"

print(yaxis)