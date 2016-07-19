from __future__ import division
import os, sys
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Input import Airfoils


class Airfoil(GeomBase):
    """
    Airfoil class, to read airfoil input file and create the fitted curve
    """

    window = Tk()
    window.wm_withdraw()

    # ### Input required from wing/tail planes ###################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from wing
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def airfoilData(self):
        """
        Path to airfoil file

        :rtype: string
        """
        return os.path.dirname(Airfoils.__file__) + '\NACA0012.dat'


    @Input(settable=settable)
    def chord(self):
        """
        reference chord for the airfoil
        :Unit: [m]
        :rtype: float
        """
        return 5.15

    # ### Attributes ####################################################################################

    @Attribute
    def pts(self):
        """
        Extract airfoil coordinates from data file and create a list of points.

        :rtype: collections.Sequence[Point]
        """
        with open(self.airfoilData, 'r') as datafile:  # this statement automatically closes the data file
            # at the end of the code block.
            points = []
            for line in datafile:
                z, y = line.split(' ', 1)  # in order to have the airfoil already correct for wing direction
                points.append(
                    Point(0, float(y)*self.chord, float(z)*self.chord))  # Convert the string to a number
                #  and make a Point of the coordinates
        return points

    @Attribute
    def ptsY(self):
        """ Extract y coordinate from airfoil data

        :rtype: collections.Sequence
        """
        with open(self.airfoilData, 'r') as datafile:  # this statement
            # automatically closes the data file at the end of the code block.
            points = []
            for line in datafile:
                x, y = line.split(' ', 1)
                points.append(float(y)*self.chord)  # Convert the string to a number
                #  and make a Point of the coordinates
        return points

    @Attribute
    def maxY(self):
        """
        Extract the maximum y-value from airfoil, for positioning

        :rtype: float
        """
        return max(self.ptsY)

    @Attribute
    def minY(self):
        """
        Extract the maximum y-value from airfoil, for positioning

        :rtype: float
        """
        return min(self.ptsY)

    @Part
    def crv(self):
        """
        Create the fitted curve representing the airfoil

        :rtype:
        """
        return FittedCurve(points=self.pts, tolerance=1e-06)

if __name__ == '__main__':
    from parapy.gui import display

    obj = Airfoil()
    display(obj)