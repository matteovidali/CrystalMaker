from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from math import sqrt
import random
from datetime import datetime
from Vector import Vector

# Seed is the global random seed value
SEED = 0 
NUM_PARTICLES = 2 
DT = 0.001
STEPS = 2000000

#Vector Functions:
def sMult(v1:Vector, num:float):
    return Vector(v1.x*num, v1.y*num, v1.z*num)

def vComp(v1:Vector, v2:Vector):
    s = v1-v2
    return True if s.magnitude == 0 else False

# Particle class for a particle simulator ... duh
class Particle:
    def __init__(self, radius, polarity, mass=1, maxV=0.05, limits=None):
        global SEED
        random.seed(SEED)
        SEED += random.randint(0,1000)
        SEED %= 999999999999
        self.radius = radius
        self.polarity=polarity
        self.mass=mass

        self.position = Vector(10,5,5)
        self.x = self.position.get('x') 
        self.y = self.position.get('y')
        self.z = self.position.get('z')

        self.velocity = Vector(random.uniform(0,.5), random.uniform(0,.5), random.uniform(0,.5))
        self.limits = (0,10)

        self.multiplier = Vector(1,1,1)

        if limits:
            self.limits = limits
        

    # Helper function so that I have simpler locals I am lazy
    def update_locals(self):
        self.x = self.position.x 
        self.y = self.position.y
        self.z = self.position.z    

    # just a port to the distance function from vector
    def compute_distance_to_point(self, point:Vector):
        return self.position.dist(point)

    # Helper
    def update_position_by_value(self, val):
        self.position.update_uniform(val, 10)
        self.x = self.position.x
        self.y = self.position.y
        self.z = self.position.z
        return self.position

    # Inaccurate Position updates
    # Lets fix this reflection scheme at some point
    def update_position(self):
        
#        testMin= Vector(np.sign(min(self.limits) - self.position.x), 
#                        np.sign(min(self.limits) - self.position.y), 
#                        np.sign(min(self.limits) - self.position.z))
#
#        testMax= Vector(np.sign(max(self.limits) - self.position.x), 
#                        np.sign(max(self.limits) - self.position.y), 
#                        np.sign(max(self.limits) - self.position.z))
#
#        #NotQuite
#        if any([self.position.x, self.position.y, self.position.z]) < min(self.limits):
#            self.multiplier = testMin
#        elif any([self.position.x, self.position.y, self.position.z]) < max(self.limits):
#            self.multiplier = testMax

        if self.position.x <= min(self.limits):
            self.position = Vector(min(self.limits), self.position.y, self.position.z)
            self.multiplier *= Vector(-1,1,1)
        elif self.position.x >= max(self.limits):
            self.position = Vector(max(self.limits), self.position.y, self.position.z)
            self.multiplier *= Vector(-1, 1, 1)
        
        if self.position.y <= min(self.limits):
            self.position = Vector(self.position.x, min(self.limits), self.position.z)
            self.multiplier *= Vector(1,-1,1)
        elif self.position.y >= max(self.limits):
            self.position = Vector(self.position.x, max(self.limits), self.position.z)
            self.multiplier *= Vector(1, -1, 1)
       
        if self.position.z <= min(self.limits):
            self.position = Vector(self.position.x, self.position.y, min(self.limits))
            self.multiplier *= Vector(1,1,-1)
        elif self.position.z >= max(self.limits):
            self.position = Vector(self.position.x, self.position.y, max(self.limits))
            self.multiplier *= Vector(1, 1, -1)

        self.position += self.multiplier*self.velocity
        self.update_locals()

    # Update Velocity based on a force vector
    def update_velocity(self, force:Vector, maxV=100):
        self.velocity = (self.velocity+force) 
        self.update_locals()
    

# Calculating the forces between each particle
def calculate_forces(particles, attractionConst=.2):
    forceVs={}
    pForces=[Vector(0,0,0)]*len(particles)

    for idx, p in enumerate(particles):
        av=0
        for idj, j in enumerate(particles):
            if idx == idj or p.position.dist(j.position)==0:
                continue
            distance = p.compute_distance_to_point(j.position)**2
            invSqr = 1/distance if distance > .5*p.radius else 0
            dVec=sMult(p.position.norm_direction_to(j.position),invSqr)
            pForces[idx]+=sMult(dVec, 2 if j.radius == 35 else 1)
            av+=1

        if av:
            pForces[idx] /= Vector(av,av,av)
        
        
        print(f"X{idx}={pForces[idx].x}",end='\t')
        print(f"Y{idx}={pForces[idx].y}",end='\t')
        print(f"Z{idx}={pForces[idx].z}",end='\n')

    return pForces
    
# This is my cursed draw loop atm...
def animate(value):
    force = calculate_forces(particles)
    for idx, p in enumerate(particles):
        p.update_position()
        p.update_velocity(force[idx])

    graph._offsets3d = ([p.x for p in particles], [p.y for p in particles],[p.z for p in particles])


colors = ['red', 'blue']
sizes = [5,35]
particles = [Particle(random.choice(sizes),1) for _ in range(0,NUM_PARTICLES)]

rparticles = [Particle(5, 1), Particle(35,1)]
x = [p.x for p in particles]
y = [p.y for p in particles]
z = [p.z for p in particles]

# size based on particles radius
so = [p.radius for p in particles]
# colors based on particles radius
co = [colors[0] if particles[c].radius==5 else colors[1] for c in range(len(x))]


fig = plt.figure()
ax = plt.axes(projection = "3d")
ax.set_xlim3d([0.0, 10])
ax.set_xlabel('X')
ax.set_ylim3d([0.0,10])
ax.set_ylabel('Y')
ax.set_zlim3d([0.0, 10])
ax.set_zlabel('Z')
ax.set_title('Crystal Generation')
graph = ax.scatter([p.x for p in particles], [p.y for p in particles] ,[p.z for p in particles], s=so,c=co)

anim = animation.FuncAnimation(fig, animate, frames=30, interval=50, repeat=True)
plt.show()

