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
import string
import base64

from sendgrid import SendGridAPIClient    # To use the sendgrid email receipt feature
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId
from dotenv import load_dotenv  # To reference the .env which includes credential information. 
from datetime import datetime   # To use the datetime, time today/now feature.
from pytz import timezone   # To utilize the timezone difference (my time vs time at local location)
from timezonefinder import TimezoneFinder  
from PIL import Image  # To use the pop up window for images.
from selenium import webdriver  # To automate some search features using google webdriver
from selenium.webdriver.common.keys import Keys

load_dotenv()

API_KEY =os.environ.get("openweather_API") # to obtain API_KEY from env file. 

def easy_timestamp(time):    #>'2019-06-21 14:00:00' (reference: from prior class discussion)
    c_time = datetime.now()
    return c_time.strftime("%Y-%m-%d %H:%M:%S")

def toCelsius(ltemp):         # Convert to Celsius
    return int(ltemp-273)

def toFahrenheit(ltemp):      # Convert to Fahrenheit
    return int((ltemp-273.15)*9/5+32)

if __name__ == "__main__":

    print("------------------------------")
    print("Welcome to MyWeatherPy. We are here to help you to provide information\n"
                "about your curiosity in the weather condition for you!")
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
            "- If you would like to search for U.S. cities, please enter 5-digit zip code (e.g. 10004) for the most accurate result.\n" 
            "- For non-U.S, please ensure to enter BOTH city name and two-letter country code (london,uk) for the best result. \n"
            "- If you are unsure about the country code, please enter help.\n")
    
        #User makes input
    
        while True:
            user_input = input("Please enter your input here:   ")
            
            if user_input =="help":  # Reference: https://realpython.com/python-csv/#reading-csv-files-with-csv
                print("\n")
                csv_file_path = os.path.join(os.path.dirname(__file__), "..", "list", "countrycode.csv")
                with open(csv_file_path, "r") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if line_count ==0:
                            print(f'Country name,    Code:')
                            print("-------------------------")
                            line_count += 1
                        else:
                            print(f'{row[0]}, {row[1]}')
                            line_count += 1
                                       
            elif user_input.isnumeric() and len(user_input) !=5:  # PRELIM VALIDATION if zip code is not 5 digits. #source: https://stackoverflow.com/questions/30994738/how-to-make-input-only-accept-a-z-etc
                print("-------------------------")
                print("ERROR MESSAGE:")
                print("OH, PLEASE ONLY USE THE LETTERS or 5 DIGIT ZIP CODE FOR YOUR INPUT. PLEASE TRY AGAIN.")
                print("-------------------------")
    
            elif user_input == "":  # PRELIM VALIDATION if no input is made, but hit enter.
                print("-------------------------")
                print("ERROR MESSAGE:")
                print("Oops. It looks like you just hit the enter by mistake. Please provide us your input!")
                print("-------------------------")
    
            elif user_input in ["!","@","#","$","%","^","&","*",")","(","-","_","=","+","[","}","[","{",":",";","'",'"',"/","?",".",">",",","<","`","~"]: # PRELIM validation if the user inputs special character.
                print("-------------------------")
                print("ERROR MESSAGE:")
                print("OH, PLEASE ONLY USE THE LETTERS or 5 DIGIT ZIP CODE FOR YOUR INPUT. PLEASE TRY AGAIN.")
                print("-------------------------")
    
            else:
            # Request weather, condition, forecast etc using API credentials through HTML request. Priority: Zip code (number first as it gives more accurate. Then, find city,code)
                request_url_2 = f"https://api.openweathermap.org/data/2.5/weather?zip={user_input}&appid={API_KEY}"
                request_url_1 = f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={API_KEY}"
    
                try:
                    response = requests.get(url = request_url_2) or requests.get(url = request_url_1)  # to check HTTP response error
                    if response.status_code in [200, 300]:
                    
                        data = response.json()
                        current_time = datetime.now()  
                        formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")  
                        
                        local_lon = data["coord"]["lon"] # To set up local time (based on input) using latitude/longitutde
                        local_lat = data["coord"]["lat"]
                        
                        tf = TimezoneFinder(in_memory=True) # Reference: https://pypi.org/project/timezonefinder/
                        timezone_region = tf.closest_timezone_at(lng=local_lon, lat=local_lat)
                        
                        utcmoment_naive = datetime.utcnow() # Reference: https://stackoverflow.com/questions/10997577/python-timezone-conversion
                        utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
                        localdatetime = utcmoment.astimezone(pytz.timezone(timezone_region))
                        formatted_localdatetime = localdatetime.strftime('%Y-%m-%d %H:%M:%S')
                        formatted_localdatetimezone = localdatetime.strftime('%Z')
                        
                        # Set up a variable for latest refresh time at the user's timezone where the script is run (to provide accurate result since there is a little delay between the report time vs my timezone time now)
                        import tzlocal
                        last_time = data["dt"]  # Reference: https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date        
                        unix_timestamp = float(last_time)    
                        my_timezone = tzlocal.get_localzone()  #get pytz timezone
                        my_time = datetime.fromtimestamp(unix_timestamp, my_timezone)
                        formatted_my_time = my_time.strftime('%Y-%m-%d %H:%M:%S')
    
                        last_timezone = data["timezone"]
                        unix_timezone = float(last_timezone)    
                        my_timezone2 = tzlocal.get_localzone()  #get pytz timezone
                        my_time2 = datetime.fromtimestamp(unix_timezone, my_timezone2)
                        formatted_my_time2 = my_time2.strftime('%Z')       
    
                        # Set up city name and country code
                        city_name = data["name"]
                        city_code = data["sys"]["country"]
    
                        # Set up a variable for current weather condition
                        list_weather = data["weather"]   
                        for w in list_weather:
                            weather_condition = w["main"]
                        
                        # Set up friendly advice/recommendation based upon the weather condition using "id"
                        for w in list_weather:
                            weather_id = w["id"]
    
                        if weather_id in [200,201,202,210,211,212,221,230,231,232,300,301,302,310,311,312,313,314,321,500,501,502,503,
                                        504,511,520,521,522,531]:
                            my_message = "You may get wet outside. Please bring umbrella with you and wear water-proof boots."
    
                        if weather_id in [600,601,602,611,612,613,615,616,620,621,622]:
                            my_message = "Roads/streets may be slippery. Please be extra careful while you are outside."
                        
                        if weather_id in [701,711,721,731,741,751,761,762,771,781]:
                            my_message = "Due to the atmosphere condition, we advise you to stay indoor. If possible, please avoid driving."    
                        
                        if weather_id in [800]:
                            my_message = "The weather is nice and clear. Enjoy your day!"
    
                        if weather_id in [801,802,803,804]:
                            my_message = "It is cloudy outside, but it is not too bad. Hope you can still enjoy your day ! "    
    
                        # Set up a variable for current weather condition - more description (longer description than "weather")
                        for w in list_weather:         
                            #print(w["description"])  
                            weather_description = w["description"]
    
                        # Set up a variable for current temp
                        last_refreshed_temp = data["main"]["temp"] 
    
                        # Set up a variable for current temp max
                        last_refreshed_temp_max = data["main"]["temp_max"] 

                        # Set up a variable for current temp min
                        last_refreshed_temp_min = data["main"]["temp_min"] 

                        # Set up a variable for current humidity
                        last_refreshed_hum = data["main"]["humidity"] 
                        #print(f"{(last_refreshed_hum)}"+"%")
                        
                        print("------------------------------")
                        print("Here is the result:")
                        print("------------------------------")
                        print("Name of city and country code:              " f"{city_name}" + "  " f"{city_code}")
                        print("Current Local Time based on your input:     " f"{formatted_localdatetime}" " " f"{formatted_localdatetimezone}")
                        print("Current Time based on your location:        " f"{formatted_current_time}" " " f"{formatted_my_time2}")
                        print("Last Refreshed based on your location:      " f"{formatted_my_time}" + " " f"{formatted_my_time2}")                  
                        print("------------------------------") 
                        print("Weather Condition:                          " f"{weather_condition}")
                        print("Weather Additional Description:             " f"{weather_description}".title())
                        print("------------------------------")
                        print("Current Temperature in Celsius:             " f"{toCelsius(last_refreshed_temp)}"+"C")
                        print("Current Temperature in Fahrenheit:          " f"{toFahrenheit(last_refreshed_temp)}"+"F")
                        print("Highest Temperature today in Celsius:       " f"{toCelsius(last_refreshed_temp_max)}"+"C")
                        print("Highest Temperature today in Fahrenheit:    " f"{toFahrenheit(last_refreshed_temp_max)}"+"F")
                        print("Lowest Temperature today in Celsius:        " f"{toCelsius(last_refreshed_temp_min)}"+"C")
                        print("Lowest Temperature today in Fahrenheit:     " f"{toFahrenheit(last_refreshed_temp_min)}"+"F")
                        print("------------------------------")
                        print("Current Humidity Level is:                  " f"{(last_refreshed_hum)}"+"%")
                        print("-------------------------")
                        print("Recommendation (on the selected location):  " f"{my_message}")
                        print("-------------------------")
    
                        # Writing CSV file for current weather output.
                        file_name2 = "current" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + ".csv"
                        csv_file_path2 = os.path.join(os.path.dirname(__file__), "..", "data", file_name2)
                        csv_headers = ["City", "Code", "My Time", "Local Time", "Weather", "Temp(C)", "Temp(F)", "High Temp(C)", "High Temp(F)", "Low Temp(C)", "Low Temp(F)", "Humidity(%)"]
                        with open(csv_file_path2, "w", newline='') as csv_file:
                            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                            writer.writeheader() # uses fieldnames set above
                            writer.writerow({
                                "City": city_name,
                                "Code": city_code,
                                "My Time": formatted_current_time,
                                "Local Time": formatted_localdatetime,
                                "Weather": weather_condition,
                                "Temp(C)": toCelsius(last_refreshed_temp),
                                "Temp(F)": toFahrenheit(last_refreshed_temp),
                                "High Temp(C)": toCelsius(last_refreshed_temp_max),
                                "High Temp(F)": toFahrenheit(last_refreshed_temp_max),
                                "Low Temp(C)": toCelsius(last_refreshed_temp_min),
                                "Low Temp(F)": toFahrenheit(last_refreshed_temp_min),
                                "Humidity(%)": last_refreshed_hum,
                            })
                        print("Your result has been saved in /data folder with city name, code and current time.")
                        print("-------------------------")
                    else:
                        # Error message if user input cannot be found in API. If 404, provide cannot be found. If other error code, encourage the user to try it again in a little bit.
                        print("ERROR: " +f"{response.status_code}")
                        if response.status_code ==404:
                            print("PAGE NOT FOUND OR SERVER NOT FOUND. PLEASE CHECK AND TRY AGAIN. GOOD-BYE.")
                            exit()
                        
                        else: 
                            print("THE SERVICE IS CURRENTLY UNAVAILABLE. PLEASE CHECK TRY IT AGAIN IN A LITTLE BIT.")
                            exit()
    
                    # To set up next 5 days forecast
    
                    pause_input = input("Please review the result. When ready, please press any button to see the weather forecast:  ")
                    print("-------------------------")

                    request_url_4 = f"https://api.openweathermap.org/data/2.5/forecast?zip={user_input}&appid={API_KEY}"
                    request_url_3 = f"http://api.openweathermap.org/data/2.5/forecast?q={user_input}&mode=json&appid={API_KEY}"
                    response = requests.get(url = request_url_4) or requests.get(url = request_url_3)
    
                    if response.status_code in [200, 300]:
                        data1 = response.json()
                       
                        list_forecast = data1["list"]                                                                                                           
                        print("WEATHER FORECAST FOR EVERY 3 HOURS FOR THE NEXT 5 DAYS!")
                        print("-------------------------")
                        print("Your Selected City: " f"{city_name}" + "  " f"{city_code}")
                        print("Date & Time", "\t", "\tWeather", "Temp(C)", "High(C)", "Low(C)", "Temp(F)", "High(F)", "Low(F)", "\tHumidity(%)")
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
                                print(f"{forecast_my_time.strftime('%Y-%m-%d %I %p')} \t{forecast_weather2} \t{toCelsius(forecast_temp)}C \t{toCelsius(forecast_temp_high)}C \t{toCelsius(forecast_temp_min)}C \t{toFahrenheit(forecast_temp)}F \t{toFahrenheit(forecast_temp_high)}F \t{toFahrenheit(forecast_temp_min)}F \t{forecast_hum}%")
                                
                                # To store the forecast information in CSV file

                                file_name3 = "forecast" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
                                csv_file_path3 = os.path.join(os.path.dirname(__file__), "..", "data", file_name3)
    
                                csv_headers = ["City", "Code", "Time", "Temp(C)", "High(C)", "Low(C)", "Temp(F)", "High(F)", "Low(F)", "Humidity(%)"]
    
                                with open(csv_file_path3, "w", newline='') as csv_file:
                                    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                                    writer.writeheader() # uses fieldnames set above
    
                                    for x in list_forecast:
                                        writer.writerow({
                                            "City": city_name,
                                            "Code": city_code,
                                            "Time": datetime.fromtimestamp(float(x["dt"]), my_timezone).strftime("%Y-%m-%d %I %p"),
                                            "Temp(C)": toCelsius(x["main"]["temp"]),
                                            "High(C)": toCelsius(x["main"]["temp_max"]),
                                            "Low(C)": toCelsius(x["main"]["temp_min"]),
                                            "Temp(F)": toFahrenheit(x["main"]["temp"]),
                                            "High(F)": toFahrenheit(x["main"]["temp_max"]),
                                            "Low(F)": toFahrenheit(x["main"]["temp_min"]),
                                            "Humidity(%)": x["main"]["humidity"]
                                    })
                        print("-------------------------") 
                        print("Your result has been saved in /data folder under name forecast, city name, code and current time. ")                       
                        print("-------------------------")  

                        # Ask user why they are using this app for more customized output
                         
                        while True:
                            choice = input("WHAT IS THE REASON FOR YOUR SEARCH OF WEATHER CONDITION?\n"
                            "\n"
                            "1. Traveling the area (Vacation, Work, Family Visit etc)\n"
                            "2. Currently Living in the area\n"
                            "3. Being bored. Just Killing time\n"
                            "4. I am done. I want to exit\n"
                            "\n"
                            "Your Choice:  ") 
                            
                            if choice =="1":
                                print("------------------------------")
                                print("Great. If you have not fully finalized your travel plan yet, these websites can help you to complete your exciting trip!\n")
                                csv_file_path1 = os.path.join(os.path.dirname(__file__), "..", "list", "travel_vendor.csv")
                                
                                # To read the travel partner list from csv

                                with open(csv_file_path1, "r") as csv_file:
                                    csv_reader = csv.reader(csv_file, delimiter=',')
                                    line_count = 0
                                    for row in csv_reader:
                                        if line_count ==0:
                                            print(f'id\t name\t \t\ttype\t \t\t website\n')
                                            line_count += 1
                                        else:
                                            dict_csv = f'{row[0]}\t {row[1]}\t \t{row[2]}\t {row[3]}'                                                                        
                                            print(dict_csv)
                                            line_count += 1         
                                print("-------------------------")

                                while True:
                                    open_web = input("If you want to navigate any website above, please press the number: ")
                                    if open_web not in ["1","2","3","4","5","6","7","8","9","10","11"]:
                                        print("Oops. Please make your selection again.")
            
                                    else:
                                        # Referece: https://stackoverflow.com/questions/46416570/how-to-format-a-list-of-dictionaries-from-csv-python    
                                        # read from CSV file for user input (based on id) as another input to automated search using ChromeDriver 
                                        suggestion_list =[]                               
                                        with open(csv_file_path1) as f:
                                            reader = list(csv.reader(f))
                                            for row in reader[1:]:
                                                web_dict ={}
                                                web_dict["id"] = row[0]
                                                web_dict["name"] = row[1]
                                                web_dict["type"] = row[2]
                                                web_dict["website"] = row[3]
                                                suggestion_list.append(web_dict)
    
                                        def link_site(x):
                                            return x["id"] == open_web
    
                                        f_site = list(filter(link_site, suggestion_list))
    
                                        for st in f_site:
                                            site_search = st["website"]
    
                                        # Reference: class the Selenium package demonstration
                                        CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chromedriver.exe") # (or wherever yours is installed)
                                        driver = webdriver.Chrome(CHROMEDRIVER_PATH)
                                        
                                        # NAVIGATE TO GOOGLE.COM
                                        
                                        driver.get("https://www.google.com/")
                                        print(driver.title) #> Google
                                        file_name4_1 = "search_results_a" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + ".png"
                                        driver.save_screenshot(os.path.join(os.path.dirname(__file__), "..", "data", file_name4_1))
                                        
                                        # FIND AN ELEMENT TO INTERACT WITH...
                                        # a reference to the HTML element:
                                    
                                        searchbox_xpath = '//input[@title="Search"]'
                                        searchbox = driver.find_element_by_xpath(searchbox_xpath)
                                        
                                        # INTERACT WITH THE ELEMENT
                                        
                                        search_term = site_search
                                        searchbox.send_keys(search_term)
                                        searchbox.send_keys(Keys.RETURN)
                                        print(driver.title) #> user_input based on id - Google Search'
                                        file_name4_a = "search_results" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + ".png"
                                        driver.save_screenshot(os.path.join(os.path.dirname(__file__), "..", "data", file_name4_a))
                                        break                        
                                break       
                                
                            elif choice =="2":
                                print("------------------------------")
                                print("We understand ! Hopefully our service has helped you to plan appropriately.\n"
                                    "If you are interested, we will help you to navigate events or other things going on in your town now")

                                # Reference: class the Selenium package demonstration
                                CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chromedriver.exe") # (or wherever yours is installed)
    
                                driver = webdriver.Chrome(CHROMEDRIVER_PATH)
                                
                                # NAVIGATE TO GOOGLE.COM
                                
                                driver.get("https://www.google.com/")
                                print(driver.title) #> Google
                                file_name6_1 = "search_results_1" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + ".png"
                                driver.save_screenshot(os.path.join(os.path.dirname(__file__), "..", "data", file_name6_1)) 
                                
                                # FIND AN ELEMENT TO INTERACT WITH...
                                # a reference to the HTML element:
    
                                searchbox_xpath = '//input[@title="Search"]'
                                searchbox = driver.find_element_by_xpath(searchbox_xpath)
    
                                # INTERACT WITH THE ELEMENT
                                
                                # To convert user input to city name and country code for purposes of web search. (finding based on zipcode may not provide an efficient result to navigate through)
                                if user_input.isnumeric():
                                    search_term = "What are the things going on in" + " " + city_name + " " + city_code +" " + 'today or this weekend?'
                                else:    
                                    search_term = "What are the things going on in" + " " + user_input + " " + 'today or this weekend?'

                                searchbox.send_keys(search_term)
                                searchbox.send_keys(Keys.RETURN)
                                print(driver.title) #> city name and code - Google Search'
                                file_name6_a = "search_results_a" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + ".png"
                                driver.save_screenshot(os.path.join(os.path.dirname(__file__), "..", "data", file_name6_a))
                                break
                                
                            elif choice =="3":
                                print("------------------------------")
                                print("No problem. Perhaps, you can read more about the city. You may find it interesting! Here is the website that you can learn more about the city!")
                                
                                # Reference: class the Selenium package demonstration
                                CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chromedriver.exe") # (or wherever yours is installed)
    
                                driver = webdriver.Chrome(CHROMEDRIVER_PATH)
                                
                                # NAVIGATE TO GOOGLE.COM
                                
                                driver.get("https://www.google.com/")
                                print(driver.title) #> Google
                                file_name5_1 = "search_results_1" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + ".png"
                                driver.save_screenshot(os.path.join(os.path.dirname(__file__), "..", "data", file_name5_1)) 
                                
                                # FIND AN ELEMENT TO INTERACT WITH...
                                # a reference to the HTML element:
    
                                searchbox_xpath = '//input[@title="Search"]'
                                searchbox = driver.find_element_by_xpath(searchbox_xpath)
    
                                # INTERACT WITH THE ELEMENT
                                
                                # To convert user input to city name and country code for purposes of web search. (finding based on zipcode may not provide an efficient result to navigate through)
                                if user_input.isnumeric():
                                    search_term = "learn more about" + " " + city_name + " " + city_code
                                else:    
                                    search_term = "learn more about" + " " + user_input

                                searchbox.send_keys(search_term)
                                searchbox.send_keys(Keys.RETURN)
                                print(driver.title) #> city name and code - Google Search'
                                file_name5_a = "search_results_a" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + ".png"
                                driver.save_screenshot(os.path.join(os.path.dirname(__file__), "..", "data", file_name5_a))
                                break
    
                                # Let user decide to close the web browser. Once closing, it moves to the next.
                                
                            elif choice =="4":
                                print("OK. We hope we provided helpful information for you")
                                break
                                
                            else:
                                print("OOPS. We do not recognize your choice. Please choose again")
                                print("------------------------------")
                                
                        print("------------------------------")
                        # To provide user an option to receive email with the information including attachment. 
                        final_input = input("Would you like to also receive the output in the email? \n"
                            "We will send the current weather report in the email with your weather forecast attachement.\n"
                            "Press y to receive. Otherwise, press any key to exit: ")
                        if final_input =="y":
                            user_email_input = input("PLEASE ENTER YOUR EMAIL ADDRESS: ") # asking user email address for input.
                            SENDGRID_API_KEY = os.environ.get("sendgrid_api_key", "OOPS, please set env var called 'SENDGRID_API_KEY'")  #private information included in .env
                            SENDGRID_TEMPLATE_ID = os.environ.get("sendgrid_template_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'") #private information included in .env
                            MY_ADDRESS = os.environ.get("my_email_address", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'") #private information included in .env
                            template_data = {   
                                "human_friendly_timestamp": str(current_time.strftime("%Y-%m-%d %I:%M %p")),
                                "human_friednly_timestamp_local_time": str(localdatetime.strftime('%Y-%m-%d %I:%M %p')),
                                "city_name": str(city_name)+" " +str(city_code),
                                "current_weather_condition": str(weather_condition),
                                "currrent_weather_description": str(weather_description).title(),
                                "current_temp_C": str(toCelsius(last_refreshed_temp)),
                                "current_temp_F": str(toFahrenheit(last_refreshed_temp)),
                                "high_temp_C": str(toCelsius(last_refreshed_temp_max)),
                                "high_temp_F": str(toFahrenheit(last_refreshed_temp_max)),
                                "low_temp_C": str(toCelsius(last_refreshed_temp_min)),
                                "low_temp_F": str(toFahrenheit(last_refreshed_temp_min)),                                
                                "current_hum": str((last_refreshed_hum)),
                                "friendly_advice": str(my_message),
                            }
                            client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
                            print("CLIENT:", type(client))
                            message = Mail(from_email=MY_ADDRESS, to_emails=user_email_input) # For to_emails, MY_ADDRESS is replaced with user_input from line 133.
                            print("MESSAGE:", type(message))
                            message.template_id = SENDGRID_TEMPLATE_ID
                            message.dynamic_template_data = template_data
                            # Sending forecast report file as attached with email. #reference: https://stackoverflow.com/questions/43061813/attach-file-to-email-using-sendgrid
                            
                            with open(csv_file_path3, 'rb') as f:                            
                                data_email = f.read()
                                f.close()
                            encoded = base64.b64encode(data_email).decode()             # reference: https://github.com/sendgrid/sendgrid-python/issues/704
                            attachment = Attachment()
                            attachment.file_content = FileContent(encoded)
                            attachment.file_type = FileType('application/csv')
                            attachment.file_name = FileName(file_name3)
                            attachment.disposition = Disposition('attachment')
                            message.attachment = attachment
                            try:
                                response = client.send(message)
                                print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
                                print(response.status_code) #> 202 indicates SUCCESS
                                print(response.body)
                                print(response.headers)
                            except Exception as e:
                                print("OOPS", e.message)
                            print("Your forecast report has been sent to the email address that you provided.")
                            print("Thank you for using MyWeatherPy. We hope to see you again. Good-Bye ~") # A friendly message thanking the user and encouragin them to use the app again. 
                            print("------------------------------")
                            print("Any feedback for us? Please email us at myweatherpy@gmail.com and provide us an opportunity to improve our customer service for you.")
                            image_path = os.path.join(os.path.dirname(__file__), "..", "image", "myweatherpyimg2.jpg")
                            img = Image.open(image_path)
                            img.show()
                            exit()
                        else:
                            print("------------------------------")
                            print("Thank you, so much again for using MyWeatherPy. Hopefully, you will visit us again in the future!") # No email receipt unless user selects y.
                            print("------------------------------")
                            print("Any feedback for us? Please email us at myweatherpy@gmail.com and provide us an opportunity to improve our customer experience.")
                            print("Good-Bye~")
                            image_path = os.path.join(os.path.dirname(__file__), "..", "image", "myweatherpyimg2.jpg")
                            img = Image.open(image_path)
                            img.show()
                            exit() 
    
                    else:
                        print("ERROR: " +f"{response.status_code}")
                        if response.status_code ==404:
                            print("PAGE NOT FOUND OR SERVER NOT FOUND. PLEASE CHECK AND TRY AGAIN. GOOD-BYE.")
                            exit()
                                                
                except requests.ConnectionError:
                    print("failed to connect")
    
    
    
    
    
    
    
    
    