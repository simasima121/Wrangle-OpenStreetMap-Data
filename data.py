#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The data has been wrangled and transformed into the following model.
The output is a list of dictionaries that look like this:
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

If you are using the process_map() procedure above on your own computer to write to a JSON file,
make sure you call it with pretty = False parameter. Otherwise, mongoimport might give you an 
error when you try to import the JSON file to MongoDB.
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


## Update the street and city names using update street name proedure in mapping.py
## before saving them to JSON. 
from mapping import audit, update_name, mapping

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    node = {'created':{}, 'address':{}}
    
    # you should process only 2 types of top level tags: "node" and "way"
    if element.tag == "node" or element.tag == "way" :
        
        node['type'] = element.tag
        
        # all attributes of "node" and "way" should be turned into regular key/value pairs
        pos = []
        for ele in element.attrib:

            # attributes for latitude and longitude should be added to a "pos" array,
            if ele == 'lon' or ele =='lat':
                pos.append(float(element.attrib[ele]))
                if len(pos) == 2:
                    new_pos = []
                    if pos[0] < 0:
                        new_pos.append(pos[1])
                        new_pos.append(pos[0])
                        node['pos'] = new_pos
                    else:
                        node['pos'] = pos
                        
            # attributes in the CREATED array should be added under a key "created"
            elif ele in CREATED:
                node['created'][ele] = element.attrib[ele]
            else:
                node[ele] = element.attrib[ele]
        
        noderefs = []
        for child in element:
            
            ## Putting node_refs in dictionary
            if 'k' not in child.attrib:
                noderefs.append(child.attrib['ref'])
            else:
                # if the second level tag "k" value contains problematic characters, it should be ignored
                if problemchars.search(child.attrib['k']):
                    continue
                #if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
                if lower_colon.search(child.attrib['k']):
                    colon = child.attrib['k'].find(':')
                    
                    # if the second level tag "k" value starts with "addr:", 
                    # it should be added to a dictionary "address"
                    if child.attrib['k'][:colon] == 'addr':
                        
                        kval = child.attrib['k'][colon+1:]
                        vval = child.attrib['v']

                        node['address'][kval] = vval
                
                ## Ensuring postcodes are added into the node dictionary
                elif child.attrib['k'] == 'postal_code':
                    kval = "postcode"
                    vval = child.attrib['v']
                    node['address'][kval] = vval
                    
                else:
                    kval = child.attrib['k']
                    vval = child.attrib['v']
                    node[kval] = vval

            node['node_refs'] = noderefs
        
        return node
    else:
        return None

## This file writes out a JSON file to be put imported into a mongo database.
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                ## Updating street names and city name to have correct mapping
                for e in el['address']:
                    if e == 'street':
                        updated = update_name(el['address'][e], mapping)
                        el['address'][e] = updated
                    if e == 'city':
                        el['address'][e] = 'London'
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('london_sample_1000.osm', False)
    print "done"
    #pprint.pprint(data)

if __name__ == "__main__":
    test()