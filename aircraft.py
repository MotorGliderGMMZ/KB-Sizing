from __future__ import division
from parapy.geom import *
from parapy.core import *
from Handler.importer import Importer
from Handler.outporter import Outporter
from Input import Files
from Output import STEP
from Main.Wing.wing import Wing
from Main.Fuselage.fuselage import Fuselage
from Main.Engine.engine import Engine
from Main.Vtp.vtp import Vtp
from Main.Htp.htp import Htp
from Main.LandingGear.landingGear import LandingGear
from Main.Analysis.evaluations import Evaluations
import tkFileDialog
import os
from parapy.exchange.step import STEPWriter


class Aircraft(GeomBase):
    """
    Basic class Aircraft
    """

    # ### Inputs #####################################################################################################

    @Input
    def projectName(self):
        """
        Name of the project or of the airplane.
        :return:
        """
        return str(Importer(Component='Configuration',
                              VariableName='Aircraft name',
                              Default='Tail sizing',
                              Path=self.filePath).getValue)

    @Input
    def maCruise(self):
        """
        Cruise Mach number
        :Unit: []
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='Cruise Mach number',
                              Default=0.22,
                              Path=self.filePath).getValue)

    @Input
    def wingLoading(self):
        """
        Aircraft wing loading
        :Unit: [kg / m^2]
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='Wing loading',
                              Default=42.86,
                              Path=self.filePath).getValue)

    @Input
    def mTOW(self):
        """
        Aircraft maximum take off weight
        :Unit: [N]
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='Maximum takeoff weight',
                              Default=7500.,
                              Path=self.filePath).getValue)

    @Input
    def twRatio(self):
        """
        Aircraft Thrust to Weight ratio
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='Thrust to Weight ratio',
                              Default=.29145,
                              Path=self.filePath).getValue)

    @Input
    def hCruise(self):
        """
        Aircraft cruise altitude
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='Aircraft cruise altitude',
                              Default=1000.,
                              Path=self.filePath).getValue)

    @Input
    def tailType(self):
        """
        Tail type, could be "conventional", "cruciform" or "T tail"
        :Unit: [ ]
        :rtype: string
        """

        return str(Importer(Component='Configuration',
                            VariableName='Tail type',
                            Default='T tail',
                            Path=self.filePath).getValue)

    @Input
    def nEngine(self):
        """
        Number of engines of the aircraft
        :Unit: [ ]
        :rtype: integer
        """
        return float(Importer(Component='Configuration',
                              VariableName='Number of engines',
                              Default=2.,
                              Path=self.filePath).getValue)

    @Input
    def enginePos(self):
        """
        Engine position, could be either "wing" or "fuselage" mounted
        :Unit: [ ]
        :rtype: float
        """
        return str(Importer(Component='Configuration',
                            VariableName='Engine location',
                            Default='wing',
                            Path=self.filePath).getValue)

    @Input
    def wingPosition(self):
        """
        Wing position, could be either "low wing" or "high wing"
        :Unit: [ ]
        :rtype: string
        """
        return str(Importer(Component='Configuration',
                            VariableName='Wing position',
                            Default='mid wing',
                            Path=self.filePath).getValue)

    # @Input
    # def outputExt(self):
    #     """
    #     Extension of output file.
    #     :return:
    #     """
    #     return 'as Input'

    # ### Attributes ##################################################################################################

    @Attribute
    def filePath(self):
        """
        Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        defaultPath = os.path.dirname(Files.__file__)
        defaultFile = os.path.dirname(Files.__file__) + '\defaultInput.json'
        file_opt = options = {}
        options['initialdir'] = defaultPath
        options['initialfile'] = defaultFile
        # get filename
        filename = tkFileDialog.askopenfilename(**file_opt)
        return str(filename)

    # @Attribute
    # def outputResult(self):
    #     """
    #     Trigger the creation of the output file
    #     """
    #     return Outporter(ListValues=self.listValues,
    #                      Path=self.filePath,
    #                      OutputExt=self.outputExt).writeValues()
    #
    # @Attribute
    # def outputSTEP(self):
    #     """
    #     Trigger the creation of the STEP file
    #     """
    #     return os.path.dirname(STEP.__file__)

    # @Attribute
    # def listValues(self):
    #     """
    #     List of elements to write the output file of the aircraft, divided in inputs and attributes
    #     """
    #     lst = {}
    #     configuration = {
    #         "Configuration":
    #             {
    #                 "Inputs":
    #                     {
    #                         "Aircraft name": {"value": self.projectName, "unit": ""},
    #                         "Tail type": {"value": self.tailType, "unit": ""},
    #                         "Number of engines": {"value": self.nEngine, "unit": ""},
    #                         "Engine location": {"value": self.enginePos, "unit": ""},
    #                         "Wing position": {"value": self.wingPosition, "unit": ""}
    #                     },
    #                 "Attributes":
    #                     {
    #                     }
    #
    #             }
    #     }
    #     lst.update(configuration)
    #     performance = {
    #         "Performance":
    #             {
    #                 "Inputs":
    #                     {
    #                         "Cruise Mach number": {"value": self.maCruise, "unit": ""},
    #                         "Wing loading": {"value": self.wingLoading, "unit": "kg / m^2"},
    #                         "Maximum takeoff weight": {"value": self.mTOW, "unit": "N"},
    #                         "Thrust to Weight ratio": {"value": self.twRatio, "unit": ""},
    #                         "Aircraft cruise altitude": {"value": self.hCruise, "unit": "m"},
    #                     },
    #                 "Attributes":
    #                     {
    #                     }
    #
    #             }
    #     }
    #     lst.update(performance)
    #     lst.update(self.fuselage.outputList)
    #     # lst.update(self.enginebase.outputList)
    #     lst.update(self.evaluations.outputList)
    #     # lst.update(self.landingGear.outputList)
    #     lst.update(self.htpbase.outputList)
    #     lst.update(self.vtpbase.outputList)
    #     lst.update(self.wingbase.outputList)
    #     return lst

    # ### Parts ######################################################################################################

    @Part
    def wingbase(self):
        """
        Wing element of the aircraft
        """
        return Wing(maCruise=self.maCruise,
                    fuselageLength=self.fuselage.fuselageLength,
                    fuselageDiameter=self.fuselage.fuselageDiameter,
                    enginePos=self.enginebase.enginePos,
                    wingLoading=self.wingLoading,
                    mTOW=self.mTOW,
                    hCruise=self.hCruise,
                    filePath=self.filePath,
                    cg=self.evaluations.cg,
                    ac=self.evaluations.ac,
                    wingPosition=self.wingPosition)

    @Part
    def fuselage(self):
        """
        Fuselage element of the aircraft
        """
        return Fuselage(maCruise=self.maCruise,
                        filePath=self.filePath)

    # @Part
    # def enginebase(self):
    #     """
    #     Engine element of the aircraft
    #     """
    #     return Engine(fuselageLength=self.fuselage.fuselageLength,
    #                   fuselageDiameter=self.fuselage.fuselageDiameter,
    #                   noseLength=self.fuselage.noseLength,
    #                   cylinderLength=self.fuselage.cylinderLength,
    #                   wingSpan=self.wingbase.span,
    #                   chord35=self.wingbase.chord35,
    #                   chord40=self.wingbase.chord40,
    #                   chord70=self.wingbase.chord70,
    #                   wingVertPos=self.wingbase.vertPos,
    #                   wingLongPos=self.wingbase.longPos,
    #                   dihedral=self.wingbase.dihedral,
    #                   sweepLE=self.wingbase.sweepLE,
    #                   tcRatio=self.wingbase.tcRatio,
    #                   filePath=self.filePath,
    #                   nEngine=self.nEngine,
    #                   enginePos=self.enginePos,
    #                   mTOW=self.mTOW,
    #                   twRatio=self.twRatio)

    @Part
    def vtpbase(self):
        """
        Vertical tail plane element of the aircraft
        """
        return Vtp(tailType=self.tailType,
                   surfaceWing=self.wingbase.surface,
                   cMACWing=self.wingbase.cMAC,
                   spanWing=self.wingbase.span,
                   fuselageLength=self.fuselage.fuselageLength,
                   fuselageDiameter=self.fuselage.fuselageDiameter,
                   posFraction=self.wingbase.posFraction,
                   conePos=self.fuselage.fuselageSectionCurves[-1].center.y,
                   tlH=self.htpbase.tl,
                   filePath=self.filePath,
                   crH=self.htpbase.chordRoot,
                   longPosH=self.htpbase.longPos,
                   vertPosH=self.htpbase.vertPos)

    @Part
    def htpbase(self):
        """
        Horizontal tail plane element of the aircraft
        """
        return Htp(tailType=self.tailType,
                   sweep25Wing=self.wingbase.sweep25,
                   surfaceWing=self.wingbase.surface,
                   cMACWing=self.wingbase.cMAC,
                   spanWing=self.wingbase.span,
                   fuselageLength=self.fuselage.fuselageLength,
                   fuselageDiameter=self.fuselage.fuselageDiameter,
                   posFraction=self.wingbase.posFraction,
                   conePos=self.fuselage.fuselageSectionCurves[-1].center.y,
                   tlV=self.vtpbase.tl,
                   spanV=self.vtpbase.span,
                   cMACyPosV=self.vtpbase.cMACyPos,
                   sweep25V=self.vtpbase.sweep25,
                   sweepLEV=self.vtpbase.sweepLE,
                   cMACV=self.vtpbase.cMAC,
                   filePath=self.filePath,
                   chordRootV=self.vtpbase.chordRoot,
                   chordTipV=self.vtpbase.chordTip,
                   longPosV=self.vtpbase.longPos,
                   vertPosV=self.vtpbase.vertPos,
                   rcr=self.vtpbase.rcr,
                   wakeDanger=self.wingbase.wake.curveDangerW,
                   wakeSafer=self.wingbase.wake.curveSaferW)

    # @Part
    # def landingGear(self):
    #     """
    #     Landing Gear element of the aircraft
    #     """
    #     return LandingGear(filePath=self.filePath,
    #                        wingPosition=self.wingbase.wingPosition,
    #                        fuselageDiameter=self.fuselage.fuselageDiameter,
    #                        fuselageLength=self.fuselage.fuselageLength,
    #                        posFraction=self.wingbase.posFraction,
    #                        cMAC=self.wingbase.cMAC,
    #                        cg=self.evaluations.cg,
    #                        fuselage=self.fuselage.loft,
    #                        wing=self.wingbase.rightWing,
    #                        engines=self.enginebase.engineSolid,
    #                        htp=self.htpbase.rightTail)

    @Part
    def evaluations(self):
        """
        Class to evaluate aircraft lift gradient, downwash gradient, aerodynamic center, center of gravity
        """
        return Evaluations(maCruise=self.maCruise,
                           tailType=self.tailType,
                           vertPosW=self.wingbase.vertPos,
                           aspectRatioW=self.wingbase.aspectRatio,
                           sweep50W=self.wingbase.sweep50,
                           sweep25W=self.wingbase.sweep25,
                           spanW=self.wingbase.span,
                           surfaceW=self.wingbase.surface,
                           taperRatioW=self.wingbase.taperRatio,
                           cMACW=self.wingbase.cMAC,
                           chordRootW=self.wingbase.chordRoot,
                           longPosW=self.wingbase.longPos,
                           posFraction=self.wingbase.posFraction,
                           vertPosT=self.htpbase.vertPos,
                           sweep50T=self.htpbase.sweep50,
                           aspectRatioT=self.htpbase.aspectRatio,
                           surfaceT=self.htpbase.surface,
                           tlH=self.htpbase.tl,
                           fuselageDiameter=self.fuselage.fuselageDiameter,
                           fuselageLength=self.fuselage.fuselageLength,
                           longPosE=self.enginebase.longPos,
                           nacelleDiameter=self.enginebase.nacelleDiameter,
                           nacelleLength=self.enginebase.nacelleLength,
                           fuselage=self.fuselage.loft,
                           wing=self.wingbase.rightWing,
                           enginePos=self.enginebase.enginePos,
                           filePath=self.filePath)

    # @Part
    # def node_writer(self):
    #     """
    #     STEP writer to allow importation in a CAD software of aircraft designed, showed in the GUI
    #     """
    #     return STEPWriter(nodes=[self.fuselage.loft,
    #                              self.wingbase.leftWing,
    #                              self.wingbase.rightWing,
    #                              self.vtpbase.tail,
    #                              self.htpbase.leftTail,
    #                              self.htpbase.rightTail,
    #                              self.enginebase.engineRight[0],
    #                              self.enginebase.engineLeft[0],
    #                              self.landingGear.noseWheel,
    #                              self.landingGear.noseHub,
    #                              self.landingGear.wheel,
    #                              self.landingGear.hub,
    #                              self.landingGear.wheelLeft,
    #                              self.landingGear.hubLeft],
    #                       default_directory=self.outputSTEP)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Aircraft()
    display(obj)