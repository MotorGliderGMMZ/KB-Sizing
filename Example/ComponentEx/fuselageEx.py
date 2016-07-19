from parapy.core import *
from parapy.geom import *
from Example.importerEx import ImporterEx

class FuselageEx(Base):

    ### Input propri del componente, possono essere cambiati qui ###

    @Input(label = 'Fuselage Length')
    def fuselageLengthEx(self):
        return ImporterEx.fuselageLength

    @Input(min = 1.)
    def radiusEx(self):
        return ImporterEx.fuselageRadius

    @Part
    def cylinderEx(self):
        return Cylinder(radius = self.radiusEx, height = self.fuselageLengthEx)

    Mach = Input(0.6, settable=False)

    ### Input passati da Airplane che non devono essere cambiati qui ###

    if __name__ == '__main__':
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def MachImportato(self):
        return 0.5

if __name__ == '__main__':
    from parapy.gui import display
    obj = FuselageEx()
    display(obj)