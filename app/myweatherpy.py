# app/myweatherpy.py

import os
import requests
import json
import re
import datetime
import tzlocal
import pytz
import time
import csv
import pprint

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone

load_dotenv()

API_KEY =os.environ.get("openweather_API") # to obtain API_KEY from env file. 
#API_KEY2 =os.environ.get("darksky_api")

current_time = datetime.now()  #> current time
formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")  #>'2019-06-21 14:00:00' (reference: from prior class discussion)


#
#
#
#


print("Welcome to MyWeatherPy. We are here to help you to provide information\n"
            "about your curiosity in the weather condition anywhere")
print("------------------------------")
# Ask User Input
confirmation = input("Are you ready to explore MyWeatherPy?\n" 
                    "------------------------------\n"
                    "Please press any key if you would like to proceed  \n"
                    "Otherwise, please press n to exit:  ")

if confirmation == "n":
    print("------------------------------")
    print("Thank you for considering, MyWeatherPy. We hope you visit us again in the future!")
    exit()
else:
    print("------------------------------")
    print("Awesome choice! For the best search result, please consider the followings:\n" 
        "If you would like to search for U.S. cities, please enter 5 digit-zip code (e.g. 10004) for the most accurate result\n" 
        "For non-U.S, please ensure to enter BOTH city name and two-letter country code (london,uk) for the best result \n"
        "If you are unsure about the country code, please enter help.")

    #User makes input

    while True:
        user_input = input("Please enter your input here:   ")

        #TODO: work on format
        if user_input =="help":  # Reference: https://realpython.com/python-csv/#reading-csv-files-with-csv
            csv_file_path = os.path.join(os.path.dirname(__file__), "..", "list", "countrycode.csv")
            with open(csv_file_path, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count ==0:
                        print(f'        Country name, Code:')
                        line_count += 1
                    else:
                        print(f'\t{row[0]}, {row[1]} {row[2]}')
                        line_count += 1           
          
        elif user_input.isnumeric() and len(user_input) !=5:  # PRELIM VALIDATION if zip code is not 5 digits. #source: https://stackoverflow.com/questions/30994738/how-to-make-input-only-accept-a-z-etc
            print("-------------------------")
            print("ERROR MESSAGE:")
            print("OH, PLEASE ONLY USE THE LETTERS or 5 DIGIT ZIP CODE FOR YOUR INPUT. PLEASE TRY AGAIN.")
            print("-------------------------")

        elif user_input == "":  # PRELIM VALIDATION if no input is made, but hit enter.
            print("-------------------------")
            print("ERROR MESSAGE:")
            print("OH, PLEASE ONLY USE THE LETTERS or 5 DIGIT ZIP CODE FOR YOUR INPUT. PLEASE TRY AGAIN.")
            print("-------------------------")

        #elif not user_input.isalpha(): # PRELIM VALIDATION for limiting the number of letters equal to or less than 6. # Source: https://stackoverflow.com/questions/8761778/limiting-python-input-strings-to-certain-characters-and-lengths
        #    print("-------------------------")
        #    print("ERROR MESSAGE:")
        #    print("OH, PLEASE ONLY USE THE LETTERS or 5 DIGIT ZIP CODE FOR YOUR INPUT. PLEASE TRY AGAIN.")
        else:
        # Request weather, condition, forecast etc using API credentials through HTML request. Priority: Zip code (number first as it gives more accurate. Then, find city,code)
            request_url_2 = f"https://api.openweathermap.org/data/2.5/weather?zip={user_input}&appid={API_KEY}"
            request_url_1 = f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={API_KEY}"

            try:
                response = requests.get(url = request_url_2) or requests.get(url = request_url_1)  # to check HTTP response error
                if response.status_code in [200, 300]:
                
                    data = response.json()

                    # Set up a variable for latest refresh time at timezone where the script is run (where the search happened)
                    import tzlocal
                    last_time = data["dt"]  # Reference: https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date        
                    unix_timestamp = float(last_time)    
                    my_timezone = tzlocal.get_localzone()  #get pytz timezone
                    my_time = datetime.fromtimestamp(unix_timestamp, my_timezone)

                    last_timezone = data["timezone"]
                    unix_timezone = float(last_timezone)    
                    my_timezone2 = tzlocal.get_localzone()  #get pytz timezone
                    my_time2 = datetime.fromtimestamp(unix_timezone, my_timezone2)
                    #print(f"{my_time.strftime('%Y-%m-%d %H:%M:%S')}" + "  " f"{(my_time2.strftime('%Z'))}")

                    # To show the current time at the local time zone

                    current_local_time = datetime.fromtimestamp(unix_timestamp)
                    friendly_current_local_time = current_local_time.strftime('%Y-%m-%d %H:%M:%S')
                    friendly_local_time = datetime.fromtimestamp(unix_timestamp)   #reference: https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
                    friendly_local_timezone = datetime.utcfromtimestamp(last_timezone).strftime('%Z')  #TODO: Need to fix the timezone display
                    #print(f"{friendly_local_time}" + "  " f"{friendly_local_timezone}")           

                    # Set up city name and country code
                    city_name = data["name"]
                    city_code = data["sys"]["country"]

                    # Set up a variable for current weather condition
                    list_weather = data["weather"]   
                    for w in list_weather:
                        #print(w["main"])
                        weather_condition = w["main"]
                    
                    # Set up wheather id for customized messsage
                    for w in list_weather:
                        weather_id = w["id"]

                    if weather_id in [200,201,202,210,211,212,221,230,231,232,300,301,302,310,311,312,313,314,321,500,501,502,503,
                                    504,511,520,521,522,531]:
                        my_message = "Please bring umbrella with you."

                    if weather_id in [600,601,602,611,612,613,615,616,620,621,622]:
                        my_message = "The road/street may be slippery. Please be extra careful while you are outside."
                    
                    if weather_id in [701,711,721,731,741,751,761,762,771,781]:
                        my_message = "Due to the atmosphere condition, we advise you to stay indoor."    
                    
                    if weather_id in [800]:
                        my_message = "The weather is clear. Enjoy your day!"

                    if weather_id in [801,802,803,804]:
                        my_message = "It is cloudy outside, but it is not too bad."    

                     # Set up a variable for current weather condition - more description
                    for w in list_weather:         
                        #print(w["description"])  
                        weather_description = w["description"]

                    # Set up a variable for current temp
                    last_refreshed_temp = data["main"]["temp"] 

                    def toCelcius(last_refreshed_temp):         # Convert to Celcius
                        return int(last_refreshed_temp-273.15)

                    def toFahrenheit(last_refreshed_temp):      # Convert to Fahrenheit
                        return int((last_refreshed_temp-273.15)*9/5+32)

                    #print(f"{toCelcius(last_refreshed_temp)}"+"C")  
                    #print(f"{toFahrenheit(last_refreshed_temp)}"+"F")

                    # Set up a variable for current temp
                    last_refreshed_hum = data["main"]["humidity"] 
                    #print(f"{(last_refreshed_hum)}"+"%")

                    print("------------------------------")
                    print("Here is the result:")
                    print("------------------------------")
                    print("Name of city and country:  " f"{city_name}" + "  " f"{city_code}")
                    print("Current Time based on your location: " f"{formatted_current_time}")
                    print("Current Local Time based on your input:  " f"{friendly_current_local_time}")
                    print("Last Refreshed at your time: " f"{my_time.strftime('%Y-%m-%d %H:%M:%S')}" + "  " f"{(my_time2.strftime('%Z'))}")
                    print("Last Refreshed at local time: " f"{friendly_local_time}" + "  " f"{friendly_local_timezone}")
                    print("------------------------------") 
                    print("Weather Condition: " f"{weather_condition}")
                    print("Weather Additional Description: " f"{weather_description}")
                    print("------------------------------")
                    print("Current Temperature in Celcius: " f"{toCelcius(last_refreshed_temp)}"+"C")
                    print("Current Temperature in Fahrenheit: " f"{toFahrenheit(last_refreshed_temp)}"+"F")
                    print("------------------------------")
                    print("Current Humidity Level is:  " f"{(last_refreshed_hum)}"+"%")
                    print("-------------------------")
                    print("Friendly Advice (based on the weather condition): " f"{my_message}")
                    print("-------------------------")

                    #Writine CSV file for current weather output.
                    file_name2 = "current" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + ".csv"
                    csv_file_path2 = os.path.join(os.path.dirname(__file__), "..", "data", file_name2)
                    csv_headers = ["City", "Code", "Time", "Weather", "Temp(C)", "Temp(F)", "Humidity(%)"]
                    with open(csv_file_path2, "w", newline='') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                        writer.writeheader() # uses fieldnames set above
                        writer.writerow({
                            "City": city_name,
                            "Code": city_code,
                            "Time": current_local_time,
                            "Weather": weather_condition,
                            "Temp(C)": toCelcius(last_refreshed_temp),
                            "Temp(F)": toFahrenheit(last_refreshed_temp),
                            "Humidity(%)": last_refreshed_hum,
                        })
                    print("Your result has been saved in /data folder with city name, code and current time")
                else:
                    print("ERROR: " +f"{response.status_code}")
                    if response.status_code ==404:
                        print("PAGE NOT FOUND OR SERVER NOT FOUND. PLEASE CHECK AND TRY AGAIN. GOOD-BYE.")
                        exit()
                    
                    else: 
                        print("THE SERVICE IS CURRENTLY UNAVAILABLE. PLEASE TRY IT AGAIN IN A LITTLE BIT.")
                        exit()

                    # To set up next 5 days forecast

                pause_input = input("Please review the result. When ready, please press any button to see the weather forecast:  ")
                print("-------------------------")

                request_url_4 = f"https://api.openweathermap.org/data/2.5/forecast?zip={user_input}&appid={API_KEY}"
                request_url_3 = f"http://api.openweathermap.org/data/2.5/forecast?q={user_input}&mode=json&appid={API_KEY}"
                response = requests.get(url = request_url_4) or requests.get(url = request_url_3)

                if response.status_code in [200, 300]:
                    data1 = response.json()
                    #print(data1)
                    
                    # Set up a variable for f
                    list_forecast = data1["list"]
                    print("WEATHER FORECAST FOR EVERY 3 HOURS FOR THE NEXT 5 DAYS")
                    print("-------------------------")
                    print("Your Selected City: " f"{city_name}" + "  " f"{city_code}")
                    print("Date      ", "Time ", "Weather  ", "Details   ", "Temp(C)", "High(C)", "Low(C)", "Temp(F)", "High(F)", "Low(F)", "Humidity(%)")
                    print("-------------------------")    
                    for f in list_forecast:
                        forecast_date = f["dt"]
                        forecast_unix_timestamp = float(forecast_date)    
                        forecast_my_time = datetime.fromtimestamp(forecast_unix_timestamp, my_timezone)    
                        forecast_temp = f["main"]["temp"]
                        forecast_temp_high = f["main"]["temp_max"]
                        forecast_temp_min = f["main"]["temp_min"]
                        forecast_hum = f["main"]["humidity"]
                        forecast_weather = f["weather"]
                        for q in forecast_weather:
                            forecast_weather2 = q["main"]
                            forecast_weather_detail = q["description"]
                            forecast_weather_id = q["id"]
                
                            print(f"{forecast_my_time.strftime('%Y-%m-%d %I %p')} {forecast_weather2} {forecast_weather_detail} {toCelcius(forecast_temp)}C {toCelcius(forecast_temp_high)}C {toCelcius(forecast_temp_min)}C {toFahrenheit(forecast_temp)}F {toFahrenheit(forecast_temp_high)}F {toFahrenheit(forecast_temp_min)}F {forecast_hum}%")

                        file_name3 = "forecast" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + ".csv"
                        csv_file_path3 = os.path.join(os.path.dirname(__file__), "..", "data", file_name3)
                        csv_headers = ["City", "Code", "Time", "Weather", "Temp(C)", "Temp(F)", "Humidity(%)"]
                        with open(csv_file_path3, "w", newline='') as csv_file:
                            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                            writer.writeheader() # uses fieldnames set above
                            writer.writerow({
                                "City": city_name,
                                "Code": city_code,
                                "Time": forecast_my_time,
                                "Weather": forecast_weather2,
                                "Temp(C)": toCelcius(forecast_temp),
                                "Temp(F)": toFahrenheit(forecast_temp),
                                "Humidity(%)": forecast_hum,
                            })
                    print("Your result has been saved in /data folder with name forecast, city name, code and current time")                       
                    print("-------------------------")   
                    while True:
                        choice = input("WHAT IS THE REASON FOR YOUR SEARCH OF WEATHER CONDITION?\n"
                        "1. Traveling the area (Vacation, Work, Family Visit etc)\n"
                        "2. Currently Living in the area\n"
                        "3. Being bored. Just Killing time\n"
                        "4. I am done. I want to exit\n"
                        "Your Choice:  ") 
                        if choice =="1":
                            print("Great. If you have not fully finalized your travel plan yet, these websites can help you to complete your exciting trip!")
                            csv_file_path1 = os.path.join(os.path.dirname(__file__), "..", "list", "travel_vendor.csv")
                            with open(csv_file_path1, "r") as csv_file:
                                csv_reader = csv.reader(csv_file, delimiter=',')
                                line_count = 0
                                for row in csv_reader:
                                    if line_count ==0:
                                        print(f'        Name, Type, website:')
                                        print("-------------------------")
                                        line_count += 1
                                    else:
                                        print(f'\t{row[0]}, {row[1]}, {row[2]}')
                                        line_count += 1

                        elif choice =="2":
                            print("We understand ! Hopefully our service has helped you to plan appropriately.")
                            exit()
                        elif choice =="3":
                            print("No problem. Perhaps, you can read more about the city. You may find it interesting! Here is the website")
                            print("www.wikipedia.com")
                            exit()
                        elif choice =="4":
                            print("OK. We hope we provided helpful information for you. Please visit us again. Good-Bye ~")
                            exit()
                        else:
                            print("OOPS. We do not recognize your choice. Please choose again")
                            print("------------------------------")
                    
                        print("------------------------------")
                        final_input = input("Thank you so much for using MyweatherPy service. Would you like to also receive the output in the email? Press y to receive. Otherwise, press any key to exit: ")
                        if final_input =="y":
                            user_email_input = input("PLEASE ENTER YOUR EMAIL ADDRESS: ") # asking user email address for input.
                            
                            
                            SENDGRID_API_KEY = os.environ.get("sendgrid_api_key", "OOPS, please set env var called 'SENDGRID_API_KEY'")  #private information included in .env
                            SENDGRID_TEMPLATE_ID = os.environ.get("sendgrid_template_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'") #private information included in .env
                            MY_ADDRESS = os.environ.get("my_email_address", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'") #private information included in .env
                            
                            template_data = {   # showing the checkout timestamp and the total price on the email receipt (minimum level of information per instruction)
                                "human_friendly_timestamp": str(current_time.strftime("%Y-%m-%d %I:%M %p")),
                                "city_name": str(city_name)+str(city_code),
                                "current_weather_condition": str(weather_condition),
                                "currrent_weather_description": str(weather_description),
                                "current_temp_C": str(toCelcius(last_refreshed_temp)),
                                "current_temp_F": str(toFahrenheit(last_refreshed_temp)),
                                "current_hum": str((last_refreshed_hum)),
                                "friendly_advice": str(my_message),

                            }
                            client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
                            print("CLIENT:", type(client))
                
                            message = Mail(from_email=MY_ADDRESS, to_emails=user_email_input) # For to_emails, MY_ADDRESS is replaced with user_input from line 133.
                            print("MESSAGE:", type(message))
                
                            message.template_id = SENDGRID_TEMPLATE_ID
                
                            message.dynamic_template_data = template_data
                
                            try:
                                response = client.send(message)
                                print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
                                print(response.status_code) #> 202 indicates SUCCESS
                                print(response.body)
                                print(response.headers)
                
                            except Exception as e:
                                print("OOPS", e.message)
                
                            print("Your report has been sent to the email address that your provided.")
                            print("Thank you for using MyweatherPy. We hope to see you again. Good-Bye ~") # A friendly message thanking the customer and/or encouraging the customer to shop again
                            exit()
                
                        else:
                            print("No problem. Thank you, so much again. Hopefully you will visit us again in the future. Good-Bye ~") # No email receipt if customer does not select y.
                            exit() 


                else:
                    print("ERROR: " +f"{response.status_code}")
                    if response.status_code ==404:
                        print("PAGE NOT FOUND OR SERVER NOT FOUND. PLEASE CHECK AND TRY AGAIN. GOOD-BYE.")
                        exit()
                            
                        
                    #print("-------------------------")    
                    #F_option = input("Do you want to see the temperature in Fahrenheit? Press y to see. Otherwise, press any button:  ")
                    #if F_option =="y":
                    #    
                    #    print("-------------------------") 
                    #    for f in list_forecast:
                    #        forecast_date_F = f["dt"]
                    #        forecast_unix_timestamp_F = float(forecast_date_F)    
                    #        forecast_my_time = datetime.fromtimestamp(forecast_unix_timestamp_F, my_timezone)    
                    #        forecast_temp_F = f["main"]["temp"]
                    #        forecast_temp_high_F = f["main"]["temp_max"]
                    #        forecast_temp_min_F = f["main"]["temp_min"]
                    #        forecast_hum_F = f["main"]["humidity"]
                    #        forecast_weather_F = f["weather"]
                    #        for q in forecast_weather_F:
                    #            forecast_weather_F = q["main"]
                    #            forecast_weather_detail_F = q["description"]
                    #    print(f"{forecast_my_time.strftime('%Y-%m-%d %I %p')} {forecast_weather_F} {forecast_weather_detail_F} {toFahrenheit(forecast_temp_F)}F {toFahrenheit(forecast_temp_high_F)}F {toFahrenheit(forecast_temp_min_F)}F {forecast_hum_F}")
                    
                        #print("-------------------------") 
                        #while True:
                        #    choice = input("WHAT IS THE REASON FOR YOUR SEARCH OF WEATHER CONDITION?\n"
                        #    "1. Currently Living in the area\n"
                        #    "2. Traveling the area (Vacation, Work, Family Visit etc)\n"
                        #    "3. Planning for my next vacation !\n"
                        #    "4. Being bored. Just Killing time\n"
                        #    "Your Choice:  ") 
                        #    if choice =="1":
                        #        #>TODO
                        #        exit()
                        #    elif choice =="2":
                        #        #>TODO
                        #        exit()
                        #    elif choice =="3":
                        #        #TODO
                        #        exit()
                        #    elif choice =="4":
                        #        #TODO
                        #        exit()
                        #    else:
                        #        print("OOPS. We do not recognize your choice. Please choose again")
                        #        print("------------------------------")



                    
                    
                        
        
                    
                    
                    
                    
                    
                    # To show the current time at the local time zone


                        #for f in list_forecast:
                        #    forecast_temp = f["main"]["temp"]
#
                        #for i in forecast_temp:
                        #    print(i)
                        #    for p in forecast_temp[i]:
                        #        print(p, ":", forecast_temp[i][p]) 


                        #forecast_temp = [forecast["main"]["temp"] for forecast in list_forecast]
                        #forecast_temp_high = [forecast["main"]["temp_max"] for forecast in list_forecast]
                        #
                        #for o in list_forecast:
                        #    print(forecast_temp)
                        #    print(forecast_temp_high)
#
                        #print(forecast_temp)


                        #for f in list_forecast:
                        ##print(w["main"])
                        #    forecast_date = f["dt"]
                        #    forecast_temp = f["main"]["temp"]
                        #    forecast_temp_high = f["main"]["temp_max"]
                        #    forecast_temp_min = f["main"]["temp_min"]
                        #    forecast_hum = f["main"]["humidity"]
                        #    forecast_weather = f["weather"]
                        #    for q in forecast_weather:
                        #        forecast_weather2 = q["main"]
                        #        forecast_weather_detail = q["description"]
                            #print(forecast_date)
                            #print(forecast_temp)
                            #print(forecast_temp_high)
                            #print(forecast_temp_min)
                            #print(forecast_hum)
                            #print(forecast_weather2)
                            #print(forecast_weather_detail)
                            #print(forecast_temp) 

                        #def toCelcius(forecast_c):         # Convert to Celcius
                        #    return int(last_refreshed_temp-273.15)
#
                        #def toFahrenheit(forecast_f):      # Convert to Fahrenheit
                        #    return int((last_refreshed_temp-273.15)*9/5+32)




                    




                    # Once result is showing, ask whether the user lives in the city, plans for trip or curious
                


                
                    




            except requests.ConnectionError:
                print("failed to connect")









        #if response.status_code in [200, 301, 302, 304]:
        #    data = response.json()
#   
        #    # Set up a variable for current time at local time zone
        #    import tzlocal
        #    last_time = data["dt"]  # Reference: https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date        
        #    unix_timestamp = float(last_time)    
        #    local_timezone = tzlocal.get_localzone()  #get pytz timezone
        #    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
        #    
        #    last_timezone = data["timezone"]
        #    unix_timezone = float(last_time)    
        #    local_timezone2 = tzlocal.get_localzone()  #get pytz timezone
        #    local_time2 = datetime.fromtimestamp(unix_timezone, local_timezone2)
        #    print(f"{local_time.strftime('%Y-%m-%d %H:%M:%S')}" + "  " f"{(local_time2.strftime('%Z'))}")
        #    
        #    # Set up a variable for current weather condition
        #    list_weather = data["weather"]   
        #    for w in list_weather:
        #        print(w["main"])
        #    
        #     # Set up a variable for current weather condition - more description
        #    for w in list_weather:         
        #        print(w["description"])     
#   
        #    # Set up a variable for current temp
        #    last_refreshed_temp = data["main"]["temp"] 
        #    
        #    def toCelcius(last_refreshed_temp):         # Convert to Celcius
        #        return int(last_refreshed_temp-273.15)
        #
        #    def toFahrenheit(last_refreshed_temp):      # Convert to Fahrenheit
        #        return int((last_refreshed_temp-273.15)*9/5+32)
        #    
        #    print(f"{toCelcius(last_refreshed_temp)}"+"C")  
        #    print(f"{toFahrenheit(last_refreshed_temp)}"+"F")
#   
        #    # Set up a variable for current temp
        #    last_refreshed_hum = data["main"]["humidity"] 
        #    print(f"{(last_refreshed_hum)}"+"%")







        #breakpoint()
        #print(last_refreshed_time + "    " + current_weather)
        
        
        
        
        
        #print(data['name'])
        
        
        
        #print(data)
     

        
        
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


    


    

    

    # Once result is showing, ask whether the user lives in the city, plans for trip or curious


    #if live in the city, advise things like take umbrella, be careful icy weather, use sunblock etc
    #if plan for trip, show other results - website to tripadvisor, priceline, avis car, marriott.com etc. then link it
    # if just curious, put a link to wikipedia to learn more about the city.


    # Search for more city, zip code, etc. 



    # Ask if user want to save the result? and store up to 5?



    # Ask if user wants to receive the information in the email. Weather they want to receive alert daily/weekly in the email.




