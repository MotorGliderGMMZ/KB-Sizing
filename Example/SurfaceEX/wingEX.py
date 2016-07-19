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


class WingEX(GeomBase):
    """
    Basic class Wing
    """
    defaultPath = os.path.dirname(Airfoils.__file__) + '\NACA_0012.dat'  # From the Airfoil folder path add name of
    # default File

    @Input
    def newAirfoil(self):
        """
        Boolean input to choose between default path or user chosen.

        :rtype: boolean
        """
        return False

    @Input
    def aspectRatio(self):
        """
        Wing aspect ratio, b^2 / S
        :Unit: [ ]
        :rtype: float
        """
        return 8.4

    @Input
    def maTechnology(self):
        """
        Wing airfoil Mach technology parameter, higher values mean higher possible Mach
        :Unit: [ ]
        :rtype: float
        """
        return 0.935

    @Input
    def sweep25(self):
        """
        Wing sweep angle calculated at quarter chord
        :Unit: [deg]
        :rtype: float
        """
        if self.maDD <= 0.705:
            return degrees(acos(1.0))
        else:
            return degrees(acos(0.75 * self.maTechnology / self.maDD))

    @Input
    def wingPosition(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 'low wing'

    @Input
    def dihedral(self):
        """
        Wing dihedral angle
        :Unit: [deg]
        :rtype: float
        """
        if self.wingPosition == 'low wing':
            return 3 - self.sweep25 / 10 + 2
        elif self.wingPosition == 'high wing':
            return 3 - self.sweep25 / 10 - 2

    @Input
    def posFraction(self):
        """
        Wing position fraction of the fuselage, due to engine position
        :Unit: [m]
        :rtype: float
        """
        if self.enginePos == 'wing':
            return 0.5
        elif self.enginePos == 'fuselage':
            return 0.6
        else:
            showwarning("Warning", "Please choose between wing or fuselage mounted")
            return 0.5

    @Input
    def visual(self):
        """
        Define the visualization of the visual checks, it could be either True or False
        :Unit: [ ]
        :rtype: string
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
    def filePath(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        filename = tkFileDialog.askopenfilename()
        return str(filename)

    @Input(settable=settable)
    def maCruise(self):
        """
        Aircraft Mach cruise number
        :Unit: [ ]
        :rtype: float
        """
        return 0.77

    @Input(settable=settable)
    def wingLoading(self):
        """
        Aircraft wing loading
        :Unit: [kg / m^2]
        :rtype: float
        """
        return 4496.946809

    @Input(settable=settable)
    def mTOW(self):
        """
        Aircraft maximum take off weight
        :Unit: [N]
        :rtype: float
        """
        return 422713.

    @Input(settable=settable)
    def hCruise(self):
        """
        Aircraft cruise altitude
        :Unit: [m]
        :rtype: float
        """
        return 10000.

    @Input(settable=settable)
    def enginePos(self):
        """
        Engine position, could be either "wing" or "fuselage" mounted
        :Unit: []
        :rtype: string
        """
        return 'wing'

    @Input(settable=settable)
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return 35.

    @Input(settable=settable)
    def fuselageDiameter(self):
        """
        Aircraft fuselage diameter
        :Unit: [m]
        :rtype: float
        """
        return 4.

    # ### Attributes ##################################################################################################

    @Attribute
    def airfoilRoot(self):
        """
        Path to airfoil file for wing root. It can either use a default path or letting the user choose the airfoil file.

        :rtype: string
        """

        if not self.newAirfoil:

            return self.defaultPath
        else:
            def callback():
                name = askopenfilename()
                return name

            filePath = callback()
            errmsg = 'Error!'
            Button(text='File Open', command=callback).pack(fill=X)

            return str(filePath)

    @Attribute
    def airfoilTip(self):
        """
        Path to airfoil file for wing tip. It can either use a default path or letting the user choose the airfoil file.

        :rtype: string
        """

        if not self.newAirfoil:

            return self.defaultPath
        else:
            def callback():
                name = askopenfilename()
                return name

            filePath = callback()
            errmsg = 'Error!'
            Button(text='File Open', command=callback).pack(fill=X)

            return str(filePath)

    @Attribute
    def maDD(self):
        """
        Aircraft Mach Dive Divergence
        :Unit: [ ]
        :rtype: float
        """
        return self.maCruise + 0.03

    @Attribute
    def surface(self):
        """
        Wing reference area
        :Unit: [m^2]
        :rtype: float
        """
        return self.mTOW / self.wingLoading

    @Attribute
    def taperRatio(self):
        """
        Wing taper ratio, tip chord over root chord
        :Unit: [ ]
        :rtype: float
        """

        return 0.2 * (2 - radians(self.sweep25))

    @Attribute
    def sweep50(self):
        """
        Wing sweep angle calculated at half chord
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0.5 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepLE(self):
        """
        Wing sweep angle calculated at Leading Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepTE(self):
        """
        Wing sweep angle calculated at Trailing Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((1 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def span(self):
        """
        Wing span, b
        :Unit: [m]
        :rtype: float
        """
        return sqrt(self.surface * self.aspectRatio)

    @Attribute
    def chordRoot(self):
        """
        Wing root chord
        :Unit: [m]
        :rtype: float
        """
        return 2 * self.surface / ((1 + self.taperRatio) * self.span)

    @Attribute
    def chordTip(self):
        """
        Wing tip chord
        :Unit: [m]
        :rtype: float
        """
        return self.taperRatio * self.chordRoot

    @Attribute
    def chord35(self):
        """
        Wing chord at 35% of span, used in engines positioning
        :Unit: [m]
        :rtype: float
        """
        return self.chordRoot + 0.35 * self.span/2 * (tan(radians(self.sweepTE))-tan(radians(self.sweepLE)))

    @Attribute
    def chord40(self):
        """
        Wing chord at 40% of span, used in engines positioning
        :Unit: [m]
        :rtype: float
        """
        return self.chordRoot + 0.4 * self.span/2 * (tan(radians(self.sweepTE))-tan(radians(self.sweepLE)))

    @Attribute
    def chord70(self):
        """
        Wing chord at 70% of span, used in engines positioning
        :Unit: [m]
        :rtype: float
        """
        return self.chordRoot + 0.7 * self.span/2 * (tan(radians(self.sweepTE))-tan(radians(self.sweepLE)))

    @Attribute
    def cMAC(self):
        """
        Wing Mean aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return (2/3) * self.chordRoot * (1 + self.taperRatio + self.taperRatio**2) / (1 + self.taperRatio)

    @Attribute
    def cMACyPos(self):
        """
        Wing Mean aerodynamic Chord span position
        :Unit: [m]
        :rtype: float
        """
        return self.span * (1 + 2*self.taperRatio) / ((1 + self.taperRatio)*6)

    @Attribute
    def pressureCruise(self):
        """
        Static pressure at cruise altitude
        :Unit: [Pa]
        :rtype: float
        """
        p0 = 101325.  # static pressure at sea level, [Pa]
        a = 0.0065  # temperature gradient, [K/m]
        T0 = 288.  # temperature at sea level, [K]
        g = 9.81  # gravitational acceleration, [m/s^2]
        R = 287.  # specific gas constant, [J/kg K]
        return p0 * (1 - a * self.hCruise / T0)**(g / (R * a))

    @Attribute
    def dynamicPressure(self):
        """
        Dynamic pressure at aircraft speed and altitude
        :Unit: [Pa]
        :rtype: float
        """
        k = 1.4  # heat capacity ratio for air, [-]
        return 0.5 * self.pressureCruise * self.maCruise**2 * k

    @Attribute
    def clCruise(self):
        """
        Lift coefficient of aircraft in cruise condition
        :Unit: [ ]
        :rtype: float
        """
        return self.wingLoading / self.dynamicPressure

    @Attribute
    def tcRatio(self):
        """
        Wing average thickness to chord ratio
        :Unit: [ ]
        :rtype: float
        """
        return min(0.18, (((cos(radians(self.sweep50))**3) * (self.maTechnology - self.maDD *
                            cos(radians(self.sweep50)))) - 0.115 * self.clCruise**1.5) /
                            cos(radians(self.sweep50))**2)

    @Attribute
    def longPos(self):
        """
        Wing root longitudinal position, in order to have the AC in the selected fuselage fraction
        :Unit: [m]
        :rtype: float
        """
        return (self.posFraction * self.fuselageLength) - (0.25*self.chordRoot) - \
               (self.cMACyPos * tan(radians(self.sweep25)))

    @Attribute
    def vertPos(self):
        """
        Wing root vertical position, depending on the selected aircraft configuration
        :Unit: [m]
        :rtype: float
        """
        if self.wingPosition == 'high wing':
            return self.fuselageDiameter/2 - 1.05*self.curveRoot.maxY
        elif self.wingPosition == 'low wing':
            return -self.fuselageDiameter/2 - 1.05*self.curveRoot.minY
        else:
            showwarning("Warning", "Please choose between high or low wing configuration")
            return 0

    @Attribute
    def xLEMAC(self):
        """
        Longitudinal position of leading edge of MAC. Used for positioning of other components (ie gear)
        :Unit: [m]
        :rtype: float
        """
        return (self.posFraction * self.fuselageLength) - (0.25*self.chordRoot)

    # ###### Parts ####################################################################################################

    @Part
    def curveRoot(self):
        """
        Root airfoil curve

        :rtype:
        """
        return Airfoil(airfoilData=self.airfoilRoot,
                       chord=self.chordRoot,
                       hidden=True)

    @Part
    def curveTip(self):
        """
        Tip airfoil curve

        :rtype:
        """
        return Airfoil(airfoilData=self.airfoilTip,
                       chord=self.chordTip,
                       hidden=True)

    @Part
    def curveRootPos(self):
        """
        Wing root airfoil placed in the final wing position

        :rtype:
        """
        return TranslatedCurve(curve_in=self.curveRoot.crv,
                               displacement=Vector(0, self.vertPos, self.longPos),
                               hidden=True)

    @Part
    def curveTipPos(self):
        """
        Wing tip airfoil placed in the final wing position

        :rtype:
        """
        return TranslatedCurve(curve_in=self.curveTip.crv,
                               displacement=Vector(self.span/2,
                                                   self.vertPos + self.span/2 * tan(radians(self.dihedral)),
                                                   self.longPos + self.span/2 * tan(radians(self.sweepLE))),
                               hidden=True)

#    @Part
#    def curveRootPos2(self):
#        return TransformedCurve(curve_in=self.curveRoot.crv,
#                                from_position=self.curveRoot.position,
#                                to_position=translate(self.curveTip.position,
#                                                      'z', self.longPos,
#                                                      'y', self.vertPos))

    @Part
    def rightWing(self):
        """
        Right wing solid representation

        :rtype:
        """
        return LoftedSolid([self.curveRootPos, self.curveTipPos])

    @Part
    def leftWing(self):
        """
        Right wing solid representation

        :rtype:
        """
        return MirroredShape(shape_in=self.rightWing,
                             reference_point=self.rightWing.position,
                             vector1=self.rightWing.position.Vy,
                             vector2=self.rightWing.position.Vz)

    @Part
    def planeMACr(self):
        """
        Intersecting plane at MAC position on right wing

        :rtype:
        """
        return Plane(Point(self.cMACyPos, 0, 0), Vector(1, 0, 0),
                     hidden=True)

    @Part
    def MACr(self):
        """
        MAC representation on right wing

        :rtype:
        """
        return IntersectedShapes(shape_in=self.rightWing,
                                 tool=self.planeMACr,
                                 color='red',
                                 hidden=self.visual)

    @Part
    def ACr(self):
        """
        Aerodynamic center representation at quarter of MAC in right wing

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACr.edges[0].point1.x,
                                     self.MACr.edges[0].point1.y,
                                     self.MACr.edges[0].point1.z - 0.75*self.cMAC),
                      color='Red',
                      hidden=self.visual)
    @Part
    def planeMACl(self):
        """
        Intersecting plane at MAC position on left wing

        :rtype:
        """
        return Plane(Point(-self.cMACyPos, 0, 0), Vector(1, 0, 0),
                     hidden=True)

    @Part
    def MACl(self):
        """
        MAC representation on left wing

        :rtype:
        """
        return IntersectedShapes(shape_in=self.leftWing,
                                 tool=self.planeMACl,
                                 color='red',
                                 hidden=self.visual)

    @Part
    def ACl(self):
        """
        Aerodynamic center representation at quarter of MAC on left wing

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACl.edges[0].point1.x,
                                     self.MACl.edges[0].point1.y,
                                     self.MACl.edges[0].point1.z - 0.75*self.cMAC),
                      color='Red',
                      hidden=self.visual)

if __name__ == '__main__':
    from parapy.gui import display

    obj = WingEX()
    display(obj)
