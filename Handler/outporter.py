import os
import Output
from time import gmtime, strftime
import openpyxl
from tkMessageBox import *


class Outporter:


    def __init__(self, ListValues, Path, OutputExt):
        self.listValues = ListValues
        self.filePath = Path
        self.outputExt = OutputExt

    def fileName(self):
        """

        :return:
        """
        name, extension = os.path.splitext(self.filePath)
        return str(name)

    def fileExtension(self, filePath):
        # type: (object) -> object
        """

        :return:
        """
        if self.outputExt == 'as Input':
            name, extension = os.path.splitext(filePath)
        else:
            extension = self.outputExt
        return str(extension)

    ##### Importer selection based on file extension #####

    def writeValues(self):
        """

        :return:
        """
        fileExt = self.fileExtension(self.filePath)
        finalString = strftime("%d-%m-%Y %H" + "h %M" + "m %S" + "s", gmtime())

        if fileExt == ".xlsx":

            outputPath = os.path.dirname(Output.__file__) + '\output ' + finalString + '.xlsx'

            wb = openpyxl.Workbook()

            wb.save(outputPath)

            from IOPorters.excelOut import ExcelOut as VarOutporter

        elif fileExt == '.json':

            outputPath = os.path.dirname(Output.__file__) + '\output ' + finalString + '.json'

            from IOPorters.jsonOut import JsonOut as VarOutporter

        else:
            print ('Warning:    File type ' + repr(fileExt) + ' is not supported in this application. '
                                                              'The file will be exported in .json format.')
            showwarning("Warning", "File type " + repr(fileExt) + " is not supported in this application."
                                                                  " The file will be exported in .json format.")
            outputPath = os.path.dirname(Output.__file__) + '\output ' + finalString + '.json'

            from IOPorters.jsonOut import JsonOut as VarOutporter

        myOutporter = VarOutporter(ListValues=self.listValues,
                                   outputPath=outputPath)

        return VarOutporter.writer(myOutporter)