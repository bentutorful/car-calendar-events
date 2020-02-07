import urllib3
import events
import calendarapi
from bs4 import BeautifulSoup

def setPageSoup(n):
    page = 'https://www.carcal.co.uk/events/'

    if (n != 1):
        page += '?pno=%s'%(n)

    http = urllib3.PoolManager()
    response = http.request('GET', page)

    soup = BeautifulSoup(response.data, 'html.parser')

    return soup

def getPages(soup):
    pagination = soup.find_all('a', 'page-numbers')
    pageNumbers = []

    for page in pagination:
        pageNumbers.append(page.attrs['title'])

    pageNumbers = list(dict.fromkeys(pageNumbers))
    pageNumbers.sort()

    return pageNumbers

def main():
    soup = setPageSoup(1)
    pages = getPages(soup)

    # NOTE gets first page before the rest as this has a URL with no
    # query params, so we can't include it in the loop
    events.getCurrentPageEvents(soup)

    print('Getting page events')
    for page in pages:
        soup = setPageSoup(page)        
        events.getCurrentPageEvents(soup)

    print('Formatting page events')
    for event in events.ALL_RAW_EVENTS:
        events.formatEventData(event)
    print('Events formatted')

    calendarApi = calendarapi.CalendarAPI('https://www.googleapis.com/auth/calendar')
    calendarApi.batchInsertEvents(events.ALL_FORMATTED_EVENTS)

if (__name__ == "__main__"):
    main()