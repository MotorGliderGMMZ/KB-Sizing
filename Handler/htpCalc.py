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
import Tkinter, Tkconstants, tkFileDialog


class HtpCalc(GeomBase):
    """
    Support class horizontal tail plane to perform all calculations
    """

    @Input
    def hVertPerc(self):
        """
        Horizontal height of htp in percentage with respect to vtp span
        :Unit: [ ]
        :rtype: float
        """
        return .75
    @Input
    def aspectRatio(self):
        """
        Horizontal tail plane aspect ratio, b^2 / S
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        return 5.

    @Input
    def taperRatio(self):
        """
        Horizontal tail plane taper ratio, tip chord / root chord
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        return .4

    @Input
    def sweep25(self):
        """
        Horizontal tail plane sweep at quarter chord
        :Unit: [deg]
        :rtype: float
        source: KBE assignment support material
        """
        return 10 + self.sweep25Wing

    @Input
    def vc(self):
        """
        Horizontal tail volume coefficient
        :Unit: [ ]
        :rtype: float
        source: KBE assignment support material
        """
        return 1.

    @Input
    def tailType(self):
        """
        Tail type, could be "conventional", "cruciform" or "T tail"
        :Unit: [ ]
        :rtype: string
        """
        return 'cruciform'

    @Input
    def sweep25Wing(self):
        """
        Wing sweep angle calculated at quarter chord
        :Unit: [deg]
        :rtype: float
        """
        return 28.75

    @Input
    def surfaceWing(self):
        """
        Wing reference area
        :Unit: [m^2]
        :rtype: float
        """
        return 84.54

    @Input
    def cMACWing(self):
        """
        Wing Mean aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.48

    @Input
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return 30.

    @Input
    def conePos(self):
        """
        Aircraft tail cone vertical position
        :Unit: [m]
        :rtype: float
        """
        return 1.05

    @Input
    def posFraction(self):
        """
        Wing position fraction of the fuselage, due to engine position
        :Unit: [m]
        :rtype: float
        """
        return .5

    @Input
    def spanV(self):
        """
        Vertical tail span
        :Unit: [m]
        :rtype: float
        """
        return 4.42

    @Input
    def sweepLEV(self):
        """
        Vertical tail sweep, evaluated at leading edge
        :Unit: [deg]
        :rtype: float
        """
        return 42.

    @Input
    def cMACyPosV(self):
        """
        Vertical tail MAC position
        :Unit: [m]
        :rtype: float
        """
        return 1.04

    @Input
    def cMACV(self):
        """
        Vertical tail Mean Aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.31

    @Input
    def chordRootV(self):
        """
        Vertical tail root chord
        :Unit: [m]
        :rtype: float
        """
        return 3.85

    @Input
    def chordTipV(self):
        """
        Vertical tail tip chord
        :Unit: [m]
        :rtype: float
        """
        return 2.69

    @Input
    def tlV(self):
        """
        Vertical tail tip chord
        :Unit: [m]
        :rtype: float
        """
        return 12.9

    @Input
    def longPosV(self):
        """
        Vertical tail plane longitudinal position
        :Unit: [m]
        :rtype: float
        """
        return 26.14

    @Input
    def vertPosV(self):
        """
        Vertical tail plane vertical position
        :Unit: [m]
        :rtype: float
        """
        return 1.05

    @Input
    def rcr(self):
        """
        Rudder chord ratio over root chord
        :Unit: [ ]
        :rtype: float
        source: Raymer
        """
        return .35

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
    def tlDecrement(self):
        """
        Tail arm decrement
        :Unit: [m]
        :rtype: float
        """
        return .0001 * self.fuselageLength

    @Attribute
    def tl(self):
        """
        Horizontal tail arm
        :Unit: [m]
        :rtype: float
        """
        if self.tailType == 'conventional':
            tl = self.fuselageLength  # first guess for tail arm
            TR = self.taperRatio
            cR = self.cMACWing  # first guess for the tail root chord
            posYMAC = 10.  # first guess for the tail MAC position

            while (self.fuselageLength - (self.wingAC + tl + 0.75*cR - posYMAC * tan(radians(self.sweep25)))) < 0:
                tl = tl - self.tlDecrement
                cR = 2/(1 + TR) * sqrt((self.vc * self.cMACWing * self.surfaceWing)/(self.aspectRatio * tl))
                posYMAC = (1+2*TR)/((1+TR)*6) * sqrt((self.aspectRatio * self.vc * self.cMACWing * self.surfaceWing)/tl)
            return tl

        else:
            res = 1  # first guess for residual, to start the cycle
            TR = self.taperRatio
            tl = self.tlV  # first guess for horizontal tail arm
            while res > 0.001:

                cR = 2 / (1 + TR) * sqrt((self.vc * self.cMACWing * self.surfaceWing) / (self.aspectRatio * tl))
                posYMAC = (1 + 2 * TR) / ((1 + TR) * 6) * \
                          sqrt((self.aspectRatio * self.vc * self.cMACWing * self.surfaceWing) / tl)
                tlNew = self.tlV - .25*self.cMACV + 0.25*cR + posYMAC * tan(radians(self.sweep25)) + \
                       (self.hVertPerc * self.spanV - self.cMACyPosV) * tan(radians(self.sweepLEV))
                res = (tlNew - tl)**2
                tl = tlNew

            return tl

    @Attribute
    def surface(self):
        """
        Vertical tail reference surface
        :Unit: [m^2]
        :rtype: float
        """
        return self.vc * self.surfaceWing * self.cMACWing / self.tl

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
        if self.tailType == 'conventional':
            return self.conePos
        else:
            return self.conePos + self.spanV * self.hVertPerc

    @Attribute
    def pointsWakeHtp(self):
        """
        List of points representing the horizontal tail plane wake after separation flow on it
        :Unit: []
        :rtype: Points
        """
        return [Point(0, self.vertPos, self.longPos),
                Point(0, self.vertPos + self.spanV, self.longPos + self.spanV * tan(pi/6)),
                Point(0, self.vertPos + self.spanV, self.longPos + self.chordRoot + self.spanV * tan(pi/3)),
                Point(0, self.vertPos, self.longPos + self.chordRoot),
                Point(0, self.vertPos, self.longPos)]

    @Attribute
    def pointsRudder(self):
        """
        List of points representing the vertical tail rudder
        :Unit: []
        :rtype: Points
        """
        return [Point(0, self.vertPosV, self.longPosV + (1-self.rcr)*self.chordRootV),
                Point(0, self.vertPosV + self.spanV, self.longPosV + self.spanV * tan(radians(self.sweepLEV)) + (1-self.rcr)*self.chordTipV),
                Point(0, self.vertPosV + self.spanV, self.longPosV + self.spanV * tan(radians(self.sweepLEV)) + self.chordTipV),
                Point(0, self.vertPosV, self.longPosV + self.chordRootV),
                Point(0, self.vertPosV, self.longPosV + (1-self.rcr)*self.chordRootV)]

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

    obj = HtpCalc()
    display(obj)
