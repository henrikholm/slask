x, a, b, phi = var('x, a, b, phi')

#f =  x*a*sin(phi) - y*b*cos(phi) - (a*a - b*b)*sin(phi)*cos(phi)

y =  (x*a*sin(phi) - (a*a - b*b)*sin(phi)*cos(phi))/ (b*cos(phi))

solve(y, phi)
