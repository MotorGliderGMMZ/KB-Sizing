from __future__ import division
from parapy.geom import *
from parapy.core import *
from math import *
from Tkinter import *
from tkMessageBox import *
from Handler.importer import Importer
import Tkinter, Tkconstants, tkFileDialog

class LandingGear(GeomBase):
    """
    Basic class Landing Gear
    """

    @Input
    def visualChecks(self):
        """
        Visualize checks for positioning.
        :type: boolean
        :return:
        """
        return False

    @Input
    def height(self):
        """
        Height of the main landing gear wrt to the belly of the aircraft
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='Landing gear height',
                              Default=1.6,
                              Path=self.filePath).getValue)

    @Input
    def longPos(self):
        """
        Gear position with regard to the MAC
        :Unit: []
        :rtype: float
        """

        return float(Importer(Component='Landing Gear',
                              VariableName='Main Gear position',
                              Default=0.6,
                              Path=self.filePath).getValue)

    @Input
    def noseLongPos(self):
        """
        Gear position with regard to the fuselage length
        :Unit: []
        :rtype: float
        """

        return float(Importer(Component='Landing Gear',
                              VariableName='Nose Gear position',
                              Default=0.08,
                              Path=self.filePath).getValue)


    @Input
    def latPos(self):
        """
        Lateral gear position with regard to the fuselage diameter
        :Unit: []
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='Lateral gear position',
                              Default=1.8,
                              Path=self.filePath).getValue)

    @Input
    def wheelRadius(self):
        """
        Diameter of the main wheel.
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='Main wheel radius',
                              Default=0.5,
                              Path=self.filePath).getValue)

    @Input
    def noseWheelRadius(self):
        """
        Diameter of the main wheel.
        :Unit: [m]
        :rtype: float
        """
        return float(Importer(Component='Landing Gear',
                              VariableName='Nose wheel radius',
                              Default=0.3,
                              Path=self.filePath).getValue)

    @Input
    def tipbackPrecision(self):
        """
        Precision of tipback angle.
        :return:
        """
        return 0.1

    window = Tk()
    window.wm_withdraw()

    # ### Input required from aircraft ################################################################################

    if __name__ == '__main__':  # permit the modification of the input only when running from engine
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
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 'low wing'

    @Input(settable=settable)
    def fuselageDiameter(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 5.0

    @Input(settable=settable)
    def fuselageLength(self):
        """
        Wing position, could be either "low" or "high" wing
        :Unit: [ ]
        :rtype: string
        """
        return 30.

    @Input(settable=settable)
    def posFraction(self):
        """
        Wing position fraction of the fuselage, due to engine position
        :Unit: [m]
        :rtype: float
        """
        return 0.5

    @Input(settable=settable)
    def cMAC(self):
        """
        MAC length
        :Unit: [m]
        :rtype: string
        """
        return 3.0

    @Input(settable=settable)
    def cg(self):
        """
        Center of gravity longitudinal position
        :Unit: [m]
        :rtype: float
        """
        return 14.97

    @Input(settable=settable)
    def fuselage(self):
        """
        Fuselage 3D representation
        :Unit: [ ]
        :rtype: lofted solid
        """
        return

    @Input(settable=settable)
    def wing(self):
        """
        Wing 3D representation
        :Unit: [ ]
        :rtype: lofted solid
        """
        return

    @Input(settable=settable)
    def engines(self):
        """
        Enigne 3D representation
        :return:
        """
        return

    @Input(settable=settable)
    def htp(self):
        """
        Htp 3D representation
        :return:
        """
        return



    # ### Attributes ##################################################################################################

    @Attribute
    def tipbackControl(self):

        if self.tipbackAngle < 14.0:
            print("Warning: the tip back angle is smaller than 14 deg.")
            showwarning('Warning', 'The tipback angle is smaller than 14 deg.'
                                   'Please increase longitudinal position value or increase the leg length')
            return "Tipback angle is too small. Risk of tail strike on takeoff and landing."
        if self.tipbackAngle > self.maxTipbackAngle:
            showwarning("Warning", "Tip back angle is bigger than the angle between the CG anf wheel hub."
                                   " Please increase the gear height or increase the longitudinal position.")
            return "Please increase height"
        else:
            return "No changes needed"

    @Attribute
    def checkLateralAngle(self):
        """


         :return:
         """
        lateral = 5 # deg
        x = self.hubLatPos
        y = -1 * self.hubHeightPos
        z = self.hubLongPos
        R = self.wheelRadius
        rotationPoint = Point(x, y - R + 0.15 / cos(radians(lateral)), z)
        piano = Plane(reference=rotationPoint, normal=Vector(-sin(radians(lateral)), cos(radians(lateral)), 0))
        intShape = IntersectedShapes(shape_in=self.fusedWE, tool=piano)
        int = intShape.edges

        if not int:
            return "Lateral angle check is satisfied"
        else:
            showwarning("Warning", "The lateral clearance constraint is not satisfied. "
                                   "Please increase gear height or move if further out.")
            return "Lateral angle check is not satisfied. Please increase gear height or move if further out."

    @Attribute
    def lateralAngle(self):
        """


        :return:
        """
        if self.checkLateralAngle=="Lateral angle check is satisfied":
            lateral = 5
        else:
            lateral = 0
        x = self.hubLatPos
        y = -1 * self.hubHeightPos
        z = self.hubLongPos
        R = self.wheelRadius
        int = []
        while int == []:
            rotationPoint = Point(x, y - R, z)

            piano = Plane(reference=rotationPoint, normal=Vector(-sin(radians(lateral)), cos(radians(lateral)), 0))
            intShape = IntersectedShapes(shape_in=self.fusedWE, tool=piano)
            int = intShape.edges
            lateral += self.tipbackPrecision

        return lateral

    @Attribute
    def maxTipbackAngle(self):
        """
        Angle between cg and wheel hub.
        :return:
        """
        o = self.hubLongPos - self.cg
        a = self.hubHeightPos
        angle = degrees(atan(o / a))
        return angle

    @Attribute
    def tipbackAngle(self):
        """


        :return:
        """
        tipback = 0
        x = self.hubLatPos
        y = -1 * self.hubHeightPos
        z = self.hubLongPos
        R = self.wheelRadius
        int = []
        while int == []:
            rotationPoint = Point(x, y - R * cos(radians(tipback)), z + R * sin(radians(tipback)))

            piano = Plane(reference=rotationPoint, normal=Vector(0, cos(radians(tipback)), -sin(radians(tipback))))
            int_shape = IntersectedShapes(shape_in=self.fuselage, tool=piano)
            int = int_shape.edges
            tipback += self.tipbackPrecision
        return tipback

    @Attribute
    def hubLongPos(self):
        """
        Longitudinal position of the wheel hub
        :Unit: [m]
        :return:
        """
        longPos = self.fuselageLength * self.posFraction + self.longPos * self.cMAC

        if longPos < self.cg:
            print("Warning: the longitudinal position of the gear is less than the cg longitudinal location.")
            showwarning('Warning', 'The main gear is in front of the center of gravity. Please increase the value '
                                   'of the longitudinal gear position.')
            longPos = self.cg + abs(self.hubHeightPos) * tan(radians(14))

        return longPos

    @Attribute
    def noseHubLongPos(self):
        """
        Longitudinal position of the wheel hub
        :Unit: [m]
        :return:
        """
        return self.noseLongPos * self.fuselageLength

    @Attribute
    def hubHeightPos(self):
        """
        Length of the main landing gear.
        :Unit: [m]
        :type: float
        :return:
        """
        return self.height + self.fuselageDiameter / 2

    @Attribute
    def noseHeightPos(self):
        """
        Length of the nose landing gear length.
        :Unit: [m]
        :type: float
        :return:
        """
        return self.height + self.fuselageDiameter / 2 - self.noseWheelRadius + self.wheelRadius

    @Attribute
    def hubLatPos(self):
        """
        Lateral position of the wheel hub with lateral tip constraint.
        :Unit: [m]
        :type: float
        :return:
        """
        YmlgGiven = self.latPos * self.fuselageDiameter / 2
        Ymlg = self.fuselageDiameter / 2
        ln = self.cg - self.noseHubLongPos
        lm = self.hubLongPos - self.cg
        z = self.hubHeightPos + self.wheelRadius
        phi = atan(Ymlg / (lm + ln))
        proj = ln * sin(phi)
        psi = degrees(atan(z / proj))

        while psi > 55:

            Ymlg += 0.01
            phi = atan(Ymlg / (lm + ln))
            proj = ln * sin(phi)
            psi = degrees(atan(z / proj))

        if YmlgGiven < Ymlg:
            print("Warning: The lateral distance between the wheels is less than the tipover constraint.")
            showwarning('Warning', 'The lateral distance between the wheels is less than the tipover constraint.'
                                   ' Please increase the value of latPos to: ' + repr(Ymlg / (self.fuselageDiameter / 2)))
        else:
            Ymlg = YmlgGiven

        return Ymlg

    @Attribute
    def outputList(self):

        lst = {}

        inputs = {
            "Landing Gear":
                {
                    "Inputs": {
                        "Landing gear height": {"value": self.height, "unit": "m"},
                        "Main Gear position": {"value": self.longPos, "unit": ""},
                        "Nose Gear position": {"value": self.noseLongPos, "unit": ""},
                        "Lateral gear position": {"value": self.latPos, "unit": ""},
                        "Main wheel radius": {"value": self.wheelRadius, "unit": "m"},
                        "Nose wheel radius": {"value": self.noseWheelRadius, "unit": "m"}
                    },
                    "Attributes": {
                        "Tipback control": {"value": self.tipbackControl, "unit": ""},
                        "Maximum tipback angle": {"value": self.maxTipbackAngle, "unit": "deg"},
                        "Angle of tipback": {"value": self.tipbackAngle, "unit": "deg"},
                        "Lateral clearance control": {"value": self.checkLateralAngle, "unit": ""},
                        "Lateral clearance angle": {"value": self.lateralAngle, "unit": ""},
                        "Longitudinal pos of main gear": {"value": self.hubLongPos, "unit": "m"},
                        "Longitudinal pos of nose gear": {"value": self.noseHubLongPos, "unit": "m"},
                        "Main landing gear length": {"value": self.hubHeightPos, "unit": "m"},
                        "Nose landing gear length": {"value": self.noseHeightPos, "unit": "m"},
                        "Lateral pos of main gear": {"value": self.hubLatPos, "unit": "m"}
                    }

                }
        }

        lst.update(inputs)
        return lst

################

    @Part
    def rotationPoint(self):
        return Sphere(radius=0.04,
                      position=Point(self.hubLatPos, -1 * self.hubHeightPos - self.wheelRadius * cos(radians(self.tipbackAngle)),
                     self.hubLongPos + self.wheelRadius * sin(radians(self.tipbackAngle))),
                      color='red',
                      hidden=not self.visualChecks)

    @Part
    def tipbackPlane(self):
        return Plane(reference=Point(self.hubLatPos, -1 * self.hubHeightPos - self.wheelRadius * cos(radians(self.tipbackAngle)),
                     self.hubLongPos + self.wheelRadius * sin(radians(self.tipbackAngle))),
                     normal=Vector(0, cos(radians(self.tipbackAngle)), -sin(radians(self.tipbackAngle))),
                     hidden=not self.visualChecks)

    @Part
    def tailStrikeArea(self):
        return IntersectedShapes(shape_in=self.fuselage,
                                 tool=self.tipbackPlane,
                                 color='red',
                                 hidden=not self.visualChecks)

    @Part
    def contactPoint(self):
        return Sphere(radius=0.04,
                      position=Point(self.hubLatPos, -1 * self.hubHeightPos - self.wheelRadius,
                     self.hubLongPos),
                      color='blue',
                      hidden=not self.visualChecks)

    @Part
    def lateralPlane(self):
        return Plane(reference=Point(self.hubLatPos, -1 * self.hubHeightPos - self.wheelRadius,
                     self.hubLongPos),
                     normal=Vector(-sin(radians(self.lateralAngle)), cos(radians(self.lateralAngle)), 0),
                     hidden=not self.visualChecks)

    @Part
    def lateralStrikeArea(self):
        return IntersectedShapes(shape_in=self.fusedWE,
                                 tool=self.lateralPlane,
                                 color='red',
                                 hidden=not self.visualChecks)

    @Part
    def fusedWE(self):
        return Fused(shape_in=self.wing,
                     tool=self.engines,
                     hidden=True)

    @Part
    def fusedFH(self):
        return Fused(shape_in=self.fuselage,
                     tool=self.htp,
                     hidden=True)
    #######################

    @Part
    def wheelCircle(self):
        """
        Wheel part.
        :return:
        """

        return Circle(radius=self.wheelRadius,
                      position=rotate(translate(self.position,
                                                'x', self.hubLatPos,
                                                'y', -1 * self.hubHeightPos,
                                                'z', self.hubLongPos),
                                      Vector(0, 1, 0), radians(90)),
                      hidden=True)

    @Part
    def noseWheel(self):
        return Torus(major_radius=self.noseWheelRadius - self.noseWheelRadius / 3,
                     minor_radius=self.noseWheelRadius / 3,
                     position=rotate(translate(self.position,
                                               'x', 0,
                                               'y', -1 * self.noseHeightPos,
                                               'z', self.noseHubLongPos),
                                     Vector(0, 1, 0), radians(90)),
                     hidden=False,
                     color='black')

    @Part
    def noseHub(self):
        return Cylinder(radius=3 * self.noseWheelRadius / 5,
                        height=2 * self.noseWheelRadius / 3,
                        position=rotate(translate(self.position,
                                                  'x', - self.noseWheelRadius / 3,
                                                  'y', -1 * self.noseHeightPos,
                                                  'z', self.noseHubLongPos),
                                        Vector(0, 1, 0), radians(90)),
                        hidden=False,
                        color='gray')

    @Part
    def wheel(self):
        return Torus(major_radius=self.wheelRadius - self.wheelRadius / 3,
                     minor_radius=self.wheelRadius / 3,
                     position=rotate(translate(self.position,
                                               'x', self.hubLatPos,
                                               'y', -1 * self.hubHeightPos,
                                               'z', self.hubLongPos),
                                     Vector(0, 1, 0), radians(90)),
                     hidden=False,
                     color='black')

    @Part
    def hub(self):
        return Cylinder(radius=3 * self.wheelRadius / 5,
                        height=2 * self.wheelRadius / 3,
                        position=rotate(translate(self.position,
                                                  'x', self.hubLatPos - self.wheelRadius / 3,
                                                  'y', -1 * self.hubHeightPos,
                                                  'z', self.hubLongPos),
                                        Vector(0, 1, 0), radians(90)),
                        hidden=False,
                        color='gray')

    @Part
    def wheelLeft(self):
        return MirroredShape(shape_in=self.wheel,
                             reference_point=Point(),
                             vector1=self.wheel.position.Vy,
                             vector2=self.wheel.position.Vx,
                             color='black')

    @Part
    def hubLeft(self):
        return MirroredShape(shape_in=self.hub,
                             reference_point=Point(),
                             vector1=self.hub.position.Vy,
                             vector2=self.hub.position.Vx,
                             color='gray')


if __name__ == '__main__':
    from parapy.gui import display

    obj = LandingGear()
    display(obj)