from __future__ import division
import os, sys
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import askopenfilename
from Main.Airfoil.airfoil import Airfoil
from Handler.htpCalc import HtpCalc
from Handler.xFoil import Xfoil
from Input import Airfoils
from Handler.importer import Importer
import Tkinter, Tkconstants, tkFileDialog


class Htp(GeomBase):
    """
    Basic class horizontal tail plane
    """
    defaultPath = os.path.dirname(Airfoils.__file__) + '\NACA_0012.dat'  # From the Airfoil folder path add name of

    # default File

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
    def hVertPerc(self):
        """
        Horizontal height of htp in percentage with respect to vtp span
        :Unit: [ ]
        :rtype: float
        """
        if self.tailType == 'T tail':
            return 1.
        else:
            return float(Importer(Component='Htp',
                                  VariableName='Horizontal height of htp in percentage of vtp',
                                  Default=.75,
                                  Path=self.filePath).getValue)

    @Input(settable=False)
    def hVertPercCalc(self):
        """
        Check on horizontal height of htp in percentage with respect to vtp span, to have at least 1/3 of rudder free
        :Unit: [ ]
        :rtype: float
        """
        hvPerc = self.hVertPerc
        check = 0.  # first guess of free portion of the rudder, in order to enter anyway the cycle
        iter = 0.
        if hvPerc < 1 / 3:
            while check < 1 / 3:
                calctail = HtpCalc(hVertPerc=hvPerc,
                                   aspectRatio=self.aspectRatio,
                                   taperRatio=self.taperRatio,
                                   sweep25=self.sweep25,
                                   vc=self.vc,
                                   tailType=self.tailType,
                                   sweep25Wing=self.sweep25Wing,
                                   surfaceWing=self.surfaceWing,
                                   cMACWing=self.cMACWing,
                                   fuselageLength=self.fuselageLength,
                                   conePos=self.conePos,
                                   posFraction=self.posFraction,
                                   spanV=self.spanV,
                                   sweepLEV=self.sweepLEV,
                                   cMACyPosV=self.cMACyPosV,
                                   cMACV=self.cMACV,
                                   chordRootV=self.chordRootV,
                                   chordTipV=self.chordTipV,
                                   tlV=self.tlV,
                                   longPosV=self.longPosV,
                                   vertPosV=self.vertPosV,
                                   rcr=self.rcr)

                check = calctail.rudderFree
                if check < 1 / 3:
                    iter += 1.
                    hvPerc += 0.01  # increment of horizontal height of htp of 1 percent
            if iter > 0:
                showwarning('Warning', 'The selected height of htp is too low, blanketing more than 2/3 of rudder. '
                                       'This is detrimental for spin control. A percentage of ' + repr(hvPerc) +
                            ' will be used instead.')
        return hvPerc

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
        Horizontal tail volume coefficient, based on type and dimension of designed aircraft
        :Unit: [ ]
        :rtype: float
        source: http://adg.stanford.edu/aa241/stability/taildesign.html
        """
        return 0.3 + 0.7 * (self.fuselageLength * self.fuselageDiameter ** 2) / (self.surfaceWing * self.cMACWing)

    @Input
    def visual(self):
        """
        Define the visualization of the visual checks, it could be either True or False
        :Unit: [ ]
        :rtype: string
        """
        return False

    @Input
    def percxfoil(self):
        """
        Span percentage for xFoil plan, user requested
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Htp',
                              VariableName='Span percentage for xFoil analysis',
                              Default=.5,
                              Path=self.filePath).getValue)

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
    def tailType(self):
        """
        Tail type, could be "conventional", "cruciform" or "T tail"
        :Unit: [ ]
        :rtype: string
        """
        return 'T tail'

    @Input(settable=settable)
    def sweep25Wing(self):
        """
        Wing sweep angle calculated at quarter chord
        :Unit: [deg]
        :rtype: float
        """
        return 28.75

    @Input(settable=settable)
    def surfaceWing(self):
        """
        Wing reference area
        :Unit: [m^2]
        :rtype: float
        """
        return 94.

    @Input(settable=settable)
    def cMACWing(self):
        """
        Wing Mean aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.67

    @Input(settable=settable)
    def spanWing(self):
        """
        Wing span, b
        :Unit: [m]
        :rtype: float
        """
        return 28.

    @Input(settable=settable)
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return 36.

    @Input(settable=settable)
    def fuselageDiameter(self):
        """
        Aircraft fuselage diameter
        :Unit: [m]
        :rtype: float
        """
        return 4.

    @Input(settable=settable)
    def conePos(self):
        """
        Aircraft tail cone vertical position
        :Unit: [m]
        :rtype: float
        """
        return 2.

    @Input(settable=settable)
    def posFraction(self):
        """
        Wing position fraction of the fuselage, due to engine position
        :Unit: [m]
        :rtype: float
        """
        return .5

    @Input(settable=settable)
    def tlV(self):
        """
        Vertical tail arm
        :Unit: [m]
        :rtype: float
        """
        return 15.96

    @Input(settable=settable)
    def spanV(self):
        """
        Vertical tail span
        :Unit: [m]
        :rtype: float
        """
        return 4.3

    @Input(settable=settable)
    def cMACyPosV(self):
        """
        Vertical tail MAC position
        :Unit: [m]
        :rtype: float
        """
        return 1.

    @Input(settable=settable)
    def sweep25V(self):
        """
        Vertical tail sweep, evaluated at quarter chord
        :Unit: [deg]
        :rtype: float
        """
        return 37.5

    @Input(settable=settable)
    def sweepLEV(self):
        """
        Vertical tail sweep, evaluated at leading edge
        :Unit: [deg]
        :rtype: float
        """
        return 42.

    @Input(settable=settable)
    def cMACV(self):
        """
        Vertical tail Mean Aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.2

    @Input(settable=settable)
    def chordRootV(self):
        """
        Vertical tail root chord
        :Unit: [m]
        :rtype: float
        """
        return 3.85

    @Input(settable=settable)
    def chordTipV(self):
        """
        Vertical tail tip chord
        :Unit: [m]
        :rtype: float
        """
        return 2.69

    @Input(settable=settable)
    def longPosV(self):
        """
        Vertical tail plane longitudinal position
        :Unit: [m]
        :rtype: float
        """
        return 26.14

    @Input(settable=settable)
    def vertPosV(self):
        """
        Vertical tail plane vertical position
        :Unit: [m]
        :rtype: float
        """
        return 1.05

    @Input(settable=settable)
    def rcr(self):
        """
        Rudder chord ratio over root chord
        :Unit: [ ]
        :rtype: float
        source: Raymer
        """
        return .35

    @Input(settable=settable)
    def wakeDanger(self):
        """
        Dangerous part of wing wake at wing root
        :Unit: [ ]
        :rtype:
        """
        return

    @Input(settable=settable)
    def wakeSafer(self):
        """
        Safer part of wing wake at wing root
        :Unit: [ ]
        :rtype:
        """
        return

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
    def airfoilRoot(self):
        """
        Path to airfoil file for wing root. It can either use a default path or letting the user choose the airfoil file

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
            posYMAC = self.fuselageDiameter / 2  # first guess for the tail MAC position

            while (self.fuselageLength - (self.wingAC + tl + 0.75 * cR - posYMAC * tan(radians(self.sweep25)))) < 0:
                tl = tl - self.tlDecrement
                cR = 2 / (1 + TR) * sqrt((self.vc * self.cMACWing * self.surfaceWing) / (self.aspectRatio * tl))
                posYMAC = (1 + 2 * TR) / ((1 + TR) * 6) * sqrt(
                    (self.aspectRatio * self.vc * self.cMACWing * self.surfaceWing) / tl)
            return tl

        else:
            res = 1  # first guess for residual, to start the cycle
            TR = self.taperRatio
            tl = self.tlV  # first guess for horizontal tail arm
            while res > 0.001:
                cR = 2 / (1 + TR) * sqrt((self.vc * self.cMACWing * self.surfaceWing) / (self.aspectRatio * tl))
                posYMAC = (1 + 2 * TR) / ((1 + TR) * 6) * \
                          sqrt((self.aspectRatio * self.vc * self.cMACWing * self.surfaceWing) / tl)
                tlNew = self.tlV - .25 * self.cMACV + 0.25 * cR + posYMAC * tan(radians(self.sweep25)) + \
                        (self.hVertPercCalc * self.spanV - self.cMACyPosV) * tan(radians(self.sweepLEV))
                res = (tlNew - tl) ** 2
                tl = tlNew

            return tl

    @Attribute
    def surface(self):
        """
        Horizontal tail reference surface
        :Unit: [m^2]
        :rtype: float
        """
        return self.vc * self.surfaceWing * self.cMACWing / self.tl

    @Attribute
    def span(self):
        """
        Horizontal tail span, b
        :Unit: [m]
        :rtype: float
        """
        return sqrt(self.surface * self.aspectRatio)

    @Attribute
    def chordRoot(self):
        """
        Horizontal tail root chord
        :Unit: [m]
        :rtype: float
        """
        return 2 * self.surface / ((1 + self.taperRatio) * self.span)

    @Attribute
    def chordTip(self):
        """
        Horizontal tail tip chord
        :Unit: [m]
        :rtype: float
        """
        return self.taperRatio * self.chordRoot

    @Attribute
    def cMAC(self):
        """
        Horizontal tail Mean Aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return (2 / 3) * self.chordRoot * (1 + self.taperRatio + self.taperRatio ** 2) / (1 + self.taperRatio)

    @Attribute
    def cMACyPos(self):
        """
        Horizontal tail Mean Aerodynamic Chord position
        :Unit: [m]
        :rtype: float
        """
        return self.span * (1 + 2 * self.taperRatio) / ((1 + self.taperRatio) * 6)

    @Attribute
    def sweep50(self):
        """
        Horizontal tail sweep angle calculated at half chord
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0.5 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepLE(self):
        """
        Horizontal tail sweep angle calculated at Leading Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((0 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def sweepTE(self):
        """
        Horizontal tail sweep angle calculated at Trailing Edge
        :Unit: [deg]
        :rtype: float
        """
        return degrees(atan(tan(radians(self.sweep25)) -
                            4 * ((1 - 0.25) * (1 - self.taperRatio) / (1 + self.taperRatio)) /
                            self.aspectRatio))

    @Attribute
    def longPos(self):
        """
        Horizontal tail root longitudinal position, in order to have the calculated tail arm
        :Unit: [m]
        :rtype: float
        """
        return self.wingAC + self.tl - .25 * self.chordRoot - self.cMACyPos * tan(radians(self.sweep25))

    @Attribute
    def vertPos(self):
        """
        Horizontal tail root vertical position
        :Unit: [m]
        :rtype: float
        """
        if self.tailType == 'conventional':
            return self.conePos
        else:
            return self.conePos + self.spanV * self.hVertPercCalc

    @Attribute
    def tailColor(self):
        """
        Horizontal tail color, depending on the wake check
        :Unit: [ ]
        :rtype: string
        """
        if self.checkDanger.edges != []:
            showwarning("Warning", "Horizontal tail plane is immersed in wing wake.")
            return "Red"
        elif (self.checkDanger.edges == [] and self.checkSafer.edges != []):
            return "Orange"
        else:
            return "Yellow"

    @Attribute
    def outputList(self):
        lst = {}
        inputs ={
            "Htp":
                {
                    "Inputs":
                        {
                            "Horizontal height of htp in percentage of vtp": {"value": self.hVertPerc, "unit": ""},
                            "Span percentage for xFoil analysis": {"value": self.percxfoil, "unit": ""}
                        },
                    "Attributes":
                        {
                            "Horizontal tail arm": {"value": self.tl, "unit": "m"},
                            "Horizontal tail volume coefficient": {"value": self.vc, "unit": ""},
                            "Htp sweep at quarter chord": {"value": self.sweep25, "unit": "deg"},
                            "Htp taper ratio": {"value": self.taperRatio, "unit": ""},
                            "Htp aspect ratio": {"value": self.aspectRatio, "unit": ""},
                            "Horizontal tail reference surface": {"value": self.surface, "unit": "m^2"},
                            "Horizontal tail span": {"value": self.span, "unit": "m"},
                            "Horizontal tail root chord": {"value": self.chordRoot, "unit": "m"},
                            "Horizontal tail tip chord": {"value": self.chordTip, "unit": "m"},
                            "Horizontal tail Mean Aerodynamic Chord": {"value": self.cMAC, "unit": "m"}
                        }

                 }
        }
        lst.update(inputs)
        return lst

    # ###### Parts ####################################################################################################

    @Part
    def curveRoot(self):
        """
        Root airfoil curve

        :rtype:
        """
        return Airfoil(airfoilData=self.airfoilRoot,
                       chord=.99 * self.chordRoot,
                       hidden=True)

    @Part
    def curveRootPol(self):
        """
        Polygon representing root airfoil curve

        :rtype:
        """
        return PolygonalFace(self.curveRoot.crv.points,
                             hidden=True)

    @Part
    def curveRootPosPol(self):
        """
        Polygon representing root airfoil curve placed in the final position

        :rtype:
        """
        return TranslatedShape(shape_in=self.curveRootPol,
                               displacement=Vector(0, self.vertPos, self.longPos),
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
        Horizontal tail root airfoil placed in the final position

        :rtype:
        """
        return TranslatedCurve(curve_in=self.curveRoot.crv,
                               displacement=Vector(0, self.vertPos, self.longPos),
                               hidden=True)

    @Part
    def curveTipPos(self):
        """
        Horizontal tail tip airfoil placed in the final position

        :rtype:
        """
        return TranslatedCurve(curve_in=self.curveTip.crv,
                               displacement=Vector(self.span / 2,
                                                   self.vertPos,
                                                   self.longPos + self.span / 2 * tan(radians(self.sweepLE))),
                               hidden=True)

    #    @Part
    #    def curveRootPos2(self):
    #        return TransformedCurve(curve_in=self.curveRoot.crv,
    #                                from_position=self.curveRoot.position,
    #                                to_position=translate(self.curveTip.position,
    #                                                      'z', self.longPos,
    #                                                      'y', self.vertPos))

    @Part
    def rightTail(self):
        """
        Right horizontal tail solid representation

        :rtype:
        """
        return LoftedSolid([self.curveRootPos, self.curveTipPos],
                           color=self.tailColor)

    @Part
    def leftTail(self):
        """
        Left horizontal tail solid representation

        :rtype:
        """
        return MirroredShape(shape_in=self.rightTail,
                             reference_point=self.rightTail.position,
                             vector1=self.rightTail.position.Vy,
                             vector2=self.rightTail.position.Vz,
                             color=self.tailColor)

    @Part
    def planeMACr(self):
        """
        Intersecting plane at MAC position on right tail plane

        :rtype:
        """
        return Plane(Point(self.cMACyPos, 0, 0), Vector(1, 0, 0),
                     hidden=True)

    @Part
    def MACr(self):
        """
        MAC representation on right tail plane

        :rtype:
        """
        return IntersectedShapes(shape_in=self.rightTail,
                                 tool=self.planeMACr,
                                 color='red',
                                 hidden=self.visual)

    @Part
    def ACr(self):
        """
        Aerodynamic center representation at quarter of MAC in right tail plane

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACr.edges[0].point1.x,
                                     self.MACr.edges[0].point1.y,
                                     self.MACr.edges[0].point1.z - 0.75 * self.cMAC),
                      color='Red',
                      hidden=self.visual)

    @Part
    def planeMACl(self):
        """
        Intersecting plane at MAC position on left tail plane

        :rtype:
        """
        return Plane(Point(-self.cMACyPos, 0, 0), Vector(1, 0, 0),
                     hidden=True)

    @Part
    def MACl(self):
        """
        MAC representation on left tail plane

        :rtype:
        """
        return IntersectedShapes(shape_in=self.leftTail,
                                 tool=self.planeMACl,
                                 color='red',
                                 hidden=self.visual)

    @Part
    def ACl(self):
        """
        Aerodynamic center representation at quarter of MAC on left tail plane

        :rtype:
        """
        return Sphere(radius=abs(self.curveRoot.maxY),
                      position=Point(self.MACl.edges[0].point1.x,
                                     self.MACl.edges[0].point1.y,
                                     self.MACl.edges[0].point1.z - 0.75 * self.cMAC),
                      color='Red',
                      hidden=self.visual)

    # ###### Wake check ###################################################################################################

    @Part
    def checkDanger(self):
        """
        Intersection between htp root airfoil and dangerous wing wake

        :rtype:
        """
        return IntersectedShapes(shape_in=self.wakeDanger, tool=self.curveRootPosPol,
                                 hidden=False)

    @Part
    def checkSafer(self):
        """
        Intersection between htp root airfoil and safer wing wake

        :rtype:
        """
        return IntersectedShapes(shape_in=self.wakeSafer, tool=self.curveRootPosPol,
                                 hidden=False)

    # ###### xFoil ################################################################################################

    @Part
    def xfoil(self):
        return Xfoil(perc=self.percxfoil,
                     sweepLE=self.sweepLE,
                     chordRoot=self.chordRoot,
                     chordTip=self.chordTip,
                     span=0.5*self.span,
                     longPos=self.longPos,
                     loft=self.rightTail.solids[0],
                     surface="horizontal tail plane",
                     hidden=not self.xfoilAnalysis)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Htp()
    display(obj)
