from __future__ import division
import os, sys
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import askopenfilename
import Tkinter, Tkconstants, tkFileDialog


class Wake(GeomBase):
    """
    Basic class for the wing wake
    """

    window = Tk()
    window.wm_withdraw()

    # ### Input required from wing ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from wing
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def cMACWing(self):
        """
        Wing Mean aerodynamic Chord
        :Unit: [m]
        :rtype: float
        """
        return 3.67

    @Input(settable=settable)
    def cRootW(self):
        """
        Wing root chord
        :Unit: [m]
        :rtype: float
        """
        return 4.5

    @Input(settable=settable)
    def cTipW(self):
        """
        Wing tip chord
        :Unit: [m]
        :rtype: float
        """
        return 2.

    @Input(settable=settable)
    def pointMAC(self):
        """
        Point representing MAC quarter chord position
        :Unit: [ ]
        :rtype: Point
        """
        return Point(5.76, -1.46, 17.53)

    @Input(settable=settable)
    def pointTip(self):
        """
        Point representing tip chord position
        :Unit: [ ]
        :rtype: Point
        """
        return Point(14., -1.15, 21.4)

    @Input(settable=settable)
    def longPosW(self):
        """
        Longitudinal position of wing model
        :Unit: [m]
        :rtype: float
        """
        return 13.

    @Input(settable=settable)
    def vertPosW(self):
        """
        Longitudinal position of wing model
        :Unit: [m]
        :rtype: float
        """
        return -1.67

    @Input
    def hidden(self):
        """
        Boolean input to choose to show the wake of the wing. True means that it is hidden

        :rtype: boolean
        """
        return True

    # ### Attributes ##################################################################################################

    # ### MAC location ################################################################################################

    @Attribute
    def xCoord(self):
        """
        Set of x coordinates to represent the wake wing function
        :Unit: [ ]
        :rtype: float
        """
        return [1.2 + (5 - 1.2) / 100 * i for i in range(101)]

    @Attribute
    def yUpMAC(self):
        """
        Set of y coordinates to represent the upper line of the wake wing function
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_1 = []
        for i in self.xCoord:
            y_1.append(Point(self.pointMAC.x,
                             self.pointMAC.y + float((.0072 * i**3 - .1016 * i**2 + .7088 * i - .0818 + 0.25) * self.cMACWing),
                             self.pointMAC.z + float(i) * self.cMACWing))
        return y_1

    @Attribute
    def yMidMAC(self):
        """
        Set of y coordinates to represent the middle line of the wake wing function
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_2 = []
        for i in self.xCoord:
            y_2.append(Point(self.pointMAC.x,
                             self.pointMAC.y + float((-.0002 * i**3 - .0063 * i**2 + .1939 * i - .094 + 0.25) * self.cMACWing),
                             self.pointMAC.z + float(i) * self.cMACWing))
        return y_2

    @Attribute
    def yMidRevMAC(self):
        """
        Reverse set of y coordinates of the middle line of the wake wing function, to make possible the polygon
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return list(reversed(self.yMidMAC))

    @Attribute
    def yBotMAC(self):
        """
        Set of y coordinates to represent the bottom line of the wake wing function
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_3 = []
        for i in self.xCoord:
            y_3.append(Point(self.pointMAC.x,
                             self.pointMAC.y + float((-.002 * i**3 + .0304 * i**2 - .1642 * i + .0882 + 0.25) * self.cMACWing),
                             self.pointMAC.z + float(i) * self.cMACWing))
        return y_3

    @Attribute
    def pointsDangerMAC(self):
        """
        Points representing the danger part of wing wake
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.yUpMAC + self.yMidRevMAC + [self.yUpMAC[0]]

    @Attribute
    def pointsSaferMAC(self):
        """
        Points representing the safer (lower) part of wing wake
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.yBotMAC + self.yMidRevMAC + [self.yBotMAC[0]]

    # ### Root location ###############################################################################################

    @Attribute
    def yUpW(self):
        """
        Set of y coordinates to represent the upper line of the wake wing function at wing root
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_1 = []
        for i in self.xCoord:
            y_1.append(Point(0,
                             self.vertPosW + float((.0072 * i**3 - .1016 * i**2 + .7088 * i - .0818 + 0.25) * self.cRootW),
                             self.longPosW + 0.25*self.cRootW + float(i) * self.cRootW))
        return y_1

    @Attribute
    def yMidW(self):
        """
        Set of y coordinates to represent the middle line of the wake wing function at wing root
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_2 = []
        for i in self.xCoord:
            y_2.append(Point(0,
                             self.vertPosW + float((-.0002 * i**3 - .0063 * i**2 + .1939 * i - .094 + 0.25) * self.cRootW),
                             self.longPosW + 0.25*self.cRootW + float(i) * self.cRootW))
        return y_2

    @Attribute
    def yMidRevW(self):
        """
        Reverse set of y coordinates of the middle line of the wake wing function, to make possible the polygon
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return list(reversed(self.yMidW))

    @Attribute
    def yBotW(self):
        """
        Set of y coordinates to represent the bottom line of the wake wing function at wing root
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_3 = []
        for i in self.xCoord:
            y_3.append(Point(0,
                             self.vertPosW + float((-.002 * i**3 + .0304 * i**2 - .1642 * i + .0882 + 0.25) * self.cRootW),
                             self.longPosW + 0.25*self.cRootW + float(i) * self.cRootW))
        return y_3

    @Attribute
    def pointsDangerW(self):
        """
        Points representing the danger part of wing wake at wing root
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.yUpW + self.yMidRevW + [self.yUpW[0]]

    @Attribute
    def pointsSaferW(self):
        """
        Points representing the safer (lower) part of wing wake at wing root
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.yBotW + self.yMidRevW + [self.yBotW[0]]

    # ### Tip location ################################################################################################

    @Attribute
    def yUpT(self):
        """
        Set of y coordinates to represent the upper line of the wake wing function at wing tip
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_1 = []
        for i in self.xCoord:
            y_1.append(Point(self.pointTip.x,
                             self.pointTip.y + float((.0072 * i**3 - .1016 * i**2 + .7088 * i - .0818 + 0.25) * self.cTipW),
                             self.pointTip.z + 0.25*self.cTipW + float(i) * self.cTipW))
        return y_1

    @Attribute
    def yMidT(self):
        """
        Set of y coordinates to represent the middle line of the wake wing function at wing tip
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_2 = []
        for i in self.xCoord:
            y_2.append(Point(self.pointTip.x,
                             self.pointTip.y + float((-.0002 * i**3 - .0063 * i**2 + .1939 * i - .094 + 0.25) * self.cTipW),
                             self.pointTip.z + 0.25*self.cTipW + float(i) * self.cTipW))
        return y_2

    @Attribute
    def yMidRevT(self):
        """
        Reverse set of y coordinates of the middle line of the wake wing function, to make possible the polygon
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return list(reversed(self.yMidT))

    @Attribute
    def yBotT(self):
        """
        Set of y coordinates to represent the bottom line of the wake wing function at wing tip
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        y_3 = []
        for i in self.xCoord:
            y_3.append(Point(self.pointTip.x,
                             self.pointTip.y + float((-.002 * i**3 + .0304 * i**2 - .1642 * i + .0882 + 0.25) * self.cTipW),
                             self.pointTip.z + 0.25 * self.cTipW + float(i) * self.cTipW))
        return y_3

    @Attribute
    def pointsDangerT(self):
        """
        Points representing the danger part of wing wake at wing tip
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.yUpT + self.yMidRevT + [self.yUpT[0]]

    @Attribute
    def pointsSaferT(self):
        """
        Points representing the safer (lower) part of wing wake at wing tip
        :Unit: [ ]
        :rtype: float
        source: KBE support material
        """
        return self.yBotT + self.yMidRevT + [self.yBotT[0]]

    # ###### Parts ####################################################################################################

    @Part
    def curveDangerMAC(self):
        """
        Curve representing the danger part of wing wake
        :Unit: [ ]
        :rtype:
        """
        return PolygonalFace(self.pointsDangerMAC,
                             color='red',
                             transparency=.7,
                             hidden=self.hidden)

    @Part
    def curveSaferMAC(self):
        """
        Curve representing the safer (lower) part of wing wake
        :Unit: [ ]
        :rtype:
        """
        return PolygonalFace(self.pointsSaferMAC,
                             color='orange',
                             transparency=.7,
                             hidden=self.hidden)

    @Part
    def curveDangerW(self):
        """
        Curve representing the danger part of wing wake at wing root
        :Unit: [ ]
        :rtype:
        """
        return PolygonalFace(self.pointsDangerW,
                             color='red',
                             transparency=.7,
                             hidden=self.hidden)

    @Part
    def curveSaferW(self):
        """
        Curve representing the safer (lower) part of wing wake at wing root
        :Unit: [ ]
        :rtype:
        """
        return PolygonalFace(self.pointsSaferW,
                             color='orange',
                             transparency=.7,
                             hidden=self.hidden)

    @Part
    def curveDangerT(self):
        """
        Curve representing the danger part of wing wake at wing tip
        :Unit: [ ]
        :rtype:
        """
        return PolygonalFace(self.pointsDangerT,
                             color='red',
                             transparency=.7,
                             hidden=self.hidden)

    @Part
    def curveSaferT(self):
        """
        Curve representing the safer (lower) part of wing wake at wing tip
        :Unit: [ ]
        :rtype:
        """
        return PolygonalFace(self.pointsSaferT,
                             color='orange',
                             transparency=.7,
                             hidden=self.hidden)

    @Part
    def wakeDangerInt(self):
        """
        Solid representing the danger part of wing wake from root to MAC
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid([self.curveDangerMAC.wires[0], self.curveDangerW.wires[0]],
                           color='red',
                           transparency=.7,
                           hidden=self.hidden)

    @Part
    def wakeSaferInt(self):
        """
        Solid representing the safer (lower) part of wing wake from root to MAC
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid([self.curveSaferMAC.wires[0], self.curveSaferW.wires[0]],
                           color='orange',
                           transparency=.7,
                           hidden=self.hidden)

    @Part
    def wakeDangerExt(self):
        """
        Solid representing the danger part of wing wake from MAC to tip
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid([self.curveDangerMAC.wires[0], self.curveDangerT.wires[0]],
                           color='red',
                           transparency=.7,
                           hidden=self.hidden)

    @Part
    def wakeSaferExt(self):
        """
        Solid representing the safer (lower) part of wing wake from MAC to tip
        :Unit: [ ]
        :rtype:
        """
        return LoftedSolid([self.curveSaferMAC.wires[0], self.curveSaferT.wires[0]],
                           color='orange',
                           transparency=.7,
                           hidden=self.hidden)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Wake()
    display(obj)
