import json

import ndspy.fnt


class FilenamesTableEncoder(json.JSONEncoder):
    """
    A JSON encoder that allows filename tables to be encoded correctly.
    """
    def default(self, obj):
        if isinstance(obj, ndspy.fnt.Folder):
            d = {}
            d['first_id'] = obj.firstID
            if obj.files:
                d['files'] = obj.files
            if obj.folders:
                d['folders'] = obj.folders
            return d
        else:
            return super().default(obj)


def convertDictToFilenamesTable(d):
    """
    Given a dict representing a filenames table, return a corresponding
    actual filenames table.
    """
    thisFolder = ndspy.fnt.Folder(firstID = d['first_id'])
    thisFolder.files = d.get('files', [])
    for folderName, folderDict in d.get('folders', []):
        thisFolder.folders.append(folderName, convertDictToFilenamesTable(folderDict))
    return thisFolder


def fntToJson(table):
    """
    Convert a filename table to a JSON encoding of same.
    """
    return json.dumps(table, indent=4, cls=FilenamesTableEncoder)


def jsonToFnt(jsonData):
    """
    Convert a JSON representing a filename table to an actual filename
    table.
    """
    return convertDictToFilenamesTable(json.loads(jsonData))
