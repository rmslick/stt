from Quaternion import Quaternion
import numpy as np
from math import pi, cos, sin
# Description: Generates a random quaternion
# Inputs: none
# Outputs: 4x1 quaternion, 1st element is scalar
# Fns used: optionally use generate_random_ProperRealOrthogonal_matrix()
def generateRandomQuaternion():
    e = np.random.rand(3,1)
    e = e/np.linalg.norm(e)
    theta = e*2*pi
    theta = theta[0][0]
    return Quaternion( cos(theta/2), e[0]*sin(theta/2) , e[1]*sin(theta/2) , e[2]*sin(theta/2) )

#Description: Obtain the bore sight vector of the camera
#Inputs: quaternion
#Outputs: Bore sight of the camera, along Z axis.

def getVBohr(q):
    r1 = [q[2]**2-q[3]**2-q[4]**2+q[1]**2, 2*(q[2]*q[3]+q[4]*q[1]), 2*(q[2]*q[4]-q[3]*q[1])]
    r2 = [2*(q[3]*q[2]-q[4]*q[1]), -1*q[2]**2+q[3]**2-q[4]**2+q[1]**2, 2*(q[3]*q[4]+q[2]*q[1])]
    r3 = [2*(q[4]*q[2]+q[3]*q[1]), 2*(q[4]*q[3]-q[2]*q[1]), -1*q[2]**2-q[3]**2+q[4]**2+q[1]**2] #; #bore sight
    return np.asarray([r1,r2,r3])
q = Quaternion( 1,2,3,4 )
# Description: Converts a vector in the ECI frame to a vector in the
# Camera frame
# Inputs: quaternion, Vector in ECI
# Outputs: Vector in Camera frame
# this may be cam specific?
def ECI2Cam(q,Veci):
    r1 = q[2]**2-q[3]**2-q[4]**2+q[1]**2,2*(q[2]*q[3]+q[4]*q[1]), 2*(q[2]*q[4]-q[3]*q[1])
    r2 = 2*(q[3]*q[2]-q[4]*q[1]),-1*q[2]**2+q[3]**2-q[4]**2+q[1]**2, 2*(q[3]*q[4]+q[2]*q[1])
    r3 = 2*(q[4]*q[2]+q[3]*q[1]), 2*(q[4]*q[3]-q[2]*q[1]), -1*q[2]**2-q[3]**2+q[4]**2+q[1]**2
    return np.asarray([r1,r2,r3]) @ Veci 

print(ECI2Cam(q,np.asarray([[1],[2],[3]])))
# Description: Johnson V filter transmission curve for real radiation spectra
# (ftp://obsftp.unige.ch/pub/mermio/filters/ph01.Vj)
# Transmission in Unity
# Inputs: none
# Outputs: range of wavelengths, Johnson V transmission curve for visualmagnitudes
def johnsonVcurve():
    lambd = []
    for i in range(5,3501,5):
        lambd.append(i*1e-9)
    top = []
    for i in range(89):
        top.append([0])
    bottom = []
    for i in range(559):
        bottom.append([0])
    A = [0.002,0.005,0.005,0.009,0.012,0.016,0.023,0.039,0.1,0.213,0.371,0.548,0.705,0.831,0.916,0.972,0.998,1.0,0.984,0.954,0.916,0.872,0.826,0.775,0.722,0.668,0.613,0.559,0.503,0.45,0.399,0.346,0.297,0.251,0.209,0.169,0.135,0.104,0.081,0.063,0.049,0.042,0.037,0.035,0.03,0.028,0.023,0.019,0.016,0.014,0.012,0.009]
    return [lambd,[top,A,bottom]]

# Description: Calculates the flux coming from the sun which is used as the
# reference star for calculating photon numbers in NumPhotons
# Inputs: none
# Outsputs: sun's flux
# Fns used: johnsonVcurve, Optionally check Wein's Displacement Law

# Note: create a star class for reference
def ref_star():
    h = 6.626*10^-34; # [J s] Planck's constant
    k = 1.38065*10^-23; # [J/K] Boltzmann's constant
    c = 2.997*10^8; # [m/s] speed of light
    sunT = 5777; # [K]
    AU = 149597871000; # [m] Astronomical Unit
    Rs = 695800000; # [m] Sun's radius
    dist = (AU/Rs)^2; # http://maths.ucd.ie/met/msc/fezzik/PhysMet/Ch04-2-Slides.pdf