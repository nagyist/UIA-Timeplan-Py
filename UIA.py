__author__ = 'PerArne'
from Form import Form

class UIA:

    def __init__(self, type):

        # Init Form object
        self.form = Form()
        self.isCalendar = False

        # Courses
        if type == 1:
            self.form.EVENTTARGET = "LinkBtn_{0}".format("studentsets")
            self.form.tLinkType = "{0}".format("studentsets")
            self.form.RadioType2 = "XMLSpreadsheet;studentsetxmlurl;SWSCUST StudentSet XMLSpreadsheet"
        # Subjects
        elif type == 2:
            self.form.EVENTTARGET = "LinkBtn_{0}".format("modules")
            self.form.tLinkType = "{0}".format("modules")
            self.form.RadioType2 = "XMLSpreadsheet;modulexmlurl;SWSCUST Module XMLSpreadsheet"
        # Teacher
        elif type == 3:
            self.form.EVENTTARGET = "LinkBtn_{0}".format("staffmembers")
            self.form.tLinkType = "{0}".format("staffmembers")
            self.form.lbDays = "1-6"
            self.form.RadioType2 = "XMLSpreadsheet;staffmembersxmlurl;SWSCUST StaffMembers XMLSpreadsheet"
            self.form.RadioType = "XMLSpreadsheet;studentsetxmlurl;SWSCUST StudentSet XMLSpreadsheet"
            self.isCalendar = True
        # Room
        elif type ==4:
            self.form.EVENTTARGET = "LinkBtn_{0}".format("locations")
            self.form.tLinkType = "{0}".format("locations")
            self.form.lbDays = "1-6"
            self.form.RadioType2 = "XMLSpreadsheet;locationsxmlurl;SWSCUST Locations XMLSpreadsheet"
            self.form.RadioType = "XMLSpreadsheet;studentsetxmlurl;SWSCUST StudentSet XMLSpreadsheet"
            self.isCalendar = True




