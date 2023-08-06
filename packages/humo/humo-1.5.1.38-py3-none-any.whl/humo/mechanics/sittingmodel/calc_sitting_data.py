import numpy as np
import matplotlib.pyplot as plt
from math import radians

import sympy as sy
from sympy import sin, cos, symbols, diff, Matrix
from sympy import solve, simplify
from sympy.physics.mechanics import LagrangesMethod, Lagrangian, inertia, outer
from sympy.physics.mechanics import ReferenceFrame, Particle, Point, RigidBody
from sympy.physics.mechanics import dynamicsymbols, kinetic_energy




class SittingModel2(object):
    def __init__(self, model, parameter, kinematics):
        self.model = model
        self.mass_matrix = self.model.mass_matrix
        self.gra = self.model.gra
        self.h = self.model.h
        self.Length = parameter[0]
        self.length = parameter[1]
        self.mass = parameter[2]
        self.angle = kinematics[0]
        self.dangle = kinematics[1]
        self.ddangle = kinematics[2]
        self.setHATlength()
        self.setInertia()


    def setHATlength(self):
        a = (self.mass["thorax"]*self.length["thorax"] + self.mass["head"]*(self.Length["thorax"]+self.length["head"]))
        b = (self.mass["thorax"] + self.mass["head"])
        self.HATlength = a/b
    
    def setInertia(self):
        self.I1 = (self.mass["tibia"]*self.Length["Ltibia"]**2)/3
        self.I2 = (self.mass["femur"]*self.Length["Lfemur"]**2)/3
        self.I3 = (self.mass["pelvis"]*self.Length["pelvis"]**2)/3
        self.I4 = ((self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"])*(self.Length["thorax"]+self.length["head"])**2)/3

    def GRA(self, modeltype=1, **kwargs):
        if modeltype == 1:
            return self.gra.subs([
                (self.model.L1, self.Length["Ltibia"]),
                (self.model.L2, self.Length["Lfemur"]),
                (self.model.L3, self.Length["pelvis"]),
                (self.model.l1, self.length["Ltibia"]),
                (self.model.l2, self.length["Lfemur"]),
                (self.model.l3, self.length["pelvis"]),
                (self.model.l4, self.HATlength),
                (self.model.m1, self.mass["tibia"]),
                (self.model.m2, self.mass["femur"]),
                (self.model.m3, self.mass["pelvis"]),
                (self.model.m4, self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]),
                (self.model.g, -0.098)
                ]).evalf(3)
        elif modeltype == 2:
            f =  self.gra.subs([
                (self.model.L1, self.Length["Ltibia"]),
                (self.model.L2, self.Length["Lfemur"]),
                (self.model.L3, self.Length["pelvis"]),
                (self.model.l1, self.length["Ltibia"]),
                (self.model.l2, self.length["Lfemur"]),
                (self.model.l3, self.length["pelvis"]),
                (self.model.l4, self.HATlength),
                (self.model.m1, self.mass["tibia"]),
                (self.model.m2, self.mass["femur"]),
                (self.model.m3, self.mass["pelvis"]),
                (self.model.m4, self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]),
                (self.model.g, -0.098)
                ])
            args = (self.model.q1,self.model.q2,self.model.q3,self.model.q4)
            return sy.lambdify(args, f, "numpy")
        elif modeltype == 3:
            f =  self.gra.subs([
                (self.model.L1, self.Length["Ltibia"]),
                (self.model.L2, self.Length["Lfemur"]),
                (self.model.L3, self.Length["pelvis"]),
                (self.model.l1, self.length["Ltibia"]),
                (self.model.l2, self.length["Lfemur"]),
                (self.model.l3, self.length["pelvis"]),
                (self.model.l4, self.HATlength),
                (self.model.m1, self.mass["tibia"]),
                (self.model.m2, self.mass["femur"]),
                (self.model.m3, self.mass["pelvis"]),
                (self.model.m4, self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]),
                (self.model.g, -0.098)
                ])
            args = (self.model.q1,self.model.q2,self.model.q3,self.model.q4)
            try:
                trial = kwargs["trial"]
                return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z[trial], self.angle[1].x[trial], -self.angle[2].x[trial], -self.angle[3].x[trial]),axis=1).T
            except:
                return np.squeeze(sy.lambdify(args, f, "numpy")(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x),axis=1).T


    def MIT(self, modeltype, **kwargs):
        if modeltype == 1:
            return self.mass_matrix.subs([
                (self.model.L1, self.Length["Ltibia"]),
                (self.model.L2, self.Length["Lfemur"]),
                (self.model.L3, self.Length["pelvis"]),
                (self.model.l1, self.length["Ltibia"]),
                (self.model.l2, self.length["Lfemur"]),
                (self.model.l3, self.length["pelvis"]),
                (self.model.l4, self.HATlength),
                (self.model.m1, self.mass["tibia"]),
                (self.model.m2, self.mass["femur"]),
                (self.model.m3, self.mass["pelvis"]),
                (self.model.m4, self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]),
                (self.model.I1, self.I1),
                (self.model.I2, self.I2),
                (self.model.I3, self.I3),
                (self.model.I4, self.I4,)
                ]).evalf(3)
        if modeltype == 2:
            f =  self.mass_matrix.subs([
                (self.model.L1, self.Length["Ltibia"]),
                (self.model.L2, self.Length["Lfemur"]),
                (self.model.L3, self.Length["pelvis"]),
                (self.model.l1, self.length["Ltibia"]),
                (self.model.l2, self.length["Lfemur"]),
                (self.model.l3, self.length["pelvis"]),
                (self.model.l4, self.HATlength),
                (self.model.m1, self.mass["tibia"]),
                (self.model.m2, self.mass["femur"]),
                (self.model.m3, self.mass["pelvis"]),
                (self.model.m4, self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]),
                (self.model.I1, self.I1),
                (self.model.I2, self.I2),
                (self.model.I3, self.I3),
                (self.model.I4, self.I4,)
                ])
            args = (self.model.q1, self.model.q2, self.model.q3, self.model.q4)
            return sy.lambdify(args, f, "numpy")
        if modeltype == 3:
            f =  self.mass_matrix.subs([
                (self.model.L1, self.Length["Ltibia"]),
                (self.model.L2, self.Length["Lfemur"]),
                (self.model.L3, self.Length["pelvis"]),
                (self.model.l1, self.length["Ltibia"]),
                (self.model.l2, self.length["Lfemur"]),
                (self.model.l3, self.length["pelvis"]),
                (self.model.l4, self.HATlength),
                (self.model.m1, self.mass["tibia"]),
                (self.model.m2, self.mass["femur"]),
                (self.model.m3, self.mass["pelvis"]),
                (self.model.m4, self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]),
                (self.model.I1, self.I1),
                (self.model.I2, self.I2),
                (self.model.I3, self.I3),
                (self.model.I4, self.I4,)
                ])
            args = (self.model.q1, self.model.q2, self.model.q3, self.model.q4)
            f = sy.lambdify(args, f, "numpy")
            try:
                trial = kwargs["trial"]
                M = []
                for a,b,c,d in zip(-self.angle[0].z[trial], self.angle[1].x[trial], -self.angle[2].x[trial], -self.angle[3].x[trial]):
                    M.append(f(a,b,c,d))
                return np.array(M)
                #return f(-self.angle[0].z[trial], self.angle[1].x[trial], -self.angle[2].x[trial], -self.angle[3].x[trial])
            except:
                M = []
                for a,b,c,d in zip(-self.angle[0].z, self.angle[1].x, -self.angle[2].x, -self.angle[3].x):
                    M.append(f(a,b,c,d))
                return np.array(M)

    def massf(self, **kwargs):
        try:
            trial = kwargs["trial"]
            acc = np.array([
                [-self.ddangle[0].z[trial]*0.0001],
                [self.ddangle[1].x[trial]*0.0001],
                [-self.ddangle[2].x[trial]*0.0001],
                [-self.ddangle[3].x[trial]*0.0001]
            ]).T
            f = self.MIT(3, trial=trial)
            res = []
            for i, j in zip(f, acc):
                res.append(i*j)
            return np.array(res)
        except:
            acc = np.array([
                [-self.ddangle[0].z*0.0001],
                [self.ddangle[1].x*0.0001],
                [-self.ddangle[2].x*0.0001],
                [-self.ddangle[3].x*0.0001]
            ]).T
            f = self.MIT(3)
            res = []
            for i, j in zip(f, acc):
                res.append(i*j)
            return np.array(res)


    def ccf(self, modeltype, **kwargs):
        if modeltype == 1:
            return self.h.subs([
                (self.model.L1, self.Length["Ltibia"]),
                (self.model.L2, self.Length["Lfemur"]),
                (self.model.L3, self.Length["pelvis"]),
                (self.model.l1, self.length["Ltibia"]),
                (self.model.l2, self.length["Lfemur"]),
                (self.model.l3, self.length["pelvis"]),
                (self.model.l4, self.HATlength),
                (self.model.m1, self.mass["tibia"]),
                (self.model.m2, self.mass["femur"]),
                (self.model.m3, self.mass["pelvis"]),
                (self.model.m4, self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]),
                ]).evalf(3)
        elif modeltype == 2:
            f =  self.h.subs([
                (self.model.L1, self.Length["Ltibia"]),
                (self.model.L2, self.Length["Lfemur"]),
                (self.model.L3, self.Length["pelvis"]),
                (self.model.l1, self.length["Ltibia"]),
                (self.model.l2, self.length["Lfemur"]),
                (self.model.l3, self.length["pelvis"]),
                (self.model.l4, self.HATlength),
                (self.model.m1, self.mass["tibia"]),
                (self.model.m2, self.mass["femur"]),
                (self.model.m3, self.mass["pelvis"]),
                (self.model.m4, self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]),
                ])
            args = (self.model.q1, self.model.q2, self.model.q3, self.model.q4, self.model.vq1, self.model.vq2, self.model.vq3, self.model.vq4)
            return sy.lambdify(args, f, "numpy")
        elif modeltype == 3:
            f =  self.h.subs([
                (self.model.L1, self.Length["Ltibia"]),
                (self.model.L2, self.Length["Lfemur"]),
                (self.model.L3, self.Length["pelvis"]),
                (self.model.l1, self.length["Ltibia"]),
                (self.model.l2, self.length["Lfemur"]),
                (self.model.l3, self.length["pelvis"]),
                (self.model.l4, self.HATlength),
                (self.model.m1, self.mass["tibia"]),
                (self.model.m2, self.mass["femur"]),
                (self.model.m3, self.mass["pelvis"]),
                (self.model.m4, self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]),
                ])
            args = (self.model.q1, self.model.q2, self.model.q3, self.model.q4, self.model.vq1, self.model.vq2, self.model.vq3, self.model.vq4)
            f = sy.lambdify(args, f, "numpy")
            try:
                trial = kwargs["trial"]
                return np.squeeze(f( -self.angle[0].z[trial],
                                                self.angle[1].x[trial],
                                                -self.angle[2].x[trial],
                                                -self.angle[3].x[trial],
                                                -self.dangle[0].z[trial]*0.02,
                                                self.dangle[1].x[trial]*0.02,
                                                -self.dangle[2].x[trial]*0.02,
                                                -self.dangle[3].x[trial]*0.02
                                                ),axis=1).T
            except:
                return np.squeeze(f(-self.angle[0].z,
                                                self.angle[1].x,
                                                -self.angle[2].x,
                                                -self.angle[3].x,
                                                -self.dangle[0].z*0.02,
                                                self.dangle[1].x*0.02,
                                                -self.dangle[2].x*0.02,
                                                -self.dangle[3].x*0.02), axis=1).T




