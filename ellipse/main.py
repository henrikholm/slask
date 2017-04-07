#!/usr/bin/python -B
# -*- coding: utf-8 -*-

import time
import logging
import math as m

import Tkinter as tk

log = logging.getLogger(__name__)
log.debug("Importing GUI")


class Ellipse(object):
	def __init__(self, p, a, b, alfa):
		self.x = p.x
		self.y = p.y
		self.a = a
		self.b = b
		self.alfa = alfa
		
		self.wa = m2wgs(a, p)
		self.wb = m2wgs(b, p)
		
	def copy(self):
		return Ellipse(self, self.a, self.b, self.alfa)
	
	def __str__(self):
		return "Ellipse: x:%.02f, y:%.02f, a:%.02f, b:%.02f, alfa:%.0f" % (self.x, self.y, self.a, self.b, self.alfa*180/m.pi)
		

class Boat(object):
	def __init__(self, lwl, b, alfa):
		self.lwl = lwl
		self.b = b
		self.alfa = alfa

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


# Borders for dates and object names
# Given normed, _not_ in pixels
#BORDER_WEST = 0.05
#BORDER_EAST = 0.1
#BORDER_SOUTH = 0.1

# Pixel size
CANVAS_WIDTH = 1000.0
CANVAS_HEIGHT = 1000.0

LABEL_LINE = 0

LLP = Point(12.02, 57.02)
URP = Point(12.08, 57.08)
DP = Point(URP.x - LLP.x, URP.y - LLP.y)


class Param(object):
	def __init__(self):
		self.A = 0.0
		self.B = 0.0
		self.C = 0.0
		self.D = 0.0
		self.E = 0.0
		self.F = 0.0
	def __str__(self):
		return "%.02f, %.02f, %.02f, %.02f, %.02f, %.02f" % (self.A, self.B, self.C, self.D, self.E, self.F)
	
def unit_vector(p1, p2):
	dx = p2.x - p1.x
	dy = p2.y - p1.y
	
	d = m.sqrt(dx*dx + dy*dy)
	
	return Point(dx/d, dy/d)
	
	

def haversine(p1, p2):
	M_PI = m.pi
	EARTH_RADIUS = (6367.0*1000.0)
	D2R = (M_PI / 180.0)
	
	_lat1 = p1.y * D2R
	_lat2 = p2.y * D2R
	
	dlong = (p2.x - p1.x) * D2R
	dlat = (p2.y - p1.y) * D2R

	dPhi = m.log(m.tan((_lat2/2) + (M_PI/4)) / m.tan((_lat1/2) + (M_PI/4)))

	#E-W line gives dPhi=0
	q = dlat/dPhi if (dPhi != 0.0) else m.cos(_lat1)

	## if dLon over 180 degrees take shorter rhumb across anti-meridian:
	if (abs(dlong) > M_PI):
		dlong = -(2*M_PI - dlong) if dlong > 0 else (2*M_PI + dlong)

	dist = m.sqrt(dlat*dlat + q*q*dlong*dlong) * EARTH_RADIUS;

	return dist


def point_distance(p1, p2):
	return m.sqrt( (p2.x - p1.x)**2 + (p2.y - p1.y)**2 )

		
def m2wgs(distance, p):
	
	a = 1.0
	p1 = Point(p.x + a, p.y + a)
	p2 = Point(p.x - a, p.y - a)
	
	d = haversine(p1, p2)
	
	dw = distance*(2*a*m.sqrt(2)/d)
		
	return dw


def vector(e1, e2):
	return Point(e2.x - e1.x, e2.y - e1.y)

def setup_ellipses(e1, e2):
	ee1 = e1.copy()
	ee2 = e2.copy()
	
	# Convert into meters
	vv = unit_vector(ee1, ee2)
	dd = haversine(ee1, ee2)
		
	ee2.x = vv.x*dd
	ee2.y = vv.y*dd
	ee1.x = 0
	ee1.y = 0
	
	
	# Rotate to ee1.alfa = 0	
	cosphi = m.cos(ee1.alfa)
	sinphi = m.sin(ee1.alfa)
	xx = ee2.x*cosphi + ee2.y*sinphi
	yy = ee2.y*cosphi - ee2.x*sinphi
	ee2.x = xx
	ee2.y = yy
	ee2.alfa = ee2.alfa - ee1.alfa
	if ( (m.fabs (ee2.alfa) > (2.0*m.pi)) ):
		ee2.alfa = m.fmod (ee2.alfa, 2.0*m.pi);

	ee1.alfa = 0.0
	
	ee1.a /= 100.0
	ee1.b /= 100.0
	ee2.x /= 100.0
	ee2.y /= 100.0
	ee2.a /= 100.0
	ee2.b /= 100.0	
	
	ee1.wa = ee1.a
	ee1.wb = ee1.b
	ee2.wa = ee2.a
	ee2.wb = ee2.b
	return (ee1, ee2)
	
		
def has_overlap(e1, e2):
	ee1 = e1.copy()
	ee2 = e2.copy()
	
	# Convert into meters
	vv = unit_vector(ee1, ee2)
	dd = haversine(ee1, ee2)
		
	ee2.x = vv.x*dd
	ee2.y = vv.y*dd
	ee1.x = 0
	ee1.y = 0
	
	
	# Rotate to ee1.alfa = 0	
	cosphi = m.cos(ee1.alfa)
	sinphi = m.sin(ee1.alfa)
	xx = ee2.x*cosphi + ee2.y*sinphi
	yy = ee2.y*cosphi - ee2.x*sinphi
	ee2.x = xx
	ee2.y = yy
	ee2.alfa = ee2.alfa - ee1.alfa
	if ( (m.fabs (ee2.alfa) > (2.0*m.pi)) ):
		ee2.alfa = m.fmod (ee2.alfa, 2.0*m.pi);

	ee1.alfa = 0.0


	#
	# Ellipses are now in meters and rotated
	#


	# Scale everything down by 100.0
	ee1.a /= 100.0
	ee1.b /= 100.0
	ee2.x /= 100.0
	ee2.y /= 100.0
	ee2.a /= 100.0
	ee2.b /= 100.0	
	
	
	#s.draw_projected_ellipse(ee1)
	#s.draw_projected_ellipse(ee2)


	# Parameters for ellipse 1
	p1 = Param()
	
	coscos = m.cos(ee1.alfa)*m.cos(ee1.alfa)
	a2 = (ee1.a*ee1.a)
	b2 = (ee1.b*ee1.b)
	
	p1.A = b2
	p1.B = 0
	p1.C = a2
	p1.D = 0
	p1.E = 0
	p1.F = -a2*b2
		

	# Parameters for ellipse 2
	p2 = Param()
	
	sinsin = m.sin(ee2.alfa)*m.sin(ee2.alfa)
	coscos = m.cos(ee2.alfa)*m.cos(ee2.alfa)
	sincos = m.sin(ee2.alfa)*m.cos(ee2.alfa)
	a2 = (ee2.a*ee2.a)
	b2 = (ee2.b*ee2.b)
	
	p2.A = b2*coscos + a2*sinsin
	p2.B = (b2*sincos) - (a2*sincos)
	p2.C = b2*sinsin + a2*coscos
	p2.D = -b2*ee2.x*m.cos(ee2.alfa) - a2*ee2.y*m.sin(ee2.alfa)
	p2.E = a2*ee2.y*m.cos(ee2.alfa) - b2*ee2.x*m.sin(ee2.alfa)
	p2.F = b2*ee2.x*ee2.x + a2*ee2.y*ee2.y - a2*b2

	
	# Coefficients
	p = Param()
	
	p.D = p1.A*p1.C*p1.F
		
	a = p1.A*p1.C*p2.F + p1.A*p1.F*p2.C + p1.C*p1.F*p2.A
	p.A = a/float(p.D)

	b = p1.A*p2.C*p2.F - p1.A*p2.E*p2.E + p1.C*p2.A*p2.F - p1.C*p2.D*p2.D + p1.F*p2.A*p2.C - p1.F*p2.B*p2.B
	p.B = b/float(p.D)
	
	c = p2.A*p2.C*p2.F - p2.A*p2.E*p2.E - p2.B*p2.B*p2.F + 2*p2.B*p2.D*p2.E - p2.C*p2.D*p2.D
	p.C = c/float(p.D)
	
	
	# Calculation
	s1 = p.A
	s2 = p.A*p.A - 3.0*p.B
	s3 = 3.0*p.A*p.C + p.B*p.A*p.A - 4.0*p.B*p.B
	s4 = -27.0*p.C*p.C + 18.0*p.C*p.A*p.B + p.A*p.A*p.B*p.B - 4.0*p.A*p.A*p.A*p.C - 4.0*p.B*p.B*p.B
			
	if s1 < 0.0 and s2 > 0.0 and s4 > 0.0:
		print "Separated ellipses"
		return False
	
	if s1 >= 0.0 and s2 > 0.0 and s3 < 0.0 and s4 > 0.0:
		print "Separated ellipses"
		return False
	
	if s1 < 0.0 and s2 < 0.0 and s3 < 0.0 and s4 < 0.0:
		print "Unknown state, persume separated"
		return False

	return True


def bounds_check(p):
	bn = 10.0**20
	sn = 10.0**-15
	
	if not ( (-bn < p.A < bn) and (-bn < p.B < bn) and (-bn < p.C < bn) and (-bn < p.D < bn) and (-bn < p.E < bn)):
		print "Bounds check error!"
		print "\t Params:", p



class Simulator(object):
	def __init__(self, run_callback=None):
		self.setup(run_callback)

	# Setup Tk window with buttons and canvas
	# Also add time axis and distance axis
	def setup(self, run_callback):

		self._root = tk.Tk()
		self._root.title("Ellipse Simulator")

		self._run_callback = run_callback

		# create frame to put control buttons onto
		#frame = tk.Frame(self._root, bg='grey', width=400, height=40)
		#frame.pack(fill='x')
		#button1 = tk.Button(frame, text='Step', command=self.step)
		#button1.pack(side='left', padx=10)
		#button2 = tk.Button(frame, text='Refresh')
		#button2.pack(side='left')

		# set canvas properties
		self._w = CANVAS_WIDTH
		self._h = CANVAS_HEIGHT

		# invoke canvas
		self._canvas = tk.Canvas(self._root, width=self._w, height=self._h, bg='white')
		self._canvas.pack()
		self.draw_canvas()

	def draw_canvas(self):
		self._canvas.delete(tk.ALL)

	def step(self):
		
		if(self._run_callback != None):
			self._run_callback()
		self.draw_canvas()

	# Wrap Tk mainloop, this is the simulator wait loop
	def mainloop(self):
		self._root.mainloop()

	# Transform normed coords [0.0, 1.0] to fit within plotting area [BORDER, 1.0]
	def coord_transform(self, x, y):
		
		x1 = ((x - LLP.x)/DP.x)*CANVAS_WIDTH
		y1 = CANVAS_HEIGHT - ((y - LLP.y)/DP.y)*CANVAS_HEIGHT
		
		return (x1, y1)
		
	def projected_coord_transform(self, x, y):
		
		MAX_VAL = 2.0
		
		x1 = ((x + MAX_VAL)/(2.0*MAX_VAL))*CANVAS_HEIGHT
		y1 = CANVAS_HEIGHT - ((y + MAX_VAL)/(2.0*MAX_VAL))*CANVAS_HEIGHT
		return (x1, y1)
		
	# Write text on the canvas
	def create_text(self, x, y, anchor=tk.CENTER, text="None"):
		r = self.coord_transform(x, y)
		self._canvas.create_text(r[0], r[1], anchor=anchor, text=text)

	# Draw line segment on canvas
	def create_line(self, p0, p1, color='black'):
		r0 = self.coord_transform(p0[0], p0[1])
		r1 = self.coord_transform(p1[0], p1[1])

		self._canvas.create_line(r0[0], r0[1], r1[0], r1[1], fill=color)

	# Draw '*' single marker on canvas
	def create_marker(self, p0, color='red'):
		r = self.coord_transform(p0[0], p0[1])
		self._canvas.create_text(r[0], r[1], fill=color, anchor=tk.CENTER, text="*")

	def create_projected_marker(self, p0, color='red'):
		r = self.projected_coord_transform(p0[0], p0[1])
		self._canvas.create_text(r[0], r[1], fill=color, anchor=tk.CENTER, text="*")



	def dot(self, P1, P2):
		return P1.x*P2.x + P1.y*P2.y

	def rotate(self, x, y, R):
		x1 = self.dot(Point(x, y), Point(R[0], R[1]))
		y1 = self.dot(Point(x, y), Point(R[2], R[3]))
		
		return (x1, y1)		
		
		
	def oval2poly(self, e, alfa1=0.0, alfa2=2*m.pi, mark=False):
		"""return an oval as coordinates suitable for create_polygon"""

		steps = int(abs(alfa2 - alfa1)/(m.pi/180.0))
		
		point_list = []
		theta = alfa1
		delta = m.pi/180.0

		alfa = e.alfa
		
		#R = [m.cos(alfa), -m.sin(alfa), m.sin(alfa), m.cos(alfa)]
		
		Acos = e.wa*m.cos(alfa)
		Bsin = e.wb*m.sin(alfa)
		Asin = e.wa*m.sin(alfa)
		Bcos = e.wb*m.cos(alfa)
		
		# create the oval as a list of points
		for i in range(steps):

			# Calculate the angle for this step
			# 360 degrees == 2 pi radians

			#x1 = e.wa * m.cos(theta)
			#y1 = e.wb * m.sin(theta)
			
			# rotate x, y
			#(x, y) = self.rotate(x1, y1, R)
			
			x = Acos*m.cos(theta) - Bsin*m.sin(theta)
			y = Asin*m.cos(theta) + Bcos*m.sin(theta)
			
			xx = e.x + x
			yy = e.y + y
						
			#if mark:
			#	self.create_projected_marker((xx, yy), color="yellow")


			point_list.append(xx)
			point_list.append(yy)
			theta += delta

		return point_list		

	def draw_ellipse(self, e, color='black'):
		
		coords = self.oval2poly(e)
		tc = []
		self.create_marker((coords[0], coords[1]), 'blue')
		

		for i in xrange(0, len(coords) - 1, 2):
			r = self.coord_transform(coords[i], coords[i+1])
			tc.append(r[0])
			tc.append(r[1])
		
		self._canvas.create_polygon(tc, fill='', outline=color)

	def draw_projected_ellipse(self, e, color='blue'):
		
		e.wa = e.a
		e.wb = e.b
		
		#print e.wa, e.wb
		#self.create_projected_marker((0.0, 0.0))
		coords = self.oval2poly(e)
		tc = []
		self.create_projected_marker((coords[0], coords[1]), 'green')
		
		for i in xrange(0, len(coords) - 1, 2):
			r = self.projected_coord_transform(coords[i], coords[i+1])
			
			tc.append(r[0])
			tc.append(r[1])
		
		self._canvas.create_polygon(tc, fill='', outline=color)

	def draw_line(self, p0, p1, color='black'):
		r0 = self.coord_transform(p0.x, p0.y)
		r1 = self.coord_transform(p1.x, p1.y)
		self._canvas.create_line(r0[0], r0[1], r1[0], r1[1], fill=color)





	def shortest_point(self, e1, e2):
		v1 = vector(e1, e2)
		#alfa = compass2lab(m.atan2(v1.y, v1.x))
		alfa = m.atan2(v1.y, v1.x)
		alfa = m.fmod(((alfa - e1.alfa) + 4*m.pi), 2*m.pi)
		
		print "call"
		ps1 = self.oval2poly(e1, alfa - m.pi/3.0, alfa + m.pi/3.0, True)
		
		p1 = Point(e1.x, e1.y)
		p1d = point_distance(p1, e2)
		for i in xrange(0, len(ps1) - 1, 2):
			
			p = Point(ps1[i], ps1[i+1])
			pd = point_distance(p, e2)
			if(pd < p1d):
				p1 = p
				p1d = pd
				#print "New shortest:", p1.x, p1.y, p1d
				
		return p1

	def shortest_distance(self, e1, e2):
		pdist = 0
		p1 = self.shortest_point(e1, e2)
		p2 = self.shortest_point(e2, e1)
		pdiff = 1.1
		iterations = 0
		while pdiff > 1.0 and iterations < 20:
			
			#p1 = self.shortest_point(e1, p2)
			#p2 = self.shortest_point(e2, p1)
			#dist = haversine(p1, p2)
			
			np1 = self.shortest_point(e1, p2)
			np2 = self.shortest_point(e2, p1)
			dist1 = haversine(np1, p2)
			dist2 = haversine(p1, np2)
			
			if dist1 < dist2:
				p1 = np1
				dist = dist1
			else:
				p2 = np2
				dist = dist2
			
			pdiff = int(abs(pdist - dist))
			pdist = dist
			iterations += 1

		if iterations == 20:
			print "Reached maximum iterations in shortest distance"
		#print iterations, "iterations"
		return (p1, p2)

	def shortest_distance2(self, e1, e2):
		pdist = 0
		p1 = self.shortest_point(e1, e2)
		p2 = self.shortest_point(e2, e1)
		pdiff = 1.1
		iterations = 0
		while pdiff > 1.0 and iterations < 20:
			
			#p1 = self.shortest_point(e1, p2)
			#p2 = self.shortest_point(e2, p1)
			#dist = haversine(p1, p2)
			
			np1 = self.shortest_point(e1, p2)
			np2 = self.shortest_point(e2, p1)
			dist1 = point_distance(np1, p2)
			dist2 = point_distance(p1, np2)
			
			if dist1 < dist2:
				p1 = np1
				dist = dist1
			else:
				p2 = np2
				dist = dist2
			
			pdiff = int(abs(pdist - dist))
			pdist = dist
			iterations += 1

		if iterations == 20:
			print "Reached maximum iterations in shortest distance 2"
		#print iterations, "iterations"
		return (p1, p2)


	def getAngle(self, p1, p2):
		dx = p2.x - p1.x
		dy = p2.y - p1.y
		a = m.atan2(dy, dx)
		
		if ( (m.fabs (a) > (m.pi)) ):
			a = m.fmod (a, m.pi)

		return a
		

	def cpat( self, p1, v1, p2, v2 ):

		dv = Point(v1.x - v2.x, v1.y - v2.y)

		dv2 = self.dot(dv, dv);

		if (dv2 < 0.00001):
			return 0

		w = Point(p1.x - p2.x, p1.y - p2.y)

		cpatime = -self.dot(w, dv) / dv2

		return cpatime;


	def scenario1(self):

		l1 = [Point(12.043, 57.039), Point(12.065, 57.069)]
		l2 = [Point(12.040, 57.0523), Point(12.062, 57.055)]
		#l2 = [Point(12.046, 57.0374), Point(12.055, 57.075)]
		#l2 = [Point(12.044, 57.0375), Point(12.069, 57.075)]

		a1 = self.getAngle(l1[0], l1[1])
		a2 = self.getAngle(l2[0], l2[1])
		
		b1 = Boat(250, 30, a1)
		b2 = Boat(250, 30, a2)

		
		self.draw_line(l1[0], l1[1], color='green')
		self.draw_line(l2[0], l2[1], color='green')
		
		
		e1 = Ellipse(l1[0], b1.lwl, b1.b, b1.alfa)
		e2 = Ellipse(l2[0], b2.lwl, b2.b, b2.alfa)
		
		if(has_overlap(e1, e2)):
			print "Ellipses has overlap in starting point"
		else:
			print "No overlap in starting point"

		print ""
		print ""

		
		self.draw_ellipse(e1)
		self.draw_ellipse(e2)

		(p1, p2) = self.shortest_distance(e1, e2)
		self.draw_line(p1, p2)

		e3 = Ellipse(l1[1], b1.lwl, b1.b, b1.alfa)
		e4 = Ellipse(l2[1], b2.lwl, b2.b, b2.alfa)
		
		if(has_overlap(e3, e4)):
			print "Ellipses has overlap in end point"
		else:
			print "No overlap in end point"

		print ""
		print ""

		self.draw_ellipse(e3)
		self.draw_ellipse(e4)
		
		(p3, p4) = self.shortest_distance(e3, e4)
		self.draw_line(p3, p4)


		self.draw_line(p1, p3, color='red')
		self.draw_line(p2, p4, color='red')

		v1 = Point(p3.x - p1.x, p3.y - p1.y)
		v2 = Point(p4.x - p2.x, p4.y - p2.y)
		cpat = self.cpat(p1, v1, p2, v2)
		
		#print "CPAT:", cpat

		pc1 = Point(p1.x + cpat*v1.x, p1.y + cpat*v1.y)
		pc2 = Point(p2.x + cpat*v2.x, p2.y + cpat*v2.y)
		cpa = haversine(pc1, pc2)
		
		#print "CPA:", cpa
		
		v1 = Point(l1[1].x - l1[0].x, l1[1].y - l1[0].y)
		v2 = Point(l2[1].x - l2[0].x, l2[1].y - l2[0].y)
		
		e1.x = l1[0].x + cpat*v1.x
		e1.y = l1[0].y + cpat*v1.y

		e2.x = l2[0].x + cpat*v2.x
		e2.y = l2[0].y + cpat*v2.y

		self.draw_ellipse(e1)
		self.draw_ellipse(e2)

		(p1, p2) = self.shortest_distance(e1, e2)
		print "Shortest distance:", haversine(p1, p2)
		self.create_marker((p1.x, p1.y))
		self.create_marker((p2.x, p2.y))

		(ee1, ee2) = setup_ellipses(e1, e2)
		(p1, p2) = self.shortest_distance2(ee1, ee2)
		#self.create_projected_marker((p1.x, p1.y))
		#self.create_projected_marker((p2.x, p2.y))
		print "PP", p1.x, p1.y, p2.x, p2.y
		print "Shortest distance:", point_distance(p1, p2)



		if(has_overlap(e1, e2)):
			print "Ellipses has overlap in CPA point"
		else:
			print "No overlap in CPA point"


s = Simulator()

if(__name__ == "__main__"):


	s.scenario1()
	s.create_text(LLP.x + 0.002, LLP.y + 0.002, text="LL-Point")
	s.create_text(URP.x - 0.002, URP.y - 0.002, text="UR-Point")
	
	s.mainloop()
	
	
	#p1 = Point(11.0,57.0)
	#p2 = Point(11.0,58.0)
	#p3 = Point(12.0,57.0)
	
	#d1 = haversine(p1, p2)
	#d2 = haversine(p1, p3)
	
	#print "D1:", d1, "D2:", d2
	#r = d1/d2
	#print "Ratio:", r, "sqrt", m.sqrt(1.0+r*r)
