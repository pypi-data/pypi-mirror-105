from sympy import sin, cos, symbols, Matrix
from sympy.physics.mechanics import dynamicsymbols

from sympy import sin, cos, symbols, Matrix
from sympy.physics.mechanics import dynamicsymbols

class MassMatrix(object):
    def __init__(self):
        self.q1, self.q2, self.q3, self.q4 = dynamicsymbols("q_1 q_2 q_3 q_4")
        self.I1, self.I2, self.I3, self.I4 = symbols("I_1 I_2 I_3 I_4")
        self.m1, self.m2, self.m3, self.m4, self.M = symbols("m_1 m_2 m_3 m_4 M")
        self.l1, self.l2, self.l3, self.l4 = symbols("l_1 l_2 l_3 l_4")
        self.L1, self.L2, self.L3, self.L4 = symbols("L_1 L_2 L_3 L_4")
        self.set_mass_matrix()


    def set_mass_matrix(self):
        self.M11 = (
                        self.I1 + self.I2 + self.I3 + self.I4
                        + self.m1*self.l1**2
                        + self.m2*(self.L1**2 + 2*self.L1*self.l2*cos(self.q2) + self.l2**2)
                        + self.m3*(self.L1**2 + 2*self.L1*self.L2*cos(self.q2) + 2*self.L1*self.l3*cos(self.q2+self.q3) + self.L2**2 + 2*self.L2*self.l3*cos(self.q3)+self.l3**2)
                        + self.m4*(self.L1**2 + 2*self.L1*self.L2*cos(self.q2) + 2*self.L1*self.L3*cos(self.q2+self.q3) +2*self.L1*self.l4*cos(self.q2+self.q3+self.q4)+self.L2**2+2*self.L2*self.L3*cos(self.q3) + 2*self.L2*self.l4*cos(self.q3+self.q4)+self.L3**2+2*self.L3*self.l4*cos(self.q4)+self.l4**2)
                        )
        self.M12 = (
                        self.I2 + self.I3 + self.I4
                        + self.l2*self.m2*(self.L1*cos(self.q2)+self.l2)
                        + self.m3*(self.L1*self.L2*cos(self.q2)+self.L1*self.l3*cos(self.q2+self.q3)+self.L2**2 + 2*self.L2*self.l3*cos(self.q3)+self.l3**2)
                        + self.m4*(self.L1*self.L2*cos(self.q2)+self.L1*self.L3*cos(self.q2+self.q3)+self.L1*self.l4*cos(self.q2+self.q3+self.q4)+self.L2**2 + 2*self.L2*self.L3*cos(self.q3)+2*self.L2*self.l4*cos(self.q3 + self.q4)+2*self.L3*self.l4*cos(self.q4)+self.l4**2)
        )
        self.M13 = (
                        self.I3 +self.I4
                        +self.l3*self.m3*(self.L1*cos(self.q2+self.q3)+self.L2*cos(self.q3)+self.l3)
                        +self.m4*(self.L1*self.L3*cos(self.q2+self.q3)+self.L1*self.l4*cos(self.q2+self.q3+self.q4)+self.L2*self.L3*cos(self.q3)+self.L2*self.l4*cos(self.q3+self.q4)+self.L3**2+2*self.L3*self.l4*cos(self.q4)+self.l4**2)
                                
        )
        self.M14 = (
                        self.I4
                        +self.l4*self.m4*(self.L1*cos(self.q2+self.q3+self.q4)+self.L2*cos(self.q3+self.q4)+self.L3*cos(self.q4)+self.l4)
        )
        self.M21 = (
                        self.I2 + self.I3 + self.I4
                        +self.l2*self.m2*(self.L1*cos(self.q2)+self.l2)
                        +self.m3*(self.L1*self.L2*cos(self.q2)+self.L1*self.l3*cos(self.q2+self.q3)+self.L2**2+2*self.L2*self.l3*cos(self.q3)+self.l3**2)
                        +self.m4*(self.L1*self.L2*cos(self.q2)+self.L1*self.L3*cos(self.q2+self.q3)+self.L1*self.l4*cos(self.q2+self.q3+self.q4)+self.L2**2 +2*self.L2*self.L3*cos(self.q3)+2*self.L2*self.l4*cos(self.q3+self.q4)+self.L3**2+2*self.L3*self.l4*cos(self.q4)+self.l4**2)
        )
        self.M22 = (
                        self.I2 + self.I3 + self.I4
                        +self.l2**2*self.m2
                        +self.m3*(self.L2**2+2*self.L2*self.l3*cos(self.q3)+self.l3**2)
                        +self.m4*(self.L2**2+2*self.L2*self.L3*cos(self.q3)+2*self.L2*self.l4*cos(self.q3+self.q4)+self.L3**2+2*self.L3*self.l4*cos(self.q4)+self.l4**2)
        )
        self.M23 = (
                        self.I3 + self.I4
                        +self.l3*self.m3*(self.L2*cos(self.q3)+self.l3)
                        +self.m4*(self.L2*self.L3*cos(self.q3)+self.L2*self.l4*cos(self.q3+self.q4)+self.L3**2+2*self.L3*self.l4*cos(self.q4)+self.l4**2)
        )
        self.M24 = (
                        self.I4
                        +self.l4*self.m4*(self.L2*cos(self.q3+self.q4)+self.L3*cos(self.q4)+self.l4)
        )
        self.M31 = (
                        self.I3 + self.I4
                        +self.l3*self.m3*(self.L1*cos(self.q2+self.q3)+self.L2*cos(self.q3)+self.l3)
                        +self.m4*(self.L1*self.L3*cos(self.q2+self.q3)+self.L1*self.l4*cos(self.q2+self.q3+self.q4)+self.L2*self.L3*cos(self.q3) + self.L2*self.l4*cos(self.q3+self.q4)+self.L3**2 +2*self.L3*self.l4*cos(self.q4)+self.l4**2)
        )
        self.M32 = (
                        self.I3 + self.I4
                        +self.l3*self.m3*(self.L2*cos(self.q3) + self.l3)
                        +self.m4*(self.L2*self.L3*cos(self.q3)+self.L2*self.l4*cos(self.q3+self.q4)+self.L3**2 + 2*self.L3*self.l4*cos(self.q4)+self.l4**2)
                        
        )
        self.M33 = (
                        self.I3 + self.I4
                        +self.l3**2*self.m3
                        +self.m4*(self.L3**2+2*self.L3*self.l4*cos(self.q4)+self.l4**2)
        )
        self.M34 = (
                        self.I4
                        +self.l4*self.m4*(self.L3*cos(self.q4)+self.l4)
        )
        self.M41 = (
                        self.I4
                        +self.l4*self.m4*(self.L1*cos(self.q2+self.q3+self.q4)+self.L2*cos(self.q3+self.q4)+self.L3*cos(self.q4)+self.l4)
        )
        self.M42 = (
                        self.I4
                        +self.l4*self.m4*(self.L2*cos(self.q3+self.q4)+self.L3*cos(self.q4)+self.l4)
        )
        self.M43 = (
                        self.I4
                        +self.l4*self.m4*(self.L3*cos(self.q4)+self.l4)
        )
        self.M44 = (
                        self.I4+self.l4**2*self.m4
        )
        self.mass_matrix = Matrix([
            [self.M11,self.M12,self.M13,self.M14],
            [self.M21,self.M22,self.M23,self.M24],
            [self.M31,self.M32,self.M33,self.M34],
            [self.M41,self.M42,self.M43,self.M44]
        ])
        return