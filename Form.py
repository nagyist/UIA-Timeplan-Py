author = 'PerArne'

class Form:


    def __init__(self):
        self.VIEWSTATE = None
        self.VIEWSTATEGENERATOR = None
        self.EVENTVALIDATION = None
        self.EVENTTARGET = None
        self.EVENTARGUMENT = None
        self.LASTFOCUS = None
        self.tLinkType = None
        self.tWildcard = ""
        self.lbWeeks = None
        self.lbDays = None
        self.dlObject = None
        self.RadioType = None # Ralted to first POST
        self.RadioType2 = None # Related to second POST (gettimetable)
        self.bGetTimetable = "Vis timeplan"

    # First post (To retrieve the <select><option></option></select> list at default.aspx
    def first(self):
        structure = {
            '__EVENTTARGET': self.EVENTTARGET,
            '__EVENTARGUMENT': self.EVENTARGUMENT,
            '__LASTFOCUS': self.LASTFOCUS,
            '__VIEWSTATE': self.VIEWSTATE,
            '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            'tLinkType': self.tLinkType,
            'tWildcard': self.tWildcard,
            'lbWeeks': self.lbWeeks,
        }

        if self.lbDays != None:
            structure['lbDays'] = self.lbDays
        if self.RadioType != None:
            structure['RadioType'] = self.RadioType

        return structure


    def second(self):
        structure =  {
            '__EVENTTARGET': "",
            '__EVENTARGUMENT': "",
            '__LASTFOCUS': "",
            '__VIEWSTATE': self.VIEWSTATE,
            '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            'tLinkType': self.tLinkType,
            'tWildcard': self.tWildcard,
            'dlObject': self.dlObject,
            'lbWeeks': self.lbWeeks,
            'RadioType': self.RadioType2,
            'bGetTimetable': self.bGetTimetable
        }
        if self.RadioType2 != None:
            structure['RadioType'] = self.RadioType2
        return structure



    def validate(self):

        if self.VIEWSTATE == None:
            print("Error: Viewstate is None")
        if self.VIEWSTATEGENERATOR == None:
            print("Error Viewstategenrator is None")
        if self.EVENTVALIDATION == None:
            print("Error EVENTVALIDATION is None")
        if self.tLinkType == None:
            print("Error tLinkType is None")
        if self.dlObject == None:
            print("Error dlObject is None")
        if self.lbWeeks == None:
            print("Error lbWeeks is None")
        if self.lbDays == None:
            print("Error lbDays are None")
        if self.RadioType == None:
            print("Error RadioType is None")
        if self.bGetTimetable == None:
            print("Error bGetTimeTable is None")