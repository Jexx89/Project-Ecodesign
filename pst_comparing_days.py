from EcoDesign import *

if __name__ == "__main__":
    Solo_config = ConfigTest(
        Test_request ='25071',
        Test_Num ='F',
        Appliance_power ='45',
    )
    test={f"{Solo_config.Test_request}{Solo_config.Test_Num}": Solo_config}

    Traitement = EcoDesign(test)
    Traitement.separating_days()
    Traitement.plot_initiate_figure()
    Traitement.plot_files_eco_design(per_day=True)
    Traitement.plot_generate_html()



