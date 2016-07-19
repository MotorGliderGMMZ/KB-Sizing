from parapy.core import *
from parapy.geom import *
from Example.importerEx import ImporterEx

class FuselageEx2(Base):

    @Input
    def fuselageLengthEx(self):
        return ImporterEx.fuselageLength+5

    @Input
    def radiusEx(self):
        return ImporterEx.fuselageRadius2

    @Input
    def Mach(self):
        return 0.7

    @Part
    def cylinderEx(self):
        return Cylinder(radius = self.radiusEx, height = self.fuselageLengthEx)

if __name__ == '__main__':
    from parapy.gui import display
    obj = FuselageEx()
    display(obj)