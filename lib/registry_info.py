import json
import os
from lib.platform import Platform
import base64
import logging
logger = logging.getLogger(__name__)

class RegistryInfo:
    """
    Encapsulates all the information for an single registry key, enabling simple comparison via a json packet.  The
    instance does not capture parent/child relationships, only current key name + the attributes at that key.

    The information here is stored in a database.
    """
    def __init__(self, path, attributes_tuple):
        self.__key_name = path
        self.__attributes = attributes_tuple

    def to_json(self):
        return json.dumps(self.__attributes)

    def encodeRegValuesJson(self):
        encodedvalues = []
        x = ()
        for v in self.__attributes:
            if isinstance(v[1], str): 
                x = (v[0], base64.b64encode(v[1]), v[2] ) # reconstruct an encoded tuple
            else: 
                x = v
            encodedvalues.append(x)
        obj = json.dumps(encodedvalues)
        
        return obj
    
    @staticmethod
    def from_json(name, atts_json):
        values = [] 
        tuple_data = json.loads(atts_json)
        for v in tuple_data:
            try:
                x = ( v[0], base64.b64decode(v[1]), v[2])
            except:
                x = ( v[0], v[1], v[2] )
                pass
            values.append(x)
        #print "decodde: ", atts_json, " to ", values, " for:", name
        return RegistryInfo(name, values) 
    @property
    def key(self):
        return self.__key_name

    @property
    def values(self):
        return self.__attributes

    @property
    def parentKey(self):
        if not "\\" in self.__key_name: 
            return 99
        parent = os.path.split(self.__key_name.replace("\\", "/"))[0]
        return parent.replace("/", "\\")
    
    @property
    def keyBaseName(self):
        if not "\\" in self.__key_name:
            return self.__key_name
        return os.path.basename(self.__key_name.replace("\\", "/")) 
    


    def __str__(self):
        return u"RegistryInfo: " + unicode(self.__key_name) + u", values:" + unicode(self.__attributes)
