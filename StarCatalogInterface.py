import pandas as pd
import numpy as np
from math import cos,sin
class Catalog:
    def __init__(self):
        pass
    def loadData(self):
        pass
'''
 if (new.mag(i) > 6)
 new.hip(i) = [];
 new.ra(i) = [];
 new.dec(i) = [];
 new.pmRa(i) = [];
 new.pmDec(i) = [];
 new.mag(i) = [];
 new.parallax(i) = []; ?
 new.bv(i) = [];
 new.vi(i) = []; ? how is this diff than mag
 HDID
'''
class HypCatalog(Catalog):
    def __init__(self, path="hygdata_v3.csv", magFilter = 6 ):
        self.pathToData = path 
        self.dataCols = ['hip', 'hd','ra','dec','pmra','pmdec','mag','ci']
        self.magFilter = magFilter
        self.df = None 
        self.loadData()
        self.hip = self.df['hip'].to_list()
        self.HDID= self.df['hd'].to_list()
        self.ra = self.df['ra'].to_list()
        self.dec = self.df['dec'].to_list()
        self.pmra = self.df['pmra'].to_list()
        self.pmdec = self.df['pmdec'].to_list()
        self.mag = self.df['mag'].to_list()
        self.bv = self.df['ci'].to_list()
        self.ECIcoord = self.df['ECIcoord'].to_list()

    def loadData(self):
        # load data from file
        self.df = pd.read_csv(self.pathToData,usecols=self.dataCols)
        # filter out stars by magnitude
        self.df = self.df[self.df['mag'] > self.magFilter]
        # strip out nans
        self.df['hd'] = self.df['hd'].replace(np.nan, 0)
        # convert ra and dec to unit vectors in ECI frame
        # add as new column in vector
        eciCoords = []
        dec = self.df['dec'].to_list()
        ra = self.df['ra'].to_list()
        for i in range( len( self.df['ra'] ) ):
            eciCoord = [0,0,0]
            eciCoord[0] = cos( dec[i] ) * cos( ra[i] )
            eciCoord[1] = cos( dec[i] ) * sin( ra[i] )
            eciCoord[2] = sin( dec[i] )
            eciCoords.append(eciCoord)
        self.df['ECIcoord'] = eciCoords
        print(self.df.columns)
t = HypCatalog()
t.loadData()