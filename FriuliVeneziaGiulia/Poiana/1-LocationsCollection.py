import tabula,os,pandas as pd,logging,datetime
os.chdir('D:/Python/Acqua/FriuliVeneziaGiulia/Poiana')
url = 'Definitions/Acque Potabili - Analisi Chimico fisiche 2018_2019.pdf'
tables = tabula.read_pdf(url,multiple_tables=True,pages='all',encoding='utf-8')
#%%
listRawtables = []
for table in tables:
    sx = table.iloc[:,0:2]
    listRawtables.append(sx)
    dx = table.iloc[:,2:4]
    listRawtables.append(dx)
  
#%%
locationList_ = []
for rt in listRawtables:
    if rt.shape == (19,2):
        alias_city = rt.iloc[2,0]
        alias_address = rt.iloc[1,0]

        string1 = alias_city.split(':')[1].strip()
        string2 = alias_address.split(':')[1].strip()
        string = string1+', '+string2
        
        loc = [alias_city,alias_address,string]
        
        locationList_.append(loc)

locationList = pd.DataFrame(locationList_,columns=["alias_city","alias_address","georeferencingString"])
#%%
locationList['type'] = 'Point'
locationList['polygonKey'] = ''#locationList['alias_city'].apply(lambda s: s.split(':')[1].strip().upper())
#%%           
locationList.to_csv('Definitions/LocationList.csv',index=False)

logging.info('Finish: %s',datetime.datetime.now())