#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats.stats import pearsonr

# Must define 'all_cars' and the fuel type variables 'b' and 'd'
import xc70data as cd


class Car(object):
	def __init__(self, data):
		self.price = data[2]
		self.dist = data[1]
		self.make = data[0]
		self.fuel = data[3]
		self.ddiv = 0.0
		self.vr = 0.0  # Holds ratio of expected price and real price

	# Set the value for norming distance
	def setDistDiv(self, v):
		self.ddiv = v*1.0

	def getNormDist(self):
		return (self.dist/self.ddiv)

	# Sloppy, only handle 2000 - 2007 cars ...
	def getNormMake(self):
		return (self.make - 2000) / 7.0

	def getFuelType(self):
		return "bensin" if self.fuel == cd.b else "diesel"

	def __str__(self):
		return "%d - %d mil - %s - %d kr - (valued: %d)" % (self.make, self.dist, self.getFuelType(), self.price, self.vr*self.price) 


def distSort(car):
	return car.dist

def rvsort(car):
	return car.vr

if (__name__ == "__main__"):

	# Create a list of car objects from the data in 'cd'
	cars = []
	for c in cd.all_cars:
		cc = Car(c)
		cars.append(cc)

	# Figure out the max distance for use when norming the data
	dsorted = sorted(cars, key=distSort)
	maxdist = dsorted[-1].dist
	
	# ugly ... set the normdivider on all objects
	for c in cars:
		c.setDistDiv(maxdist)
	
	# Separate lists for all values
	prices = [c.price for c in cars]
	dists = [c.getNormDist() for c in cars]
	makes = [c.getNormMake() for c in cars]

	# Create Numpy arrays from data lists
	x = np.array(dists)
	y = np.array(makes)
	z = np.array(prices)

	# Quadratic variables
	xx = x*x
	yy = y*y

	# Calculations are estimated to follow the function:
	# price = const1*distance + const2*distance^2 + const3*make + const4*make^2 + const5

	# Create the 'A' matrix in 'Ax = y' and reduce with least square
	A = np.column_stack((x, xx, y, yy, np.ones(x.size)))
	c, resid,rank,sigma = np.linalg.lstsq(A,z)

	# Reverse calculate the price with 'c1x + c2x^2 + c3y + c4y^2 + c5 = price'
	line = (x*c[0] + xx*c[1] + y*c[2] + yy*c[3] + c[4])

	# Value ratio by dividing expected price by real price
	valued = line/prices
	for i,cc in enumerate(cars):
		cc.vr = valued[i]

	# Sort by value ratio and print, best car on top
	valuelist = sorted(cars, key=rvsort)
	valuelist.reverse()
	for car in valuelist:
		print car
	
	# Show X-Y plot of real price and expected price
	# Best cars will be to the left of the X = Y line
	plt.plot(prices, line, 'r*')
	plt.plot([0, 180000], [0, 180000])
	plt.show()
