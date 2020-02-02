#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:52:40 2020

@author: andrea
"""
##
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import pandas as pd
import numpy as np
import os,logging,datetime
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium import webdriver
##
os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Lta')
logging.basicConfig(level=logging.DEBUG)
idGestore = 23007 #lta
data_report = 'settembre 2919'
listParameters = parm.getListSynonyms('Definitions/SynParametri.csv')
parm.crea_dizionario('Definitions/SynParametri.csv')
##
df = pd.read_csv('Definitions/LocationList.csv')
df.set_index(['alias_city','alias_address'],inplace=True)
locationList = df.index
##
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
##
logging.info( 'Start: %s', datetime.datetime.now() )
ll = []
i=0
##
for loc in locationList:
    i=i+1
    #loc=('Annone Veneto ','Annone Veneto - Viale Venezia')
    driver.get( "https://www.lta.it/le-analisi-della-tua-acqua" )
    control_loc = Select( driver.find_element_by_id( 'punto-di-analisi' ) )
    control_loc.select_by_visible_text( loc[1] )
    logging.info('Anayzing %s..(%s/%s)',loc[1],i,len(locationList))
    soup = BeautifulSoup( driver.page_source, 'html.parser' )
    htmlTable = soup.findAll('table',{'class':'table table-striped'})
    rawTable = pd.read_html(str(htmlTable),decimal=',',thousands='.',header=0)[0]
    #
    label_ = rawTable[['Parametro','Valore']]
    label_ = label_.apply( lambda x: x.str.lower() )
    l = label_['Parametro'].isin(listParameters)
    label = label_[l]
    label = label.set_index('Parametro').to_dict()

    lb = al.create_label( idGestore, data_report, label['Valore'] )
    glb = al.addGeocodeData( lb, loc, 'Definitions/GeoReferencedLocationsList.csv' )
    for j in range(0,len(glb)): ll.append( glb[j] )
##
logging.info('End.')
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file(fc,'Lta.geojson')
coll.display(fc)





