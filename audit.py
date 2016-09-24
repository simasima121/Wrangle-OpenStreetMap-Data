#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re # regular expression
import pprint

osm_file = open("london_sample_100.osm", "r")

# match sequence of non-white space characters optionally 
# followed by a period and match must occur at end of the string.
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE) 
street_types = defaultdict(set) # set so you don't have duplicate entries in the dictionary

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Way", "Walk", "Gardens", "Close"]

def audit_street_type(street_types, street_name):
    # matches the last word in a street name (as they end with the street type i.e. avenue)

    m = street_type_re.search(street_name)
    if m: # if theres a match
        street_type = m.group() # get the specific match using group()
        if street_type not in expected: # if the matched street_type is not in the expected list, add to street_types dictionary.
            street_types[street_type].add(street_name)

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

def is_street_name(elem):
    # looks at k attribute of element that was passed in
    # with k attribue having "addr:street" value i.e. a street name
    return (elem.attrib['k'] == "addr:street")

def audit():
    # looping through xml file using SAX style parsing part of c element tree module.
    # this allows you to rearrange or remove parts of the tree whilst parsing and takes less resources.
    # parse with event based parsing. Every time it sees the event, it will emit the event and the element it finds.
    # Any time it sees a start tag, (as a tuple) generate next item in its iteration.
    for event, elem in ET.iterparse(osm_file, events=("start",)):  
        if elem.tag == "way":
            for tag in elem.iter("tag"): # iter method returns in an iteration all the subtags within the element named "tag"
                if is_street_name(tag): # if I have a tag that is specified in the way we want in is_street_name
                    audit_street_type(street_types, tag.attrib['v'])     
    pprint.pprint(dict(street_types))
    #print_sorted_dict(street_types)    

if __name__ == '__main__':
    audit()