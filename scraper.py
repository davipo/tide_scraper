"""
Tide scraper exercise
David "Davi" Post, david.post@pobox.com
2022-10
"""

from datetime import datetime
import os
import re

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By

NUM_DAYS = 5  # number of days to list tides for (up to 30)

CHROMEDRIVER_PATH = os.path.expanduser('~/Devel/chromedriver')
URL_TEMPLATE = 'https://www.tide-forecast.com/locations/{}/tides/latest'

TIME_REGEX = r'(\d{1,2}:\d{2}[ap]m)'
SUN_REGEX = 'Sunrise is at ' + TIME_REGEX + ' and sunset is at ' + TIME_REGEX
SUN_PATTERN = re.compile(SUN_REGEX)

locations = """
Half Moon Bay, California
Huntington Beach, California
Providence, Rhode Island
Wrightsville Beach, North Carolina
""".strip().splitlines()  # make a list


chrome_service = webdriver.chrome.service.Service(executable_path=CHROMEDRIVER_PATH)
chrome_options = webdriver.chrome.options.Options()
chrome_options.headless = True
browser = webdriver.Chrome(service=chrome_service, options=chrome_options)


for location in locations:
    print(f'Daylight low tides for {location}:')
    location_code = location.replace(',', '').replace(' ', '-')
    browser.get(URL_TEMPLATE.format(location_code))
    
    try:
        summary = browser.find_element(By.CLASS_NAME, 'tide-header-summary')
    except NoSuchElementException:
        print('location not found\n')
        continue
    
    sun_times = SUN_PATTERN.search(summary.text).groups()
    sunrise, sunset = [datetime.strptime(sun_time, '%I:%M%p') for sun_time in sun_times]
    #   Note: only valid for first day
        
    day_tables = browser.find_elements(By.CLASS_NAME, 'tide-day-tides')
    for table in day_tables[:NUM_DAYS]:
        rows = table.find_elements(By.TAG_NAME, 'tr')
        # TODO: If table with class tide-day__sun-moon follows,
        #  read it to update sunrise and sunset 
        for row in rows[1:]:  # skip row 0, it is header
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) != 3:
                break  # bad row
            tide, tide_time, tide_height = [cell.text for cell in cells]
            row_text = (tide_time + ' ' + tide_height).replace('\n', ' ')
            tide_time = tide_time.split('\n')[0]  # remove date
            if tide.startswith('Low'):
                tide_datetime = datetime.strptime(tide_time, '%I:%M %p') 
                if sunrise < tide_datetime < sunset:
                    print(row_text)
    print()

browser.quit()

