import pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
aq.setEnv('Lombardia//MM')
df = pd.read_csv('Definitions/ReportFoundList.csv')
useThisDictionary = parm.crea_dizionario('Medadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Medadata/SynParametri.csv')

reportFoundList = df.rename(columns=useThisDictionary)

reportFoundList['pH'].plot(kind='bar')
parm.getVL('pH')

reportFoundList['cloro_residuo'].plot(kind='bar')


df2 = df.str.replace('<','')