import threading
from gi.repository import GObject
from datetime import datetime

from view import *
from model import *

class Controller():
    def __init__(self):
        self.model = Model(self)
        self.view1 = View(self)
        self.fecha = self.view1.getDate()
        self.user = ""
        self.subjects = []
        GetEvents(self.fecha, self.subjects, self.model, self.view1).start()
    
    def on_close(self,w,e=None):
        Gtk.main_quit()
    
    def on_acercade(self,w):
        self.view1.showAcercade()
        
    def on_monthChanged(self,w):
        self.view1.clearMarks()
        self.fecha = self.view1.getDate()
        GetEvents(self.fecha, self.subjects, self.model, self.view1).start()
    
    def on_daySelected(self,w):
        self.view1.clearDescription()
        self.fecha = self.view1.getDate()
        if self.fecha.day in self.view1.getMarkedDays():
            GetDescription(self.fecha, self.subjects, self.model, self.view1).start()
    
    def on_callLogin(self,w):
        if self.view1.showLogin() == 1:
            self.user = self.view1.getLoginText()
            if self.user == "":
                self.subjects = []
            else:
                GetSubjects(self.user, self, self.model).start()
    
    def updateSubjects(self, subjects):
        self.subjects = subjects
        self.on_monthChanged(None)
        self.on_daySelected(None)

class GetEvents(threading.Thread):
    def __init__(self, fecha, subjects, model, view):
        super(GetEvents, self).__init__()
        self.fecha = fecha
        self.model = model
        self.view = view
        self.subjects = subjects
    
    def run(self):
        self.markedDays = self.model.getEventDays(self.fecha, self.subjects)
        GObject.idle_add(self.informar)
    
    def informar(self):
        self.view.markDays(self.markedDays, self.fecha)
        
class GetDescription(threading.Thread):
    def __init__(self, fecha, subjects, model, view):
        super(GetDescription, self).__init__()
        self.fecha = fecha
        self.model = model
        self.view = view
        self.text = []
        self.subjects = subjects
    
    def run(self):
        self.text = self.model.getEventDesc(self.fecha, self.subjects)
        GObject.idle_add(self.informar)
    
    def informar(self):
        self.view.showDescription(self.text, self.fecha)
        
        
class GetSubjects(threading.Thread):
    def __init__(self, user, controller, model):
        super(GetSubjects, self).__init__()
        self.user = user
        self.model = model
        self.controller = controller
    
    def run(self):
        subjects = self.model.getSubjects(self.user)
        GObject.idle_add(self.controller.updateSubjects, subjects)
        
        
