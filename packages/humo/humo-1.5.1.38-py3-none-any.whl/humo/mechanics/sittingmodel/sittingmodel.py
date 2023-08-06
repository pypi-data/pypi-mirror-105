import humo
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import radians

import sympy as sy
from sympy import sin, cos, symbols, diff, Matrix
from sympy import solve, simplify
from sympy.physics.mechanics import LagrangesMethod, Lagrangian, inertia, outer
from sympy.physics.mechanics import ReferenceFrame, Particle, Point, RigidBody
from sympy.physics.mechanics import dynamicsymbols, kinetic_energy

class SittingModel(object):
    def __init__(self, kinematics, parameta, weight):
        # data from VICON
        self.angle = kinematics[0]
        self.anglevel = kinematics[1]
        self.angleacc = kinematics[2]
        self.segmentlength = parameta[0]
        self.segmentCOMlength = parameta[1]
        self.mass = parameta[2]
        # data for sympy
        self.q1, self.q2, self.q3, self.q4 = dynamicsymbols(r"q_1 q_2 q_3 q_4")
        self.q1_, self.q2_, self.q3_, self.q4_ = dynamicsymbols(r"\dot{q_1} \dot{q_2} \dot{q_3} \dot{q_4}")
        self.t, self.g = symbols("t g")
        self.m1, self.m2, self.m3, self.m4, self.M = symbols("m_1 m_2 m_3 m_4 M")
        self.l1, self.l2, self.l3, self.l4 = symbols("l_1 l_2 l_3 l_4")
        self.L1, self.L2, self.L3, self.L4 = symbols("L_1 L_2 L_3 L_4")
        self.I1, self.I2, self.I3, self.I4 = symbols("I_1 I_2 I_3 I_4")
        # body mass ratio
        self.setHATlength()
        self.weight = weight
        self.setModel()
        #self.g = 0.098
        #self.bodymass = dict(zip(self.bodymassratio.keys(),np.array(list(self.bodymassratio.values()))*self.weight))

        # 慣性モーメントテンソル部分
        
    def setHATlength(self):
        a = (self.mass["thorax"]*self.segmentCOMlength["thorax"] + self.mass["head"]*(self.segmentlength["thorax"]+self.segmentCOMlength["head"]))
        b = (self.mass["thorax"] + self.mass["head"])
        self.HATlength = a/b

    def setFrame(self):
        self.base = ReferenceFrame("B")
        self.tibia = ReferenceFrame("tibia")
        self.thigh = ReferenceFrame("thigh")
        self.pelvis = ReferenceFrame("pelvis")
        self.thorax = ReferenceFrame("thorax")
        self.tibia.orient(self.base, "axis", [self.q1, self.base.z])
        self.thigh.orient(self.tibia, "axis", [self.q2, self.tibia.z])
        self.pelvis.orient(self.thigh, "axis", [self.q3, self.thigh.z])
        self.thorax.orient(self.pelvis, "axis", [self.q4, self.pelvis.z])

    def setJointCenter(self):
        self.O = Point("O")
        self.ankle = Point("ankle")
        self.knee = Point("knee")
        self.hip = Point("hip")
        self.spine = Point("spine")
        self.neck = Point("neck")
        self.ankle.set_pos(self.O, 0*self.base.y)
        self.knee.set_pos(self.ankle, self.L1*self.tibia.y)
        self.hip.set_pos(self.knee, self.L2*self.thigh.y)
        self.spine.set_pos(self.hip, self.L3*self.pelvis.y)
        self.neck.set_pos(self.spine, self.L4*self.thorax.y)

    def setCOM(self):
        self.com1 = Point("tibia")
        self.com2 = Point("thigh")
        self.com3 = Point("pelvis")
        self.com4 = Point("thorax")
        self.com1.set_pos(self.ankle, self.l1*self.tibia.y)
        self.com2.set_pos(self.knee, self.l2*self.thigh.y)
        self.com3.set_pos(self.hip, self.l3*self.pelvis.y)
        self.com4.set_pos(self.spine, self.l4*self.thorax.y)

    def setParticle(self):
        self.pa1 = Particle("com1", self.com1, self.m1)
        self.pa2 = Particle("com2", self.com2, self.m2)
        self.pa3 = Particle("com3", self.com3, self.m3)
        self.pa4 = Particle("com4", self.com4, self.m4)
        
    def description_of_motion(self):
        self.com1.set_vel(self.base, self.com1.pos_from(self.O).express(self.base).diff(self.t, self.base))
        self.com2.set_vel(self.base, self.com2.pos_from(self.O).express(self.base).diff(self.t, self.base))
        self.com3.set_vel(self.base, self.com3.pos_from(self.O).express(self.base).diff(self.t, self.base))
        self.com4.set_vel(self.base, self.com4.pos_from(self.O).express(self.base).diff(self.t, self.base))
        self.tibia.set_ang_vel(self.base, self.q1.diff()*self.base.z)
        self.thigh.set_ang_vel(self.tibia, self.q2.diff()*self.tibia.z)
        self.pelvis.set_ang_vel(self.thigh, self.q3.diff()*self.thigh.z)
        self.thorax.set_ang_vel(self.pelvis, self.q4.diff()*self.pelvis.z)

    def setInertia(self):
        self.ituple1 = (inertia(self.base, 0, 0, self.I1), self.com1)
        self.ituple2 = (inertia(self.base, 0, 0, self.I2), self.com2)
        self.ituple3 = (inertia(self.base, 0, 0, self.I3), self.com3)
        self.ituple4 = (inertia(self.base, 0, 0, self.I4), self.com4)

    def setRigidbody(self):
        self.tibia_segment = RigidBody("tibia_segment", self.com1, self.tibia, self.m1, self.ituple1)
        self.thigh_segment = RigidBody("thigh_segment", self.com2, self.thigh, self.m2, self.ituple2)
        self.pelvis_segment = RigidBody("pelvis_segment", self.com3, self.pelvis, self.m3, self.ituple3)
        self.thorax_segment = RigidBody("thorax_segment", self.com4, self.thorax, self.m4, self.ituple4)

    def setPotential_energy(self):
        self.tibia_segment.potential_energy = self.m1 * self.g * self.com1.pos_from(self.O).to_matrix(self.base)[1]
        self.thigh_segment.potential_energy = self.m2 * self.g * self.com2.pos_from(self.O).to_matrix(self.base)[1]
        self.pelvis_segment.potential_energy = self.m3 * self.g * self.com3.pos_from(self.O).to_matrix(self.base)[1]
        self.thorax_segment.potential_energy = self.m4 * self.g * self.com4.pos_from(self.O).to_matrix(self.base)[1]
        self.Rbodies = [self.tibia_segment, self.thigh_segment, self.pelvis_segment, self.thorax_segment]

    def setModel(self):
        self.setFrame()
        self.setJointCenter()
        self.setCOM()
        self.setParticle()
        self.description_of_motion()
        self.setInertia()
        self.setRigidbody()
        self.setPotential_energy()
        self.L = Lagrangian(self.base, *self.Rbodies)
        self.LM = LagrangesMethod(self.L, [self.q1, self.q2, self.q3, self.q4])

    def calcEquation_of_motion(self):
        self.eom = self.LM.form_lagranges_equations()

    def getCOMposition(self, name, modeltype=0, **kwargs):
        """Summary line.
        Get the mass center coordinates of each segment. 
        Depending on the model type you specify, you can choose the coordinate format you get.

        Parameters
        ----------
        name : str
            Name of joint.
                - tibia
                - thigh
                - pelvis
                - thorax
        modeltype : int
            - 0 :
            Output the mass center coordinates as a mathematical formula.
            - 1 :
            Output the formula of the mass center coordinates with the body parameters input.
            - 2 :
            Output as a universal function of numpy.
            The variable is each joint angle.
            - 3 :
            The mass center coordinates of the segment for which the body parameters and joint angles are input are output. 
            That is, it is the actual coordinates of each segment.

        Returns
        -------
        Mathematical model of mass center coordinates of each segment.
        """
        if name == "tibia":
            x = self.com1.pos_from(self.O).to_matrix(self.base)[0].simplify()
            y = self.com1.pos_from(self.O).to_matrix(self.base)[1].simplify()
            if modeltype == 0:
                return Matrix([x,y])
            elif modeltype == 1:
                return Matrix([x,y]).subs(
                    [
                        (self.l1, self.segmentCOMlength["Ltibia"])
                    ]
                )
            elif modeltype == 2:
                args = (self.q1)
                f = Matrix([x,y]).subs(
                    [
                        (self.l1, self.segmentCOMlength["Ltibia"])
                    ]
                )
                return sy.lambdify(args, f, "numpy")
            elif modeltype == 3:
                args = (self.q1)
                f = Matrix([x,y]).subs(
                    [
                        (self.l1, self.segmentCOMlength["Ltibia"])
                    ]
                )
                return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle.Lankle),axis=1).T
        elif name == "femur":
            x = self.com2.pos_from(self.O).to_matrix(self.base)[0].simplify()
            y = self.com2.pos_from(self.O).to_matrix(self.base)[1].simplify()
            if modeltype == 0:
                return Matrix([x,y])
            elif modeltype == 1:
                return Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.l2, self.segmentCOMlength["Lfemur"])
                    ]
                )
            elif modeltype == 2:
                args = (self.q1, self.q2)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.l2, self.segmentCOMlength["Lfemur"])
                    ]
                )
                return sy.lambdify(args, f, "numpy")
            elif modeltype == 3:
                args = (self.q1, self.q2)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentCOMlength["Ltibia"]),
                        (self.l2, self.segmentCOMlength["Lfemur"])
                    ]
                )
                try:
                    num = kwargs["trial"]
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z[num], self.angle[1].x[num]),axis=1).T
                except:
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z, self.angle[1].x),axis=1).T

        elif name == "pelvis":
            x = self.com3.pos_from(self.O).to_matrix(self.base)[0].simplify()
            y = self.com3.pos_from(self.O).to_matrix(self.base)[1].simplify()
            if modeltype == 0:
                return Matrix([x,y])
            elif modeltype == 1:
                return Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.l3, self.segmentCOMlength["pelvis"])
                    ]
                )
            elif modeltype == 2:
                args = (self.q1, self.q2, self.q3)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.l3, self.segmentCOMlength["pelvis"])
                    ]
                )
                return sy.lambdify(args, f, "numpy")
            elif modeltype == 3:
                args = (self.q1, self.q2, self.q3)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.l3, self.segmentCOMlength["pelvis"])
                    ]
                )
                try:
                    num = kwargs["trial"]
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num]),axis=1).T
                except:
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].x, self.angle[1].x, self.angle[2].x),axis=1).T

        elif name == "thorax":
            x = self.com4.pos_from(self.O).to_matrix(self.base)[0].simplify()
            y = self.com4.pos_from(self.O).to_matrix(self.base)[1].simplify()
            if modeltype == 0:
                return Matrix([x,y])
            elif modeltype == 1:
                return Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.L3, self.segmentlength["pelvis"]),
                        (self.l4, self.HATlength)
                    ]
                )
            elif modeltype == 2:
                args = (self.q1, self.q2, self.q3)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.L3, self.segmentlength["pelvis"]),
                        (self.l4, self.HATlength)
                    ]
                )
                return sy.lambdify(args, f, "numpy")
            elif modeltype == 3:
                args = (self.q1, self.q2, self.q3, self.q4)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.L3, self.segmentlength["pelvis"]),
                        (self.l4, self.HATlength)
                    ]
                )
                try:
                    num = kwargs["trial"]
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num]),axis=1).T
                except:
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x),axis=1).T
    
    def getJointCenterposition(self, name, modeltype=0, **kwargs):
        if name == "ankle":
            if modeltype == 3:
                return np.array([0]*self.angle.Lankle.size*2).reshape(-1,2)
            else:
                print("Please enter modeltype=3.")
        elif name == "knee":
            x = self.knee.pos_from(self.O).to_matrix(self.base)[0].simplify()
            y = self.knee.pos_from(self.O).to_matrix(self.base)[1].simplify()
            if modeltype == 0:
                return Matrix([x,y])
            elif modeltype == 1:
                return Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"])
                    ]
                )
            elif modeltype == 2:
                args = (self.q1)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"])
                    ]
                )
                return sy.lambdify(args, f, "numpy")
            elif modeltype == 3:
                args = (self.q1)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"])
                    ]
                )
                try:
                    num = kwargs["trial"]
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z[num]),axis=1).T
                except:
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z),axis=1).T

        elif name == "hip":
            x = self.hip.pos_from(self.O).to_matrix(self.base)[0].simplify()
            y = self.hip.pos_from(self.O).to_matrix(self.base)[1].simplify()
            if modeltype == 0:
                return Matrix([x,y])
            elif modeltype == 1:
                return Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"])
                    ]
                )
            elif modeltype == 2:
                args = (self.q1, self.q2)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"])
                    ]
                )
                return sy.lambdify(args, f, "numpy")
            elif modeltype == 3:
                args = (self.q1, self.q2)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"])
                    ]
                )
                try:
                    num = kwargs["trial"]
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z[num], self.angle[1].x[num]),axis=1).T
                except:
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z, self.angle[1].x),axis=1).T

        elif name == "spine":
            x = self.spine.pos_from(self.O).to_matrix(self.base)[0].simplify()
            y = self.spine.pos_from(self.O).to_matrix(self.base)[1].simplify()
            if modeltype == 0:
                return Matrix([x,y])
            elif modeltype == 1:
                return Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.L3, self.segmentlength["pelvis"])
                    ]
                )
            elif modeltype == 2:
                args = (self.q1, self.q2, self.q3)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.L3, self.segmentlength["pelvis"])
                    ]
                )
                return sy.lambdify(args, f, "numpy")
            elif modeltype == 3:
                args = (self.q1, self.q2, self.q3)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.L3, self.segmentlength["pelvis"])
                    ]
                )
                try:
                    num = kwargs["trial"]
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], - self.angle[2].x[num]),axis=1).T
                except:
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x),axis=1).T

        elif name == "neck":
            x = self.neck.pos_from(self.O).to_matrix(self.base)[0].simplify()
            y = self.neck.pos_from(self.O).to_matrix(self.base)[1].simplify()
            if modeltype == 0:
                return Matrix([x,y])
            elif modeltype == 1:
                return Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.L3, self.segmentlength["pelvis"]),
                        (self.L4, self.segmentlength["thorax"])
                    ]
                )
            elif modeltype == 2:
                args = (self.q1, self.q2, self.q3, self.q4)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.L3, self.segmentlength["pelvis"]),
                        (self.L4, self.segmentlength["thorax"])
                    ]
                )
                return sy.lambdify(args, f, "numpy")
            elif modeltype == 3:
                args = (self.q1, self.q2, self.q3, self.q4)
                f = Matrix([x,y]).subs(
                    [
                        (self.L1, self.segmentlength["Ltibia"]),
                        (self.L2, self.segmentlength["Lfemur"]),
                        (self.L3, self.segmentlength["pelvis"]),
                        (self.L4, self.segmentlength["thorax"])
                    ]
                )
                try:
                    num = kwargs["trial"]
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num]),axis=1).T
                except:
                    return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x),axis=1).T

    def getCOM(self, modeltype=0, **kwargs):
        try:
            com = self.com
        except:
            tibia, thigh, pelvis, thorax = self.getCOMposition("tibia",0), self.getCOMposition("femur",0), self.getCOMposition("pelvis",0), self.getCOMposition("thorax",0)
            com = (self.m1*tibia + self.m2*thigh + self.m3*pelvis + self.m4*thorax)/self.M
            self.com = com
        if modeltype == 0:
            return com
        elif modeltype == 1:
            com_ = com.subs(
                [
                    (self.l1, self.segmentCOMlength["Ltibia"]),
                    (self.l2, self.segmentCOMlength["Lfemur"]),
                    (self.l3, self.segmentCOMlength["pelvis"]),
                    (self.l4, self.HATlength),
                    (self.L1, self.segmentlength["Ltibia"]),
                    (self.L2, self.segmentlength["Lfemur"]),
                    (self.L3, self.segmentlength["pelvis"]),
                    (self.L4, self.segmentlength["thorax"]),
                    (self.m1, self.mass["tibia"]),
                    (self.m2, self.mass["femur"]),
                    (self.m3, self.mass["pelvis"]),
                    (self.m4,  (self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"])),
                    (self.M, self.weight)
                ]
            )
            return com_.evalf(3)
        elif modeltype == 2:
            args = (self.q1, self.q2, self.q3, self.q4)
            f = com.subs(
                [
                    (self.l1, self.segmentCOMlength["Ltibia"]),
                    (self.l2, self.segmentCOMlength["Lfemur"]),
                    (self.l3, self.segmentCOMlength["pelvis"]),
                    (self.l4, self.HATlength),
                    (self.L1, self.segmentlength["Ltibia"]),
                    (self.L2, self.segmentlength["Lfemur"]),
                    (self.L3, self.segmentlength["pelvis"]),
                    (self.L4, self.segmentlength["thorax"]),
                    (self.m1, self.mass["tibia"]),
                    (self.m2, self.mass["femur"]),
                    (self.m3, self.mass["pelvis"]),
                    (self.m4,  (self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"])),
                    (self.M, self.weight)
                ]
            )
            return sy.lambdify(args, f, "numpy")
        elif modeltype == 3:
            args = (self.q1, self.q2, self.q3, self.q4)
            f = com.subs(
                [
                    (self.l1, self.segmentCOMlength["Ltibia"]),
                    (self.l2, self.segmentCOMlength["Lfemur"]),
                    (self.l3, self.segmentCOMlength["pelvis"]),
                    (self.l4, self.HATlength),
                    (self.L1, self.segmentlength["Ltibia"]),
                    (self.L2, self.segmentlength["Lfemur"]),
                    (self.L3, self.segmentlength["pelvis"]),
                    (self.L4, self.segmentlength["thorax"]),
                    (self.m1, self.mass["tibia"]),
                    (self.m2, self.mass["femur"]),
                    (self.m3, self.mass["pelvis"]),
                    (self.m4,  (self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"])),
                    (self.M, self.weight)
                ]
            )
            try:
                num = kwargs["trial"]
                return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num]),axis=1).T
            except:    
                return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x , -self.angle[3].x),axis=1).T

    def jacobian_matrix(self, modeltype=0, **kwargs):
        com = self.getCOM(0)
        c1 = com.diff(self.q1)
        c2 = com.diff(self.q2)
        c3 = com.diff(self.q3)
        c4 = com.diff(self.q4)
        jacobian = Matrix(
            [
                [c1[0], c2[0], c3[0], c4[0]],
                [c1[1], c2[1], c3[1], c4[1]]
            ]
        )
        if modeltype == 0:
            return jacobian
        elif modeltype == 1:
            j = jacobian.subs(
                [
                    (self.l1, self.segmentCOMlength["Ltibia"]),
                    (self.l2, self.segmentCOMlength["Lfemur"]),
                    (self.l3, self.segmentCOMlength["pelvis"]),
                    (self.l4, self.HATlength),
                    (self.L1, self.segmentlength["Ltibia"]),
                    (self.L2, self.segmentlength["Lfemur"]),
                    (self.L3, self.segmentlength["pelvis"]),
                    (self.L4, self.segmentlength["thorax"]),
                    (self.m1, self.mass["tibia"]),
                    (self.m2, self.mass["femur"]),
                    (self.m3, self.mass["pelvis"]),
                    (self.m4,  (self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"])),
                    (self.M, self.weight)
                ]
            )
            return j.evalf(3)
        elif modeltype == 2:
            args = (self.q1, self.q2, self.q3, self.q4)
            f = jacobian.subs(
                [
                    (self.l1, self.segmentCOMlength["Ltibia"]),
                    (self.l2, self.segmentCOMlength["Lfemur"]),
                    (self.l3, self.segmentCOMlength["pelvis"]),
                    (self.l4, self.HATcomlength),
                    (self.L1, self.segmentlength["Ltibia"]),
                    (self.L2, self.segmentlength["Lfemur"]),
                    (self.L3, self.segmentlength["pelvis"]),
                    (self.L4, self.segmentlength["thorax"]),
                    (self.m1, self.mass["tibia"]),
                    (self.m2, self.mass["femur"]),
                    (self.m3, self.mass["pelvis"]),
                    (self.m4,  (self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"])),
                    (self.M, self.weight)
                ]
            )
            return sy.lambdify(args, f, "numpy")
        elif modeltype == 3:
            args = (self.q1, self.q2, self.q3, self.q4)
            f = jacobian.subs(
                [
                    (self.l1, self.segmentCOMlength["Ltibia"]),
                    (self.l2, self.segmentCOMlength["Lfemur"]),
                    (self.l3, self.segmentCOMlength["pelvis"]),
                    (self.l4, self.HATcomlength),
                    (self.L1, self.segmentlength["Ltibia"]),
                    (self.L2, self.segmentlength["Lfemur"]),
                    (self.L3, self.segmentlength["pelvis"]),
                    (self.L4, self.segmentlength["thorax"]),
                    (self.m1, self.mass["tibia"]),
                    (self.m2, self.mass["femur"]),
                    (self.m3, self.mass["pelvis"]),
                    (self.m4,  (self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"])),
                    (self.M, self.weight)
                ]
            )
            try:
                num = kwargs["trial"]
                return sy.lambdify(args, f, "numpy")(-self.angle.Lankle.x[num], self.angle.Lknee.x[num], -self.angle.Lhip.x[num]+self.angle.Lpelvis.x[num], -self.angle.Lspine.x[num]).T.transpose(0, 2, 1)
            except:
                return sy.lambdify(args, f, "numpy")(-self.angle.Lankle.x, self.angle.Lknee.x, -self.angle.Lhip.x+self.angle.Lpelvis.x[num], -self.angle.Lspine.x).T.transpose(0, 2, 1)

    def xCOMvel(self, **kwargs):
        jx = self.jacobian_matrix(1)[0,:]
        x1, x2, x3, x4 = jx[0]*self.q1_, jx[1]*self.q2_, jx[2]*self.q3_, jx[3]*self.q4_
        args1 = (self.q1, self.q2, self.q3, self.q4, self.q1_)
        args2 = (self.q1, self.q2, self.q3, self.q4, self.q2_)
        args3 = (self.q1, self.q2, self.q3, self.q4, self.q3_)
        args4 = (self.q1, self.q2, self.q3, self.q4, self.q4_)
        try:
            num = kwargs["trial"]
            x1_ = sy.lambdify(args1, x1, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num], -self.anglevel[0].z[num])
            x2_ = sy.lambdify(args2, x2, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num],  self.anglevel[1].x[num])
            x3_ = sy.lambdify(args3, x3, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num], -self.anglevel[2].x[num])
            x4_ = sy.lambdify(args4, x4, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num], -self.anglevel[3].x[num])
        except:
            x1_ = sy.lambdify(args1, x1, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x, -self.anglevel[0].z)
            x2_ = sy.lambdify(args2, x2, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x, self.anglevel[1].x)
            x3_ = sy.lambdify(args3, x3, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x, -self.anglevel[2].x)
            x4_ = sy.lambdify(args4, x4, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x, -self.anglevel[3].x)

        return np.array([x1_, x2_, x3_, x4_]).T

    def yCOMvel(self, **kwargs):
        jx = self.jacobian_matrix(1)[1,:]
        y1, y2, y3, y4 = jx[0]*self.q1_, jx[1]*self.q2_, jx[2]*self.q3_, jx[3]*self.q4_
        args1 = (self.q1, self.q2, self.q3, self.q4, self.q1_)
        args2 = (self.q1, self.q2, self.q3, self.q4, self.q2_)
        args3 = (self.q1, self.q2, self.q3, self.q4, self.q3_)
        args4 = (self.q1, self.q2, self.q3, self.q4, self.q4_)
        try:
            num = kwargs["trial"]
            y1_ = sy.lambdify(args1, y1, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num], -self.anglevel[0].z[num])
            y2_ = sy.lambdify(args2, y2, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num], self.anglevel[1].x[num])
            y3_ = sy.lambdify(args3, y3, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num], -self.anglevel[2].x[num])
            y4_ = sy.lambdify(args4, y4, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num], -self.anglevel[3].x[num])
        except:
            y1_ = sy.lambdify(args1, y1, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x, -self.anglevel.Lankle.x)
            y2_ = sy.lambdify(args2, y2, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x, self.anglevel.Lknee.x)
            y3_ = sy.lambdify(args3, y3, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x, -self.anglevel.Lhip.x)
            y4_ = sy.lambdify(args4, y4, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x, -self.anglevel.Lspine.x)

        return np.array([y1_, y2_, y3_, y4_]).T

    def antiGRAtorque(self, name, modeltype=1, **kwargs):
            if modeltype == 0:
                gravity_torque = Matrix([0,0])
                for i, j in zip(["tibia", "femur", "pelvis", "thorax"], [self.m1, self.m2, self.m3, self.m4]):
                    gravity_torque += -self.g*self.getCOMposition(i, 0)*j
                if name == "ankle":
                    return gravity_torque[1].diff(self.q1)
                elif name == "knee":
                    return gravity_torque[1].diff(self.q2)
                if name == "hip":
                    return gravity_torque[1].diff(self.q3)
                if name == "spine":
                    return gravity_torque[1].diff(self.q4)
            
            elif modeltype == 1:
                try:
                    gravity_torque = self.gravity_torque
                except:
                    gravity_torque = Matrix([0,0])
                    for i in ["tibia", "femur", "pelvis", "thorax"]:
                        if i == "thorax":
                            gravity_torque += -0.098*(-1)*self.getCOMposition(i,1)*(self.bodymass[i]+ self.bodymass["head"])
                        else:
                            gravity_torque += -0.098*(-1)*self.getCOMposition(i,1)*(self.bodymass[i])
                    self.gravity_torque = gravity_torque[1]
                    
                if name == "ankle":
                    return self.gravity_torque.diff(self.q1).evalf(3)
                elif name == "knee":
                    return self.gravity_torque.diff(self.q2).evalf(3)
                elif name == "hip":
                    return self.gravity_torque.diff(self.q3).evalf(3)
                elif name == "spine":
                    return self.gravity_torque.diff(self.q4).evalf(3)

            elif modeltype == 2:
                try:
                    f = self.gravity_torque
                except:
                    gravity_torque = Matrix([0,0])
                    for i in ["tibia", "femur", "pelvis", "thorax"]:
                        gravity_torque += -0.098*(-1)*self.getCOMposition(i,1)*self.bodymass[i]
                    self.gravity_torque = gravity_torque[1]
                    f = gravity_torque
                    if name == "ankle":
                        f = f.diff(self.q1)
                    elif name == "knee":
                        f = f.diff(self.q2)
                    elif name == "hip":
                        f = f.diff(self.q3)
                    elif name == "spine":
                        f = f.diff(self.q4)
                args = (self.q1, self.q2, self.q3, self.q4)
                return sy.lambdify(args, f, "numpy")
            elif modeltype == 3:                
                try:
                    f = self.gravity_torque
                except:
                    gravity_torque = Matrix([0,0])
                    for i in ["tibia", "femur", "pelvis", "thorax"]:
                        gravity_torque += -0.098*(-1)*self.getCOMposition(i,1)*self.bodymass[i]
                    self.gravity_torque = gravity_torque[1]
                    f = gravity_torque[1]
                if name == "ankle":
                    f = f.diff(self.q1)
                elif name == "knee":
                    f = f.diff(self.q2)
                elif name == "hip":
                    f = f.diff(self.q3)
                elif name == "spine":
                    f = f.diff(self.q4)
                args = (self.q1, self.q2, self.q3, self.q4)
                try:
                    num = kwargs["trial"]
                    return sy.lambdify(args, f, "numpy")(-self.angle[0].z[num], self.angle[1].x[num], -self.angle[2].x[num], -self.angle[3].x[num])
                except:
                    return sy.lambdify(args, f, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x)

    def mass_matrix(self):
        M11 = (
                        self.I1 + self.I2 + self.I3 + self.I4
                        + self.m1*self.l1**2
                        + self.m2*(self.L1**2 + 2*self.L1*self.l2*sin(self.q2) + self.l2**2)
                        + self.m3*(self.L1**2 + 2*self.L1*self.L2*cos(self.q2) + 2*self.L1*self.l3*cos(self.q1+self.q3) + self.L2**2 + 2*self.L2*self.l3*cos(self.q3)+self.l3**2)
                        + self.m4*(self.L1**2 + 2*self.L1*self.L2*cos(self.q2) + 2*self.L1*self.L3*cos(self.q2+self.q3) +2*self.L1*self.l4*cos(self.q2+self.q3+self.q4)+self.L2**2+2*self.L2*self.L3*cos(self.q3) + 2*self.L2*self.l4*cos(self.q3+self.q4)+self.L3**2+2*self.L3*self.l4*cos(self.q4)+self.l4**2)
                        )
        return M11




