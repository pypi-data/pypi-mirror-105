import numpy as np
from math import radians
import sympy as sy
from sympy import sin, cos, symbols, diff, Matrix
from sympy import solve, simplify
from sympy.physics.mechanics import LagrangesMethod, Lagrangian, inertia, outer
from sympy.physics.mechanics import ReferenceFrame, Particle, Point, RigidBody
from sympy.physics.mechanics import dynamicsymbols, kinetic_energy

from .sitmodel import mathModel
from .mass_matrix import MassMatrix
from .velocity_term import Velocity_term
from .gravity_term import Gravity_term
from .force_term import Force_term

class Modeling(object):
    def __init__(self, kinematics, parameter, **kwargs):
    # data from VICON
        self.test = parameter
        self.angle = [i.x for i in kinematics[0]]
        self.anglevel = [i.x for i in kinematics[1]]
        self.angleacc = [i.x for i in kinematics[2]]
        self.Length = parameter[0] # segment length
        self.length = parameter[1] # length to COM
        self.mass =parameter[2]
        if "weight" in kwargs:self.BW = kwargs["weight"]
        else:self.BW = parameter[3]
        self.HAT_m = self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"]
        
        # data for sympy
        self.q1, self.q2, self.q3, self.q4 = dynamicsymbols(r"q_1 q_2 q_3 q_4")
        self.vq1, self.vq2, self.vq3, self.vq4 = dynamicsymbols(r"\dot{q_1} \dot{q_2} \dot{q_3} \dot{q_4}")
        self.t, self.g = symbols("t g")
        self.m1, self.m2, self.m3, self.m4, self.M = symbols("m_1 m_2 m_3 m_4 M_{body}")
        self.l1, self.l2, self.l3, self.l4 = symbols("l_1 l_2 l_3 l_4")
        self.L1, self.L2, self.L3, self.L4 = symbols("L_1 L_2 L_3 L_4")
        self.I1, self.I2, self.I3, self.I4 = symbols("I_1 I_2 I_3 I_4")

        # initial process
        self.model = mathModel() # set Sympy model
        self.setHATlength()
        self.setInertia()
        self.MM = MassMatrix().mass_matrix 
        self.VEL = Velocity_term().VEL
        self.GRA = Gravity_term().GRA
        self.Force = Force_term().force


    def setHATlength(self):
        a = (self.mass["thorax"]*self.length["thorax"] + self.mass["head"]*(self.Length["thorax"]+self.length["head"]))
        b = (self.mass["thorax"] + self.mass["head"])
        self.HATlength = a / b

    def setInertia(self):
        self.I1_ = (self.mass["tibia"]*self.Length["Ltibia"]**2)/3
        self.I2_ = (self.mass["femur"]*self.Length["Lfemur"]**2)/3
        self.I3_ = (self.mass["pelvis"]*self.Length["pelvis"]**2)/3
        self.I4_ = ((self.mass["thorax"]+self.mass["head"]+self.mass["humerus"]+self.mass["radius"]+self.mass["hand"])*(self.Length["thorax"]+self.length["head"])**2)/3

    def substitute(self, res):
            return res.subs([
                (self.L1, self.Length["Ltibia"]), (self.L2, self.Length["Lfemur"]), (self.L3, self.Length["pelvis"]),
                (self.l1, self.length["Ltibia"]), (self.l2, self.length["Lfemur"]), (self.l3, self.length["pelvis"]), (self.l4, self.HATlength),
                (self.m1, self.mass["tibia"]), (self.m2, self.mass["femur"]), (self.m3, self.mass["pelvis"]), (self.m4, self.HAT_m),(self.M, self.BW),
                (self.I1, self.I1_), (self.I2, self.I2_), (self.I3, self.I3_), (self.I4, self.I4_),
                (self.g, -9.8)
                ])

    def SegCOMpos(self, name, modeltype="sympy1", **kwargs):
        """Summary line.
        Get the mass center coordinates of each segment. 
        Depending on the model type you specify, you can choose the coordinate format you get.

        Parameters
        ----------
        name : str
            Name of joint.
                - tibia
                - femur
                - pelvis
                - thorax
        modeltype : int
            - sympy1 :
            Output the mass center coordinates as a mathematical formula.
            - sympy2 :
            Output the formula of the mass center coordinates with the body parameters input.
            - ufunc :
            Output as a universal function of numpy.
            The variable is each joint angle.
            - value :
            The mass center coordinates of the segment for which the body parameters and joint angles are input are output. 
            That is, it is the actual coordinates of each segment.

        Returns
        -------
        Mathematical model of mass center coordinates of each segment.
        """
        if name == "tibia":
            x = self.model.com1.pos_from(self.model.O).to_matrix(self.model.base)[0].simplify()
            y = self.model.com1.pos_from(self.model.O).to_matrix(self.model.base)[1].simplify()
            res = Matrix([x,y])
            if modeltype == "sympy1" : return res
            elif modeltype == "sympy2" : return self.substitute(res).evalf(3)
            elif modeltype == "ufunc" :return  sy.lambdify((self.q1), self.substitute(res), "numpy")
            elif modeltype == "value":
                f = sy.lambdify((self.q1), self.substitute(res), "numpy")
                if "trial" in kwargs:
                    trial = kwargs["trial"]
                    return np.squeeze(f(-self.angle[0][trial]),axis=1).T
                else:
                    return np.squeeze(f(-self.angle[0]),axis=1).T

        elif name == "femur":
            x = self.model.com2.pos_from(self.model.O).to_matrix(self.model.base)[0].simplify()
            y = self.model.com2.pos_from(self.model.O).to_matrix(self.model.base)[1].simplify()
            res = Matrix([x,y])
            if modeltype == "sympy1" : return res
            elif modeltype == "sympy2" : return self.substitute(res).evalf(3)
            elif modeltype == "ufunc" :return sy.lambdify((self.q1, self.q2),  self.substitute(res), "numpy")
            elif modeltype == "value":
                f = sy.lambdify((self.q1, self.q2),  self.substitute(res), "numpy")
                if "trial" in kwargs:
                    trial = kwargs["trial"]
                    return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial]),axis=1).T
                else:
                    return np.squeeze(f(-self.angle[0], self.angle[1]),axis=1).T

        elif name == "pelvis":
            x = self.model.com3.pos_from(self.model.O).to_matrix(self.model.base)[0].simplify()
            y = self.model.com3.pos_from(self.model.O).to_matrix(self.model.base)[1].simplify()
            res = Matrix([x,y])
            if modeltype == "sympy1" : return res
            elif modeltype == "sympy2" : return self.substitute(res).evalf(3)
            elif modeltype == "ufunc" :return  sy.lambdify((self.q1, self.q2, self.q3), self.substitute(res), "numpy")
            elif modeltype == "value":
                f = sy.lambdify((self.q1, self.q2, self.q3), self.substitute(res), "numpy")
                if "trial" in kwargs:
                    trial = kwargs["trial"]
                    return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial]),axis=1).T
                else:
                    return np.squeeze(f(-self.angle[0], self.angle[1], -self.angle[2]),axis=1).T

        elif name == "thorax":
            x = self.model.com4.pos_from(self.model.O).to_matrix(self.model.base)[0].simplify()
            y = self.model.com4.pos_from(self.model.O).to_matrix(self.model.base)[1].simplify()
            res = Matrix([x,y])
            if modeltype == "sympy1" : return res
            elif modeltype == "sympy2" : return self.substitute(res).evalf(3)
            elif modeltype == "ufunc" :return  sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(res), "numpy")
            elif modeltype == "value":
                f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(res), "numpy")
                if "trial" in kwargs:
                    trial = kwargs["trial"]
                    return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial]),axis=1).T
                else:
                    return np.squeeze(f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3]),axis=1).T

    def JointCenterpos(self, name, modeltype = "sympy1", **kwargs):
        if name == "ankle":
            if modeltype == "value":
                if "trial" in kwargs:
                    trial = kwargs["trial"]
                return np.array([0]*self.angle[0][trial].size*2).reshape(-1,2)
            else:
                print("Please enter modeltype=value.")
        
        elif name == "knee":
            x = self.model.knee.pos_from(self.model.O).to_matrix(self.model.base)[0].simplify()
            y = self.model.knee.pos_from(self.model.O).to_matrix(self.model.base)[1].simplify()
            res = Matrix([x,y])
            if modeltype == "sympy1":return res
            elif modeltype == "sympy2":return self.substitute(res).evalf(3)
            elif modeltype == "ufunc":return  sy.lambdify((self.q1, self.q2), self.substitute(res), "numpy")
            elif modeltype == "value":
                f = sy.lambdify((self.q1, self.q2), self.substitute(res), "numpy")
                if "trial" in kwargs:
                    trial = kwargs["trial"]
                    return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial]),axis=1).T
                else:
                    return np.squeeze(f(-self.angle[0], self.angle[1]),axis=1).T

        elif name == "hip":
            x = self.model.hip.pos_from(self.model.O).to_matrix(self.model.base)[0].simplify()
            y = self.model.hip.pos_from(self.model.O).to_matrix(self.model.base)[1].simplify()
            res = Matrix([x,y])
            if modeltype == "sympy1":return res
            elif modeltype == "sympy2":return self.substitute(res).evalf(3)
            elif modeltype == "ufunc":return  sy.lambdify((self.q1, self.q2, self.q3), self.substitute(res), "numpy")
            elif modeltype == "value":
                f = sy.lambdify((self.q1, self.q2, self.q3), self.substitute(res), "numpy")
                if "trial" in kwargs:
                    trial = kwargs["trial"]
                    return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial]),axis=1).T
                else:
                    return np.squeeze(f(-self.angle[0], self.angle[1], -self.angle[2]),axis=1).T

        elif name == "spine":
            x = self.model.spine.pos_from(self.model.O).to_matrix(self.model.base)[0].simplify()
            y = self.model.spine.pos_from(self.model.O).to_matrix(self.model.base)[1].simplify()
            res = Matrix([x,y])
            if modeltype == "sympy1":return res
            elif modeltype == "sympy2":return self.substitute(res).evalf(3)
            elif modeltype == "ufunc":return  sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(res), "numpy")
            elif modeltype == "value":
                f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(res), "numpy")
                if "trial" in kwargs:
                    trial = kwargs["trial"]
                    return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial]),axis=1).T
                else:
                    return np.squeeze(f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3]),axis=1).T

        elif name == "neck":
            x = self.model.neck.pos_from(self.model.O).to_matrix(self.model.base)[0].simplify()
            y = self.model.neck.pos_from(self.model.O).to_matrix(self.model.base)[1].simplify()
            res = Matrix([x,y])
            if modeltype == "sympy1":return res
            elif modeltype == "sympy2":return self.substitute(res).evalf(3)
            elif modeltype == "ufunc":return  sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(res), "numpy")
            elif modeltype == "value":
                f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(res), "numpy")
                if "trial" in kwargs:
                    trial = kwargs["trial"]
                    return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial]),axis=1).T
                else:
                    return np.squeeze(f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3]),axis=1).T

    def COMpos(self, modeltype="sympy1", **kwargs):
        try:self.com
        except:
            mt = "sympy1"
            s1, s2, s3, s4 =  self.SegCOMpos("tibia",mt), self.SegCOMpos("femur",mt), self.SegCOMpos("pelvis",mt), self.SegCOMpos("thorax",mt)
            self.com = (self.m1*s1 + self.m2*s2 + self.m3*s3 + self.m4*s4)/self.M
        if modeltype == "sympy1":return self.com
        elif modeltype == "sympy2":return self.substitute(self.com).evalf(3)
        elif modeltype == "ufunc":return  sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.com), "numpy")
        elif modeltype == "value":
            f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.com), "numpy")
            if "trial" in kwargs:
                trial = kwargs["trial"]
                return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial]),axis=1).T
            else:
                return np.squeeze(f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3]),axis=1).T
        elif modeltype == "values":
            f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.com), "numpy")
            res = []
            for i in range(len(self.angle[0])):
                res.append(np.squeeze(f(-self.angle[0][i], self.angle[1][i], -self.angle[2][i], -self.angle[3][i]),axis=1).T)
            return res


    def jacobian_matrix(self, modeltype="sympy1", **kwargs):
        com = self.COMpos("sympy1")
        c1, c2, c3, c4 = com.diff(self.q1), com.diff(self.q2), com.diff(self.q3), com.diff(self.q4)
        jacobian = Matrix([
            [c1[0], c2[0], c3[0], c4[0]],
            [c1[1], c2[1], c3[1], c4[1]]
        ])
        if modeltype == "sympy1":return jacobian
        elif modeltype == "sympy2":return self.substitute(jacobian).evalf(3)
        elif modeltype == "ufunc":return sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.com), "numpy")
        elif modeltype == "value":
            f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(jacobian), "numpy")
            if "trial" in kwargs:
                trial = kwargs["trial"]
                return f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial])
            else:
                return f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3])

    def p_jacobian_matrix(self, modeltype="value", **kwargs):
        com = self.COMpos("sympy1")
        c1, c2, c3, c4 = com.diff(self.q1), com.diff(self.q2), com.diff(self.q3), com.diff(self.q4)
        jacobian = Matrix([
            [c1[0], c2[0], c3[0], c4[0]],
            [c1[1], c2[1], c3[1], c4[1]]
        ])
        if modeltype == "sympy1":return jacobian
        elif modeltype == "sympy2":return self.substitute(jacobian).evalf(3)
        elif modeltype == "ufunc":return sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.com), "numpy")
        elif modeltype == "value":
            f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(jacobian), "numpy")
            if "trial" in kwargs:
                trial = kwargs["trial"]
                return np.linalg.pinv(f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial]))
            else:
                return np.linalg.inv(f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3]))

    def jacobian_matrix2(self, modeltype="sympy1", **kwargs):
        if "trial" in kwargs:
            trial = kwargs["trial"]
            com = self.COMpos("sympy1")
            c1, c2, c3, c4 = com.diff(self.q1).diff(self.t), com.diff(self.q2).diff(self.t), com.diff(self.q3).diff(self.t), com.diff(self.q4).diff(self.t)
            c1 = self.substitute(c1)
            c2 = self.substitute(c2)
            c3 = self.substitute(c3)
            c4 = self.substitute(c4)
            f1 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.q1.diff(self.t), self.q2.diff(self.t), self.q3.diff(self.t), self.q4.diff(self.t)), c1, "numpy")
            f2 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.q1.diff(self.t), self.q2.diff(self.t), self.q3.diff(self.t), self.q4.diff(self.t)), c2, "numpy")
            f3 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.q1.diff(self.t), self.q2.diff(self.t), self.q3.diff(self.t), self.q4.diff(self.t)), c3, "numpy")
            f4 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.q1.diff(self.t), self.q2.diff(self.t), self.q3.diff(self.t), self.q4.diff(self.t)), c4, "numpy")
            res1 = f1(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[0][trial], self.anglevel[1][trial], -self.anglevel[2][trial], -self.anglevel[3][trial])
            res2 = f2(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[0][trial], self.anglevel[1][trial], -self.anglevel[2][trial], -self.anglevel[3][trial])
            res3 = f3(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[0][trial], self.anglevel[1][trial], -self.anglevel[2][trial], -self.anglevel[3][trial])
            res4 = f4(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[0][trial], self.anglevel[1][trial], -self.anglevel[2][trial], -self.anglevel[3][trial])
            res = np.array([
                [res1[0], res2[0], res3[0], res4[0]],
                [res1[1], res2[1], res3[1], res4[1]]
            ])
            return np.squeeze(res, axis=2)
        else:
            pass

        #jacobian = Matrix([
        #    [c1[0], c2[0], c3[0], c4[0]],
        #    [c1[1], c2[1], c3[1], c4[1]]
        #])
        #if modeltype == "sympy1":return jacobian
        #elif modeltype == "sympy2":return self.substitute(jacobian).evalf(3)
        #elif modeltype == "ufunc":return sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq1, self.vq2, self.vq3, self.vq4), self.substitute(self.com), "numpy")
        #elif modeltype == "value":
        #    f = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq1, self.vq2, self.vq3, self.vq4), self.substitute(self.com), "numpy")
        #    if "trial" in kwargs:
        #        trial = kwargs["trial"]
        #        return f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[0][trial], self.anglevel[1][trial], -self.anglevel[2][trial], -self.anglevel[3][trial])
        #    else:
        #        return f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3],-self.anglevel[0], self.anglevel[1], -self.anglevel[2], -self.anglevel[3])

    def xCOMvel(self, **kwargs):
        jm = self.jacobian_matrix("sympy2")[0,:]
        x1, x2, x3, x4 = jm[0]*self.vq1, jm[1]*self.vq2, jm[2]*self.vq3, jm[3]*self.vq4
        f1 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq1), x1, "numpy")
        f2 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq2), x2, "numpy")
        f3 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq3), x3, "numpy")
        f4 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq4), x4, "numpy")

        if "trial" in kwargs:
            trial = kwargs["trial"]
            x1_ = f1(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[0][trial])
            x2_ = f2(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], self.anglevel[1][trial])
            x3_ = f3(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[2][trial])
            x4_ = f4(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[3][trial])
            return np.array([x1_, x2_, x3_, x4_]).T
        elif "trials" in kwargs:
            res = []
            for i in range(self.angle[0]):
                x1_ = f1(-self.angle[0][i], self.angle[1][i], -self.angle[2][i], -self.angle[3][i], -self.anglevel[0][i])
                x2_ = f2(-self.angle[0][i], self.angle[1][i], -self.angle[2][i], -self.angle[3][i], self.anglevel[1][i])
                x3_ = f3(-self.angle[0][i], self.angle[1][i], -self.angle[2][i], -self.angle[3][i], -self.anglevel[2][i])
                x4_ = f4(-self.angle[0][i], self.angle[1][i], -self.angle[2][i], -self.angle[3][i], -self.anglevel[3][i])
                res.append(np.array([x1_, x2_, x3_, x4_]).T)
            return res
        else:
            x1_ = f1(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3], -self.anglevel[0])
            x2_ = f2(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3], self.anglevel[1])
            x3_ = f3(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3], -self.anglevel[2])
            x4_ = f4(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3], -self.anglevel[3])
            return np.array([x1_, x2_, x3_, x4_]).T
        

    def yCOMvel(self, **kwargs):
        jm = self.jacobian_matrix("sympy2")[1,:]
        y1, y2, y3, y4 = jm[0]*self.vq1, jm[1]*self.vq2, jm[2]*self.vq3, jm[3]*self.vq4
        f1 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq1), y1, "numpy")
        f2 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq2), y2, "numpy")
        f3 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq3), y3, "numpy")
        f4 = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq4), y4, "numpy")

        if "trial" in kwargs:
            trial = kwargs["trial"]
            y1_ = f1(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[0][trial])
            y2_ = f2(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial],  self.anglevel[1][trial])
            y3_ = f3(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[2][trial])
            y4_ = f4(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[3][trial])
            return np.array([y1_, y2_, y3_, y4_]).T
        elif "trials" in kwargs:
            res = []
            for i in range(len(self.angle[0])):
                y1_ = f1(-self.angle[0][i], self.angle[1][i], -self.angle[2][i], -self.angle[3][i], -self.anglevel[0][i])
                y2_ = f2(-self.angle[0][i], self.angle[1][i], -self.angle[2][i], -self.angle[3][i],  self.anglevel[1][i])
                y3_ = f3(-self.angle[0][i], self.angle[1][i], -self.angle[2][i], -self.angle[3][i], -self.anglevel[2][i])
                y4_ = f4(-self.angle[0][i], self.angle[1][i], -self.angle[2][i], -self.angle[3][i], -self.anglevel[3][i])
                res.append(np.array([y1_, y2_, y3_, y4_]).T)
            return res
        else:
            y1_ = f1(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3], -self.anglevel[0])
            y2_ = f2(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3], self.anglevel[1])
            y3_ = f3(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3], -self.anglevel[2])
            y4_ = f4(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3], -self.anglevel[3])
        return np.array([y1_, y2_, y3_, y4_]).T

    def antiGRAtorque(self, modeltype = "sympy1", **kwargs):
        if modeltype == "sympy1":return self.GRA
        elif modeltype == "sympy2":return self.substitute(self.GRA).evalf(3)
        elif modeltype == "ufunc":return sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.GRA), "numpy")
        elif modeltype == "value":
            f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.GRA), "numpy")
            try:
                trial = kwargs["trial"]
                return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial]), axis=1).T
            except:
                return np.squeeze(f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3]), axis=1).T
                
    def antiVELtorque(self, modeltype = "sympy1", **kwargs):
        if modeltype == "sympy1":return self.VEL
        elif modeltype == "sympy2":return self.substitute(self.VEL).evalf(3)
        elif modeltype == "ufunc":return sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq1, self.vq2, self.vq3, self.vq4), self.substitute(self.GRA), "numpy")
        elif modeltype == "value":
            f = sy.lambdify((self.q1, self.q2, self.q3, self.q4, self.vq1, self.vq2, self.vq3, self.vq4), self.substitute(self.VEL), "numpy")
            try:
                trial = kwargs["trial"]
                return np.squeeze(f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial], -self.anglevel[0][trial], self.anglevel[1][trial], -self.anglevel[2][trial], -self.anglevel[3][trial]), axis=1).T
            except:
                return np.squeeze(f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3],-self.anglevel[0], self.anglevel[1], -self.anglevel[2], -self.anglevel[3]), axis=1).T

    def Mmatrix(self, modeltype="sympy1", **kwargs):
        if modeltype == "sympy1":return self.MM
        elif modeltype == "sympy2":return self.substitute(self.MM).evalf(3)
        elif modeltype == "ufunc":return sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.MM), "numpy")
        elif modeltype == "value":
            f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.MM), "numpy")
            try:
                trial = kwargs["trial"]
                mm = np.array([f(a,b,c,d) for a,b,c,d in zip(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial])])
            except:
                mm = np.array([f(a,b,c,d) for a,b,c,d in zip(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3])])
            return mm


    def Motiontorque(self, modeltype = "sympy1", **kwargs):
        if modeltype == "sympy1":return self.MM
        elif modeltype == "sympy2":return self.substitute(self.MM).evalf(3)
        elif modeltype == "ufunc":return sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.MM), "numpy")
        elif modeltype == "value":
            f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.MM), "numpy")
            try:
                trial = kwargs["trial"]
                mm = np.array([f(a,b,c,d) for a,b,c,d in zip(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial])])
                acc = -np.array([i[trial] for i in self.angleacc])
                acc[1] = acc[1]*(-1)
                acc = acc.T
                return np.array([i*j for i, j in zip(mm,acc)])
            except:
                mm = np.array([f(a,b,c,d) for a,b,c,d in zip(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3])])
                acc = -self.angleacc
                acc[1] = acc[1]*(-1)
                acc = acc.T
                np.array([i*j for i, j in zip(mm,self.angleacc)])

    def antiForcetorque(self, modeltype="sympy1", **kwargs):
        if modeltype == "sympy1":return self.Force
        elif modeltype == "sympy2":return self.substitute(self.Force)
        elif modeltype == "ufunc":return sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.Force), "numpy")
        elif modeltype == "value":
            f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.Force), "numpy")
            try:
                trial = kwargs["trial"]
                return f(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial])
            except:
                return f(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3])


    def NETtorque(self, **kwargs):
        try:
            trial = kwargs["trial"]
            return self.Motiontorque("value", trial=trial).sum(axis=2) + self.antiVELtorque("value", trial=trial) + self.antiGRAtorque("value", trial=trial)
        except:
            return self.Motiontorque("value").sum(axis=2) + self.antiVELtorque("value") + self.antiGRAtorque("value")

    def NETtorqueVICON(self, **kwargs):
        try:
            trial = kwargs["trial"]
            return self.Motiontorque("value", trial=trial).sum(axis=2) - self.antiVELtorque("value", trial=trial) - self.antiGRAtorque("value", trial=trial)
        except:
            return self.Motiontorque("value").sum(axis=2) - self.antiVELtorque("value") - self.antiGRAtorque("value")


    def invMM(self, **kwargs):
        f = sy.lambdify((self.q1, self.q2, self.q3, self.q4), self.substitute(self.MM), "numpy")
        try:
            trial = kwargs["trial"]
            mm = np.array([f(a,b,c,d) for a,b,c,d in zip(-self.angle[0][trial], self.angle[1][trial], -self.angle[2][trial], -self.angle[3][trial])])
            return np.linalg.inv(mm)
        except:
            mm = np.array([f(a,b,c,d) for a,b,c,d in zip(-self.angle[0], self.angle[1], -self.angle[2], -self.angle[3])])
            return np.linalg.inv(mm)

    def IAA(self, **kwargs):
        try:
            trial = kwargs["trial"]
            MUS = self.Motiontorque("value", trial=trial).sum(axis=2) + self.antiVELtorque("value", trial=trial)
            VEL = (-1)*self.antiVELtorque("value", trial=trial)
            invMM = self.invMM(trial=trial)
            accMUS = np.array([matrix * vector for matrix, vector in zip(invMM, MUS)])
            accVEL = np.array([matrix * vector for matrix, vector in zip(invMM, VEL)])
            return accMUS, accVEL.sum(axis=2)
        except:
            MUS = self.Motiontorque("value").sum(axis=2) + self.antiVELtorque("value")
            VEL = (-1)*self.antiVELtorque("value")
            invMM = self.invMM()
            accMUS = np.array([matrix * vector for matrix, vector in zip(invMM, MUS)])
            accVEL = np.array([matrix * vector for matrix, vector in zip(invMM, VEL)])
            return accMUS, accVEL.sum(axis=2)


    def xCOMacc(self, **kwargs):
        if "trial" in kwargs:
            trial = kwargs["trial"]
            res = self.jacobian_matrix("value", trial=trial)[0].T
            invM = self.invMM(trial=trial)
            MUS = self.Motiontorque("value", trial=trial).sum(axis=2) + self.antiVELtorque("value", trial=trial)
            VEL = (-1)*self.antiVELtorque("value", trial=trial)
            res2 = self.jacobian_matrix2(trial=trial)[0]
            anglevel = np.array([i[trial] for i in self.anglevel])
            tau = []
            for i in range(res[:,0].size):
                tau.append(res[i] * invM[i].T)
            tau = np.array(tau).sum(axis=1)
            yCOMacc = tau * MUS
            vel = []
            for i in range(res[:,0].size):
                vel.append(invM[i]*VEL[i])
            vel = np.array(vel).sum(axis=2)
            vel_ = []
            for i in range(res[:,0].size):
                vel_.append(res[i]*vel[i])
            vel_ = np.array(vel_).sum(axis=1)
            vel2 = np.array([i*j for i, j in zip(res2, anglevel)]).sum(axis=0)
            return yCOMacc, vel_, vel2
        else:
            pass

    def yCOMacc(self, **kwargs):
        if "trial" in kwargs:
            trial = kwargs["trial"]
            res = self.jacobian_matrix("value", trial=trial)[1].T
            invM = self.invMM(trial=trial)
            MUS = self.Motiontorque("value", trial=trial).sum(axis=2) + self.antiVELtorque("value", trial=trial)
            VEL = (-1)*self.antiVELtorque("value", trial=trial)
            res2 = self.jacobian_matrix2(trial=trial)[1]
            anglevel = np.array([i[trial] for i in self.anglevel])
            tau = []
            for i in range(res[:,0].size):
                tau.append(res[i] * invM[i].T)
            tau = np.array(tau).sum(axis=1)
            yCOMacc = tau * MUS
            vel = []
            for i in range(res[:,0].size):
                vel.append(invM[i]*VEL[i])
            vel = np.array(vel).sum(axis=2)
            vel_ = []
            for i in range(res[:,0].size):
                vel_.append(res[i]*vel[i])
            vel_ = np.array(vel_).sum(axis=1)
            vel2 = np.array([i*j for i, j in zip(res2, anglevel)]).sum(axis=0)
            return yCOMacc, vel_, vel2
        else:
            pass



    




