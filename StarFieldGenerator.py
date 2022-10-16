from Quaternion import Quaternion
from StarCatalogInterface import Catalog
from StarTrackerUtil import *
from math import cos,sin,pi,e,pow
import pandas as pd
class Star:
    def __init__(self):
        pass
class Sun(Star):
    def __init__(self):
        self.h = 6.626*10*-34; # [J s] Planck's constant
        self.k = 1.38065*10*-23; # [J/K] Boltzmann's constant
        self.c = 2.997*10*8; # [m/s] speed of light
        self.sunT = 5777; # [K]
        self.AU = 149597871000; # [m] Astronomical Unit
        self.Rs = 695800000; # [m] Sun's radius
        self.dist = (self.AU/self.Rs)**2; # http://maths.ucd.ie/met/msc/fezzik/PhysMet/Ch04-2-Slides.pdf   
    #ref_star
    def getFlux(self):
        jcurve = johnsonVcurve()
        lambd = jcurve[0]
        #p = ((2*pi*h*c^2)./(lambda.^5.*( exp( (h*c) ./(lambda.*k*sunT) ) -1) )) ';
        lambdar = [l*self.k*self.sunT for l in lambd ] #lambda.*k*sunT
        innerexp1 = [(self.h*self.c)/i for i in lambdar] # (h*c) ./(lambda.*k*sunT)
        innerexp2 = [ pow(e,i)-1 for i in innerexp1] # exp( (h*c) ./(lambda.*k*sunT) )-1
        lambda5 = [l**5 for l in lambd] #lambda.^5
        p = np.asarray( [(2*pi*self.h*self.c**2)/lambda5[i] * innerexp2[i] for i in range(len(innerexp2))] ) #((2*pi*h*c^2)./(lambda.^5.*( exp( (h*c) ./(lambda.*k*sunT) ) -1) ))
        p = np.transpose( p )
        # for each element in JV, mult p
        ele = np.asarray( [p@jv for jv in jcurve[1:] ] ) # p.*JV
        flux = np.trapz(lambd,ele)
        return [f/self.dist for f in flux]





class StarFieldGenerator:
    def __init__(self, camera, catalog , sttInterface, referenceStar):
        self.catalog = catalog
        self.mag6 = sttInterface
        self.cam = camera
        self.refStar = 
    # Description: Converts the coordinates of stars from camera frame to pixelspace
    # Inputs: camera specs, x,y,z coordinates in camera frame
    # Outsputs: u,v coordnates in Pixel Space
    def camera2PixelSpace(self,specs,vx,vy,vz):
        f = specs.f
        pp = specs.pp
        U = specs.U
        V = specs.V
        uc = (U/2)+1
        vc = (V/2)+1
        d = f/vz
        u = uc - (vx*d)/pp
        v = vc - (vy*d)/pp
        return [u,v]
    # Description: Obtains all the star coordinates in the camera's FOV and
    # converts them from ECI to camera frame
    # Inputs: quaternion, camera specs
    # Outputs: mag6bore structure with star vector parameters including
    # Hipparcos ID, RA, Dec, mag, bv, HDID, ECI coordinates
    # Fns used: get_Vbohr, Veci_2Vcam
    def cameraStarCoordinates(self,q,specs):
        FOV = specs.FOV
        Vbore = getVBohr(q)
        cols = ['hip','ra', 'dec','mag','bv','HDID','ECIcoord','CameraCoord','PixelCoord'] 
        
        mag6bore = []
        for i in range(0, len(self.mag6.hip)):
            j = np.asarray( self.mag6.ECIcoord[i] )
            prod = j@Vbore
            mag6Map = dict(zip(cols, [0]*len()))
            if prod >= cos(FOV):
                mag6Map["hip"] = self.mag6.hip[i]
                mag6Map["ra"] = self.mag6.ra[i]
                mag6Map["dec"] = self.mag6.dec[i]
                mag6Map["mag"] = self.mag6.mag[i]
                mag6Map["bv"] = self.mag6.bv[i]
                mag6Map["HDID"] = self.mag6.HDID[i]
                mag6Map["ECIcoord"] = self.mag6.ECIcoord[i]
                vxyz = ECI2Cam(q,self.mag6.ECIcoord[i])
                mag6Map["CameraCoord"] = vxyz
                mag6Map["PixelCoord"] = self.camera2PixelSpace(specs,vxyz[0],vxyz[1],vxyz[2])
                mag6bore.append(mag6Map)
        return mag6bore
