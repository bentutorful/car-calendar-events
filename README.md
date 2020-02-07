# Car Calendar event scraper

Scrapes data from `https://www.carcal.co.uk/events/` and inserts them as Google Calendar events

## Prerequisites

- Python 3.6 or above

## Usage

To run the script

```
python index.py
```

When the program has formatted all the data, a browser tab will open asking you to login to Google (If not already signed in) and authenticate the application. Click `allow` when prompted.

Events are inserted with an event name, start date, end date (if applicable), and location.
