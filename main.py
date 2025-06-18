'''
---command to activate the virtual environement---
source .venv/Scripts/activate

---command to generate a .exe file---
pyinstaller --onefile main.py --name EcoDesign_processing -i "C:/ACV/Coding Library/Python/Project-Ecodesign/Media/plot.ico"

'''
from EcoDesign import *


print("-"*50)
print("-"*50)
print("\nWelcome to the *** post-processing device ***\n")
print("-"*50)
print("-"*50)
print("\nHello my beautifull people This tools is to post process the files that comes with the EcoDesign project.")
print("This tools is used to post process the files that comes with the EcoDesign project.")
print("I only need a folder in which I can found all the data (microplan, SEEB, and microCom).")
print("Note : only the excel files are needed from the macro design in Excel")
print("\nThis script is provided by my freind Marcello and myself(JS) \n")
print("-"*50)

print("First choice is the kind of file you need ?")
print("\t1. Single file to post process ")
print("\t2. Need to compare 2 or more files")
print("\t3. Need to check and compare all the days from one test")
print("\tQ : Run for your lives (O_O;)!!! and quit the application !")
result = input("Your choice is : ").upper()

if result=='1':
    Traitement = EcoDesign()
    Traitement.plot_initiate_figure()
    Traitement.plot_files_eco_design()
    Traitement.plot_generate_html()
elif result=='2':
    print("Okay, okay you want to make me work don't you... so, how many file do you need to compare?[max 3] ")
    count = input("Your choice is : ").upper()
    print("Thanks!, I will now post procee each test in a sequence, I will need information's for each new test to add, ")
    print("SOOOOOOOO, please stay next to your computer please (☞ﾟヮﾟ)☞")
    nCount = int(count)
    global_config={}
    try:
        for x in range(nCount):
            test_config = ConfigTest()
            global_config[f"TestNum{x}"] = test_config
        Traitement = EcoDesign(global_config)
        Traitement.plot_initiate_figure()
        Traitement.plot_files_eco_design()
        Traitement.plot_generate_html()
    except Exception as e:
        print(f"Ouuuuups, I had an error describe as bellow : \n {e}")  
        input("Press Enter to exit...")
elif result=='3':
    Traitement = EcoDesign()
    Traitement.separating_days()
    Traitement.plot_initiate_figure()
    Traitement.plot_files_eco_design(per_day=True)
    Traitement.plot_generate_html()
elif result=='Q':
    print(" I will miss you .... bye bye 🤙🖐")
    print("-"*50)
    print("-"*50)

    input("Press Enter to exit...")


