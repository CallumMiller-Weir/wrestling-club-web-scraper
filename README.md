# wrestling-club-web-scraper
## Overview
This script scrapes the British Wrestling club finder page (see [here](https://britishwrestling.org/club-finder/)) to fetch information about clubs and their contact details (phone, email, and address), and outputs the results in a JSON file.

## Requirements
To run this script, the dependencies are specified in the requirements.txt file. You can install all the required packages by running:

```pip install -r requirements.txt```

The requirements.txt file includes the following dependencies:
- selenium
- beautifulsoup4
- webdriver-manager

## How to Use
- Ensure you have Python v3.13.2 (or later) installed, which you can download [here](https://www.python.org/downloads/).
- Install the required dependencies (see above).
- Navigate to the root dir and execute the `run.bat` batch script.

## Notes
Please install Chrome before using:
- This script uses Chrome in headless mode (without UI) for efficient scraping.
- The script is intended for scraping dynamic web content and requires the ChromeDriver to function correctly.