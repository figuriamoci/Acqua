import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import pandas as pd
import numpy as np
import tabula,os,logging,pickle

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC')
logging.basicConfig(level=logging.DEBUG)

filename = 'ListLabels.pickle'
infile = open(filename,'rb')
ll = pickle.load(infile)
infile.close()

fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file( fc, 'CAFC.geojson' )
coll.display(fc)