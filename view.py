from gi.repository import Gtk
from datetime import datetime
from gi.repository import Pango
import locale
import gettext
import os

locale.setlocale(locale.LC_ALL,'')
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")
locale.bindtextdomain('calendario', LOCALE_DIR)
gettext.bindtextdomain('calendario', LOCALE_DIR)
gettext.textdomain('calendario')
_ = gettext.gettext
N_ = gettext.ngettext

class View():
    def __init__(self, controller):
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain('calendario')
        self.builder.add_from_file("calendar1.glade")
        self.builder.connect_signals(controller)
        w = self.builder.get_object("window1")
        self.calendar = self.builder.get_object("calendar1")
        self.treeview = self.builder.get_object("treeview1")
        self.about = self.builder.get_object("aboutdialog1")
        self.liststore = Gtk.ListStore(str, str)
        self.treeview.set_model(model=self.liststore)
        columns = [_('Evento'), _('Tags')]
        for i in range(len(columns)):
            cell = Gtk.CellRendererText()
            if i == 0:
                cell.props.weight = Pango.Weight.BOLD
            col = Gtk.TreeViewColumn(columns[i], cell, text=i)
            col.set_min_width(160)
            self.treeview.append_column(col)
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
    
    def clearMarks(self):
        self.markedDays = []
        self.calendar.clear_marks()
    
    def clearDescription(self):
        self.liststore.clear()
        
    def getDate(self):
        year, month, day = self.calendar.get_date()
        return datetime(year, month+1, day, 0, 0, 0)
    
    def getSelectedDay(self):
        year, month, day = self.calendar.get_date()
        return day
        
    def getMarkedDays(self):
        return self.markedDays
    
    def showDescription(self, text, fecha):
        year, month, day = self.calendar.get_date()
        if fecha == datetime(year, month+1, day, 0, 0, 0):
            self.liststore.clear()
            for row in text:
                tags = ''
                for tag in row [1]:
                    tags = tags + ' ' + tag
                row[1] = tags
                self.liststore.append(row)
    
    
