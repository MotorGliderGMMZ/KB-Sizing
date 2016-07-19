import os

class Importer:

    def __init__(self, Component, VariableName, Default, Path = []):
        self.component = Component
        self.variableName = VariableName
        self.default = Default
        self.filePath = Path
    """
    Handler that takes care of opening different format files.
    Supported files are :
        *txt
        *excel
        *csv
        *matlab
        *xml
        """


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
        name, extension = os.path.splitext(filePath)
        return str(extension)

    ##### Importer selection based on file extension #####

    @property
    def getValue(self):
        """

        :return:
        """
        fileExt = self.fileExtension(self.filePath)

        if fileExt == ".xlsx":

            from IOPorters.excelIn import Excel as VarImporter

        elif fileExt == '.json':

            from IOPorters.jsonIn import JsonIn as VarImporter

        elif fileExt == '.mat':

            pass

        else:
            print ('LOG:    File type ' + repr(fileExt) + ' is not supported in this application. Variable '
                   + repr(self.variableName) + ' will set to the default value: ' + repr(self.default))
            return self.default

        myImporter = VarImporter(Component=self.component,
                                 VariableName=self.variableName,
                                 Default=self.default,
                                 filePath=self.filePath)

        return VarImporter.finder(myImporter)

