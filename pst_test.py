from EcoDesign import *

if __name__ == "__main__":
    Solo_config = ConfigTest(
        Test_request ='24082',
        Test_Num ='D',
        Appliance_power ='45',
    )
    # Solo_config = ConfigTest(
    #     Test_request ='25072',
    #     Test_Num ='H',
    #     Appliance_power ='120',
    # )

    test={f"{Solo_config.Test_request}{Solo_config.Test_Num}": Solo_config}
    Traitement = EcoDesign(test)

    Traitement.plot_initiate_figure()
    Traitement.plot_files_eco_design()
    Traitement.plot_generate_html()



