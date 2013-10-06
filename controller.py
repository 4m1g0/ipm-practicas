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
        GetEvents(self.fecha, self.model, self.view1).start()
    
    def on_close(self,w,e=None):
        Gtk.main_quit()
    
    def on_acercade(self,w):
        self.view1.showAcercade()
        
    def on_monthChanged(self,w):
        self.view1.clearAll()
        self.fecha = self.view1.getDate()
        GetEvents(self.fecha, self.model, self.view1).start()

class GetEvents(threading.Thread):
    def __init__(self, fecha, model, view):
        super(GetEvents, self).__init__()
        self.fecha = fecha
        self.model = model
        self.view = view
    
    def run(self):
        self.markedDays = self.model.getEventDays(self.fecha)
        GObject.idle_add(self.informar)
    
    def informar(self):
        self.view.markDays(self.markedDays, self.fecha)
