#!/usr/bin/env python3

import asyncio
import time
from logs.log_config import logger
import main.utils as utils


async def main():
    """This is the main program function for the application that will be executed 
    and called from the main.py file later
    """
    # This will list the prompt of the program
    app_start = True
    prompt_welcome = "👋 Welcome to Triage Assist — your intelligent companion for emergency triage!\n"
    prompt_welcome += "🚨 Helping you locate the nearest medical care based on your location.\n"
    prompt_welcome += "1 - Locate nearest medical facility\n"
    prompt_welcome += "2 - Exit application (enter 'exit' to terminate )\n"
    prompt_welcome += "Select the options (1 or 2): "
    while app_start:
        try:
            prompt_response = input(prompt_welcome)

            # Log the prompt
            logger.info(f"User Key interactions: {prompt_response}")
            
            if prompt_response == "2" or prompt_response.lower() == 'exit':
                print("Exiting the program...")
                logger.info("Exiting the program...")
                break
            elif prompt_response == "1":
                app_loc = True
                while app_loc:
                    # prompt the user to enter location and severity of the emergency
                    user_name = input("Please Enter your name: ")
                    logger.info(f"Log the user name: {user_name}")
                    
                    if user_name == " ":
                        continue
                    if not user_name.isalpha():
                        continue

                    user_loc = input("Please Enter current location(state, city, town or area): ")
                    user_emerg_serv = input("Enter the severity of emergency (low, medium, high, critical): ")

                    logger.info(f"Log the user name location: {user_loc}")
                    logger.info(f"Log the user name emergency severity: {user_emerg_serv}")

                    # Do some checks
                    if user_loc == "" or user_emerg_serv == "":
                        print("⚠️ Location and severity fields cannot be empty.")
                        logger.info("⚠️ Location and severity fields cannot be empty.")
                        continue

                    # All fields valid — process
                  
                    logger.info(f"\nHi {user_name}, searching for hospitals near {user_loc}...")
                    logger.info(f"Emergency Severity: {user_emerg_serv}")
                    print(f"\nHi {user_name}, searching for hospitals near {user_loc}...")
                    
                    # Simulate a small await time to search and return results
                    await asyncio.sleep(2)
                       
                    # List the hospitals based on ETA
                    logger.info("✅ Returning the list of hospitals within the area based on the shortest ETA...")
                    print("✅ Returning the list of top 5 hospitals within the area based on the shortest ETA...\n")
                    results_hospitals = utils.get_hosp_severity(
                                        username=user_name, 
                                        user_location=user_loc, 
                                        user_severity=user_emerg_serv
                                        )
                    async for result_hospital in results_hospitals:

                        # Figure out how to move operation to function before yielding 
                        # sort the result of the search based on the eta 
                        sorted_hospital_result = sorted(result_hospital, key= lambda d: d['ETA_in_minutes'])

                       
                        #Return the top 5 closet hospitals based on EAT   
                        print(f"Hospital Name | ETA to hospital | Distance to hospital") 
                        for eta_hos in sorted_hospital_result[:5]:
                            print(f"{eta_hos['name']}  {eta_hos['ETA_in_minutes']} minutes - {eta_hos['distance']} KM ")
                            logger.info(f"""Hospital Name: {eta_hos['name']} ETA to hospital: {eta_hos['ETA_in_minutes']} minutes
                                            Distance to hospital: {eta_hos['distance']} KM""")

                    # Ask if the user if the want to continue using the app
                    user_res = input("Do you want to continue using the application (yes or no): ")
                    logger.info(f"Do you want to continue using the application (yes or no): {user_res} ✅")
                    if user_res.lower() == "yes" or user_res == 'Y':
                        continue
                    else:
                        app_loc = False
                        app_start = False
                        logger.info(f"👋 Goodbye {user_name}")
                        print(f"👋 Goodbye {user_name}")
                        break
                
            else:
                logger.info("⚠️ Invalid input. Please enter 1 or 2.\n")
                print("⚠️ Invalid input. Please enter 1 or 2.\n")

        except KeyboardInterrupt:
            logger.info("\n⛔ Program interrupted. Exiting gracefully...")
            print("\n⛔ Program interrupted. Exiting gracefully...")
            break
          
            
        
                    




if __name__ == "__main__":
    # run the main coroutine
    asyncio.run(main())


