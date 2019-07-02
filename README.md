# MyweatherPy (Freestyle Project) by ktg269, Youjam95 (This readme file have been adopted from readme file in 
(https://github.com/prof-rossetti/robo-advisor-demo-2019/blob/master/README.md) and modified specifically for this app.

## Introduction

Welcome to MyweatherPy Application ! (https://github.com/ktg269/myweatherpy)

This application ("app") will display the current weather information based on user input (Zip code or City name,country code) including 1) current time at the user's location, 2) local time at the searched location 3) weather condition, 4) temperature in Celcius and Fahrenheit, 5) humidity, and 6) friendly advice/recommendation based upon the weather condition. This app will also display the weather forecast for the next 5 days every 3 hours including all the above plus the high and low for the foreacst period. After that, the user is asked the reason for their search.
Depending upon the user input, customized result will display. User has an option to receipt the weather search result
in the email including the forecast information attached as a CSV file. 

This app uses openweather API (https://openweathermap.org/api) to provide the automated weather information for the current and the weather forecast. (See below set up section for more information)

## Prerequisites

  + Anaconda 3.7
  + Python 3.7
  + Pip
  + ChromeDriver (see installation section for instruction)

## Installation

Fork this repository under your own control, then clone or download the resulting repository onto your computer. Then navigate there from the command line:

```sh
cd myweaterpy
```

> NOTE: subsequent usage and testing commands assume you are running them from the repository's root directory.

Use Anaconda to create and activate a new virtual environment, perhaps called "myweatherpy-env": 

```sh
conda create -n myweatherpy-env python=3.7 # (first time only)
conda activate myweatherpy-env
```

From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: The requirements.txt include all packages that you need for running the application. If you still see error messages for part of or all packages, please install them individually using the following instructions:

```sh
To install requests package:   pip install requests

To install python-dotenv package:   pip install python-dotenv # note: NOT just "dotenv"

To install tzlocal package:   pip install pytz tzlocal

To install sendgrid package:   pip install sendgrid==6.0.5

To install pillow package:   pip install Pillow

To install selenium package:   pip install selenium

To install timezonefinder package:   pip install timezonefinder
```

This app also uses automated google search function depending upon your input using ChromeDriver. Please follow the below instructions if you do not have ChromeDriver installed already:

1. Go to the website (https://sites.google.com/a/chromium.org/chromedriver/)
2. Download the version that is appropriate for your operating system.
3. Unzip the file.
4. Place the file into data directory of your repository. This application detects the location of ChromeDriver using os.path.join(os.path.dirname(__file__)

## Setup

Before using this application, take a moment to [obtain an openweather API Key](https://openweathermap.org/api) (e.g. "abc123").

After obtaining an API Key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your real API Key:

    API_KEY="your key"

Please ensure that you save your real API key in .env file only and DO NOT update the myweatherpy.py script for your real API key in order to ensure your real API key is protected privately. 

## Usage

Run the recommendation script:

```py
python app/myweatherpy.py
```

## Testing

Install pytest (first time only):

```sh
pip install pytest
```

Run tests:

```sh
pytest robo_advisor_test.py






















