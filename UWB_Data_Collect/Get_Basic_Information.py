import requests
import time
import pandas

data = {}
An0094 = []
An0095 = []
An0096 = []
An0099 = []
An0011 = []
Tag1198 = []
Coord0011= []
locator = {}

for i in range(0,4):
    response = requests.get(url="http://192.168.8.107/php/vilsnodes.php")
    data = response.json()
    for i in data.keys():
        if "ANCHOR" in i:
            for value in data.values():
                if "An0094" in value:
                    An0094 = value.split(',')
                elif "An0095" in value:
                    An0095 = value.split(',')
                elif "An0096" in value:
                    An0096 = value.split(',')
                elif "An0099" in value:
                    An0099 = value.split(',')
                elif "An0011" in value:
                    An0011 = value.split(',')
        elif "TAG" in i:
            for value in data.values():
                if "Tag1198" in value:
                    Tag1198 = value.split(',')
        elif "COORD" in i:
            for value in data.values():
                if "Coord0011" in value:
                    Coord0011 = value.split(',')
        elif "LOCATOR" in i:
            locator = data
        break
