import pymongo
import json
from bson import ObjectId
from rdflib import Graph
import regex as re
from tqdm import tqdm
import rdflib

#ttl

graph = Graph()
graph.parse(r"C:\Users\Cezary\Downloads\skos_lit_25_08.ttl", format='ttl')
graph.parse(r"C:\Users\Cezary\Downloads\new_bnskos_25_08.ttl", format='ttl')
graph.serialize(format='json-ld', indent=4)
print(graph.serialize(format='json-ld', indent=4))
print(graph.serialize(format='rdf/xml', indent=4))



#jsonld

with open(r"C:\Users\Cezary\Downloads\bn_skos.jsonld", 'r', encoding='utf-8') as f:
    data = json.load(f)

inv_map = {v.replace('<','').replace('>',''): f"{k.split(' ')[-1]}:" for k, v in data.get('@context').items()}

pat = '|'.join(r"\b{}\b".format(x) for x in inv_map.keys())
test = [{re.sub(pat, lambda x: inv_map.get(x.group(0)), k):v for k,v in e.items()} for e in data.get('@graph')]

#mongodb

# test = data.get('@graph')
client = pymongo.MongoClient()
mydb = client['jsonld']
mycol = mydb['dane_hubara']
[mycol.insert_one(e) for e in tqdm(test)]

for _ in mycol.find({ 'http://schema.org/name' : 'Bitwa_pod_Barkweda_(1807)' }):
    print(_)
for _ in mycol.find({"_id" : ObjectId('6308c0b284e06e5f643f1e97')}):
    print(_)
for _ in mycol.find({ 'http://schema.org/name': 'Bitwa_pod_Barkweda_(1807)' }):
    print(_)













