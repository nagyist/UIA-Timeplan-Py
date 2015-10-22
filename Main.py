__author__ = 'PerArne'

from Scraper import Scraper
from UIA import UIA
import Database
from datetime import date


if __name__ == "__main__":

    season = ""
    while True:
        season = input('Which season (g or h): ')

        try:
            year = int(input("Which year (default: {0}): ".format(date.today().year)))
        except ValueError:
            year = date.today().year

        if season == "g" or season == "h":
            break


    Database.Teacher.create_table(fail_silently=True)
    Database.Course.create_table(fail_silently=True)
    Database.Subject.create_table(fail_silently=True)




    uia_courses = UIA(1)
    uia_subject = UIA(2)
    uia_teacher = UIA(3)
    uia_room = UIA(4)


    # Start scraper
    scraper = Scraper(season, year)


    scraper.scrape(uia_courses)
    scraper.scrape(uia_subject)


    # Scrape difficulties
    #scraper.scrape(uia_teacher)
    #scraper.scrape(uia_room)