from PyQt4.QtCore import QSettings, QByteArray

class GeometryHelper(object):
    def __init__(self):
        pass

    def save(self, data, name):
        info = QSettings()
        info.setValue("geo/" + name, data)

    def load(self, name, default_value = None):
        info = QSettings()
        key = "geo/" + name
        if info.contains(key):
            return info.value(key, QByteArray()).toByteArray()
        return None