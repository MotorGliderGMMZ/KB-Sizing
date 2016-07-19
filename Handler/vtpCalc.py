from __future__ import division
import os, sys
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import askopenfilename
from Main.Airfoil.airfoil import Airfoil
from Input import Airfoils


class VtpCalc(GeomBase):
    """
    Support class Vertical tail plane to perform all calculations
    """

    @Input
    def rcr(self):
        """
        Rudder chord ratio over root chord
        :Unit: [ ]
        :rtype: float
        source: Raymer
        """
        return .35

    @Input
    def aspectRatio(self):
        """
        Vertical tail plane aspect ratio, b^2 / S
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        if self.tailType == 'conventional':
            return 1.9
        else:
            return 1.35

    @Input
    def taperRatio(self):
        """
        Vertical tail plane taper ratio, tip chord / root chord
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        if self.tailType == 'conventional':
            return 0.3
        else:
            return 0.7

    @Input
    def sweep25(self):
        """
        Vertical tail plane sweep at quarter chord
        :Unit: [deg]
        :rtype: float
        source: KBE assignment support material
        """
        return 37.5

    @Input
    def vc(self):
        """
        Vertical tail volume coefficient
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        return .083

    @Input
    def tl(self):
        """
        Vertical tail plane arm
        :Unit: [m]
        :rtype: float
        """
        return 15.96

    @Input
    def tailType(self):
        """
        Tail type, could be "conventional", "cruciform" or "T tail"
        :Unit: [ ]
        :rtype: string
        """
        return 'T tail'

    @Input
    def surfaceWing(self):
        """
        Wing reference area
        :Unit: [m^2]
        :rtype: float
        """
        return 94.

    @Input
    def cMACWing(self):
        """
        Wing Mean aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.67

    @Input
    def spanWing(self):
        """
        Wing span, b
        :Unit: [m]
        :rtype: float
        """
        return 28.

    @Input
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return 36.

    @Input
    def conePos(self):
        """
        Aircraft tail cone most upper point vertical position
        :Unit: [m]
        :rtype: float
        """
        return 2.

    @Input
    def posFraction(self):
        """
        Wing position fraction of the fuselage, due to engine position
        :Unit: [m]
        :rtype: float
        """
        return .5

    @Input
    def crH(self):
        """
        Horizontal tail plane root chord
        :Unit: [m]
        :rtype: float
        """
        return 2.6

    @Input
    def longPosH(self):
        """
        Horizontal tail plane longitudinal position
        :Unit: [m]
        :rtype: float
        """
        return 33.16

    @Input
    def vertPosH(self):
        """
        Horizontal tail plane vertical position
        :Unit: [m]
        :rtype: float
        """
        return 2.


    window = Tk()
    window.wm_withdraw()

    # ### Attributes ##################################################################################################

    @Attribute
    def wingAC(self):
        """
        Wing aerodynamic center position, with respect to the fuselage nose
        :Unit: [m]
        :rtype: float
        """
        return self.posFraction * self.fuselageLength

    @Attribute
    def surface(self):
        """
        Vertical tail reference surface
        :Unit: [m^2]
        :rtype: float
        """
        return self.vc * self.surfaceWing * self.spanWing / self.tl

    @Attribute
    def span(self):
        """
        Vertical tail span, b
        :Unit: [m]
        :rtype: float
        """
        return sqrt(self.surface * self.aspectRatio)

    @Attribute
    def chordRoot(self):
        """
        Vertical tail root chord
        :Unit: [m]
        :rtype: float
        """
        return 2 * self.surface / ((1 + self.taperRatio) * self.span)

    @Attribute
    def chordTip(self):
        """
        Vertical tail tip chord
        :Unit: [m]
        :rtype: float
        """
        return self.taperRatio * self.chordRoot

    @Attribute
    def cMAC(self):
        """
        Vertical tail Mean Aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return (2/3) * self.chordRoot * (1 + self.taperRatio + self.taperRatio**2) / (1 + self.taperRatio)

    @Attribute
    def cMACyPos(self):
        """
        Vertical tail Mean Aerodynamic Chord position
        :Unit: [m]
        :rtype: float
        """
        return self.span * (1 + 2*self.taperRatio) / ((1 + self.taperRatio)*6)

    @Attribute
    def sweep50(self):
        """
        Vertical tail sweep angle calculated at half chord
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0.5 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepLE(self):
        """
        Vertical tail sweep angle calculated at Leading Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepTE(self):
        """
        Vertical tail sweep angle calculated at Trailing Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((1 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def longPos(self):
        """
        Vertical tail root longitudinal position, in order to have the calculated tail arm
        :Unit: [m]
        :rtype: float
        """
        return self.wingAC + self.tl - .25*self.chordRoot - self.cMACyPos * tan(radians(self.sweep25))

    @Attribute
    def vertPos(self):
        """
        Vertical tail root vertical position
        :Unit: [m]
        :rtype: float
        """
        return self.conePos

    @Attribute
    def pointsWakeHtp(self):
        """
        List of points representing the horizontal tail plane wake after separation flow on it
        :Unit: []
        :rtype: Points
        """
        return [Point(0, self.vertPosH, self.longPosH),
                Point(0, self.vertPosH + self.span, self.longPosH + self.span * tan(pi/6)),
                Point(0, self.vertPosH + self.span, self.longPosH + self.crH + self.span * tan(pi/3)),
                Point(0, self.vertPosH, self.longPosH + self.crH),
                Point(0, self.vertPosH, self.longPosH)]

    @Attribute
    def pointsRudder(self):
        """
        List of points representing the vertical tail rudder
        :Unit: []
        :rtype: Points
        """
        return [Point(0, self.vertPos, self.longPos + (1-self.rcr)*self.chordRoot),
                Point(0, self.vertPos + self.span, self.longPos + self.span * tan(radians(self.sweepLE)) + (1-self.rcr)*self.chordTip),
                Point(0, self.vertPos + self.span, self.longPos + self.span * tan(radians(self.sweepLE)) + self.chordTip),
                Point(0, self.vertPos, self.longPos + self.chordRoot),
                Point(0, self.vertPos, self.longPos + (1-self.rcr)*self.chordRoot)]

    @Attribute
    def rudderFree(self):
        """
        Rudder area portion free of htp wake, with respect to the total rudder area
        :Unit: [ ]
        :rtype: float
        """
        if self.check.faces == []:
            return 0
        else:
            return self.check.faces[0].area / self.rudder.area

    @Attribute
    def rudderBlanketed(self):
        """
        Rudder area portion blanketed by htp wake, with respect to the total rudder area
        :Unit: [ ]
        :rtype: float
        """
        return 1. - self.rudderFree


    # ###### Parts ####################################################################################################

    @Part
    def htpWake(self):
        """
        Horizontal tail plane wake 3D representation

        :rtype:
        """
        return PolygonalFace(self.pointsWakeHtp,
                             color='red',
                             transparency=.7)

    @Part
    def rudder(self):
        """
        Vertical tail plane rudder 3D representation

        :rtype:
        """
        return PolygonalFace(self.pointsRudder,
                             color='blue',
                             transparency=.7)

    @Part
    def check(self):
        """
        Intersection between rudder and htp wake, for the spin resistance check

        :rtype:
        """
        return Subtracted(shape_in=self.rudder, tool=self.htpWake,
                          color='black',
                          transparency=.7)

if __name__ == '__main__':
    from parapy.gui import display

    obj = VtpCalc()
    display(obj)
