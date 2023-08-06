import numpy as np
from math import radians

import sympy as sy
from sympy import sin, cos, symbols, diff, Matrix
from sympy import solve, simplify
from sympy.physics.mechanics import LagrangesMethod, Lagrangian, inertia, outer
from sympy.physics.mechanics import ReferenceFrame, Particle, Point, RigidBody
from sympy.physics.mechanics import dynamicsymbols, kinetic_energy

class mathModel(object):
    def __init__(self):
        # data for sympy
        self.q1, self.q2, self.q3, self.q4 = dynamicsymbols(r"q_1 q_2 q_3 q_4")
        self.q1_, self.q2_, self.q3_, self.q4_ = dynamicsymbols(r"\dot{q_1} \dot{q_2} \dot{q_3} \dot{q_4}")
        self.t, self.g = symbols("t g")
        self.m1, self.m2, self.m3, self.m4, self.M = symbols("m_1 m_2 m_3 m_4 M")
        self.l1, self.l2, self.l3, self.l4 = symbols("l_1 l_2 l_3 l_4")
        self.L1, self.L2, self.L3, self.L4 = symbols("L_1 L_2 L_3 L_4")
        self.I1, self.I2, self.I3, self.I4 = symbols("I_1 I_2 I_3 I_4")
        self.setModel()

    # setting for sitting model
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
