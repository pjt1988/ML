#physical constants..
c = 299 792 458 # m/s
Me = 5.972E24 # mass earth, kg
Ms = 1.989E30 # mass sun, kg
G = 6.67408E-11 #gravitational constant m^3 / kg / s^2 
h = 6.62607004E-34 #planck m^2 kg / s
pi = 3.14159265359
hbar = h / (2*pi)

import optparse
parser = optparse.OptionParser()

def calc_schwarzschild(mass):
    #GMm / rs = 0.5 mc^2
    #rs = 2GM/c^2
    return (2 * G * mass / (c ** 2))

def calc_density(mass, radius):
    if(radius == -1 * Me):
        rs = calc_schwarzschild(mass)
    return mass / calc_vol(mass, rs)

def calc_vol(mass, radius):
    if(radius == -1 * Me):
        rs = calc_schwarzschild(mass)
    vol = 4.0 / 3.0 * pi * rs ** 3
    return vol

def calc_area(mass, radius):
    if(radius == -1 * Me):
        rs = calc_schwarzschild(mass)
    area = 2.0 * pi * rs ** 2
    return area


def main():
    #every single black hole is fully described by its mass, charge, and angular momentum..
    parser.add_option('-m', '--mass', action="store",dest="m", help="mass - 1Me (default)", type="float", default=-Me)
    parser.add_option('-p', '--density', actions="store", dest="p", help="density - 1 g/cm^3 (default)", type="float", default=-0.001)
    parser.add_option('-r', '--radius', actions="store", dest="r", help="Schwarzschild radius - 1 m (default)", type="float", default=-1.0)
    
    
    options, args = parser.parse_args()

