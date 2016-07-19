from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Handler.importer import Importer
import Tkinter, Tkconstants, tkFileDialog


class Fuselage(GeomBase):
    """
    Basic class Fuselage
    """

    @Input
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='Fuselage Length',
                              Default=8.57,
                              Path=self.filePath).getValue)

    @Input
    def fuselageSlenderness(self):
        """
        Aircraft nose slenderness, equal to nose length over fuselage diameter
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='Fuselage Slenderness',
                              Default=10.,
                              Path=self.filePath).getValue)

    @Input
    def numberSections(self):
        """
        Number of sections to be used in the construction of fuselage.
        :return:
        """
        return 50.


    @Attribute
    def fuselageSections(self):
        """
        Aircraft nose sections magnitude percentage
        x, y, r
        :Unit: [ ]
        :rtype: collections.Sequence[float]
        """
        sections = []
        number = int(round(self.numberSections))
        inc = 1 / number
        for i in range(0, number + 1):
            x = i * inc
            # r = -8.3455 * x**4 + 20.709 * x**3 - 17.273 * x**2 + 4.9759 * x + 0.0447
            r =  -7.9732 * x**4 + 19.918 * x**3 - 16.929 * x**2 + 5.0189 * x + 0.0096
            p = -1.027 * x**4 + 3.7455 * x**3 - 4.5225 * x**2 + 2.0679 * x - 0.2925
            row = [i * inc, p, r]
            sections.append(row)

        return sections

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ###################################################################

    if __name__ == '__main__':
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def maCruise(self):
        return float(Importer(Component='Performance',
                              VariableName='M cruise',
                              Default=0.7,
                              Path=self.filePath).getValue)

    @Input(settable=settable)
    def filePath(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        filename = tkFileDialog.askopenfilename()
        return str(filename)

    # ### Attributes ####################################################################################

    @Attribute
    def fuselageDiameter(self):
        """
        Aircraft Diameter
        :Unit: [m]
        :rtype: float
        """
        return self.fuselageLength / self.fuselageSlenderness

    # @Attribute
    # def outputList(self):
    #     lst = {}
    #
    #     inputs = {
    #         "Fuselage":
    #             {
    #                 "Inputs": {
    #                     "Fuselage Length": {"value": self.fuselageLength, "unit": "m"},
    #                     "Fuselage Diameter": {"value": self.fuselageDiameter, "unit": "m"},
    #                     "Tail Slenderness": {"value": self.tailSlendernessCalc, "unit": ""},
    #                     "Tail Up Angle": {"value": self.maxTailUp, "unit": "deg"}
    #                 },
    #                 "Attributes": {
    #                     "Tail divergence angle": {"value": self.tailDivergenceAngle, "unit": "deg"},
    #                     "Nose Slenderness": {"value": self.noseSlenderness, "unit": ""},
    #                     "Nose length": {"value": self.noseLength, "unit": "m"},
    #                     "Cylinder length": {"value": self.cylinderLength, "unit": "m"},
    #                     "Tail length": {"value": self.tailLength, "unit": "m"}
    #                 }
    #
    #             }
    #     }
    #
    #     lst.update(inputs)
    #     return lst


# #### part ############################################################################################

    @Part
    def fuselageSectionCurves(self):
        """
        Sequence of curves composing the nose section of fuselage
        :Unit: [ ]
        :rtype:
        """
        return Circle(quantify=len(self.fuselageSections),
                      radius=self.fuselageSections[child.index][2] * self.fuselageDiameter,
                      position=self.position.translate('z', self.fuselageLength * self.fuselageSections[child.index][0],
                                                       'y', self.fuselageDiameter * self.fuselageSections[child.index][1]),
                      hidden=True)


    @Part
    def loft(self):
        """
        3D solid representation of the fuselage
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid(profiles=self.fuselageSectionCurves, color="yellow", tolerance=1e-3)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Fuselage()
    display(obj)