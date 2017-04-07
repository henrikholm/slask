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
	def __init__(self, a, b, c, d, cog):
		self.lwl = a + b
		self.beam = c + d
		self.cog = cog
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.alfa = (m.pi/2.0) - ((cog*m.pi)/180.0)
		
		self.dx = ((c + d)/2.0) - d
		self.dy = ((a + b)/2.0) - a
		

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

LLP = Point(12.04, 57.04)
URP = Point(12.06, 57.06)
DP = Point(URP.x - LLP.x, URP.y - LLP.y)

	
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

def inv_haversine(p1, distance, brng):
	EARTH_RADIUS = (6367.0*1000.0)
	D2R = (m.pi / 180.0)
	R2D = (180.0 / m.pi)

	_lat1 = p1.y * D2R;
	_lon1 = p1.x * D2R;

	dR = distance/EARTH_RADIUS;

	lat2 = m.asin( m.sin(_lat1)*m.cos(dR) + m.cos(_lat1)*m.sin(dR)*m.cos(brng));
	lon2 = _lon1 + m.atan2(m.sin(brng)*m.sin(dR)*m.cos(_lat1), m.cos(dR) - m.sin(_lat1)*m.sin(lat2));

	x = lon2*R2D;
	y = lat2*R2D;

	return (x,y)

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
		wa = e.wa/2.0
		wb = e.wb/2.0
		Acos = wa*m.cos(alfa)
		Bsin = wb*m.sin(alfa)
		Asin = wa*m.sin(alfa)
		Bcos = wb*m.cos(alfa)
		
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
				
	def oval2poly2(self, e):
		"""return an oval as coordinates suitable for create_polygon"""

		steps = 36
		
		point_list = []
		theta = 0
		delta = (360/steps)*m.pi/180.0

		alfa = e.alfa
		
		R = [m.cos(alfa), -m.sin(alfa), m.sin(alfa), m.cos(alfa)]
		a = e.a / 2.0
		b = e.b / 2.0
		
		# create the oval as a list of points
		for i in range(steps):

			# Calculate the angle for this step
			# 360 degrees == 2 pi radians

			x1 = a * m.cos(theta)
			y1 = b * m.sin(theta)
			
			# rotate x, y
			(x, y) = self.rotate(x1, y1, R)
			
			dist = m.sqrt(x*x + y*y)
			brng = m.atan2(x, y)
			(xx, yy) = inv_haversine(Point(e.x, e.y), dist, brng)
			#xx = e.x + x
			#yy = e.y + y
			


			point_list.append(xx)
			point_list.append(yy)
			theta += delta

		return point_list
		
		
	def draw_ellipse(self, e, color='black'):
		
		coords = self.oval2poly2(e)
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

		p1 = Point(12.053, 57.054)
		
		steps = 36
		for i in range(steps):
			b1 = Boat(200, 0, 0, 25, i*(360/steps))
			R = [m.cos(b1.alfa), -m.sin(b1.alfa), m.sin(b1.alfa), m.cos(b1.alfa)]
			
			self.create_marker([p1.x, p1.y])
			
			
			(xp, yp) = self.rotate(-b1.dy, b1.dx, R)
			
			crad = (m.pi/2.0) - m.atan2(yp, xp)
			dist = m.sqrt(xp*xp + yp*yp)
			
			(ppx, ppy) = inv_haversine(p1, dist, crad)
			
			p2 = Point(ppx, ppy)

			self.create_marker([p2.x, p2.y])
			
			print haversine(p1, p2)
			
			e1 = Ellipse(p2, b1.lwl, b1.beam, b1.alfa)		
			self.draw_ellipse(e1)



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
