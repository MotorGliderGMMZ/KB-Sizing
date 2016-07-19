from openpyxl import Workbook
from openpyxl import load_workbook

class ExcelAdvanced:

    def __init__(self, filePath = 'C:\Users\Jacopo\Desktop\Academic\GitHub\KBE_Retake\Input\Files\input.xlsx'):
        self.excelFile = load_workbook(filePath)
        self.sheet = self.excelFile['Sheet1']

    wb = Workbook()

    def finder(self, componentName, valueName, Default):
        componentRead = None
        row = 1

        while componentRead != 'EOF':
            valueRead = None
            componentRead = str(self.sheet['A'+str(row)].value)

            if componentRead == componentName:
                while valueRead != valueName and valueRead != 'EOC':
                    valueRead = str(self.sheet['B'+str(row)].value)
                    row += 1
                if valueRead == valueName:
                    return self.sheet['C'+str(row-1)].value
                elif valueRead == 'EOC':
                    return Default
            if componentRead == 'EOF':
                return Default
            row += 1

    def fuselageLength(self): return float(self.finder('Fuselage', 'fuselageLength', Default = 30.0))

    def fuselageRadius(self): return float(self.finder('Fuselage', 'fuselageDiameter', Default = 5.0))

    def fuselageRadius2(self): return float(self.finder('Fuselage', 'fuselageRadius2', Default = 1.0))
