__author__ = 'PerArne'

from Scraper import Scraper
from UIA import UIA
import Database
from datetime import date
import API
import cherrypy
import wsgiref.handlers
import threading

def start_api():

    root = API.Root()
    root.course = API.Course()

    cherrypy.quickstart(root)


def start_scraper(uia_object):
    scraper = Scraper(season, year)
    scraper.scrape(uia_object)



def do_input():
    season = ""
    while True:
        season = input('Which season (v or h): ')

        try:
            year = int(input("Which year (default: {0}): ".format(date.today().year)))
        except ValueError:
            year = date.today().year

        if season == "g" or season == "h":
            break
    return season, year






if __name__ == "__main__":

    # Start WEB API
    t = threading.Thread(target=start_api)
    t.daemon = True
    t.start()

    # Input
    season, year = do_input()

    # Database definitions
    Database.Teacher.create_table(fail_silently=True)
    Database.Course.create_table(fail_silently=True)
    Database.Subject.create_table(fail_silently=True)

    # Scraping objects
    uia_courses = UIA(1)
    uia_subject = UIA(2)
    uia_teacher = UIA(3)
    uia_room = UIA(4)

    # Start Scraper thread (COURSE)
    for t in [
        threading.Thread(target=start_scraper, args=(uia_courses,)),
        threading.Thread(target=start_scraper, args=(uia_subject,)),
        #threading.Thread(target=start_scraper, args=(uia_teacher,)),
        #threading.Thread(target=start_scraper, args=(uia_room,)),
    ]:
        t.daemon = True
        t.start()

    input('Pres ENTER to exit...')
    input('Pres ENTER again to exit...')