from math import sqrt
# A class to keep track of 3d vectors
class Vector:
    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z

    # Addition Overloading
    def __add__(self, v):
        return Vector(self.x+v.x, self.y+v.y, self.z+v.z)

    # Exponential overloading
    def __pow__(self, num):
        return Vector(self.x**num, self.y**num, self.z**num)
    
    # Division Overloading
    def __truediv__(self, other):
        return Vector(self.x/other.x, self.y/other.y, self.z/other.z)

    # Modular Overloading
    def __mod__(self, num):
        return Vector(self.x%num, self.y%num, self.z%num)
    
    def __mul__(self, other):
        return Vector(self.x*other.x, self.y*other.y, self.z*other.z)
    
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)
    # Helper Function (not strictly necessary)
    def get(self, coord):
        if coord=='x':
            return self.x
        if coord=='y': 
            return self.y
        if coord=='z':
            return self.z
        return None
    
    # Distance between two vectors
    def dist(self, v):
        return sqrt((self.x - v.x)**2 + (self.y - v.y)**2 + (self.z - v.z)**2)
    
    def norm_direction_to(self, v):
        mag = self.dist(v)
        return (self - v)/Vector(mag, mag, mag)

    # Helper function (not strictly necessary)
    def update_uniform(self, step, mod=0):
        self.x += step
        self.y += step
        self.z += step

        if mod:
            self.x %= mod 
            self.y %= mod
            self.z %= mod
    
    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def isZero(self):
        return True if self.x == self.y == self.z == 0 else False

