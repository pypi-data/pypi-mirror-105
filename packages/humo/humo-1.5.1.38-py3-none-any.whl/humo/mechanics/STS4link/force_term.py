from sympy import sin, cos, symbols, Matrix
from sympy.physics.mechanics import dynamicsymbols

class Force_term(object):
    def __init__(self):
        self.q1, self.q2, self.q3, self.q4 = dynamicsymbols(r"q_1 q_2 q_3 q_4")
        self.vq1, self.vq2, self.vq3, self.vq4 = dynamicsymbols(r"\dot{q_1} \dot{q_2} \dot{q_3} \dot{q_4}")
        self.m1, self.m2, self.m3, self.m4, self.M = symbols("m_1 m_2 m_3 m_4 M")
        self.l1, self.l2, self.l3, self.l4 = symbols("l_1 l_2 l_3 l_4")
        self.L1, self.L2, self.L3, self.L4 = symbols("L_1 L_2 L_3 L_4")
        self.set_force()

    def set_force(self):
        self.f1x = (
            -self.L1*cos(self.q1) - self.L2*cos(self.q1+self.q2)
        )
        self.f1y = (
            -self.L1*sin(self.q1) - self.L2*sin(self.q1+self.q2)
        )
        self.f2x = (
            - self.L2*cos(self.q1+self.q2)
        )
        self.f2y = (
            - self.L2*sin(self.q1+self.q2)
        )
        self.f3x = 0
        self.f3y = 0
        self.f4x = 0
        self.f4y = 0
        
        self.force = Matrix([
            [self.f1x, self.f1y],
            [self.f2x, self.f2y],
            [self.f3x, self.f3y],
            [self.f4x, self.f4y]
        ])
