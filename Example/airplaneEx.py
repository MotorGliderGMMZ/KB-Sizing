from parapy.core import *
from parapy.geom import *
from ComponentEx.fuselageEx import FuselageEx
from ComponentEx.fuselage2 import FuselageEx2
from ComponentEx.wingEx import WingEx

class AirplaneEx(Base):

    @Part
    def cylinder(self):
        return FuselageEx(MachImportato = self.cylinder2.Mach)

    @Part
    def cylinder2(self):
        return FuselageEx2()

    @Part
    def wingEx(self):
        return WingEx()

if __name__ == '__main__':
    from parapy.gui import display
    obj = AirplaneEx()
    display(obj)