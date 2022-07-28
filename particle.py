from vector import *
import random

SEED = 0 
DT = 0.01

class Particle:
    def __init__(self, radius, polarity, mass=2, maxV=0.05, limits=(-50,50),ipos=None, fixed=False):
        global SEED
        random.seed(SEED)
        SEED += random.randint(0,1000)
        SEED %= 999999999999
        self.radius = radius
        self.polarity=polarity
        self.mass=mass*radius

        self.position = ipos if ipos else Vector(10,5,5)

        self.x = self.position.x
        self.y = self.position.y
        self.z = self.position.z

        #self.velocity = Vector(random.uniform(0,.5), random.uniform(0,.5), random.uniform(0,.5))
        self.velocity = Vector(0,0,0)
        self.force = Vector(0,0,0)

        self.limits = (-10,10)
        if limits:
            self.limits = limits
        self.fixed=fixed
        

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
    # Velocity updates by FORCE :)
    def update_position(self):
        if self.fixed:
            return
        if self.position.x <= min(self.limits) or self.position.x >= max(self.limits):
            self.velocity *= Vector(-1,1,1)
        if self.position.y <= min(self.limits) or self.position.y >= max(self.limits):
            self.velocity *= Vector(1,-1,1)
        if self.position.z <= min(self.limits) or self.position.z >= max(self.limits):
            self.velocity *= Vector(1,1,-1)

        self.position += sMult(self.velocity, DT)

        self.update_locals()

    # Update Velocity based on a force vector
    def update_velocity(self, force:Vector):
        a = force/ Vector(self.mass,self.mass,self.mass)
        self.velocity += sMult(a, DT)

        self.update_locals