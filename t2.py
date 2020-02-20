import pandas
import pickle
import time
import json
import msgpack
import yaml
from dicttoxml import dicttoxml
import xmltodict
from random import randint
import sys
import matplotlib.pyplot as plt
import csv

randomList = []
for i in range(99999):
    value = randint(0, 10000)
    randomList.append(value) 

data = {"list": randomList,
        "boolean": False,
        "string": "No comfort do written conduct at prevent manners on. Celebrated contrasted discretion him sympathize her collecting occasional. Do answered bachelor occasion in of offended no concerns. Supply worthy warmth branch of no ye. Voice tried known to as my to. Though wished merits or be. Alone visit use these smart rooms ham. No waiting in on enjoyed placing it inquiry. ",
        "int": 645564456,
        "string2": "No comfort do written conduct at prevent manners on. Celebrated contrasted discretion him sympathize her collecting occasional. Do answered bachelor occasion in of offended no concerns. Supply worthy warmth branch of no ye. Voice tried known to as my to. Though wished merits or be. Alone visit use these smart rooms ham. No waiting in on enjoyed placing it inquiry. ",
}
def dict_to_xml(tag, d):
   
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return (elem)

def pickSerialize():
    global data
    start_time = time.time()
    serialized = pickle.dumps(data)                      
    aika = time.time() - start_time

    koko = sys.getsizeof(serialized)
    start_time2 = time.time()
    data = pickle.loads(serialized)
    aika2 = time.time() - start_time2

    return[aika,aika2,koko]

def xmlSerialize():
    global data
    startSerialization = time.time()
    xmlSerialized = dicttoxml(data)  # serialize dict to xml
    serializationTime = time.time() - startSerialization
    startDeSerialization = time.time()
    xmlDeSerialized = xmltodict.parse(
        xmlSerialized)  # deserialize xml back to dict
    deSerializationTime = time.time() - startDeSerialization
    SeriliazeSize = sys.getsizeof(xmlSerialized)
    return [serializationTime, deSerializationTime, SeriliazeSize]
    
    

   
def jsonSerialize():
    global data

    jstart_time = time.time()
    jserialized = json.dumps(data)                      
    aika3 = time.time() - jstart_time

    
    jkoko = sys.getsizeof(jserialized)
    jstart_time2 = time.time()
    data = json.loads(jserialized)
    aika4= time.time() - jstart_time2
 
    return[aika3,aika4,jkoko]
def messagepackSerialize():
    global data
    start_time = time.time()
    serialized = msgpack.packb(data)
    aika = time.time() - start_time

    start_time2 = time.time()
    deserialized = msgpack.unpackb(serialized)
    aika2 = time.time() - start_time2

    koko = sys.getsizeof(serialized)
    return[aika,aika2,koko]
    
def yamlserialize():
    global data
    jstart_time2 = time.time()
    ser = yaml.dump(data)
    aika4= time.time() - jstart_time2    
    start_time = time.time()
    dser = yaml.safe_load(ser)                     
    aika = time.time() - start_time
    koko = sys.getsizeof(ser)
    return[aika4,aika,koko]

def write(lista):
    file = open("Datat.txt","a")
    
    for i in lista:
        file.write(i+","+str(lista[i][0])+"," + str(lista[i][1])+","+str(lista[i][2])+" \n")

    file.close()
    x=[]
    y=[]
    z=[]

    with open('Datat.txt', 'r') as csvfile:
        plots= csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(float(row[1]))
            y.append(float(row[2]))
            #z.append(float(row[3]))
            


    plt.plot(x,y, marker='o')

    plt.title('Data from the CSV File: Ser/Deser')

    plt.xlabel('Serialization time')
    plt.ylabel('Deserialization time')

    plt.show()


def main():
    lista =  {}
    lista["PICKLE"] =(pickSerialize())
    lista["JSON"] =(jsonSerialize())
    lista["XML"] =(xmlSerialize())
    lista["MSGPAK"] =(messagepackSerialize())
    lista["YAML"] =(yamlserialize())
    #write(lista)
    for i,v in lista.items():
        print(i,v)
   
if __name__ == '__main__':    
    main()
    
