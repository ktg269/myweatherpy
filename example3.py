try:
                response = requests.get(url = request_url_1) or requests.get(url = request_url_2)  # to check HTTP response error
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