__author__ = 'perar'
import cherrypy
import Database
import peewee
import json
from playhouse.shortcuts import *
from icalendar import Calendar, Event
from datetime import datetime
from cherrypy.lib.static import serve_file
from UIA import UIA
from Scraper import Scraper
import os.path

def default(obj):
    """Default JSON serializer."""
    import calendar, datetime

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    millis = int(
        calendar.timegm(obj.timetuple()) * 1000 +
        obj.microsecond / 1000
    )
    return millis

class Root: pass


class Admin:
    @cherrypy.expose
    def update(self, year, season):
        print("Starting update...")
        uia_courses = UIA(1)
        uia_subject = UIA(2)

        scraper = Scraper(season, year)
        scraper.scrape(uia_courses)

        scraper = Scraper(season, year)
        scraper.scrape(uia_subject)


        return "Done!"

class Course:

    @cherrypy.expose
    def list(self):
        return json.dumps([{
            'id': course.id,
            'name': course.name,
            'type': course.type,
            'season': course.season,
            'year': course.year
        } for course in peewee.SelectQuery(Database.Course, Database.Course.id, Database.Course.name, Database.Course.year, Database.Course.season, Database.Course.type)])

    @cherrypy.expose
    def item(self, id):

        course = model_to_dict(Database.Course.get(Database.Course.id == id))
        items = [model_to_dict(item) for item in Database.Subject.select().where(Database.Subject.course == course['id'])]
        dates = list(set([str(item["date_to"].date()) for item in items]))


        return json.dumps({
            'course': course,
            'items': items,
            'dates': dates
        }, default=default)


    @cherrypy.expose
    def info(self, id):
        course = model_to_dict(Database.Course.get(Database.Course.id == id))
        return json.dumps(course)


    @cherrypy.expose
    def ical(self, id):
        course = model_to_dict(Database.Course.get(Database.Course.id == id))
        items = Database.Subject.select().where(Database.Subject.course == course['id'])

        cal = Calendar()

        for item in items:
            event = Event()
            event.add('summary', item.activity)
            event.add('dtstart', item.date_from)
            event.add('dtend', item.date_to)
            event.add('dtstamp', datetime.now())
            event.add('organizer', item.educator)
            event.add('location', item.room)
            cal.add_component(event)

        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="{0}.ics"'.format(course['name'].replace(" ", "_"))
        cherrypy.response.headers['Content-Type'] = 'text/calendar'
        return cal.to_ical()






