##
import pymongo as py
conn = py.MongoClient("mongodb+srv://Acqua:nato1968@principal-4g7w8.mongodb.net/test?retryWrites=true&w=majority")
db = conn.Acqua
collection = db.etichette
print(collection)
##
doc1 = {'nome':'Andrea','cognome':'Fantini','sesso':'mas'}
doc2 = {'nome':'Elisabetta','cognome':'Dalla Valle','sesso':'fem'}
ll = []
ll.append(doc1)
ll.append(doc2)
##
collection.insert_many(ll)
