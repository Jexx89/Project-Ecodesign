from EcoDesign import *

if __name__ == "__main__":
    first_config = ConfigTest(
        Test_request ='25069',
        Test_Num ='B',
        Appliance_power ='35',
        Time_correction = 0
    )
    second_config = ConfigTest(
        Test_request ='25063',
        Test_Num ='M',
        Appliance_power ='35',
        Time_correction = 28
    )
    third_config = ConfigTest(
        Test_request ='25072',
        Test_Num ='E',
        Appliance_power ='120',
        Time_correction = 0
    )
    fourth_config = ConfigTest(
        Test_request ='25072',
        Test_Num ='H',
        Appliance_power ='120',
        Time_correction = 0
    )
    multitest=  {   f"{first_config.Test_request}{first_config.Test_Num}": first_config,
                    f"{second_config.Test_request}{second_config.Test_Num}": second_config,
                    #f"{third_config.Test_request}{third_config.Test_Num}": third_config
                    }
    # multitest=  {   f"{third_config.Test_request}{third_config.Test_Num}": third_config,
    #                 f"{fourth_config.Test_request}{fourth_config.Test_Num}": fourth_config,
    #                 }


    Traitement = EcoDesign(multitest)
    Traitement.plot_initiate_figure()
    Traitement.plot_files_eco_design()
    Traitement.plot_generate_html()



