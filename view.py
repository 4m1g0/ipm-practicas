from gi.repository import Gtk
from datetime import datetime

class View():
    def __init__(self, controller):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("calendar1.glade")
        self.builder.connect_signals(controller)
        w = self.builder.get_object("window1")
        self.calendar = self.builder.get_object("calendar1")
        self.about = self.builder.get_object("aboutdialog1")
        self.markedDays = []
        w.show_all()
    
    def showAcercade(self):
        self.about.run()
        self.about.hide()

    def markDays(self, days, fecha):
        year, month, day = self.calendar.get_date()
        if fecha.year == year and fecha.month == month+1:
            self.markedDays = days
            for day in days:
                self.calendar.mark_day(day)
    
    def clearAll(self):
        self.markedDays = []
        self.calendar.clear_marks()
        
    def getDate(self):
        year, month, day = self.calendar.get_date()
        return datetime(year, month+1, day, 0, 0, 0)
    
    def getSelectedDay(self):
        year, month, day = self.calendar.get_date()
        return day
        
    def getMarkedDays(self):
        return self.markedDays
