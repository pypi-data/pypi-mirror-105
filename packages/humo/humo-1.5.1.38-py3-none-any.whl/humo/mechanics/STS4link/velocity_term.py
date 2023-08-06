from sympy import sin, cos, symbols, Matrix
from sympy.physics.mechanics import dynamicsymbols

class Velocity_term(object):
	def __init__(self):
		self.q1, self.q2, self.q3, self.q4 = dynamicsymbols(r"q_1 q_2 q_3 q_4")
		self.vq1, self.vq2, self.vq3, self.vq4 = dynamicsymbols(r"\dot{q_1} \dot{q_2} \dot{q_3} \dot{q_4}")
		self.m1, self.m2, self.m3, self.m4, self.M = symbols("m_1 m_2 m_3 m_4 M")
		self.l1, self.l2, self.l3, self.l4 = symbols("l_1 l_2 l_3 l_4")
		self.L1, self.L2, self.L3, self.L4 = symbols("L_1 L_2 L_3 L_4")
		self.set_h()

        
	def set_h(self):
		self.h1 = (
			self.L1*self.L2*(2*self.m3*sin(self.q2)*self.vq1*self.vq2 + self.m3*sin(self.q2)*self.vq2**2 + 2*self.L1*self.L2*self.m4*sin(self.q2)*self.vq1*self.vq2 + self.L1*self.L2*self.m4*sin(self.q2)*self.vq2**2) +
			self.L1*self.L3*(2*self.m4*sin(self.q2+self.q3)*self.vq1*self.vq2 + 2*self.m4*sin(self.q2+self.q3)*self.vq1*self.vq3 + self.m4*sin(self.q2+self.q3)*self.vq2**2 + 2*self.m4*sin(self.q2+self.q3)*self.vq2*self.vq3 + self.m4*sin(self.q2+self.q3)*self.vq3**2) +
			self.L1*self.l2*(self.m2*sin(self.q2)*self.vq1*self.vq2 + self.m2*sin(self.q2)*self.vq2**2) +
			self.L1*self.l3*(2*self.m3*sin(self.q2+self.q3)*self.vq1*self.vq2 + 2*self.m3*sin(self.q2+self.q3)*self.vq1*self.vq3 + self.m3*sin(self.q2+self.q3)*self.vq2**2 + 2*self.m3*sin(self.q2+self.q3)*self.vq2*self.vq3 + self.m3*sin(self.q2+self.q3)*self.vq3**2) +
			self.L1*self.l4*(2*self.m4*sin(self.q2+self.q3+self.q4)*self.vq1*self.vq2 + 2*self.m4*sin(self.q2+self.q3+self.q4)*self.vq1*self.vq3 +2*self.m4*sin(self.q2+self.q3+self.q4)*self.vq1*self.vq4 + self.m4*sin(self.q2+self.q3+self.q4)*self.vq2**2 + 2*self.m4*sin(self.q2+self.q3+self.q4)*self.vq2*self.vq3 + self.m4*sin(self.q2+self.q3+self.q4)*self.vq2*self.vq4 + self.m4*sin(self.q2+self.q3+self.q4)*self.vq3**2 + 2*self.m4*sin(self.q2+self.q3+self.q4)*self.vq3*self.vq4 + self.m4*sin(self.q2+self.q3+self.q4)*self.vq4**2) +
			self.L2*self.L3*(2*self.m4*sin(self.q3)*self.vq1*self.vq3 + 2*self.m4*sin(self.q3)*self.vq2*self.vq3 + self.m4*sin(self.q3)*self.vq3**2) +
			self.L2*self.l3*(2*self.m3*sin(self.q3)*self.vq1*self.vq3 + 2*self.m3*sin(self.q3)*self.vq2*self.vq3 + self.m3*sin(self.q3)*self.vq3**2) + 
			self.L2*self.l4*(2*self.m4*sin(self.q3+self.q4)*self.vq1*self.vq3 + 2*self.m4*sin(self.q3+self.q4)*self.vq1*self.vq4 + 2*self.m4*sin(self.q3+self.q4)*self.vq2*self.vq3 +2*self.m4*sin(self.q3+self.q4)*self.vq2*self.vq4 + self.m4*sin(self.q3+self.q4)*self.vq3**2 + 2*self.m4*sin(self.q3+self.q4)*self.vq3*self.vq4 + self.m4*sin(self.q3+self.q4)*self.vq4**2) +
			self.L3*self.l4*(2*self.m4*sin(self.q4)*self.vq1*self.vq4 + 2*self.m4*sin(self.q4)*self.vq2*self.vq4 + 2*self.m4*sin(self.q4)*self.vq3*self.vq4 + self.m4*sin(self.q4)*self.vq4**2)
		)

		self.h2 = (
			-self.L1*self.L2*(self.m3*sin(self.q2)*self.vq1**2 + self.m4*sin(self.q2)*self.vq1**2) +
			-self.L1*self.L3*self.m4*sin(self.q2+self.q3)*self.vq1**2 +
			-self.L1*self.l2*self.m2*sin(self.q2)*self.vq1**2 +
			-self.L1*self.l3*sin(self.q2+self.q3)*self.vq1**2 +
			-self.L1*self.l4*self.m4*sin(self.q2+self.q3+self.q4)*self.vq1**2 +
			self.L2*self.L3*(2*self.m4*sin(self.q3)*self.vq1*self.vq3 + 2*self.m4*sin(self.q3)*self.vq2*self.vq3 + self.m4*sin(self.q3)*self.vq3**2)+
			self.L2*self.l3*(self.m3*sin(self.q3)*self.vq1*self.vq3 + 2*self.m3*sin(self.q3)*self.vq2*self.vq3 + self.m3*sin(self.q3)*self.vq3**2) +
			self.L2*self.l4*(2*self.m4*sin(self.q3+self.q4)*self.vq1*self.vq3 + 2*self.m4*sin(self.q3+self.q4)*self.vq1*self.vq4 + 2*self.m4*sin(self.q3+self.q4)*self.vq2*self.vq3 +2*self.m4*sin(self.q3+self.q4)*self.vq2*self.vq4 + self.m4*sin(self.q3+self.q4)*self.vq3**2 + 2*self.m4*sin(self.q3+self.q4)*self.vq3*self.vq4 + self.m4*sin(self.q3+self.q4)*self.vq4**2) +
			self.L3*self.l4*(2*self.m4*sin(self.q4)*self.vq1*self.vq4 + 2*self.m4*sin(self.q4)*self.vq2*self.vq4 + 2*self.m4*sin(self.q4)*self.vq3*self.vq4 + self.m4*sin(self.q4)*self.vq4**2)
		)

		self.h3 = (
			-self.L1*self.L3*self.m4*sin(self.q2+self.q3)*self.vq1**2 +
			-self.L1*self.l3*self.m3*sin(self.q2+self.q3)*self.vq1**2 +
			-self.L1*self.l4*sin(self.q2+self.q3+self.q4)*self.vq1**2 +
			-self.L2*self.L3*(self.m4*sin(self.q3)*self.vq1**2 + 2*self.m4*sin(self.q3)*self.vq1*self.vq2 +self.m4*sin(self.q3)*self.vq2**2) +
			-self.L2*self.l3*(self.m3*sin(self.q3)*self.vq1**2 + 2*self.m3*sin(self.q3)*self.vq1*self.vq2 + self.m3*sin(self.q3)*self.vq2**2) + 
			-self.L2*self.l4*(self.m4*sin(self.q3+self.q4)*self.vq1**2 + 2*self.m4*sin(self.q3+self.q4)*self.vq1*self.vq2 + self.m4*sin(self.q3+self.q4)*self.vq2**2) + 
			self.L3*self.l4*(self.m4*sin(self.q4)*self.vq1*self.vq4 +2*self.m4*sin(self.q4)*self.vq2*self.vq4 + 2*self.m4*sin(self.q4)*self.vq3*self.vq4 + self.m4*sin(self.q4)*self.vq4**2)
		)

		self.h4 = (
			-self.l4*self.m4*(self.L1*sin(self.q2+self.q3+self.q4)*self.vq1**2 + self.L2*sin(self.q3+self.q4)*self.vq1**2 + 2*self.L2*sin(self.q3 + self.q4)*self.vq1*self.vq2 + self.L2*sin(self.q3+self.q4)*self.vq2**2 +self.L3*sin(self.q4)*self.vq1**2 + self.L3*sin(self.q4)*self.vq1**2 +2*self.L3*sin(self.q4)*self.vq1*self.vq2 + 2*self.L3*sin(self.q4)*self.vq1*self.vq3 + self.L3*sin(self.q4)*self.vq2**2 + 2*self.L3*sin(self.q4)*self.vq2*self.vq3 + self.L3*sin(self.q4)*self.vq3**2) 
		)

		self.VEL = Matrix([
			[self.h1],
			[self.h2],
			[self.h3],
			[self.h4]
		])
		return