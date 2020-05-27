import pandas as pd,requests
import acqua.aqueduct as aq,logging
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "ACAMLaSpezia"
aq.setEnv('Liguria//'+gestore)
locationList = pd.read_csv('Metadata/LocationList.csv')
def to_date(d):
    from datetime import datetime
    return datetime.strptime( d, '%d/%m/%y' )
def to_char(d):
    return d.strftime('%d/%m/%y' )
#
locationList['data_report_format'] = locationList['data_report'].apply(to_date)
locationListReviewed = locationList.groupby(['alias_city','alias_address']).max()[['data_report_format','georeferencingString','type']]
locationListReviewed['data_report'] = locationListReviewed['data_report_format'].apply(to_char)
locationListReviewed.reset_index(inplace=True)
locationListReviewed.drop('data_report_format', axis=1, inplace=True)
locationListReviewed.to_csv('Metadata/LocationListReviewed.csv',index=False)
