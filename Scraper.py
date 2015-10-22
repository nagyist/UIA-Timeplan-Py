__author__ = 'PerArne'
import requests
from bs4 import BeautifulSoup
import Database
from peewee import IntegrityError
from datetime import datetime


class Scraper:


    def __init__(self, season, year):
        self.HOME = "http://timeplan.uia.no/swsuia{0}/restrict/no/default.aspx".format(season)
        self.TIMETABLE = "http://timeplan.uia.no/swsuia{0}/restrict/no/showtimetable.aspx".format(season)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'
        }


        self.year = year
        self.season = season
        self.form = {}

        # Create Session
        self.session = requests.Session()

        # Fetch main page
        result = self.session.get(self.HOME, headers=self.headers)

        # Parse html
        soup = BeautifulSoup(result.text, 'html.parser')

        # Populate form data
        self.form['__VIEWSTATE'] = soup.find(id="__VIEWSTATE")['value']
        self.form['__VIEWSTATEGENERATOR'] = soup.find(id="__VIEWSTATEGENERATOR")['value']
        self.form['__EVENTVALIDATION'] = soup.find(id="__EVENTVALIDATION")['value']
        self.form['lbWeeks'] = soup.find(id="lbWeeks").find_all("option")[1]["value"]

    def scrape(self, uia):

        form = uia.form
        form.VIEWSTATE = self.form['__VIEWSTATE']
        form.VIEWSTATEGENERATOR = self.form['__VIEWSTATEGENERATOR']
        form.EVENTVALIDATION = self.form['__EVENTVALIDATION']
        form.lbWeeks = self.form['lbWeeks']

        # POST default.aspx with Eventtarget
        r1 = self.session.post(self.HOME, data=form.first())

        # Parse html
        soup = BeautifulSoup(r1.text, 'html.parser')

        # Populate new form data
        form.VIEWSTATE = soup.find(id="__VIEWSTATE")['value']
        form.VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value']
        form.EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value']
        form.lbWeeks =  soup.find(id="lbWeeks").find_all("option")[1]["value"]

        # Parse html
        soup = BeautifulSoup(r1.text, 'html.parser')

        # Fetch all options
        options = [(option.text, option['value']) for option in soup.find(id="dlObject").find_all("option")]
        print("Found: {0} items to scrape!".format(len(options)))


        second_form = form.second()
        for option in options:
            name = option[0]
            code = option[1]


            second_form['dlObject'] = option[1]

            r2 = self.session.post(self.HOME, data=second_form, headers={
                'Host': 'timeplan.uia.no',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Origin': 'http://timeplan.uia.no',
                'Upgrade-Insecure-Requests': "1",
                'User-Agent':  self.headers['User-Agent'],
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': self.HOME,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'nb-NO,nb;q=0.8,no;q=0.6,nn;q=0.4,en-US;q=0.2,en;q=0.2'
            })

            db_couse = Database.Course(name=name, value=code, season=self.season, type=second_form['tLinkType'])
            try:
                db_couse.save()
                print("Item: {0}".format(name))
                self.parse(r2.text, True, uia.isCalendar, db_couse)
            except IntegrityError:
                print("Could not add {0}... IGNORING".format(name))
                db_couse = Database.Course.get(Database.Course.value == code)
                self.parse(r2.text, False, uia.isCalendar, db_couse)


    def parse(self, html, isNew, isCalendar, db_course):
        # Parse html
        soup = BeautifulSoup(html, 'html.parser')

        # Delete all existing records if not new
        if not isNew:
            query = Database.Subject.delete().where(Database.Subject.course == db_course.id)
            print("Deleted: {0} items.".format(query.execute()))


        if isCalendar:
            # Calendar Type
            pass

        else:
            # List Type

            for row in soup.find_all("tr", class_="tr2"):
                columns = row.find_all("td")

                day = columns[0].text
                date = columns[1].text
                times = columns[2].text.split("-")
                activity = columns[3].text
                room = columns[4].text
                educator = columns[5].text

                # 20 Aug 09.15
                date_object_from = datetime.strptime("{0} {2} {1}".format(date, times[0], self.year), "%d %b %Y %H.%M")
                date_object_to = datetime.strptime("{0} {2} {1}".format(date, times[0], self.year), "%d %b %Y %H.%M")

                db_subject = Database.Subject(
                    date_from=date_object_from,
                    date_to=date_object_to,
                    room=room,
                    activity=activity,
                    educator=educator,
                    course=db_course.id
                )
                db_subject.save()






            pass



