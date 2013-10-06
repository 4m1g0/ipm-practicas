import pycouchdb
from datetime import datetime

class Model():
    def __init__(self, controller):
        self.connect()
    
    def connect(self):
        try:
            couch = pycouchdb.Server("http://localhost:5984")
            self.db = couch.database("prueba")
            self.connected = True
        except:
            self.connected = False
            print("Error: No se pudo conectar con la base de datos")
    
    def getEventDays(self, fechaCalendario):
        if not self.connected:
            return []
        
        map_fun = '''function(doc) {
            if (doc.type == "Event") {
                emit(doc.id, doc.date);
            }
        }'''
        result = self.db.temporary_query(map_fun)
        days = []
        for row in result:
            fecha = datetime.strptime(row['value'], "%Y-%m-%d")
            if fecha.month == fechaCalendario.month and fecha.year == fechaCalendario.year:
                days.append(fecha.day)
        return days
