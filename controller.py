import threading
from gi.repository import GObject
from datetime import datetime

from view import *
from model import *

_ = gettext.gettext
N_ = gettext.ngettext

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
        self.view1.setStatus(_("Obteniendo dias marcados para el mes actual..."), 1)
        GetEvents(self.fecha, self.subjects, self.model, self.view1).start()
    
    def on_daySelected(self,w):
        self.view1.clearDescription()
        self.fecha = self.view1.getDate()
        if self.fecha.day in self.view1.getMarkedDays():
            self.view1.setStatus(_("Obteniendo eventos para el dia seleccionado..."), 1)
            GetDescription(self.fecha, self.subjects, self.model, self.view1).start()
    
    def on_callLogin(self,w):
        if self.view1.showLogin() == 1:
            self.user = self.view1.getLoginText()
            self.view1.setStatus(_("Obteniendo asignaturas para el usuario ") + self.user + "...", 1)
            GetSubjects(self.user, self, self.model, self.view1).start()
    
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
        self.view.statusPop()
        
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
        self.view.statusPop()
        
        
class GetSubjects(threading.Thread):
    def __init__(self, user, controller, model, view):
        super(GetSubjects, self).__init__()
        self.user = user
        self.model = model
        self.subjects = []
        self.controller = controller
        self.view = view
        
    def run(self):
        (subjects, subtype) = self.model.getSubjects(self.user)
        self.subjects = subjects
        GObject.idle_add(self.controller.updateSubjects, self.subjects)
        if (subtype != -1):
            GObject.idle_add(self.view.setStatus, _("Viendo eventos de ") + self.user, 0)
        else:
            GObject.idle_add(self.error)
    
    def error(self):
        self.view.clearStatus()
        self.view.showError()
        
        
        
