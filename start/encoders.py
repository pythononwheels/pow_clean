#
# encoders for various output formats
# 
import io
import csv
import json
import dicttoxml


class Json():
    """
        calls the standard json module.
        this wrapper just enables us to decide wether or not 
        to ensure_ascii=True or False.
    """
    def __init__(self, ensure_ascii=False):
        print("  .. Json encoder got: ensure_ascii: " + str(ensure_ascii))
        self.ensure_ascii = ensure_ascii
    
    def dumps(self, data):
        return json.dumps(data, ensure_ascii=self.ensure_ascii)

class JsonToCsv():
    """ flattens json and converts the flattened
        data to csv
    """
    def flattenjson(self, mp, delim="_"):
        """ flattens a json. 
            separated nested keys are chained using delim
            {
                "a" : {
                    "b" : "1",
                    "c" : "2"
                }
            }
            rsults in =>
            {
                "a_b"   :  "1",
                "a_c"   :  "2",
            }
        """
        ret = []
        if isinstance(mp, dict):
            for k in mp.keys():
                csvs = self.flattenjson(mp[k], delim)
                for csv in csvs:
                    ret.append(k + delim + str(csv))
        elif isinstance(mp, list):
            for k in mp:
                csvs = self.flattenjson(k, delim)
                for csv in csvs:
                    ret.append(str(csv))
        else:
                ret.append(mp)

        return ret
    
    def dumps(self, data):
        """ dumps data to csv.
            data will be flattened before
        """
        flat_json = self.flattenjson(data)
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(flat_json)
        return output.getvalue()


class JsonToXml():
    def dumps(self, data, root="root"):
        """ returns the xml representation of a dict input data
        """
        #print(data)
        #print(dicttoxml.dicttoxml(data))
        return dicttoxml.dicttoxml(data)
