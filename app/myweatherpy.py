# app/myweatherpy.py

import os
import requests
import json
import re
import datetime
import tzlocal

from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

API_KEY =os.environ.get("openweather_API") # to obtain API_KEY from env file. 
API_KEY2 =os.environ.get("darksky_api")

current_time = datetime.now()  #> current time
#formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")  #>'2019-06-21 14:00:00' (reference: from prior class discussion)

#
#
#
#


print("Welcome to MyWeatherPy. We are here to help you to provide information\n"
            "about your curiosity in the weather condition anywhere")

# Ask User Input
confirmation = input("Are you ready to explore MyWeatherPy? Please press n to exit.\n"
                "Otherwise, please press any key if you would like to proceed:  ")

if confirmation == "n":
    print("Thank you for considering, MyWeatherPy. We hope you visit us again in the future!")
    exit()
else:
    user_input = input("Awesome choice! Please enter zip code, or city name and state to start\n"
                        "For example, you can input 10004 or New York,NY: ")
    
    # Request weather, condition, forecast etc using API credentials through HTML request
    request_url_1 = f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={API_KEY}"
    request_url_2 = f"https://api.openweathermap.org/data/2.5/weather?zip={user_input}&appid={API_KEY}"
    response = requests.get(url = request_url_1 or request_url_2)
    
    if response.status_code in [200, 301, 302, 304]:
        data = response.json()

        # Set up a variable for current time at local time zone
        import tzlocal
        last_time = data["dt"]  # Reference: https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date        
        unix_timestamp = float(last_time)    
        local_timezone = tzlocal.get_localzone()  #get pytz timezone
        local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
        
        last_timezone = data["timezone"]
        unix_timezone = float(last_time)    
        local_timezone2 = tzlocal.get_localzone()  #get pytz timezone
        local_time2 = datetime.fromtimestamp(unix_timezone, local_timezone2)
        print(f"{local_time.strftime('%Y-%m-%d %H:%M:%S')}" + "  " f"{(local_time2.strftime('%Z'))}")
        
        # Set up a variable for current weather condition
        list_weather = data["weather"]   
        for w in list_weather:
            print(w["main"])
        
         # Set up a variable for current weather condition - more description
        for w in list_weather:         
            print(w["description"])     

        # Set up a variable for current temp
        last_refreshed_temp = data["main"]["temp"] 
        
        def toCelcius(last_refreshed_temp):         # Convert to Celcius
            return int(last_refreshed_temp-273.15)
    
        def toFahrenheit(last_refreshed_temp):      # Convert to Fahrenheit
            return int((last_refreshed_temp-273.15)*9/5+32)
        
        print(f"{toCelcius(last_refreshed_temp)}"+"C")  
        print(f"{toFahrenheit(last_refreshed_temp)}"+"F")

        # Set up a variable for current temp
        last_refreshed_hum = data["main"]["humidity"] 
        print(f"{(last_refreshed_hum)}"+"%")

        





        #breakpoint()
        #print(last_refreshed_time + "    " + current_weather)
        
        
        
        
        
        #print(data['name'])
        
        
        
        #print(data)
     
    else:
        print("OOPS")
        exit()
        
        
        
        #print(response.status_code) #> 200

       

        #try:
        #    parsed_response["name"]
        #    print(parsed_response["name"])



        #if user_input == "london":
        #    print("OK!")
        #    exit()
        #else:
        #    print("OOPS. Please try again")        
        
        
        
        
        
        
        
        
        
        
    #    except: #> "OOPS" will generate below error message
    #        print("-------------------------")
    #        print("ERROR MESSAGE:")
    #        print("SORRY. WE COULD NOT FIND ANY TRADING DATA FOR THE ENTERED STOCK SYMBOL.\n"+
    #        "PLEASE CHECK THE SYMBOL AND TRY IT AGAIN")
    #        exit()
        #return parsed_response




            





#
#        try:
#           parsed_response["name"]
#        except: #> "OOPS" will generate below error message
#           print("-------------------------")
#           print("ERROR MESSAGE:")
#           print("SORRY. WE COULD NOT FIND ANY TRADING DATA FOR THE ENTERED STOCK SYMBOL.\n"+
#           "PLEASE CHECK THE SYMBOL AND TRY IT AGAIN")
#           exit()
        
        
        
        
        
        
        
 #       parsed_response = get_response(user_input)













#def get_response(user_input):  #> To define and return the result after user input. 
#    request_url = f"api.openweathermap.org/data/2.5/weather?q=London,uk&APPID={api_key}"
#    response = requests.get(request_url)
#    parsed_response = json.loads(response.text)
#    #print(response.status_code) #> 200
#
#    try:
#        parsed_response["name"]
#    except: #> "OOPS" will generate below error message
#        print("-------------------------")
#        print("ERROR MESSAGE:")
#        print("SORRY. WE COULD NOT FIND ANY TRADING DATA FOR THE ENTERED STOCK SYMBOL.\n"+
#        "PLEASE CHECK THE SYMBOL AND TRY IT AGAIN")
#        exit()

    #return parsed_response

#if __name__ == "__main__":
#    # Welcome message.
#
#    print("Welcome to MyWeatherPy. We are here to help you to provide information\n"
#            "about your curiosity in the weather condition anywhere")
#
#    confirmation = input("Are you ready to explore MyWeatherPy? Please press n to exit.\n"
#                "Otherwise, please press any button if you would like to proceed:  ")
#    while True:
#        if confirmation == "n":
#            print("Thank you for considering, MyWeatherPy. We hope you visit us again in the future!")
#            exit()
#
#        else:
#            user_input = input("Awesome choice ! Please enter zip code, or city name and state to start\n"
#                                "For example, you can input 10004 or New York, NY: ")
#            parsed_response = get_response(user_input)
#









                                
    # Decide whether we want to do command line style application or pop up screen, clickable type or HTML web application


    


    

    # Ask wheather user wants to see historical data or forecast

    # Once result is showing, ask whether the user lives in the city, plans for trip or curious


    #if live in the city, advise things like take umbrella, be careful icy weather, use sunblock etc
    #if plan for trip, show other results - website to tripadvisor, priceline, avis car, marriott.com etc. then link it
    # if just curious, put a link to wikipedia to learn more about the city.


    # Search for more city, zip code, etc. 



    # Ask if user want to save the result? and store up to 5?



    # Ask if user wants to receive the information in the email. Weather they want to receive alert daily/weekly in the email.




