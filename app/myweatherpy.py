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


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId
from dotenv import load_dotenv
from datetime import datetime, timezone
from pytz import timezone
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from timezonefinder import TimezoneFinder

load_dotenv()

API_KEY =os.environ.get("openweather_API") # to obtain API_KEY from env file. 


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
        "If you would like to search for U.S. cities, please enter 5-digit zip code (e.g. 10004) for the most accurate result.\n" 
        "For non-U.S, please ensure to enter BOTH city name and two-letter country code (london,uk) for the best result. \n"
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
                        print(f'{row[0]}, {row[1]} {row[2]}')
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

        elif user_input in ["!","@","#","$","%","^","&","*",")","(","-","_","=","+","[","}","[","{",":",";","'",'"',"/","?",".",">",",","<","`","~"]:
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


                    current_time = datetime.now()  #> current time
                    formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")  #>'2019-06-21 14:00:00' (reference: from prior class discussion)
                    
                    local_lon = data["coord"]["lon"] # To set up local time (based on input) using latitude/longitutde
                    local_lat = data["coord"]["lat"]
                    
                    tf = TimezoneFinder(in_memory=True) # Reference: https://pypi.org/project/timezonefinder/
                    timezone_region = tf.closest_timezone_at(lng=local_lon, lat=local_lat)
                    
                    utcmoment_naive = datetime.utcnow() # Reference: https://stackoverflow.com/questions/10997577/python-timezone-conversion
                    utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
                    localdatetime = utcmoment.astimezone(pytz.timezone(timezone_region))
                    formatted_localdatetime = localdatetime.strftime('%Y-%m-%d %H:%M:%S')
                    formatted_localdatetimezone = localdatetime.strftime('%Z')
                    

                    # Set up a variable for latest refresh time at timezone where the script is run (the region for the search)
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
                    #print(f"{my_time.strftime('%Y-%m-%d %H:%M:%S')}" + "  " f"{(my_time2.strftime('%Z'))}")

                    #print(my_time)
                                   

                    #localrefreshdatetime = utcmoment.astimezone(pytz.timezone(my_time))
                    #formatted_localrefreshdatetime = localrefreshdatetime.strftime('%Y-%m-%d %H:%M:%S')
                    #print(formatted_localrefreshdatetime)

                    # To show the current time at the local time zone
                    #last_refreshed_local_time = datetime.fromtimestamp(last_time).strftime('%Y-%m-%d %H:%M:%S')
                    #current_local_time = datetime.fromtimestamp(unix_timestamp)
                    #friendly_current_local_time = current_local_time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    #friendly_local_time = datetime.fromtimestamp(unix_timestamp)   #reference: https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
                    #friendly_local_timezone = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unix_timestamp))  #TODO: Need to fix the timezone display
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
                    print("Current Local Time based on your input:  " f"{formatted_localdatetime}" " " f"{formatted_localdatetimezone}")
                    print("Current Time based on your location: " f"{formatted_current_time}" " " f"{formatted_my_time2}")
                    #print("Last Refreshed at local time: " f"{last_refreshed_local_time}" + "  " f"{friendly_local_timezone}")
                    print("Last Refreshed based on your location: " f"{formatted_my_time}" + "  " f"{formatted_my_time2}")                  
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
                    csv_headers = ["City", "Code", "My Time", "Local Time", "Weather", "Temp(C)", "Temp(F)", "Humidity(%)"]
                    with open(csv_file_path2, "w", newline='') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                        writer.writeheader() # uses fieldnames set above
                        writer.writerow({
                            "City": city_name,
                            "Code": city_code,
                            "My Time": formatted_current_time,
                            "Local Time": formatted_localdatetime,
                            "Weather": weather_condition,
                            "Temp(C)": toCelcius(last_refreshed_temp),
                            "Temp(F)": toFahrenheit(last_refreshed_temp),
                            "Humidity(%)": last_refreshed_hum,
                        })
                    print("Your result has been saved in /data folder with city name, code and current time")
                    print("-------------------------")
                else:
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
                   
                    # Set up a variable for f

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
                            print(f"{forecast_my_time.strftime('%Y-%m-%d %I %p')} \t{forecast_weather2} \t{toCelcius(forecast_temp)}C \t{toCelcius(forecast_temp_high)}C \t{toCelcius(forecast_temp_min)}C \t{toFahrenheit(forecast_temp)}F \t{toFahrenheit(forecast_temp_high)}F \t{toFahrenheit(forecast_temp_min)}F \t{forecast_hum}%")

                            file_name3 = "forecast" + city_name + city_code + current_time.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
                            csv_file_path3 = os.path.join(os.path.dirname(__file__), "..", "data", file_name3)

                            csv_headers = ["City", "Code", "Time", "Temp(C)", "Temp(F)", "Humidity(%)"]

                            with open(csv_file_path3, "w", newline='') as csv_file:
                                writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                                writer.writeheader() # uses fieldnames set above

                                for x in list_forecast:
                                    writer.writerow({
                                        "City": city_name,
                                        "Code": city_code,
                                        "Time": datetime.fromtimestamp(float(x["dt"]), my_timezone).strftime("%Y-%m-%d %I %p"),
                                        #"Weather": list(map(lambda x: x["main"]["weather"]["main"], list_forecast)),
                                        "Temp(C)": toCelcius(x["main"]["temp"]),
                                        "Temp(F)": toFahrenheit(x["main"]["temp"]),
                                        "Humidity(%)": x["main"]["humidity"]
                                })
                    print("-------------------------") 
                    print("Your result has been saved in /data folder under name forecast, city name, code and current time.")                       
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
                                        print(f'is, name, type, website:')
                                        print("-------------------------")
                                        line_count += 1
                                    else:
                                        dict_csv = f'{row[0]} {row[1]}, {row[2]}, {row[3]}'                                                                        
                                        print(dict_csv)
                                        line_count += 1         
                            print("-------------------------")
                            while True:
                                open_web = input("If you want to navigate any website above, please press the number: ")
                                if open_web not in ["1","2","3","4","5","6","7","8","9","10","11"]:
                                    print("Oops. Please make your selection again.")
                                    break
                                else:
                                    # Referece: https://stackoverflow.com/questions/46416570/how-to-format-a-list-of-dictionaries-from-csv-python    
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
                                    #
                                    # NAVIGATE TO GOOGLE.COM
                                    #
                                    driver.get("https://www.google.com/")
                                    print(driver.title) #> Google
                                    driver.save_screenshot("search_page.png")  
                                    #
                                    # FIND AN ELEMENT TO INTERACT WITH...
                                    # a reference to the HTML element:
                                    # <input title="Search">
                                    searchbox_xpath = '//input[@title="Search"]'
                                    searchbox = driver.find_element_by_xpath(searchbox_xpath)
                                    #
                                    # INTERACT WITH THE ELEMENT
                                    #
                                    search_term = site_search
                                    searchbox.send_keys(search_term)
                                    searchbox.send_keys(Keys.RETURN)
                                    print(driver.title) #> user_input city or zipcode - Google Search'
                                    driver.save_screenshot("search_results.png")
                                    break
                                   
                            
                        elif choice =="2":
                            print("We understand ! Hopefully our service has helped you to plan appropriately.")
                            
                            
                        elif choice =="3":
                            print("No problem. Perhaps, you can read more about the city. You may find it interesting! Here is the website that you can learn more about the city!")
                            # Reference: class the Selenium package demonstration
                            CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chromedriver.exe") # (or wherever yours is installed)

                            driver = webdriver.Chrome(CHROMEDRIVER_PATH)
                            #
                            # NAVIGATE TO GOOGLE.COM
                            #
                            driver.get("https://www.google.com/")
                            print(driver.title) #> Google
                            driver.save_screenshot("search_page.png")  
                            #
                            # FIND AN ELEMENT TO INTERACT WITH...
                            # a reference to the HTML element:
                            # <input title="Search">

                            searchbox_xpath = '//input[@title="Search"]'
                            searchbox = driver.find_element_by_xpath(searchbox_xpath)

                            #
                            # INTERACT WITH THE ELEMENT
                            #

                            if user_input.isnumeric():
                                search_term = city_name + " " + city_code
                            else:    
                                search_term = user_input
                            searchbox.send_keys(search_term)
                            searchbox.send_keys(Keys.RETURN)
                            
                            print(driver.title) #> user_input city or zipcode - Google Search'
                            driver.save_screenshot("search_results.png")
                            

                            # Let user decide to close the web browser. Once closing, it moves to the next.
                            
                        elif choice =="4":
                            print("OK. We hope we provided helpful information for you")
                            
                            
                            
                        else:
                            print("OOPS. We do not recognize your choice. Please choose again")
                            print("------------------------------")
                            
                        print("------------------------------")
                        final_input = input("Would you like to also receive the output in the email? \n"
                            "We will send the current weather report in the email with your forecast input attachement.\n"
                            "Press y to receive. Otherwise, press any key to exit: ")
                        if final_input =="y":
                            user_email_input = input("PLEASE ENTER YOUR EMAIL ADDRESS: ") # asking user email address for input.

                            SENDGRID_API_KEY = os.environ.get("sendgrid_api_key", "OOPS, please set env var called 'SENDGRID_API_KEY'")  #private information included in .env
                            SENDGRID_TEMPLATE_ID = os.environ.get("sendgrid_template_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'") #private information included in .env
                            MY_ADDRESS = os.environ.get("my_email_address", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'") #private information included in .env

                            template_data = {   # showing the checkout timestamp and the total price on the email receipt (minimum level of information per instruction)
                                "human_friendly_timestamp": str(current_time.strftime("%Y-%m-%d %I:%M %p")),
                                "city_name": str(city_name)+" " +str(city_code),
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

                            # Sending forecast report file as attached with email. #reference: https://stackoverflow.com/questions/43061813/attach-file-to-email-using-sendgrid
                            with open(csv_file_path3, 'rb') as f:                             #https://github.com/sendgrid/sendgrid-python/issues/704
                                data_email = f.read()
                                f.close()
                            encoded = base64.b64encode(data_email).decode()
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

                            print("Your forecast report has been sent to the email address that your provided.")
                            print("Thank you for using MyweatherPy. We hope to see you again. Good-Bye ~") # A friendly message thanking the customer and/or encouraging the customer to shop again
                            print("Any feedback for us? Please email us at myweatherpy@gmail.com and provide us an opportunity to improve our customer experience.")
                            image_path = os.path.join(os.path.dirname(__file__), "..", "image", "myweatherpyimg1.jpg")
                            img = Image.open(image_path)
                            img.show()
                            exit()

                        else:
                            print("------------------------------")
                            print("Thank you, so much again for using MyweatherPy. Hopefully, you will visit us again in the future!") # No email receipt if customer does not select y.
                            print("------------------------------")
                            print("Any feedback for us? Please email us at myweatherpy@gmail.com and provide us an opportunity to improve our customer experience.")
                            print("Good-Bye~")
                            image_path = os.path.join(os.path.dirname(__file__), "..", "image", "myweatherpyimg1.jpg")
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




