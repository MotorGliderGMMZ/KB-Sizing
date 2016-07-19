import json
import os

class JsonOut:

    def __init__(self,ListValues, outputPath):
        self.path = outputPath
        self.listValues = ListValues




    def writer(self):

        fout = open(self.path, 'w')
        json.dump(self.listValues, fout, indent=5, sort_keys=True)
        return "Output file correctly generated"