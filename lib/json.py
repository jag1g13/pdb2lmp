import json
import os


class AttrDict(dict):
    """
    Class allowing dictionary entries to be accessed as attributes as well as keys.
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Parser:
    """
    Class to read data from JSON files.  Supports including other files and filtering a single section.
    """
    def __init__(self, filename, section=None):
        """
        Create a new CFG JSON parser.

        :param filename: JSON file to read
        :param section: Optional section to select from file
        """

        with open(filename) as f:
            self._json = json.load(f, object_hook=AttrDict)

        # Recurse through include lists and add to self._json
        while self._json.include:
            include_file = os.path.join(os.path.dirname(filename), self._json.include.pop())
            with open(include_file) as include_file:
                include_json = json.load(include_file, object_hook=AttrDict)

            for sec_name, sec_data in include_json.items():
                try:
                    self._json[sec_name] += sec_data
                except TypeError:
                    self._json[sec_name].update(sec_data)
                except KeyError:
                    self._json[sec_name] = sec_data

        self._records = self._json
        if section is not None:
            try:
                self._records = self._json[section]
            except KeyError as e:
                e.args = ("Section '{0}' not in file '{1}'".format(section, filename),)
                raise

    def __getitem__(self, item):
        return self._records[item]

    def __getattr__(self, item):
        return self._records[item]

    def __contains__(self, item):
        return item in self._records
