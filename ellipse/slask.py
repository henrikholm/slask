
def ellipse2param(e):
	p = Param()
	
	#p.A = (m.cos(e.alfa)*m.cos(e.alfa))/(e.a*e.a) + (m.sin(e.alfa)*m.sin(e.alfa))/(e.b*e.b)
	#p.B = (2.0*m.sin(e.alfa)*m.cos(e.alfa))/(e.a*e.a) - (2.0*m.sin(e.alfa)*m.cos(e.alfa))/(e.b*e.b)
	#p.C = (m.sin(e.alfa)*m.sin(e.alfa))/(e.a*e.a) + (m.cos(e.alfa)*m.cos(e.alfa))/(e.b*e.b)
	#p.D = (-2.0*m.cos(e.alfa)/(e.a*e.a) ) * (e.x*m.cos(e.alfa) + e.y*m.sin(e.alfa)) + (2.0*m.sin(e.alfa)/(e.b*e.b) ) * (e.y*m.cos(e.alfa) - e.x*m.sin(e.alfa))
	#p.E = (-2.0*m.sin(e.alfa)/(e.a*e.a) ) * (e.x*m.cos(e.alfa) + e.y*m.sin(e.alfa)) + (2.0*m.cos(e.alfa)/(e.b*e.b) ) * (e.x*m.sin(e.alfa) - e.y*m.cos(e.alfa))
	
	#f1 = ((e.x*m.cos(e.alfa) + e.y*m.sin(e.alfa))/e.a)
	#f2 = ((e.x*m.sin(e.alfa) - e.y*m.cos(e.alfa))/e.b)
	#p.F = f1*f1 + f2*f2 - 1.0



	sinsin = m.sin(e.alfa)*m.sin(e.alfa)
	coscos = m.cos(e.alfa)*m.cos(e.alfa)
	sincos = m.sin(e.alfa)*m.cos(e.alfa)
	a2 = (e.a*e.a)
	b2 = (e.b*e.b)


	paper=True
	if(paper):
		
		p.A = coscos/a2 + sinsin/b2
		p.B = (2.0*sincos)/a2 - (2.0*sincos)/b2
		p.C = sinsin/a2 + coscos/b2
		p.D = (-2.0*m.cos(e.alfa) * (e.x*m.cos(e.alfa) + e.y*m.sin(e.alfa)))/a2 + (2.0*m.sin(e.alfa) * (e.y*m.cos(e.alfa) - e.x*m.sin(e.alfa)))/b2
		p.E = (-2.0*m.sin(e.alfa) * (e.x*m.cos(e.alfa) + e.y*m.sin(e.alfa)))/a2 + (2.0*m.cos(e.alfa) * (e.x*m.sin(e.alfa) - e.y*m.cos(e.alfa)))/b2
		
		f1 = ((e.x*m.cos(e.alfa) + e.y*m.sin(e.alfa))/e.a)
		f2 = ((e.x*m.sin(e.alfa) - e.y*m.cos(e.alfa))/e.b)
		p.F = f1*f1 + f2*f2 - 1.0
	else:	
		p.A = b2*coscos + a2*sinsin
		p.B = (2.0*b2*sincos) - (2.0*a2*sincos)
		p.C = b2*sinsin + a2*coscos
		p.D = -2.0*b2*e.x*m.cos(e.alfa) - 2.0*a2*e.y*m.sin(e.alfa)
		p.E = 2.0*a2*e.y*m.cos(e.alfa) - 2.0*b2*e.x*m.sin(e.alfa)
		p.F = b2*e.x*e.x + a2*e.y*e.y - a2*b2
	
	
	if( (p.A*p.C - (p.B/2.0)*(p.B/2.0)) <= 0.0 ):
		print "Ellipse criteria not met"
		print "\t Parameters:", p
	
	return p



	
def has_overlap(e1, e2):
	
	(ee1, ee2) = setup_ellipses(e1, e2)
	print ee1
	print ee2
	
	#print "E1:", ee1.x, ee1.y, ee1.a, ee1.b, ee1.alfa*180.0/m.pi
	#print "E2:", ee2.x, ee2.y, ee2.a, ee2.b, ee2.alfa*180.0/m.pi
	#print "X", ee1.a, ee1.b, ee1.x, ee1.y, ee1.alfa, ee2.a, ee2.b, ee2.x, ee2.y, ee2.alfa
	
	
	p1 = ellipse2param(ee1)
	p2 = ellipse2param(ee2)
	
	#print p1
	#print p2
	
	
	p = Param()
	
	paper = False
	if(paper):
		p.D = p1.A*(p1.C*p1.F - p1.E*p1.E) - (p1.C*p1.D*p1.D - 2*p1.B*p1.D*p1.E + p1.F*p1.B*p1.B)
		
		a = p1.A*(p1.C*p2.F - 2.0*p1.E*p2.E + p1.F*p2.C) + 2.0*p1.B*(p1.E*p2.D - p1.F*p2.B + p1.D*p2.E) 
		a += 2.0*p1.D*(p1.E*p1.B - p1.C*p2.D) - (p1.B*p1.B*p2.F + p1.D*p1.D*p2.C + p1.E*p1.E*p2.A) # NOTE last term might be wrong!!
		a += p1.C*p1.F*p2.A
		p.A = a/p.D
		
		b = p1.A*(p2.C*p2.F - p2.E*p2.E) + 2.0*p1.B*(p2.E*p2.D - p2.F*p2.B)
		b += 2.0*p1.D*(p2.E*p2.B - p2.C*p2.D) +  p1.C*(p2.A*p2.F - p2.D*p2.D)
		b += 2.0*p1.E*(p2.B*p2.D - p2.A*p2.E) + p1.F*(p2.A*p2.C - p2.B*p2.B)
		p.B = b/p.D
		
		c = p2.A*(p2.C*p2.F - p2.E*p2.E) - (p2.B*p2.B*p2.F - 2*p2.B*p2.D*p2.E + p2.D*p2.D*p2.C)
		p.C = c/p.D
	else:
		p.D = p1.A*p1.C*p1.F - p1.A*p1.E*p1.E - p1.B*p1.B*p1.F + 2*p1.B*p1.D*p1.E - p1.C*p1.D*p1.D
		
		a = p1.A*p1.C*p2.F - 2*p1.A*p1.E*p2.E + p1.A*p1.F*p2.C - p1.B*p1.B*p2.F + 2*p1.B*p1.D*p2.E + 2*p1.B*p1.E*p2.D
		a += -2*p1.B*p1.F*p2.B - 2*p1.C*p1.D*p2.D + p1.C*p1.F*p2.A - p1.D*p1.D*p2.C + 2*p1.D*p1.E*p2.B - p1.E*p1.E*p2.A
		p.A = a/float(p.D)

		b = p1.A*p2.C*p2.F - p1.A*p2.E*p2.E - 2*p1.B*p2.B*p2.F + 2*p1.B*p2.D*p2.E + p1.C*p2.A*p2.F - p1.C*p2.D*p2.D
		b += 2*p1.D*p2.B*p2.E - 2*p1.D*p2.C*p2.D - 2*p1.E*p2.A*p2.E + 2*p1.E*p2.B*p2.D + p1.F*p2.A*p2.C - p1.F*p2.B*p2.B
		p.B = b/float(p.D)

		c = p2.A*p2.C*p2.F - p2.A*p2.E*p2.E - p2.B*p2.B*p2.F + 2*p2.B*p2.D*p2.E - p2.C*p2.D*p2.D
		p.C = c/float(p.D)
	
	###############
	
	print "Old coeffs:", p
	
	s1 = p.A
	s2 = p.A*p.A - 3.0*p.B
	s3 = 3.0*p.A*p.C + p.B*p.A*p.A - 4.0*p.B*p.B
	s4 = -27.0*p.C*p.C + 18.0*p.C*p.A*p.B + p.A*p.A*p.B*p.B - 4.0*p.A*p.A*p.A*p.C - 4.0*p.B*p.B*p.B
	
	#print "S-variables:", s4, s3, s2, s1
	if s1 < 0.0 and s2 < 0.0 and s3 < 0.0 and s4 < 0.0:
		print "Unknown state, persume separated"
		return False
	
	if s1 < 0.0 and s2 > 0.0 and s4 > 0.0:
		print "Separated ellipses"
		return False
	
	if s1 >= 0.0 and s2 > 0.0 and s3 < 0.0 and s4 > 0.0:
		print "Separated ellipses"
		return False
	
	
	return True
	

def setup_ellipses(e1, e2):
	ee1 = e1.copy()
	ee2 = e2.copy()
	
	vv = unit_vector(ee1, ee2)
	dd = haversine(ee1, ee2)
	
	ee2.x = vv.x*dd
	ee2.y = vv.y*dd
	ee1.x = 0
	ee1.y = 0


	
	

	#ee1.a = ee1.a/2.0
	#ee1.b = ee1.b/2.0
	#ee2.a = ee2.a/2.0
	#ee2.b = ee2.b/2.0
	
	
	ee2.x /= 100.0
	ee2.y /= 100.0
	ee1.a /= 100.0
	ee1.b /= 100.0
	ee2.a /= 100.0
	ee2.b /= 100.0
	
	#print point_distance(ee1, ee2)
	
	
	#ee1.alfa = compass2lab(ee1.alfa)
	#ee2.alfa = compass2lab(ee2.alfa)
	
	
	

	return (ee1, ee2)


#	def shortest_projection(self, e1, e2):
#		v1 = self.vector(e1, e2)
#
#		alfa = self.compass2lab(m.atan2(v1.y, v1.x))
#		alfa = m.fmod(((alfa - e1.alfa) + 4*m.pi), 2*m.pi)
#		
#		ps1 = self.oval2poly(e1, alfa - m.pi/3.0, alfa + m.pi/3.0, False)
#		
#		dotv1 = self.dot(v1, v1)
#		
#		umax = 0
#		pmax = Point(0,0)
#		for i in xrange(0, len(ps1) - 1, 2):
#			v2 = Point(ps1[i] - e1.x, ps1[i+1] - e1.y)
#			
#			u = self.dot(v2, v1)/dotv1
#			if u < 0.0 or u > 1.0:
#				#print "u out of scope .."
#				continue
#			
#			if u > umax:
#				#print "New max-u", u
#				umax = u
#				pmax = v2
#		
#		return (Point(e1.x + pmax.x, e1.y + pmax.y), umax)
		
