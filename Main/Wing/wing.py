from __future__ import division
import os
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import askopenfilename
from Main.Airfoil.airfoil import Airfoil
from Input import Airfoils
from Main.Wing.wake import Wake
from Handler.xFoil import Xfoil
from Handler.importer import Importer
import tkFileDialog


class Wing(GeomBase):
    """
    Basic class Wing
    """
    defaultPath = os.path.dirname(Airfoils.__file__) + '\NACA_0012.dat'  # From the Airfoil folder path add name of
    # default File

    @Input
    def wakeCheck(self):
        """
        Boolean input to choose to show the wake of the wing. True means that it is hidden

        :rtype: boolean
        """
        return False

    @Input
    def xfoilAnalysis(self):
        """
        Boolean input to choose to start the xfoil analysis

        :rtype: boolean
        """
        return False

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
        return float(Importer(Component='Wing',
                              VariableName='Aspect ratio',
                              Default=22.8,
                              Path=self.filePath).getValue)

    @Input
    def maTechnology(self):
        """
        Wing airfoil Mach technology parameter, higher values mean higher possible Mach.
        The technology factor in the formula is equal to 0.87 for NACA 6 airfoil, 0.935 for supercritical airfoils
        and 1 to other conventional airfoils.

        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Wing',
                              VariableName='Airfoil Mach technology parameter',
                              Default=1.0,
                              Path=self.filePath).getValue)

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
    def taperRatio(self):
        """
        Wing taper ratio, tip chord over root chord
        :Unit: [ ]
        :rtype: float
        """
        return 0.2 * (2 - radians(self.sweep25))

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
        else:
            return 0.

    @Input
    def posFraction(self):
        """
        Wing position fraction of the fuselage, due to engine position
        :Unit: [m]
        :rtype: float
        """
        return 0.35

    @Input
    def visual(self):
        """
        Define the visualization of the visual checks, it could be either True or False
        :Unit: [ ]
        :rtype: string
        """
        return True

    @Input
    def percxfoil(self):
        """
        Span percentage for xFoil plan, user requested
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Wing',
                              VariableName='Span percentage for xFoil analysis',
                              Default=0.5,
                              Path=self.filePath).getValue)

    @Input
    def visc(self):
        """
        Trigger for viscous calculation in Q3D, 0 for inviscid and 1 for viscous analysis
        :Unit: [ ]
        :rtype: boolean
        """
        return 0

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
    def wingPosition(self):
        """
        Wing position, could be either "low wing" or "high wing"
        :Unit: [ ]
        :rtype: string
        """
        return str(Importer(Component='Configuration',
                            VariableName='wingPosition',
                            Default="low wing",
                            Path=self.filePath).getValue)

    @Input(settable=settable)
    def maCruise(self):
        """
        Aircraft Mach cruise number
        :Unit: [ ]
        :rtype: float
        """
        return 0.22

    @Input(settable=settable)
    def wingLoading(self):
        """
        Aircraft wing loading
        :Unit: [kg / m^2]
        :rtype: float
        """
        return 43.

    @Input(settable=settable)
    def mTOW(self):
        """
        Aircraft maximum take off weight
        :Unit: [N]
        :rtype: float
        """
        return 7500.

    @Input(settable=settable)
    def hCruise(self):
        """
        Aircraft cruise altitude
        :Unit: [m]
        :rtype: float
        """
        return 1000.

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
        return 8.75

    @Input(settable=settable)
    def fuselageDiameter(self):
        """
        Aircraft fuselage diameter
        :Unit: [m]
        :rtype: float
        """
        return 1.

    @Input(settable=settable)
    def cg(self):
        """
        Center of gravity longitudinal position
        :Unit: [m]
        :rtype: float
        """
        return 4.5

    @Input(settable=settable)
    def ac(self):
        """
        Aircraft-less-tail aerodynamic center longitudinal position
        :Unit: [m]
        :rtype: float
        """
        return 4.55

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
            showwarning("Airfoil root selection", "Please choose ROOT airfoil")
            defaultPath = os.path.dirname(Airfoils.__file__)
            defaultFile = os.path.dirname(Airfoils.__file__) + '\NACA_0012.dat'
            file_opt = options = {}
            options['initialdir'] = defaultPath
            options['initialfile'] = defaultFile
            # get filename
            filename = tkFileDialog.askopenfilename(**file_opt)
            return str(filename)

    @Attribute
    def airfoilTip(self):
        """
        Path to airfoil file for wing tip. It can either use a default path or letting the user choose the airfoil file.

        :rtype: string
        """

        if not self.newAirfoil:

            return self.defaultPath
        else:
            showwarning("Airfoil tip selection", "Please choose TIP airfoil")
            defaultPath = os.path.dirname(Airfoils.__file__)
            defaultFile = os.path.dirname(Airfoils.__file__) + '\NACA_0012.dat'
            file_opt = options = {}
            options['initialdir'] = defaultPath
            options['initialfile'] = defaultFile
            # get filename
            filename = tkFileDialog.askopenfilename(**file_opt)
            return str(filename)

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
        surface = self.mTOW / (self.wingLoading * 9.81)
        span = sqrt(surface * self.aspectRatio)
        rootCr = 2 * surface / ((1 + self.taperRatio) * span)

        if rootCr > 0.33 * self.fuselageLength:
            showwarning("Warning", "Attention: the wing surface is too big for the selected fuselage. "
                                   "This might produce unexpected results."
                                   "Please reduce MTOW accordingly.")

        return surface

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
    def temperatureCruise(self):
        """
        Static temperature at cruise altitude
        :Unit: [K]
        :rtype: float
        """
        T0 = 288.15  # static temperature at sea level, [K]
        a = 0.0065  # temperature gradient, [K/m]
        if self.hCruise < 11000.:
            return T0 - a * self.hCruise
        else:
            return 216.65

    @Attribute
    def densityCruise(self):
        """
        Static density at cruise altitude
        :Unit: [kg/m^3]
        :rtype: float
        """
        R = 287.  # specific gas constant, [J/kg K]
        return self.pressureCruise / (R * self.temperatureCruise)

    @Attribute
    def viscosityCruise(self):
        """
        Static viscosity at cruise altitude, evaluated by Sutherland's law
        :Unit: [ ]
        :rtype: float
        Source: http://www.cfd-online.com/Wiki/Sutherland's_law
        """
        Tref = 273.15  # reference temperature, [K]
        Muref = 1.716e-5  # reference viscosity, [ ]
        S = 110.4  # Sutherland temperature [K]
        T = self.temperatureCruise
        return Muref * (T / Tref)**1.5 * ((Tref + S) / (T + S))

    @Attribute
    def speedCruise(self):
        """
        Aircraft speed at cruise altitude
        :Unit: [m/s]
        :rtype: float
        """
        k = 1.4  # heat capacity ratio, [ ]
        R = 287.  # specific gas constant, [J/kg K]
        return self.maCruise * sqrt(k * R * self.temperatureCruise)

    @Attribute
    def re(self):
        """
        Aircraft Reynolds number evaluated at cruise altitude and speed, based on MAC
        :Unit: [ ]
        :rtype: float
        """
        rho = self.densityCruise
        U = self.speedCruise
        L = self.cMAC
        mu = self.viscosityCruise
        return (rho * U * L) / mu

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
        tc = min(0.18, (((cos(radians(self.sweep50))**3) * (self.maTechnology - self.maDD *
                            cos(radians(self.sweep50)))) - 0.115 * self.clCruise**1.5) /
                            cos(radians(self.sweep50))**2)
        if self.maDD < 0.4:
            tc = 0.18
        return tc

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
        elif self.wingPosition == 'mid wing':
            return 0.
        else:
            showwarning("Warning", "Please choose between high or low wing configuration")
            return 0.

    # @Attribute
    # def outputList(self):
    #     lst = {}
    #     inputs ={
    #         "Wing":
    #             {
    #                 "Inputs":
    #                     {
    #                         "Aspect ratio": {"value": self.aspectRatio, "unit": ""},
    #                         "Airfoil Mach technology parameter": {"value": self.maTechnology, "unit": ""},
    #                         "Span percentage for xFoil analysis": {"value": self.percxfoil, "unit": ""}
    #                     },
    #                 "Attributes":
    #                     {
    #                         "Aircraft Mach Dive Divergence": {"value": self.maDD, "unit": ""},
    #                         "Dihedral angle": {"value": self.dihedral, "unit": "deg"},
    #                         "Sweep at quarter chord": {"value": self.sweep25, "unit": "deg"},
    #                         "Wing reference surface": {"value": self.surface, "unit": "m^2"},
    #                         "Wing span": {"value": self.span, "unit": "m"},
    #                         "Wing root chord": {"value": self.chordRoot, "unit": "m"},
    #                         "Wing tip chord": {"value": self.chordTip, "unit": "m"},
    #                         "Wing Mean Aerodynamic Chord": {"value": self.cMAC, "unit": "m"},
    #                         "Wing position fraction of the cylinder": {"value": self.cylinderFraction, "unit": ""},
    #                         "Static pressure at cruise altitude": {"value": self.pressureCruise, "unit": "Pa"},
    #                         "Dynamic pressure at aircraft speed and altitude": {"value": self.dynamicPressure, "unit": "Pa"},
    #                         "Lift coefficient of aircraft in cruise condition": {"value": self.clCruise, "unit": ""},
    #                         "Wing average thickness to chord ratio": {"value": self.tcRatio, "unit": ""},
    #                         "Wing taper ratio": {"value": self.taperRatio, "unit": ""},
    #                         "Static temperature at cruise altitude": {"value": self.temperatureCruise, "unit": "K"},
    #                         "Static density at cruise altitude": {"value": self.densityCruise, "unit": "kg/m^3"},
    #                         "Static viscosity at cruise altitude": {"value": self.viscosityCruise, "unit": ""},
    #                         "Aircraft speed at cruise altitude": {"value": self.speedCruise, "unit": "m/s"},
    #                         "Aircraft Reynolds number": {"value": self.re, "unit": ""},
    #                         "Wing position fraction of the fuselage": {"value": self.posFraction, "unit": ""}
    #                     }
    #
    #              }
    #     }
    #     lst.update(inputs)
    #     return lst

    # ###### Parts ####################################################################################################

    @Part
    def curveRoot(self):
        """
        Root airfoil curve

        :rtype:
        """
        return Airfoil(airfoilData=self.airfoilRoot,
                       chord=.99*self.chordRoot,
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

    @Part
    def rightWing(self):
        """
        Right wing solid representation

        :rtype:
        """
        return LoftedSolid([self.curveRootPos, self.curveTipPos])

    @Part
    def solidWing(self):
        """
        Right wing solid representation

        :rtype:
        """
        return Solid(self.rightWing)

    @Part
    def leftWing(self):
        """
        Left wing solid representation

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
                                 hidden=False)

    @Part
    def ACwr(self):
        """
        Wing aerodynamic center representation at quarter of MAC in right wing

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACr.edges[0].point1.x,
                                     self.MACr.edges[0].point1.y,
                                     self.MACr.edges[0].point1.z - 0.75*self.cMAC),
                      color='Red',
                      hidden=False)

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
                                 hidden=False)

    @Part
    def ACwl(self):
        """
        Wing aerodynamic center representation at quarter of MAC on left wing

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACl.edges[0].point1.x,
                                     self.MACl.edges[0].point1.y,
                                     self.MACl.edges[0].point1.z - 0.75*self.cMAC),
                      color='Red',
                      hidden=False)

    @Part
    def CGr(self):
        """
        Center of gravity representation on MAC in right wing

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACr.edges[0].point1.x,
                                     self.MACr.edges[0].point1.y,
                                     self.cg),
                      color='Blue',
                      hidden=self.visual)

    @Part
    def CGl(self):
        """
        Center of gravity representation on MAC in left wing

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACl.edges[0].point1.x,
                                     self.MACl.edges[0].point1.y,
                                     self.cg),
                      color='Blue',
                      hidden=self.visual)

    @Part
    def ACr(self):
        """
        Aircraft-less-tail aerodynamic center representation at quarter of MAC on right wing

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACr.edges[0].point1.x,
                                     self.MACr.edges[0].point1.y,
                                     self.ac),
                      color='Green',
                      hidden=self.visual)

    @Part
    def ACl(self):
        """
        Aircraft-less-tail aerodynamic center representation at quarter of MAC on left wing

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACl.edges[0].point1.x,
                                     self.MACl.edges[0].point1.y,
                                     self.ac),
                      color='Green',
                      hidden=self.visual)

    # ###### Wing wake ################################################################################################

    @Part
    def wake(self):
        return Wake(cMACWing=self.cMAC,
                    pointMAC=self.ACwr.position,
                    cRootW=self.chordRoot,
                    longPosW=self.longPos,
                    vertPosW=self.vertPos,
                    cTipW=self.chordTip,
                    pointTip=self.rightWing.edges[2].midpoint,
                    hidden=not self.wakeCheck)

    # ###### xFoil ################################################################################################

    @Part
    def xfoil(self):
        return Xfoil(perc=self.percxfoil,
                     sweepLE=self.sweepLE,
                     chordRoot=self.chordRoot,
                     chordTip=self.chordTip,
                     span=0.5*self.span,
                     longPos=self.longPos,
                     loft=self.rightWing.solids[0],
                     surface="wing",
                     hidden=not self.xfoilAnalysis)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Wing()
    display(obj)
