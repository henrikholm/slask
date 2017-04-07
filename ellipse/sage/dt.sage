
t = var('t')
dx1, dy1, dx2, dy2 = var('dx1, dy1, dx2, dy2')

# Ellipse 1
phi1, a1, b1 = var('phi1, a1, b1')

h1 = dx1*t
k1 = dy1*t

AA1 = var('AA1')
BB1 = var('BB1')
CC1 = var('CC1')

DD11, DD12, EE11, EE12, FF11, FF12, FF13 = var('DD11, DD12, EE11, EE12, FF11, FF12, FF13')

#DD1 = (-(b1^2)*cos(phi1)*h1 - (a1^2)*sin(phi1)*k1)*2
DD1 = (-DD11*h1 - DD12*k1)*2
#EE1 = a1^2*cos(phi1)*k1 - (b1^2)*sin(phi1)*h1
EE1 = EE11*k1 - EE12*h1
#FF1 = -(a1^2)*(b1^2) + (b1^2)*(h1^2) + (a1^2)*(k1^2)
FF1 = -FF11 + FF12*(h1^2) + FF13*(k1^2)

# Ellipse 2
phi2, a2, b2 = var('phi2, a2, b2')

h2 = dx2*t
k2 = dy2*t

AA2 = var('AA2')
BB2 = var('BB2')
CC2 = var('CC2')

DD21, DD22, EE21, EE22, FF21, FF22, FF23 = var('DD21, DD22, EE21, EE22, FF21, FF22, FF23')

#DD2 = (-(b2^2)*h2*cos(phi2) - (a2^2)*k2*sin(phi2))*2
DD2 = (-DD21*h2 - DD22*k2)*2
#EE2 = a2^2*k2*cos(phi2) - (b2^2)*h2*sin(phi2)
EE2 = EE21*k2 - EE22*h2
#FF2 = -(a2^2)*(b2^2) + (b2^2)*(h2^2) + (a2^2)*(k2^2)
FF2 = -FF21 + FF22*(h1^2) + FF23*(k1^2)


d = AA1*(CC1*FF1 - EE1^2)

a = (1/d)*( AA1*(CC1*FF2 - 2*EE1*EE2 + FF1*CC2) + 2*BB1*(EE1*DD2 - FF1*BB2 + DD1*EE2) + 2*DD1*(EE1*BB2 - CC1*DD2) - (BB1*BB1*FF2 + DD1*DD1*CC2 + EE1*EE1*AA2) + (CC1*FF1*AA2) )

b = (1/d)*( AA1*(CC2*FF2 - EE2*EE2) + 2*BB1*(EE2*DD2 - FF2*BB2) + 2*DD1*(EE2*BB2 - CC2*DD2) + CC1*(AA2*FF2 - DD2*DD2) + 2*EE1*(BB2*DD2 - AA2*EE2) + FF1*(AA2*CC2 - BB2*BB2) )

c = (1/d)*( AA2*(CC2*FF2 - EE2*EE2) - (BB2*BB2*FF2 - 2*BB2*DD2*EE2 + DD2*DD2*CC2) )

s4 = -27*c*c + 18*c*a*b + a*a*b*b - 4*a*a*a*c - 4*b*b*b

#solve(s4.diff(t) == 0, t)
