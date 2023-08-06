from sympy import sin, cos, symbols, Matrix
from sympy.physics.mechanics import dynamicsymbols

class Gravity_term(object):
    def __init__(self):
        self.q1, self.q2, self.q3, self.q4 = dynamicsymbols(r"q_1 q_2 q_3 q_4")
        self.m1, self.m2, self.m3, self.m4, self.M = symbols("m_1 m_2 m_3 m_4 M")
        self.l1, self.l2, self.l3, self.l4 = symbols("l_1 l_2 l_3 l_4")
        self.L1, self.L2, self.L3, self.L4 = symbols("L_1 L_2 L_3 L_4")
        self.g = symbols("g")
        self.set_GRA()
    
    def set_GRA(self):
        self.g1 =   self.g * (
                        + self.m1*self.l1*sin(self.q1)
                        + self.m2*(self.L1*sin(self.q1)+self.l2*sin(self.q1+self.q2))
                        + self.m3*(self.L1*sin(self.q1)+self.L2*sin(self.q1+self.q2)+self.l3*sin(self.q1+self.q2+self.q3))
                        + self.m4*(self.L1*sin(self.q1)+self.L2*sin(self.q1+self.q2)+self.L3*sin(self.q1+self.q2+self.q3)+self.l4*sin(self.q1+self.q2+self.q3+self.q4))
        )
        self.g2 =   self.g * (
                        + self.m2*self.l2*sin(self.q1+self.q2)
                        + self.m3*(self.L2*sin(self.q1+self.q2)+self.l3*sin(self.q1+self.q2+self.q3))
                        + self.m4*(self.L2*sin(self.q1+self.q2)+self.L3*sin(self.q1+self.q2+self.q3)+self.l4*sin(self.q1+self.q2+self.q3+self.q4))                        
        )
        self.g3 =   self.g * (
                        + self.m3*self.l3*sin(self.q1+self.q2+self.q3)
                        + self.m4*(self.L3*sin(self.q1+self.q2+self.q3) + self.l4*sin(self.q1+self.q2+self.q3+self.q4))
        )
        self.g4 =   self.g * (
                        self.m4*self.l4*sin(self.q1+self.q2+self.q3+self.q4)
        )
        self.GRA = Matrix([
            [self.g1],
            [self.g2],
            [self.g3],
            [self.g4]
        ])
        return