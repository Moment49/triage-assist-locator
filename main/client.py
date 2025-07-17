#!/usr/bin/env python3

import asyncio
import time



async def main():
    """This is the main program function for the application that will be executed 
    and called from the main.py file later
    """
    # This will list the prompt of the program
    app_start = True
    prompt_welcome = "👋 Welcome to Triage Assist — your intelligent companion for emergency triage!"
    prompt_welcome += "🚨 Helping you locate the nearest medical care based on your location.\n"
    prompt_welcome += "1 - Locate nearest medical facility"
    prompt_welcome += "2 - Exit application (enter 'exit' to terminate )"
    prompt_welcome += "Select the options (1 or 2): "
    while app_start:
        prompt_response = input(prompt_welcome)
        
        if prompt_response == "2" or prompt_response == 'exit':
            print("Exiting the program...")
            break
        if prompt_response == "1":
            ...
            # prompt the user to enter location and severity of the emergency
            user_loc = input("Please Enter current location(town or area): ")
            await time.sleep(1)
            user_emerg_serv = input("Enter the severity of emergency: ")

            # add data recieved to the function to compute and re 
            print(user_loc)
            print(user_emerg_serv)
            print("Returning the list of hospitals within the areas...")





if __name__ == "__main__()":
    # run the main coroutine
    asyncio(main())


