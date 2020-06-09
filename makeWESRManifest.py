#!/usr/bin/env python3
import sys
import time
import urllib.parse
import requests
import xml.etree.ElementTree as ET

BASE_URL = "https://environmentlive.unep.org/api/"
INDICATOR_LIST_URL = BASE_URL + "indicators.php"
INDICATOR_DATA_URL = BASE_URL + "country_data.php?indicator_id={}"

LOOKUP_URL = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=country&QueryString="

BAD_INDICATORS = ["910", "3577", "3602", "3675", "3725"]

def getCountryUri(country_name):

    print("Searching dbpedia for {}.".format(country_name))

    r = requests.get(LOOKUP_URL + urllib.parse.quote(country_name, safe=''))

    tree = ET.fromstring(r.content)

    if len(tree) == 0:
        print("Could not find uri for {}.".format(country_name))
        return None
    else:
        uri = tree[0].findall('{http://lookup.dbpedia.org/}URI')[0].text

        print("Found uri for {0}: {1}".format(country_name, uri))

        return uri

def getIndicators():
    print("Fetching indicator list.")
    r = requests.get(INDICATOR_LIST_URL)
    if r.status_code != 200:
        raise Exception("Received status code {} while fetching indicator list.".format(r.status_code))
    return r.json()

def getIndicatorData(code):
    print("Fetching data for indicator {}.".format(code))
    r = requests.get(INDICATOR_DATA_URL.format(code))
    if r.status_code != 200:
        raise Exception("Received status code {0} while fetching {1} data.".format(r.status_code, code))
    return r.json()

def writeTTL(code, data, fp, country_uris):

    print("Writing data for indicator {}".format(code))

    rows = data.keys()

    countries = set()
    for r in rows:
        row = data[r]
        if row['country_name'] == None or row['country_name'] == '': continue
        countries.add(row['country_name'])

    indicator_uri = ':Indicator_{}'.format(code.zfill(4))

    countries = sorted(list(countries))
    for c in countries:
        if c not in country_uris: 
            country_uris[c] = getCountryUri(c)

            # Throttle requests to dbpedia so we don't get cut off
            time.sleep(1)

    for c in countries:
        if country_uris[c] == None: continue

        format_obj = {"indicator_uri": indicator_uri, "country_uri": country_uris[c]}
        fp.write("{country_uri} sio:001277 {indicator_uri} .\n\n".format(**format_obj))

def main():
    try:
        indicators = getIndicators()

        #start_index = next((index for (index, d) in enumerate(indicators) if d["indicator_id"] == "3576"), None)
        #indicators = indicators[start_index+1:]

        # Remove indicators that return 500 or malformed json
        indicators = list(filter(lambda i: i["indicator_id"] not in BAD_INDICATORS, indicators))

        country_uris = {}

        fp = open("wesr_data_manifest.owl", "w")

        for ind in indicators:
            while True:
                try:
                    data = getIndicatorData(ind["indicator_id"])

                    writeTTL(ind["indicator_id"], data, fp, country_uris)
                except Exception as e:
                    print(e)
                    continue
                break

    except Exception as e:
        print(e)
        print("Could not fetch indicator data.")

if __name__ == "__main__":
    main()
