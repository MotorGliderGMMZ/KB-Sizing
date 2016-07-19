from __future__ import division
import os, sys
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from parapy.lib.cst import points_to_cst
from parapy.lib.xfoil import *
from tkMessageBox import *
from tkFileDialog import askopenfilename
from Main.Airfoil.airfoil import Airfoil
from Input import Airfoils
from Main.Wing.wake import Wake
import Tkinter, Tkconstants, tkFileDialog


class Airfoil2D(GeomBase):
    """
    Basic class that starts xFoil analysis on a lifting surface
    """

    @Input
    def re(self):
        """
        Reynolds number for xfoil calculation
        :Unit: [ ]
        :rtype: float
        """
        return 2e6

    @Input
    def aoaMin(self):
        """
        Minimum angle of attack for xfoil calculation
        :Unit: [deg]
        :rtype: float
        """
        return 0.

    @Input
    def aoaMax(self):
        """
        Minimum angle of attack for xfoil calculation
        :Unit: [deg]
        :rtype: float
        """
        return 20.

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from wing
        settable = True
    else:
        settable = False

    @Input(settable=settable)
    def perc(self):
        """
        Span percentage for xFoil plan, user requested
        :Unit: [ ]
        :rtype: float
        """
        return 0.5

    @Input(settable=settable)
    def sweepLE(self):
        """
        Leading edge sweep
        :Unit: [deg]
        :rtype: float
        """
        return 30.

    @Input(settable=settable)
    def chordRoot(self):
        """
        Root chord
        :Unit: [m]
        :rtype: float
        """
        return 5.

    @Input(settable=settable)
    def chordTip(self):
        """
        Tip chord
        :Unit: [m]
        :rtype: float
        """
        return 2.

    @Input(settable=settable)
    def span(self):
        """
        Span
        :Unit: [m]
        :rtype: float
        """
        return 20.

    @Input(settable=settable)
    def longPos(self):
        """
        Wing longitudinal position
        :Unit: [m]
        :rtype: float
        """
        return 20.

    @Input(settable=settable)
    def vertPos(self):
        """
        Vertical tail vertical position
        :Unit: [m]
        :rtype: float
        """
        return 0.

    @Input(settable=settable)
    def loft(self):
        """
        Solid representation of lifting surface, it has to be the one on the right side of the aircraft!
        :Unit: [ ]
        :rtype:
        """
        return

    @Input(settable=settable)
    def surface(self):
        """
        Indicate which surface is being analyzed, could be either "wing", "htp" or "vtp"
        :Unit: [ ]
        :rtype: string
        """
        return "wing"

    # ### Attributes ##################################################################################################

    @Attribute
    def nVector(self):
        """
        Normal vector, directed as wing leading edge
        :Unit: [ ]
        :rtype: float
        """
        if self.surface == "vtp":
            return Vector(0, cos(radians(self.sweepLE)), sin(radians(self.sweepLE)))
        else:
            return Vector(cos(radians(self.sweepLE)), 0, sin(radians(self.sweepLE)))

    @Attribute
    def point(self):
        """
        Point for the plane, expressed in span percentage as requested by user, already modified to permit only
        intersections based on having a complete airfoil (excluding part of wing root)
        :Unit: [ ]
        :rtype: float
        """
        sweepLE = radians(self.sweepLE)
        if self.surface == "vtp":
            return Point(0,
                         self.vertPos + self.chordRoot * tan(sweepLE) +
                         self.perc * (self.span * (1 + (tan(sweepLE)) ** 2) - self.chordRoot * tan(sweepLE)),
                         self.longPos)
        else:
            return Point(self.chordRoot * tan(sweepLE) +
                         self.perc * (self.span * (1 + (tan(sweepLE)) ** 2) - self.chordRoot * tan(sweepLE)),
                         0,
                         self.longPos)

    @Attribute
    def pointsxfoil3D(self):
        """
        Point equispaced for xFoil analysis, taken on the selected airfoil
        :Unit: [ ]
        :rtype: Point
        """
        return self.airfoil.edges[0].equispaced_points(100)

    @Attribute
    def pointsxfoil2D(self):
        """
        Point equispaced for xFoil analysis, exported in x,y coordinates
        :Unit: [ ]
        :rtype: Point
        """
        if self.surface == "vtp":
            return points_in_plane(self.pointsxfoil3D, self.pointsxfoil3D[0], Vector(1, 0, 0), Vector(0, 1, 0))
        else:
            return self.pointsxfoil3D


    @Attribute
    def clAlpha(self):
        """
        Returns two lists: first alpha range, then Cl range.
        :Unit: [ ]
        :rtype: float
        """
        data = run_xfoil(self.pointsxfoil2D, self.re, (self.aoaMin, self.aoaMax, 1))
        columns = zip(*data)  # Switch rows and columns
        return columns[0], columns[1]

    @Attribute
    def clMax(self):
        """
        Maximum lift coefficient found
        :Unit: [ ]
        :rtype: float
        """
        return max(self.clAlpha[1])

    @Attribute
    def alphaStall(self):
        """
        Angle of attack at which stall occurs, at max AoA
        :Unit: [deg]
        :rtype: float
        """
        for cl in range(0, len(self.clAlpha[1])):
            if self.clAlpha[1][cl] == max(self.clAlpha[1]):
                index = cl
        return self.clAlpha[0][index]

    @Attribute
    def plot(self):
        """
        plot of lift coefficient vs angle of attach for the selected airfoil
        :Unit: [ ]
        :rtype:
        """
        import matplotlib.pyplot as plt
        plt.plot(*self.clAlpha)
        plt.xlabel('alpha (alphaStall = %g)' % self.alphaStall)
        plt.ylabel('Cl (ClMax = %g)' % self.clMax)
        plt.title('Cl vs Alpha at %g span' % self.perc)
        plt.grid(b=True, which='both', color='0.65', linestyle='-')
        return plt.show()

    # ###### Parts ####################################################################################################

    @Part
    def plane(self):
        """
        Intersecting plane at span percentage position

        :rtype:
        """
        return Plane(self.point, self.nVector,
                     hidden=False)

    @Part
    def airfoil(self):
        """
        airfoil requested

        :rtype:
        """
        return IntersectedShapes(shape_in=self.loft,
                                 tool=self.plane,
                                 color='black',
                                 hidden=False)

    @Part
    def prova(self):
        return FittedCurve(self.pointsxfoil2D)

    @Attribute
    def pts(self):
        return Point(0, 0, 2), Point(2, 0, 0), Point(2, 0, 2), Point(0, 0, 2)

    @Input
    def cardine(self):
        return Point(1, 0, 1)

    @Part
    def ptsShow(self):
        return PolygonalFace(self.pts)

    @Attribute
    def pts2d(self):
        return points_in_plane(self.pts, self.cardine, Vector(0, 1, 0), Vector(1, 0, 0))

    @Part
    def ptsShowsd(self):
        return PolygonalFace(self.pts2d)

    @Part
    def cardineShow(self):
        return Sphere(radius=.1,
                      position=self.cardine)


if __name__ == '__main__':
    from parapy.gui import display

    obj = Airfoil2D()
    display(obj)
