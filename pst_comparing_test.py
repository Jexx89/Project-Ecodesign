from EcoDesign import *

if __name__ == "__main__":
    first_config = ConfigTest(
        Test_request ='25028',
        Test_Num ='I',
        Appliance_power ='60',
        Time_correction = 0
    )
    second_config = ConfigTest(
        Test_request ='25072',
        Test_Num ='F',
        Appliance_power ='120',
        Time_correction = 0
    )
    third_config = ConfigTest(
        Test_request ='25072',
        Test_Num ='E',
        Appliance_power ='120',
        Time_correction = 0
    )
    multitest=  {   f"{first_config.Test_request}{first_config.Test_Num}": first_config,
                    f"{second_config.Test_request}{second_config.Test_Num}": second_config,
                    #f"{third_config.Test_request}{third_config.Test_Num}": third_config
                    }

    Traitement = EcoDesign(multitest)
    Traitement.plot_initiate_figure()
    Traitement.plot_files_eco_design()
    Traitement.plot_generate_html()



