from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from math import sqrt
import random
from datetime import datetime
from vector import Vector, sMult, vComp
from particle import Particle

# Seed is the global random seed value
NUM_PARTICLES = 2 
STEPS = 2000000
BOUNDING_SPACE=(-10,10)



# Particle class for a particle simulator ... duh

    

# Calculating the forces between each particle
def calculate_forces(particles, attractionConst=.2):
    forceVs={}
    pForces=[Vector(0,0,0)]*len(particles)

    for idx, p in enumerate(particles):
        av=0
        for idj, j in enumerate(particles):
            if idx == idj or p.position.dist(j.position)==0:
                continue
            distance = p.compute_distance_to_point(j.position)

            if distance < p.radius+j.radius:
                print("COLLISION")

            invSqr = 1/distance if distance != 0 else 0
            dVec=sMult(p.position.norm_direction_to(j.position),invSqr)
            pForces[idx]+=sMult(dVec, 2 if j.radius == 35 else 1)
            av+=1

        if av:
            pForces[idx] /= Vector(av,av,av)
        
        
#        print(f"X{idx}={pForces[idx].x}",end='\t')
#        print(f"Y{idx}={pForces[idx].y}",end='\t')
#        print(f"Z{idx}={pForces[idx].z}",end='\n')

    return pForces
    
# This is my cursed draw loop atm...
def animate(value):
    force = calculate_forces(particles)
    for idx, p in enumerate(particles):
        p.update_position()
        #p.update_velocity(force[idx])

    graph._offsets3d = ([p.x for p in particles], [p.y for p in particles],[p.z for p in particles])


colors = ['red', 'blue']
sizes = [0.5, 1]
particles = [Particle(random.choice(sizes),1) for _ in range(0,NUM_PARTICLES)]

rparticles = [Particle(0.5,1, ipos=Vector(0,-10,-10))]

x = [p.x for p in particles]
y = [p.y for p in particles]
z = [p.z for p in particles]

# size based on particles radius
so = [p.radius for p in particles]
# colors based on particles radius
co = [colors[0] if particles[c].radius==min(sizes) else colors[1] for c in range(len(x))]


NUM_DIV=abs(BOUNDING_SPACE[0]-BOUNDING_SPACE[1])

fig = plt.figure(figsize=(10,10), dpi=72)

size = fig.get_size_inches()*fig.dpi
sizePerDivision=size[0]/NUM_DIV


ax = fig.add_subplot(projection = "3d")

ax.set_xlim3d([BOUNDING_SPACE[0], BOUNDING_SPACE[1]])
ax.set_xlabel('X')
ax.set_xticks(np.arange(min(BOUNDING_SPACE), max(BOUNDING_SPACE)+1, max(NUM_DIV/20, 1)))

ax.set_ylim3d([BOUNDING_SPACE[0], BOUNDING_SPACE[1]])
ax.set_ylabel('Y')
ax.set_yticks(np.arange(min(BOUNDING_SPACE), max(BOUNDING_SPACE)+1, max(NUM_DIV/20, 1)))

ax.set_zlim3d([BOUNDING_SPACE[0], BOUNDING_SPACE[1]])
ax.set_zlabel('Z')
ax.set_zticks(np.arange(min(BOUNDING_SPACE), max(BOUNDING_SPACE)+1, max(NUM_DIV/20, 1)))

ax.set_title('Crystal Generation')
graph = ax.scatter([p.x for p in particles], [p.y for p in particles] ,[p.z for p in particles], s=[((sv*sizePerDivision)**2)*np.pi for sv in so],c=co)
anim = animation.FuncAnimation(fig, animate, frames=30, interval=50, repeat=True)
plt.show()
