from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Handler.importer import Importer
import Tkinter, Tkconstants, tkFileDialog


class Engine(GeomBase):
    """
    Basic class Engine
    """

    @Input
    def visual(self):
        """
        Define the visualization of the visual checks, it could be either True or False
        :Unit: [ ]
        :rtype: string
        """
        return False

    @Input
    def bypassRatio(self):
        """
        Engine bypass-Ratio
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='Engine bypass ratio',
                              Default=3.0,
                              Path=self.filePath).getValue)

    @Input
    def a0(self):
        """
        Speed of sound at sea level - standard conditions
        :Unit: [m/s]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='Speed of sound at sea level',
                              Default=340.3,
                              Path=self.filePath).getValue)

    @Input
    def rho0(self):
        """
        Air density at sea level - standard conditions
        :Unit: [kg/m^3]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='Air density at sea level',
                              Default=1.225,
                              Path=self.filePath).getValue)

    @Input
    def TIT(self):
        """
        Temperature at Inlet of Turbine
        :Unit: [K]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='Temperature at Inlet of Turbine',
                              Default=1375.,
                              Path=self.filePath).getValue)

    @Input
    def etaNozzle(self):
        """
        Efficiency of engine nozzle
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='Nozzle efficiency',
                              Default=.97,
                              Path=self.filePath).getValue)

    @Input
    def etaMech(self):
        """
        Mechanical efficiency of engine
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='Mechanical efficiency',
                              Default=.75,
                              Path=self.filePath).getValue)

    @Input
    def cowlingType(self):
        """
        Cowling type of the engine, could be either "full" or "partial"
        :Unit: [ ]
        :rtype: string
        """
        return str(Importer(Component='Engine',
                            VariableName='Cowling type',
                            Default='partial',
                              Path=self.filePath).getValue)

    @Input
    def cowlingPos(self):
        """
        Cowling position of the engine, depends on the type of cowling
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='Cowling position',
                              Default=.75,
                              Path=self.filePath).getValue)

    @Input
    def engineStagger(self):
        """
        Position of the engine with regard to the wing LE.
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Engine',
                              VariableName='Engine-LE stagger',
                              Default=-0.15,
                              Path=self.filePath).getValue)

    @Input
    def fusVertPos(self):
        """
        Vertical position on fuselage wrt to the fuselage diameter.
        :return:
        """
        return float(Importer(Component='Engine',
                              VariableName='Engine vertical pos on fuselage',
                              Default=0.01,
                              Path=self.filePath).getValue)

    @Input
    def fusLongPos(self):
        """
        Longitudinal position on fuselage wrt to the nacelle length.
        :return:
        """
        return float(Importer(Component='Engine',
                              VariableName='Engine longitudinal pos on fuselage',
                              Default=0.2,
                              Path=self.filePath).getValue)

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from engine
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def nEngine(self):
        """
        Number of engine of the aircraft
        :Unit: [ ]
        :rtype: integer
        """
        return float(Importer(Component='Configuration',
                              VariableName='nEngine',
                              Default=2.,
                              Path=self.filePath).getValue)

    @Input(settable=settable)
    def enginePos(self):
        """
        Engine position, could be either "wing" or "fuselage" mounted
        :Unit: [ ]
        :rtype: float
        """
        return str(Importer(Component='Configuration',
                            VariableName='engine Position',
                            Default='wing',
                              Path=self.filePath).getValue)

    @Input(settable=settable)
    def filePath(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        filename = tkFileDialog.askopenfilename()
        return str(filename)

    @Input(settable=settable)
    def mTOW(self):
        """
        Aircraft maximum Take-Off Weight
        :Unit: [N]
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='MTOW',
                              Default=422713.,
                              Path=self.filePath).getValue)

    @Input(settable=settable)
    def twRatio(self):
        """
        Aircraft thrust to weight ratio
        :Unit: [ ]
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='Thrust to Weight ratio',
                              Default=.29145,
                              Path=self.filePath).getValue)

    @Input(settable=settable)
    def fuselageLength(self):
        """
        Aircraft fuselage length
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='fuselageLength',
                              Default=30.0,
                              Path=self.filePath).getValue)

    @Input(settable=settable)
    def fuselageDiameter(self):
        """
        Aircraft fuselage diameter
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Fuselage',
                              VariableName='fuselageDiameter',
                              Default=4.0,
                              Path=self.filePath).getValue)

    @Input(settable=settable)
    def wingSpan(self):
        """
        Wing span, b
        :Unit: [m]
        :rtype: float
        """
        return 28.

    @Input(settable=settable)
    def chord35(self):
        """
        Wing chord at 35% of span, used in engines positioning
        :Unit: [m]
        :rtype: float
        """
        return 3.88

    @Input(settable=settable)
    def chord40(self):
        """
        Wing chord at 40% of span, used in engines positioning
        :Unit: [m]
        :rtype: float
        """
        return 3.7

    @Input(settable=settable)
    def chord70(self):
        """
        Wing chord at 70% of span, used in engines positioning
        :Unit: [m]
        :rtype: float
        """
        return 2.62

    @Input(settable=settable)
    def wingVertPos(self):
        """
        Wing root vertical position, depending on the selected aircraft configuration
        :Unit: [m]
        :rtype: float
        """
        return -1.69

    @Input(settable=settable)
    def wingLongPos(self):
        """
        Wing root longitudinal position, depending on the selected aircraft configuration
        :Unit: [m]
        :rtype: float
        """
        return 13.

    @Input(settable=settable)
    def dihedral(self):
        """
        Wing dihedral angle
        :Unit: [deg]
        :rtype: float
        """
        return 2.12

    @Input(settable=settable)
    def sweepLE(self):
        """
        Wing sweep angle at Leading Edge
        :Unit: [deg]
        :rtype: float
        """
        return 31.5

    @Input(settable=settable)
    def noseLength(self):
        """
        Aircraft nose length
        :Unit: [m]
        :rtype: float
        """
        return 5.13

    @Input(settable=settable)
    def cylinderLength(self):
        """
        Aircraft fuselage cylindrical section length
        :Unit: [m]
        :rtype: float
        """
        return 21.

    @Input(settable=settable)
    def tcRatio(self):
        """
        Airfoil profile thickness to chord ratio.
        :Unit: [m]
        :rtype: float
        """
        return 0.15

    # ### Attributes ##################################################################################################

    @Attribute
    def thrustTO(self):
        """
        Engine thrust at Take-Off
        :Unit: [N]
        :rtype: float
        """
        return self.twRatio * self.mTOW

    @Attribute
    def specificGenPower(self):
        """
        Specific gas generator power
        :Unit: [W]
        :rtype: float
        """
        return (self.TIT / 600) - 1.25

    @Attribute
    def massFlow(self):
        """
        Engine mass flow
        :Unit: [kg/s]
        :rtype: float
        """
        return self.thrustTO / (self.nEngine * self.a0) * (1 + self.bypassRatio) /\
            (sqrt(5 * self.etaNozzle * self.specificGenPower * (1 + self.etaMech * self.bypassRatio)))

    @Attribute
    def spinnerInletRatio(self):
        """
        Ratio between spinner and inlet diameter
        :Unit: [ ]
        :rtype: float
        """
        return 0.05 * (1 + 0.1 * self.rho0 * self.a0 / self.massFlow + 3 * self.bypassRatio / (1 + self.bypassRatio))

    @Attribute
    def inletDiameter(self):
        """
        Inlet diameter
        :Unit: [m]
        :rtype: float
        """
        return 1.65 * sqrt((self.massFlow / (self.rho0*self.a0) + 0.005) / (1 - self.spinnerInletRatio**2))

    @Attribute
    def spinnerDiameter(self):
        """
        Spinner diameter
        :Unit: [m]
        :rtype: float
        """
        return self.spinnerInletRatio * self.inletDiameter

    @Attribute
    def cowlLengthPar(self):
        """

        :Unit: [ ]
        :rtype: float
        """
        if self.cowlingType == "full":
            return 9.8
        elif self.cowlingType == "partial":
            return 7.8
        else:
            showwarning("Warning", "Please insert 'full' or 'partial' in cowling type input")
            return "Please insert 'full' or 'partial' in cowling type."

    @Attribute
    def dl(self):
        """

        :Unit: [ ]
        :rtype: float
        """
        if self.cowlingType == "full":
            return 0.05
        elif self.cowlingType == "partial":
            return 0.10
        else:
            return "Please insert 'full' or 'partial' in cowling type."

    @Attribute
    def phi(self):
        """

        :Unit: [ ]
        :rtype: float
        """
        if self.cowlingType == "full":
            return 1
        elif self.cowlingType == "partial":
            return self.cowlingPos
        else:
            return "Please insert 'full' or 'partial' in cowling type."

    @Attribute
    def beta(self):
        """

        :Unit: [ ]
        :rtype: float
        """
        if self.cowlingType == "full":
            return 0.35
        elif self.cowlingType == "partial":
            return 0.20
        else:
            return "Please insert 'full' or 'partial' in cowling type."

    @Attribute
    def nacelleLength(self):
        """
        Length of the engine nacelle
        :Unit: [m]
        :rtype: float
        """
        return self.cowlLengthPar * (self.dl + sqrt(self.massFlow *
                                                    (1 + 0.2 * self.bypassRatio) /
                                                    (self.rho0 * self.a0 * (1 + self.bypassRatio))))

    @Attribute
    def cowlLength(self):
        """
        Length of the engine cowling
        :Unit: [m]
        :rtype: float
        """
        return self.phi * self.nacelleLength

    @Attribute
    def nacelleDiameter(self):
        """
        Diameter of the engine nacelle
        :Unit: [m]
        :rtype: float
        """
        return self.inletDiameter + 0.06 * self.cowlLength + 0.03

    @Attribute
    def bypassDiameter(self):
        """
        Diameter of the engine bypass part
        :Unit: [m]
        :rtype: float
        """
        return self.nacelleDiameter * (1 - (self.phi**2)/3)

    @Attribute
    def generatorDiameter(self):
        """
        Diameter of the engine gas generator part
        :Unit: [m]
        :rtype: float
        """
        return self.bypassDiameter * (((0.089 * self.massFlow * self.bypassRatio / (self.rho0 * self.a0) + 4.5) /
                                       (0.067 * self.massFlow * self.bypassRatio / (self.rho0 * self.a0) + 5.8))**2)

    @Attribute
    def coreDiameter(self):
        """
        Diameter of the engine core
        :Unit: [m]
        :rtype: float
        """
        return self.generatorDiameter * 0.55

    @Attribute
    def nacelleDiameters(self):
        """
        Sequence of diameters of the engine nacelle part
        :Unit: [m]
        :rtype: sequence.float
        """
        return [self.inletDiameter, self.nacelleDiameter, self.bypassDiameter]

    @Attribute
    def nacellePos(self):
        """

        :Unit: [ ]
        :rtype:
        """
        return [0, self.beta * self.nacelleLength, self.cowlLength]

    @Attribute
    def coreDiameters(self):
        """
        Sequence of diameters of the engine core part
        :Unit: [m]
        :rtype: sequence.float
        """
        return [0.01 * self.spinnerDiameter, 0.8 * self.generatorDiameter,
                0.85 * self.generatorDiameter, 0.9 * self.generatorDiameter,
                self.generatorDiameter, 0.95 * self.generatorDiameter,
                0.90 * self.generatorDiameter, 0.85 * self.generatorDiameter,
                self.coreDiameter]

    @Attribute
    def corePos(self):
        """

        :Unit: [ ]
        :rtype:
        """
        return self.nacelleLength / (len(self.coreDiameters))

    @Attribute
    def latPos(self):
        """
        Engine lateral position, depending on the number of engine and their positions
        :Unit: [m]
        :rtype:
        """
        if self.nEngine == 2 and self.enginePos == 'wing':
            return [self.wingSpan/2 * 0.35]
        elif self.nEngine == 4 and self.enginePos == 'wing':
            return [self.wingSpan/2 * 0.4, self.wingSpan/2 * 0.7]
        elif self.nEngine == 2 and self.enginePos == 'fuselage':
            return [0.75 * self.nacelleDiameter + self.fuselageDiameter/2]
        else:
            showwarning("Warning", "Please choose 2 or 4 engines, or 2 engines for the fuselage mounted option")
            return 'Error, choose 2 or 4 engines, or 2 engines for the fuselage mounted option'

    @Attribute
    def vertPos(self):
        """
        Engine vertical position, depending on the number of engine and their positions
        :Unit: [m]
        :rtype:
        """
        if self.enginePos == 'wing' and -0.2 < self.engineStagger < 0.18:
            if self.nEngine == 2 and self.enginePos == 'wing':
                return [-1 * (0.07 + 0.03 * cos(15 * (self.engineStagger + 0.03)) + self.tcRatio / 4) * self.chord35 +
                        self.wingVertPos - self.nacelleDiameter/2 + tan(radians(self.dihedral)) * self.latPos[0]]
            elif self.nEngine == 4 and self.enginePos == 'wing':
                return [-1 * (0.07 + 0.03 * cos(15 * (self.engineStagger + 0.03)) + self.tcRatio / 4) * self.chord40 +
                        self.wingVertPos - self.nacelleDiameter/2 + tan(radians(self.dihedral)) * self.latPos[0],
                        -1 * (0.07 + 0.03 * cos(15 * (self.engineStagger + 0.03)) + self.tcRatio / 4) * self.chord70 +
                        self.wingVertPos - self.nacelleDiameter/2 + tan(radians(self.dihedral)) * self.latPos[1]]
        elif self.enginePos == 'wing' and self.engineStagger > 0.18:
            if self.nEngine == 2 and self.enginePos == 'wing':
                return [(-1 * 0.04 - self.tcRatio / 4) * self.chord35 + self.wingVertPos - self.nacelleDiameter/2 +
                        tan(radians(self.dihedral)) * self.latPos[0]]
            elif self.nEngine == 4 and self.enginePos == 'wing':
                return [(-1 * 0.04 - self.tcRatio / 4) * self.chord40 + self.wingVertPos - self.nacelleDiameter/2 +
                        tan(radians(self.dihedral)) * self.latPos[0],
                        (-1 * 0.04 - self.tcRatio / 4) * self.chord70 + self.wingVertPos-self.nacelleDiameter/2 +
                        tan(radians(self.dihedral)) * self.latPos[1]]
        elif self.enginePos == 'fuselage':
            return [self.fusVertPos * self.fuselageDiameter / 2]
        else:
            print "Choose a value for engineStagger larger than -0.2"

    @Attribute
    def longPos(self):
        """
        Engine longitudinal position, depending on the number of engine and their positions
        :Unit: [m]
        :rtype:
        """
        if self.nEngine == 2 and self.enginePos == 'wing':
            return [self.engineStagger * self.chord35 + tan(radians(self.sweepLE)) * self.latPos[0] +
                    self.wingLongPos - self.cowlLength]
        elif self.nEngine == 4 and self.enginePos == 'wing':
            return [self.engineStagger * self.chord40 + tan(radians(self.sweepLE)) * self.latPos[0] +
                    self.wingLongPos - self.cowlLength,
                    self.engineStagger * self.chord70 + tan(radians(self.sweepLE)) * self.latPos[1] +
                    self.wingLongPos - self.cowlLength]
        elif self.nEngine == 2 and self.enginePos == 'fuselage':
            return [self.noseLength + self.cylinderLength + self.fusLongPos * self.nacelleLength]


    @Attribute
    def outputList(self):
        lst = {}

        inputs = {
            "Engine":
                {
                    "Inputs": {
                        "Engine bypass ratio": {"value": self.bypassRatio, "unit": ""},
                        "Speed of sound at sea level": {"value": self.a0, "unit": "m/s"},
                        "Air density at sea level": {"value": self.rho0, "unit": "kg/m^3"},
                        "Temperature at Inlet of Turbine": {"value": self.TIT, "unit": "K"},
                        "Nozzle efficiency": {"value": self.etaNozzle, "unit": ""},
                        "Mechanical efficiency": {"value": self.etaMech, "unit": ""},
                        "Cowling type": {"value": self.cowlingType, "unit": ""},
                        "Cowling position": {"value": self.cowlingPos, "unit": ""},
                        "Engine-LE stagger": {"value": self.engineStagger, "unit": ""},
                        "Engine vertical pos on fuselage": {"value": self.fusVertPos, "unit": ""},
                        "Engine longitudinal pos on fuselage": {"value": self.fusLongPos, "unit": ""}
                    },
                    "Attributes": {
                        "Engine thrust at Take-Off": {"value": self.thrustTO, "unit": "N"},
                        "Specific gas generator power": {"value": self.specificGenPower, "unit": "W"},
                        "Engine mass flow": {"value": self.massFlow, "unit": "kg/s"},
                        "Inlet diameter": {"value": self.inletDiameter, "unit": "m"},
                        "Length of the engine nacelle": {"value": self.nacelleLength, "unit": "m"},
                        "Length of the engine cowling": {"value": self.cowlLength, "unit": "m"},
                        "Diameter of the engine nacelle": {"value": self.nacelleDiameter, "unit": "m"},
                        "Diameter of the engine core": {"value": self.coreDiameter, "unit": "m"}
                    }

                }
        }

        lst.update(inputs)
        return lst

# #### Part ##########################################################################################################

    @Part
    def nacelleSections(self):
        """
        Sequence of circular sections composing the nacelle part of the engine
        :Unit: [ ]
        :rtype: sequence
        """
        return Circle(quantify=len(self.nacelleDiameters),
                      radius=self.nacelleDiameters[child.index]/2,
                      position=self.position.translate('z', self.nacellePos[child.index]),
                      hidden=True)

    @Part
    def nacelle(self):
        """
        Solid 3D representation of engine nacelle
        :Unit: [ ]
        :rtype:
        """
        return LoftedSurface(self.nacelleSections, hidden=True)

    @Part
    def solidEngine(self):
        """
        Solid 3D representation of engine nacelle
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid(self.nacelleSections, hidden=True)


    @Part
    def coreSections(self):
        """
        Sequence of circular sections composing the core part of the engine
        :Unit: [ ]
        :rtype: sequence
        """
        return Circle(quantify=len(self.coreDiameters),
                      radius=self.coreDiameters[child.index]/2,
                      position=self.position.translate('z', self.corePos * child.index),
                      hidden=True)

    @Part
    def gasGenerator(self):
        """
        Solid 3D representation of engine core, the gas generator
        :Unit: [ ]
        :rtype:
        """
        return LoftedSurface(self.coreSections, hidden=True)

    @Part
    def bypassTubeSection(self):
        """
        Sequence of circular sections composing the exhaust plume of engine bypass part
        :Unit: [ ]
        :rtype: sequence
        """
        return Circle(quantify=2,
                      radius=self.bypassDiameter/2,
                      position=self.position.translate('z', self.fuselageLength * child.index + self.cowlLength),
                      hidden=True)

    @Part
    def bypassTube(self):
        """
        Transparent 3D representation of engine bypass exhaust plume
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid(self.bypassTubeSection, color="cyan", transparency=0.8, hidden=True)

    @Part
    def coreTubeSections(self):
        """
        Sequence of circular sections composing the exhaust plume of engine bypass part
        :Unit: [ ]
        :rtype: sequence
        """
        return Circle(quantify=2,
                      radius=self.coreDiameter/2,
                      position=self.position.translate('z', self.fuselageLength * child.index + self.cowlLength),
                      hidden=True)

    @Part
    def coreTube(self):
        """
        Transparent 3D representation of engine core exhaust plume
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid(self.coreTubeSections, color="red", transparency=0.9, hidden=True)

    @Part
    def engine(self):
        """
        Solid 3D representation of complete engine
        :Unit: [ ]
        :rtype:
        """
        return Fused(self.nacelle, self.gasGenerator,
                     hidden=True)

    @Part
    def engineLeft(self):
        """
        Solid 3D representation of left engine, in its correct position
        :Unit: [ ]
        :rtype:
        """
        return TransformedShape(shape_in=self.engine, quantify=int(self.nEngine/2),
                                from_position=XOY,
                                to_position=translate(rotate(XOY, 'z', 0.0),
                                                      'x_', self.latPos[child.index],
                                                      'y', self.vertPos[child.index],
                                                      'z', self.longPos[child.index]),
                                color='blue')

    @Part
    def engineRight(self):
        """
        Solid 3D representation of left engine, in its correct position
        :Unit: [ ]
        :rtype:
        """
        return TransformedShape(shape_in=self.engine, quantify=int(self.nEngine/2),
                                from_position=XOY,
                                to_position=translate(rotate(XOY, 'z', 0.0),
                                                      'x', self.latPos[child.index],
                                                      'y', self.vertPos[child.index],
                                                      'z', self.longPos[child.index]),
                                color='blue')

    @Part
    def engineSolid(self):
        """
        Solid 3D representation of left engine, in its correct position
        :Unit: [ ]
        :rtype:
        """
        return TransformedShape(shape_in=self.solidEngine, quantify=int(self.nEngine/2),
                                from_position=XOY,
                                to_position=translate(rotate(XOY, 'z', 0.0),
                                                      'x', self.latPos[child.index],
                                                      'y', self.vertPos[child.index],
                                                      'z', self.longPos[child.index]),
                                color='yellow',
                                hidden=True)

    @Part
    def bypassExhaustLeft(self):
        """
        Solid 3D representation of left engine exhaust bypass plume, in its correct position
        :Unit: [ ]
        :rtype:
        """
        return TransformedShape(shape_in=self.bypassTube, quantify=int(self.nEngine/2),
                                from_position=XOY,
                                to_position=translate(rotate(XOY, 'z', 0.0),
                                                      'x_', self.latPos[child.index],
                                                      'y', self.vertPos[child.index],
                                                      'z', self.longPos[child.index]),
                                color='cyan', transparency=0.75,
                                hidden=not self.visual)

    @Part
    def coreExhaustLeft(self):
        """
        Solid 3D representation of left engine exhaust core plume, in its correct position
        :Unit: [ ]
        :rtype:
        """
        return TransformedShape(shape_in=self.coreTube, quantify=int(self.nEngine/2),
                                from_position=XOY,
                                to_position=translate(rotate(XOY, 'z', 0.0),
                                                      'x_', self.latPos[child.index],
                                                      'y', self.vertPos[child.index],
                                                      'z', self.longPos[child.index]),
                                color='red', transparency=0.7,
                                hidden=not self.visual)

    @Part
    def bypassExhaustRight(self):
        """
        Solid 3D representation of right engine exhaust bypass plume, in its correct position
        :Unit: [ ]
        :rtype:
        """
        return TransformedShape(shape_in=self.bypassTube, quantify=int(self.nEngine/2),
                                from_position=XOY,
                                to_position=translate(rotate(XOY, 'z', 0.0),
                                                      'x', self.latPos[child.index],
                                                      'y', self.vertPos[child.index],
                                                      'z', self.longPos[child.index]),
                                color='cyan', transparency=0.75,
                                hidden=not self.visual)

    @Part
    def coreExhaustRight(self):
        """
        Solid 3D representation of right engine exhaust core plume, in its correct position
        :Unit: [ ]
        :rtype:
        """
        return TransformedShape(shape_in=self.coreTube, quantify=int(self.nEngine/2),
                                from_position=XOY,
                                to_position=translate(rotate(XOY, 'z', 0.0),
                                                      'x', self.latPos[child.index],
                                                      'y', self.vertPos[child.index],
                                                      'z', self.longPos[child.index]),
                                color='red', transparency=0.7,
                                hidden=not self.visual)

if __name__ == '__main__':
    from parapy.gui import display

    obj = Engine()
    display(obj)