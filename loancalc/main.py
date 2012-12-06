#!/usr/bin/env python

import math


amount = 4500000	# Amount to pay back

intrestbase = 0.033	# Lowest level of intrest
intrestperiod = 10*2.0	# Intrest full cycle from base -> top -> base, given in years
intrestdeltamax = 0.05	# Added on base to form intrest max
inflation = 0.01	# Yearly inflation
maxpressure = 15000	# Max household pressure from start


i=0
while (amount>10000):
	i += 1

	# intrest = base + delta*cycle
	intrestdelta = intrestdeltamax*math.sin(2.0*math.pi*(i/intrestperiod))**2
	intrest = intrestbase + intrestdelta
	monthlyintrest = amount*intrest/12.0
	
	# Pressure after adding inflation
	inflpressure = maxpressure*((1.0 + (inflation + intrestdelta/2.0))**i)
	
	for m in xrange(1,13):
		
		# If intrest is above max pressure then only pay 500 in deduct
		if(monthlyintrest >= inflpressure):
			# print "Pressure is too high!"
			monthlyamort = 500
		else:
			monthlyamort = inflpressure - monthlyintrest

		#
		totalcost = monthlyamort + monthlyintrest
		
		# Amount we pay off each month
		amount -= monthlyamort


	print "Year: %d, Monthly Amort: %d, Monthly Intrest: %d, Total Monthly Cost: %d, Amount Left: %d, Inflation: %f" %(i, monthlyamort, monthlyintrest, totalcost, amount, (inflation + intrestdelta))

