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
# attractive coefficient:
G=1


# Particle class for a particle simulator ... duh

    

# Calculating the forces between each particle
def calculate_forces(particles, attractionConst=.2):
    forceVs={}
    pForces=[Vector(0,0,0)]*len(particles)
    for idx, p in enumerate(particles[:-1]):
        av=0
        for idj, j in enumerate(particles[idx+1:]):
            # checkif j==p (ditance will be zero or index positino will be same)
            if p.position.dist(j.position)==0:
                continue
            
            #calculate distance to point
            distance = p.compute_distance_to_point(j.position)
            direction_pj = p.position.norm_direction_to(j.position)
            direction_jp = sMult(direction_pj, -1)


            #is distance too small? collision
            if distance < p.radius+j.radius:
                print("COLLISION")
        
            # Gravitational Attraction scalar
            # F_jp is the force exerted upon j by p
            F_jp = sMult(direction_jp, -G * (p.mass * j.mass) / (distance**2))
            # F_pj is the force exerted upon p by j
            F_pj = sMult(F_jp, -1)



            pForces[idx]+=F_pj
            pForces[idj+1]+=F_jp

            if idj+1 == idx+1:
                j.force = pForces[idj+1]
        p.force = pForces[idx]
        if av:
            pForces[idx] /= Vector(av,av,av)

        print(f"Distance: {distance}")

        
    
#        print(f"X{idx}={pForces[idx].x}",end='\t')
#        print(f"Y{idx}={pForces[idx].y}",end='\t')
#        print(f"Z{idx}={pForces[idx].z}",end='\n')

    return pForces
    
# This is my cursed draw loop atm...
def animate(value):
    force = calculate_forces(particles)
    for idx, p in enumerate(particles):
        p.update_position()
        p.update_velocity(force[idx])

    graph._offsets3d = ([p.x for p in particles], [p.y for p in particles],[p.z for p in particles])

if __name__ == "__main__":
    colors = ['red', 'blue']
    sizes = [0.5, 1]
    rparticles = [Particle(random.choice(sizes),1) for _ in range(0,NUM_PARTICLES)]

    particles = [Particle(0.5,1, ipos=Vector(9,0,0)), Particle(0.5,1,ipos=Vector(-9,0,0))]

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
