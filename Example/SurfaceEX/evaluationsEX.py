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


class EvaluationsEX(GeomBase):
    """
    Class to perform te evaluations of lift gradient, downwash gradient, aerodynamic center, center of gravity
    """

    @Input
    def airfoilEffW(self):
        """
        Wing airfoil efficiency factor
        :Unit: [ ]
        :rtype: float
        """
        return .95

    @Input
    def airfoilEffT(self):
        """
        Htp airfoil efficiency factor
        :Unit: [ ]
        :rtype: float
        """
        return .95

    @Input
    def precision(self):
        """
        Trigger for the precision evaluation, but slower, of exposed surface and wetted area
        :Unit: [ ]
        :rtype: float
        """
        return False

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from wing
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def maCruise(self):
        """
        Vertical position of aircraft MAC
        :Unit: [ ]
        :rtype: float
        """
        return .77

    @Input(settable=settable)
    def tailType(self):
        """
        Tail type, could be "conventional", "cruciform" or "T tail"
        :Unit: [ ]
        :rtype: string
        """
        return 'T tail'

    @Input(settable=settable)
    def vertPosW(self):
        """
        Vertical position of aircraft wing root
        :Unit: [ ]
        :rtype: float
        """
        return -1.7

    @Input(settable=settable)
    def aspectRatioW(self):
        """
        Wing aspect ratio
        :Unit: [ ]
        :rtype: float
        """
        return 8.4

    @Input(settable=settable)
    def sweep50W(self):
        """
        Wing sweep evaluated at half chord
        :Unit: [deg]
        :rtype: float
        """
        return 25.9

    @Input(settable=settable)
    def sweep25W(self):
        """
        Wing sweep evaluated at quarter chord
        :Unit: [deg]
        :rtype: float
        """
        return 28.8

    @Input(settable=settable)
    def spanW(self):
        """
        Wing span, b
        :Unit: [m]
        :rtype: float
        """
        return 26.6

    @Input(settable=settable)
    def surfaceW(self):
        """
        Wing surface, S
        :Unit: [m^2]
        :rtype: float
        """
        return 84.5

    @Input(settable=settable)
    def taperRatioW(self):
        """
        Wing taper ratio
        :Unit: [ ]
        :rtype: float
        """
        return 0.3

    @Input(settable=settable)
    def cMACW(self):
        """
        Wing Mean Aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.5

    @Input(settable=settable)
    def posFraction(self):
        """
        Wing position fraction
        :Unit: [m]
        :rtype: float
        """
        return .5

    @Input(settable=settable)
    def vertPosT(self):
        """
        Vertical position of htp
        :Unit: [ ]
        :rtype: float
        """
        return 5.47

    @Input(settable=settable)
    def sweep50T(self):
        """
        Htp sweep evaluated at half chord
        :Unit: [deg]
        :rtype: float
        """
        return 35.6

    @Input(settable=settable)
    def aspectRatioT(self):
        """
        Htp aspect ratio
        :Unit: [deg]
        :rtype: float
        """
        return 5.0

    @Input(settable=settable)
    def surfaceT(self):
        """
        Htp surface
        :Unit: [m]
        :rtype: float
        """
        return 17.

    @Input(settable=settable)
    def tlH(self):
        """
        Htp tail arm
        :Unit: [m]
        :rtype: float
        """
        return 17.36

    @Input(settable=settable)
    def fuselageDiameter(self):
        """
        Aircraft Diameter
        :Unit: [m]
        :rtype: float
        """
        return 4.0

    @Input(settable=settable)
    def fuselageLength(self):
        """
        Fuselage length
        :Unit: [m]
        :rtype: float
        """
        return 30.

    @Input(settable=settable)
    def longPosE(self):
        """
        Engine longitudinal position
        :Unit: [m]
        :rtype: list
        """
        return [10.]

    @Input(settable=settable)
    def nacelleDiameter(self):
        """
        Engine nacelle diameter
        :Unit: [m]
        :rtype: float
        """
        return 1.3

    @Input(settable=settable)
    def nacelleLength(self):
        """
        Engine nacelle Length
        :Unit: [m]
        :rtype: float
        """
        return 4.

    @Input(settable=settable)
    def fuselage(self):
        """
        Engine nacelle Length
        :Unit: [m]
        :rtype: float
        """
        return

    @Input(settable=settable)
    def wing(self):
        """
        Engine nacelle Length
        :Unit: [m]
        :rtype: float
        """
        return

    # ### Evaluations #################################################################################################

    # ### Lift gradients ##############################################################################################

    @Attribute
    def clAlphaW(self):
        """
        Wing lift curve slope
        :Unit: [1/rad]
        :rtype: float
        source: KBE support material
        """
        A = 2 * pi * self.aspectRatioW
        B = (self.aspectRatioW * self.betaW / self.airfoilEffW)**2
        C = 1 + ((tan(radians(self.sweep50W)))**2) / (self.betaW**2)
        return A / (2 + sqrt(4 + B * C))

    @Attribute
    def clAlphaWF(self):
        """
        Lift rate coefficient of wing plus fuselage
        :Unit: [1/rad]
        :rtype: float
        source: KBE support material
        """
        A = (1 + 2.15 * self.fuselageDiameter / self.spanW) * self.exposedSurf / self.surfaceW
        B = pi * (self.fuselageDiameter**2) / (2 * self.surfaceW)
        return self.clAlphaW * A + B


    @Attribute
    def clAlphaT(self):
        """
        Htp lift curve slope
        :Unit: [1/rad]
        :rtype: float
        source: KBE support material
        """
        A = 2 * pi * self.aspectRatioT
        B = (self.aspectRatioT * self.betaT / self.airfoilEffT)**2
        C = 1 + ((tan(radians(self.sweep50T)))**2) / (self.betaT**2)
        return A / (2 + sqrt(4 + B * C))

    # ### Wing downwash gradients #####################################################################################

    @Attribute
    def downwashGradW(self):
        """
        Wing downwash gradient on htp
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        A = self.r / (self.r**2 + self.mTV**2)
        B = 0.4876 / (sqrt(self.r**2 + 0.6319 + self.mTV**2))
        C = 1 + (self.r**2 / (self.r**2 + 0.7915 + 5.0734 * self.mTV**2))**0.3113
        D = 1 - sqrt(self.mTV**2 / (1 + self.mTV**2))
        return self.Kepsilon * (A * B + C * D) * self.clAlphaW / (pi * self.aspectRatioW)

    # ### Aircraft-less-tail aerodynamic center #######################################################################

    @Attribute
    def ac(self):
        """
        Aerodynamic center position of aircraft minus tail
        :Unit: [m]
        :rtype: float
        source: KBE support material
        """
        return self.acWF + self.acN

    # ### C.G. most aft position ######################################################################################

    @Attribute
    def cg(self):
        """
        Gravity center position of aircraft minus tail
        :Unit: [m]
        :rtype: float
        source: KBE support material
        """
        A = self.clAlphaT / self.clAlphaWF
        B = (1 - self.downwashGradW)
        C = (self.surfaceT * self.tlH) / (self.surfaceW * self.cMACW)
        sm = 0.05 * self.cMACW  # static margin, approximated as 5% of aircraft MAC
        return self.ac + A * B * C * self.speedRatio**2 - sm

    # ### Attributes needed for evaluation ############################################################################

    @Attribute
    def acW(self):
        """
        Aerodynamic center location of wing, approximated at 0.25 of MAC
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.fuselageLength * self.posFraction

    @Attribute
    def betaW(self):
        """
        Prandtl-Glauert compressibility correction factor for the wing
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        if self.maCruise > 1:
            return 0
        else:
            return sqrt(1 - self.maCruise**2)

    @Attribute
    def speedRatio(self):
        """
        Tail/wing speed ratio
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        if self.tailType == 'conventional':
            return 0.85
        elif self.tailType == 'cruciform':
            return 0.95
        else:
            return 1.0

    @Attribute
    def maTail(self):
        """
        Mach number of flow investing the htp
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.maCruise * sqrt(self.speedRatio)

    @Attribute
    def betaT(self):
        """
        Prandtl-Glauert compressibility correction factor for the htp
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        if self.maTail > 1:
            return 0
        else:
            return sqrt(1 - self.maTail**2)

    @Attribute
    def exposedSurf(self):
        """
        Wing exposed surface, for a more precise but slower calculation set "precision" to True
        :Unit: [m^2]
        :rtype: float
        source: KBE support material
        """
        if self.precision:
            pass
        else:
            return self.surfaceW - self.fuselageDiameter * self.cMACW

    @Attribute
    def r(self):
        """
        Parameter linear dependent on horizontal tail arm
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.tlH / (self.spanW / 2)

    @Attribute
    def mTV(self):
        """
        Parameter linear dependent on the distance between the horizontal tail and the vortex shed plane
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        distance = abs(self.vertPosT - self.vertPosW)  # distance between htp and vortex shred plane,
                                                       # approximated with the wing root chordplane
        return distance / (self.spanW / 2)

    @Attribute
    def Kepsilon(self):
        """
        Term accounting for the wing sweep angle
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        kE = 2 + 0.1024 / self.r + (0.1124 + 0.1265 * radians(self.sweep25W) + 0.1766 * radians(self.sweep25W)**2) / \
                                   (self.r**2)
        kE0 = 2 + 0.1024 / self.r + 0.1124 / (self.r**2)
        return kE / kE0

    @Attribute
    def acWF(self):
        """
        Aerodynamic center position of wing plus fuselage
        :Unit: [m]
        :rtype: float
        source: KBE support material
        """
        cg = self.surfaceW / self.spanW  # mean geometric chord
        lfn = self.acW  # position of wing root exiting the fuselage
        A = self.acW / self.cMACW
        B = 1.8 * self.fuselageDiameter * self.fuselageDiameter * lfn / (self.clAlphaWF * self.surfaceW * self.cMACW)
        C = 0.273 * self.fuselageDiameter * cg * (self.spanW - self.fuselageDiameter) * tan(radians(self.sweep25W))
        D = ((1 + self.taperRatioW) * (self.spanW + 2.15 * self.fuselageDiameter) * self.cMACW**2)
        return (A - B + C / D) * self.cMACW

    @Attribute
    def kn(self):
        """
        Parameter linked to shift of AC due to engine nacelle
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        if self.posFraction == 0.5:  # wing mounted engines
            return -4.0
        elif self.posFraction == 0.6:  # tail mounted engines
            return -2.5

    @Attribute
    def acN(self):
        """
        Aerodynamic center shift due to nacelles
        :Unit: [m]
        :rtype: float
        source: KBE support material
        """
        acSum = 0.0
        for i in self.longPosE:
            if self.posFraction == 0.5:  # wing mounted engines
                ln = self.acW - i
            elif self.posFraction == 0.6:  # tail mounted engines
                ln = self.acW - (i + self.nacelleLength)
            acSum = +self.kn * ln * (self.nacelleDiameter**2) / (self.surfaceW * self.cMACW * self.clAlphaWF)
        return acSum

    # ###### Parts ####################################################################################################

    @Part
    def AC(self):
        """
        Aerodynamic center of aircraft-less-tail representation

        :rtype:
        """
        return Sphere(radius=.25,
                      position=Point(0, 0, self.ac),
                      color='Red')

    @Part
    def CG(self):
        """
        Center of gravity representation at quarter of MAC on left wing

        :rtype:
        """
        return Sphere(radius=.25,
                      position=Point(0, 0, self.cg),
                      color='Red')

    @Part
    def sottrazione(self):
        return SubtractedSolid(shape_in=self.wing, tool=self.fuselage)

    @Part
    def plane(self):
        """
        Intersecting plane at MAC position on right wing

        :rtype:
        """
        return Plane(Point(0, self.evaluations.sottrazione.edges[2].point1.y, 0), Vector(0, 1, 0),
                     hidden=False)

    @Part
    def MACr(self):
        """
        MAC representation on right wing

        :rtype:
        """
        return IntersectedShapes(shape_in=self.sottrazione,
                                 tool=self.plane,
                                 color='red')

    @Part
    def point(self):
        """
        Aerodynamic center representation at quarter of MAC in right wing

        :rtype:
        """
        return Sphere(radius=0.25,
                      position=Point(self.evaluations.sottrazione.edges[2].point1.x,
                                     self.evaluations.sottrazione.edges[2].point1.y,
                                     self.evaluations.sottrazione.edges[2].point1.z - self.evaluations.MACr.edges[1].length),
                      color='Red')


if __name__ == '__main__':
    from parapy.gui import display

    obj = EvaluationsEX()
    display(obj)
