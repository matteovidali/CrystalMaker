from errno import WSAEDQUOT
from tkinter import W
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from math import sqrt
import random
from datetime import datetime

SEED = 0 

class Coordinate:
    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z
    
    def update_uniform(self, step, mod=0):
        self.x += step
        self.y += step
        self.z += step

        if mod:
            self.x %= mod 
            self.y %= mod
            self.z %= mod

class Particle:
    def __init__(self, radius, polarity):
        global SEED
        random.seed(SEED)
        SEED += random.randint(0,1000)
        self.radius = radius
        self.polarity=polarity

        self.position = Coordinate(random.randint(0,10),random.randint(0,10),random.randint(0,10))
        self.x = self.position.x
        self.y = self.position.y
        self.z = self.position.z

        self.velocity = [0, 0, 0]
    
    def compute_distance_to_point(self, point:Coordinate):
        return sqrt((self.x - point.x)**2 + (self.y - point.y)**2 + (self.z - point.z)**2)

    def update_position(self, val):
        print(self.x, self.y, self.z)
        self.position.update_uniform(val, 10)
        self.x = self.position.x
        self.y = self.position.y
        self.z = self.position.z
        return self.position


        
    

def animate(value):
    for p in particles:
        p.update_position(0.05)

    graph._offsets3d = ([p.x for p in particles], [p.y for p in particles],[p.z for p in particles])


colors = ['red', 'blue']
particles = [Particle(1,1) for _ in range(0,5)]
print(type(particles[0].x))

x = [p.x for p in particles]
y = [p.y for p in particles]
z = [p.z for p in particles]

so = [5,35,5,35,5]
co = [colors[c%2] for c in range(len(x))]




fig = plt.figure()
ax = plt.axes(projection = "3d")
ax.set_xlim3d([0.0, 10])
ax.set_xlabel('X')

ax.set_ylim3d([0.0,10])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 10])
ax.set_zlabel('Z')

ax.set_title('3D Test')
graph = ax.scatter([p.x for p in particles], [p.y for p in particles] ,[p.z for p in particles], s=so,c=co)

anim = animation.FuncAnimation(fig, animate, frames=30, interval=5, repeat=True)
plt.show()

