# mytest.py

import pytest
import os
import datetime

from app.myweatherpy import easy_timestamp, toCelcius, toFahrenheit
from datetime import datetime

def test_easy_timestamp(): # to test timestamp
    t = datetime.today()
    assert easy_timestamp(t) == t.strftime("%Y-%m-%d %H:%M:%S")

def test_toCelcius():  # to test temporature conversions (from Kelvin to Celcius)

    assert int(303-273) == 30  

def test_toFahrenheit():  # to test temporature conversions (from Kelvin to Fahrenheit)

    assert int((303-273)*9/5+32) == 86  



