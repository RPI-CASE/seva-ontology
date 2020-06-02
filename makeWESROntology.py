#!/usr/bin/env python
import sys
import time
import re
import requests
import sdgio

BASE_URL = "https://environmentlive.unep.org/api/"

INDICATOR_LIST_URL = BASE_URL + "indicators.php"

def cleanString(s):
    if isinstance(s, float): return str(int(s))
    return "\"" + s.encode("ascii", "replace").rstrip() + "\""

def getIndicators():
    print("Fetching indicator list.")
    r = requests.get(INDICATOR_LIST_URL)
    if r.status_code != 200:
        raise Exception("Received status code {} while fetching indicator list.".format(r.status_code))
    return r.json()

def makeIndicatorClass(indicator):
    text = ':Indicator_{} a owl:Class;\n'.format(indicator["indicator_id"].zfill(4))
    text += '     rdfs:label "Indicator {}" ;\n'.format(indicator["indicator_id"])
    text += '     skos:definition "{}" ;\n'.format(indicator["indicator_short"].rstrip())

    if("SDG " in indicator["indicator_short"]):
        found_indicators = re.findall(r'\d+\.\w+\.\w+\.?\w?', indicator["indicator_short"])

        for fi in found_indicators:
            filtered = list(filter(lambda s: s["indicator"] == fi, sdgio_indicators))
            if(len(filtered) > 0):
                text += '     rdfs:seeAlso <{}>;\n'.format(filtered[0]["uri"])

    text += '     rdfs:subClassOf <http://purl.org/seva/WESRIndicator> .\n\n'

    return text

print("Loading SDGIO ontology.")

sdgio_indicators = sdgio.SDGIO().getIndicators()

print("Successfully loaded SDGIO ontology")

indicators = getIndicators()

print("Writing indicator turtle.")

f = open("ssio.owl", "w")

for ind in indicators:
    f.write(makeIndicatorClass(ind))
        
