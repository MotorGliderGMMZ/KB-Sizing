from __future__ import division
from parapy.geom import *
from parapy.core import *
from Handler.importer import Importer
from Input import Files
from math import *
import Tkinter
import tkMessageBox
from tkMessageBox import *
from Example.SurfaceEX.evaluationsEX import EvaluationsEX
from Example.SurfaceEX.fuselageEX import FuselageEX
from Example.SurfaceEX.wingEX import WingEX
from Main.Analysis.evaluations import Evaluations
import tkFileDialog
import os


class AircraftEX(GeomBase):
    """
    Basic class Aircraft
    """

    @Input
    def maCruise(self):
        """
        Cruise Mach number
        :Unit: []
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='M cruise',
                              Default=0.77,
                              Path=self.filePath).getValue)

    @Input
    def wingLoading(self):
        """
        Aircraft wing loading
        :Unit: [kg / m^2]
        :rtype: float
        """
        return float(Importer(Component='Performance',
                              VariableName='wingLoading',
                              Default=5000.,
                              Path=self.filePath).getValue)

    @Input
    def mTOW(self):
        """
        Aircraft maximum take off weight
        :Unit: [N]
        :rtype: float
        """
        return 422713.

    @Input
    def hCruise(self):
        """
        Aircraft cruise altitude
        :Unit: [m]
        :rtype: float
        """
        return 10000.

    @Input
    def tailType(self):
        """
        Tail type, could be "conventional", "cruciform" or "T tail"
        :Unit: [ ]
        :rtype: string
        """
        tailType = askyesnocancel(title="Tail type selection", message="Yes = T tail, No = cruciform, Cancel = conventional")

        if tailType:
            return 'T tail'
        elif tailType is None:
            return 'conventional'
        else:
            return 'cruciform'

    #### Attributes ###

    @Attribute
    def filePath(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        defaultPath = os.path.dirname(Files.__file__)
        defaultFile = os.path.dirname(Files.__file__) + '\input.xlsx'
        file_opt = options = {}
        options['initialdir'] = defaultPath
        options['initialfile'] = defaultFile
        # get filename
        filename = tkFileDialog.askopenfilename(**file_opt)
        return str(filename)

    @Part
    def wingbase(self):
        return WingEX(maCruise=self.maCruise,
                    fuselageLength=self.fuselage.fuselageLength,
                    fuselageDiameter=self.fuselage.fuselageDiameter,
                    wingLoading=self.wingLoading,
                    mTOW=self.mTOW,
                    hCruise=self.hCruise,
                    filePath=self.filePath)

    @Part
    def fuselage(self):
        return FuselageEX(maCruise=self.maCruise,
                        filePath=self.filePath)
    @Part
    def evaluations(self):
        return EvaluationsEX(maCruise=self.maCruise,
                             tailType=self.tailType,
                             vertPosW=self.wingbase.vertPos,
                             aspectRatioW=self.wingbase.aspectRatio,
                             sweep50W=self.wingbase.sweep50,
                             sweep25W=self.wingbase.sweep25,
                             spanW=self.wingbase.span,
                             surfaceW=self.wingbase.surface,
                             taperRatioW=self.wingbase.taperRatio,
                             cMACW=self.wingbase.cMAC,
                             posFraction=self.wingbase.posFraction,
                             fuselageDiameter=self.fuselage.fuselageDiameter,
                             fuselageLength=self.fuselage.fuselageLength,
                             fuselage=self.fuselage.loft,
                             wing=self.wingbase.rightWing)


if __name__ == '__main__':
    from parapy.gui import display

    obj = AircraftEX()
    display(obj)