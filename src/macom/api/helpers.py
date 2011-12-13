# -*- encoding: utf-8 -*-
from cStringIO import StringIO # mas rápido que StringIO
from piston.emitters import Emitter
import codecs
import csv
import sys

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode('utf-8') for s in row])
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class CSVEmitter(Emitter):
    def render_record(self, element):
        record = []
        for field_name in element:
            field_value = element[field_name]
            if type(field_value) in [bool, int, long]:
                field_value = unicode(field_value)
            if 'encode' in dir(field_value):
                record.append(field_value)
        return record
    def render(self, request):
        data = self.construct()
        f = StringIO()
        try:
            w = UnicodeWriter(f)
            if type(data) in [list]:
                for element in data:
                    w.writerow(self.render_record(element))
            else:
                w.writerow(self.render_record(data))
            return f.getvalue()
        finally:
            f.close()

def callee_name():
    return sys._getframe(1).f_code.co_name

def flatten(seq):
    res = []
    for item in seq:
        if (isinstance(item, (tuple, list))):
            res.extend(flatten(item))
        else:
            res.append(item)
    return res
