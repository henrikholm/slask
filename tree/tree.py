from visual import *
from math import *
from random import *


# Set the scene and create a background frame
scene.background = (1.0,1.0,1.0)
scene.width = 1200
scene.height = 1200
scene.visible = 1
fr = frame( pos=(0,-0.8,0) )


########################################################################################
# Input:	frm	Frame to plot inside
#		p	Starting point
#		a	Branch vector
#		r	Radius of branch
#		c	Color
#		ml	Length multiplier for next level of branches
#		mr	Radius multiplier
#		e	Separation angle between branches
#		d	Current recursion level
########################################################################################
def tree(frm, p, a, r, c, ml, mr, e, d):
    # Endpoint q
    q = p + a

    # Animate at a slow rate to see the tree get built
    rate(600)

    # Create the 'branch', starting at 'p' and with the direction vector 'a'
    cylinder(frame=frm, pos=p, axis=a, radius=r, color=c)
    # Place a spere at the end of each branch, as a joint for the next set of branches
    sphere(frame=frm, pos=q, radius=r, color=c)

    # Stop recursion at d == 0, also stop recursion for some of the smaller twigs
    if (d > 0) and ( (d > 1) or (random() > 0.33) ):
	# Get rotation axis by cross product of direction vector 'a'
        a1 = cross(a, (0,0,1) )

	# New direction vector: first calc new length, the rotate it around
	# perpendicular axis 'a1'
	s = ml * a * ( 0.8 + 0.4 * random() )
        s = rotate(s,axis=a1,angle=e)

	# Number of branches in this step
        n = 4 if random() > 0.3 else 3
	# Smaller twigs only get 2 branches
        if (d < 3):
            n = 2

        for i in range(n):
            # Distribute the branches a full rotation around the axis 'a'
            v = rotate( rotate(s, axis=a, angle=2.0*pi/n*i+pi/5.0/d*random()), axis=a, angle=pi/4.0*(random()-0.5))
            # Recurse
            tree(frm, q, v, mr*r, c, ml, mr, e, d-1)
    else:
	return


# Add the tree
tr = tree( fr, vector(0,0,0), vector(0,0.8,0), 0.075, (0.2,0.2,0.2), 0.65, 0.55, (pi-0.4)/3.0, 8)


