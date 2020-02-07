from datetime import datetime
from geopy.geocoders import Nominatim
import re

ALL_RAW_EVENTS = []
ALL_FORMATTED_EVENTS = []

def checkEventLocation(locality: str) -> bool:
    geolocator = Nominatim(user_agent="car_calendar")
    location = geolocator.geocode(locality)
    
    if ('United Kingdom' in location.address):
        return True
    return False

def formatDate(date: str) -> str:
    dateObject = datetime.strptime(date, '%d/%m/%Y')
    dateString = datetime.strftime(dateObject, '%Y-%m-%d')
    return dateString

def formatEventData(event):
    name: str = event.find('h2', itemprop='name').text
    date: str = event.find('meta', itemprop='startDate')['content']
    address: str = event.find('span', itemprop='streetAddress').text
    locality: str = event.find('span', itemprop='addressLocality').text

    print('Formatting ' + name)

    eventIsInCountry: bool = checkEventLocation(locality)

    if (not eventIsInCountry):
        return

    # NOTE some are single dates, some have start and end
    # i.e. dd/mm/yyyy - dd/mm/yyyy
    # look aheads on colon as dates are suffixed with :0900
    if (' - ' in date):
        startDate = re.search("(.*?)(?=\-)", date).group().strip()
        endDate = re.search("(?<=\-)(.*?)(?=\:)", date).group().strip()
        startDate = formatDate(startDate)
        endDate = formatDate(endDate)
    else:
        startDate = re.search("(.*?)(?=\:)", date).group().strip()
        startDate = formatDate(startDate)
        endDate = startDate

    eventData: dict = {
        "summary": name,
        "start": {
            "date": startDate
        },
        "end": {
            "date": endDate
        },
        "location": address + ', ' + locality
    }

    ALL_FORMATTED_EVENTS.append(eventData)

def getCurrentPageEvents(soup):
    events = soup.find_all('li', itemtype='http://schema.org/Event')
    for event in events:
        ALL_RAW_EVENTS.append(event)