import os
from Tkinter import *
from tkFileDialog import askopenfilename
from Importers.excelAdvanced import ExcelAdvanced

class ImporterEx:

    '''
    Handler that takes care of opening different format files.
    Supperted files are :
        *txt
        *excel
        *csv
        *matlab
        *xml
    '''

    def callback():
        '''
        GUI to open a desired file.
        '''
        name = askopenfilename()
        return name

    filePath = callback()
    filename, file_extension = os.path.splitext(filePath)  # File extension for use in the rest of input file.

    errmsg = 'Error!'
    Button(text='File Open', command=callback).pack(fill=X)

    if file_extension == ".xlsx":

        #importer = ExcelImporter(filePath=filePath)
        importerADV = ExcelAdvanced(filePath=filePath)

        ###### Fuselage #####

        fuselageLength = ExcelAdvanced.fuselageLength(importerADV)
        fuselageRadius = ExcelAdvanced.fuselageRadius(importerADV)
        fuselageRadius2 = ExcelAdvanced.fuselageRadius2(importerADV)

    elif file_extension == '.txt':
        pass

    elif file_extension == '.dat':

        airfoilPath = str(filePath)

    else:
        print ("File type is not supported in this application. Please choose a different format")