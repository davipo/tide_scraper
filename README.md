# Tide scraper

Lists low tides during daylight for specified locations.


## Installation

- Install Python 3.8 or later

- Clone this repo, or download the files
- Make a virtual environment (Use `python3 -m venv <path>` or another tool)
- Activate virtual environment (`source <path>/bin/activate`)
- `pip install selenium`

- Download chrome webdriver from `https://chromedriver.chromium.org/downloads`, unzip it
- Adjust `CHROMEDRIVER_PATH` in `scraper.py` to point to it
- `NUM_DAYS` can be adjusted for how many days of tides to list
- Additional locations can be added in `scraper.py`


## Run the scraper

`python scraper.py`

Note that this version does not use the correct sunrise and sunset times for
days following the current date.


## To Do

- Update to use correct sunrise and sunset times for all days
- Refactor to make reusable functions
- Make into a command-line tool, with options
 
