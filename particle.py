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
NUM_PARTICLES = 5

# Particle class for a particle simulator ... duh
class Particle:
    def __init__(self, radius, polarity, maxV=0.05):
        global SEED
        random.seed(SEED)
        SEED += random.randint(0,1000)
        self.radius = radius
        self.polarity=polarity
        self.position = Vector(random.randint(0,10),random.randint(0,10),random.randint(0,10))
        self.x = self.position.get('x') 
        self.y = self.position.get('y')
        self.z = self.position.get('z')

        self.velocity = Vector(random.uniform(-maxV,maxV),random.uniform(-maxV,maxV), random.uniform(-maxV,maxV))

    def update_locals(self):
        self.x = self.position.x 
        self.y = self.position.y
        self.z = self.position.z    
    

    def compute_distance_to_point(self, point:Vector):
        return self.position.dist(point)


    def update_position_by_value(self, val):
        self.position.update_uniform(val, 10)
        self.x = self.position.x
        self.y = self.position.y
        self.z = self.position.z
        return self.position

    def update_position(self):
        self.position = (self.position + self.velocity) % 10
        self.update_locals()

    def update_velocity(self, force:Vector):
        self.velocity = (self.velocity+force)%1
        self.update_locals()
    

def calculate_forces(particles):
    pForces=[Vector(0,0,0)]*len(particles)
    for idx, p in enumerate(particles):
        for idj, j in enumerate(particles[1:]):
            distance = p.compute_distance_to_point(j.position)**2
            invSqr = 1/distance if distance else 0
            pForces[idx] += Vector(invSqr, invSqr, invSqr)
        pForces[idx]/Vector(idj,idj,idj)

    print(pForces)
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

anim = animation.FuncAnimation(fig, animate, frames=30, interval=500, repeat=True)
plt.show()

