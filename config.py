"""
Configuration settings for the election tracker.
"""
from datetime import datetime

# Data storage settings
DATA_DIR = "data"
CSV_FILE = "elections.csv"
JSON_FILE = "elections.json"

# Scraping settings
REQUEST_DELAY = 2.0  # Seconds between requests
MAX_RETRIES = 3
TIMEOUT = 10  # Request timeout in seconds

# Years to track
CURRENT_YEAR = datetime.now().year
YEARS_TO_TRACK = list(range(CURRENT_YEAR, CURRENT_YEAR + 7))  # Next 0-6 years

# States to track (can be expanded to all 50)
PRIORITY_STATES = [
    "California", "Texas", "Florida", "New York", "Pennsylvania",
    "Illinois", "Ohio", "Georgia", "North_Carolina", "Michigan",
    "New_Jersey", "Virginia", "Washington", "Arizona", "Massachusetts",
    "Tennessee", "Indiana", "Missouri", "Maryland", "Wisconsin",
    "Colorado", "Minnesota", "South_Carolina", "Alabama", "Louisiana"
]

ALL_STATES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New_Hampshire', 'New_Jersey', 'New_Mexico', 'New_York',
    'North_Carolina', 'North_Dakota', 'Ohio', 'Oklahoma', 'Oregon',
    'Pennsylvania', 'Rhode_Island', 'South_Carolina', 'South_Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
    'West_Virginia', 'Wisconsin', 'Wyoming'
]

# Office types to track
OFFICE_TYPES = [
    "State Senate",
    "State House",
    "County Commissioner",
    "Mayor",
    "City Council",
    "School Board"
]
