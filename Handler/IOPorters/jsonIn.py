import json


class JsonIn:

    def __init__(self, Component, VariableName, Default, filePath):
        with open(filePath) as data_file:
            self.data = json.load(data_file)
        self.component = Component
        self.variableName = VariableName
        self.default = Default

    def finder(self):

        try:
            component = self.data[self.component]
            value = component["Inputs"][self.variableName]["value"]
            print('LOG:    Value of ' + repr(self.variableName) + ' is set to: ' + repr(value))
        except KeyError:
            value = self.default
            print('LOG:    Could not find variable ' + repr(self.variableName) + '. Using the default value: ' \
            + repr(self.default))

        return value


