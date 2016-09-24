#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


OSMFILE = "london_sample_100.osm"

# match sequence of non-white space characters optionally 
# followed by a period and match must occur at end of the string.
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Way", "Walk", "Gardens", "Close", "Acre", "Colonnade",
            "Hill", "Mead", "Rise", "Terrace", "Village", "Square","North"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "st": "Street",
            "street": "Street",
            "STREET":"Street",
            "Sq": "Square",
            "boulevard": "Boulevard",
            "HILL":"Hill",
            "place": "Place",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Ln": "Lane",
            "N": "North",
            "Rd": "Road",
            "road": "Road",
            "Road)": "Road",
            "ROAD": "Road",
            "Rd.": "Road"}

def audit_street_type(street_types, street_name):
    # matches the last word in a street name (as they end with the street type i.e. avenue)
    m = street_type_re.search(street_name)
    if m: # if theres a match
        street_type = m.group() # get the specific match using group()
        if street_type not in expected: # if the matched street_type is not in the expected list, add to street_types dictionary.
            street_types[street_type].add(street_name)

def is_street_name(elem):
    # looks at k attribute of element that was passed in
    # with k attribue having "addr:street" value i.e. a street name
    return (elem.attrib['k'] == "addr:street")

def is_city_name(elem):
    # looks at k attribute of element that was passed in
    # with k attribue having "addr:city" value i.e. a city name
    return (elem.attrib['k'] == "addr:city")

def is_postcode_name(elem):
    # looks at k attribute of element that was passed in
    # with k attribue having "addr:postcode" value i.e. a postcode name
    if elem.attrib['k'] == "addr:postcode":
        return (elem.attrib['k'] == "addr:postcode")
    if elem.attrib['k'] == "postal_code":
        return (elem.attrib['k'] == "postal_code")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postcode_types = set()
    city_types = set()
    tag_types = set()
    attrib_types = defaultdict(set)


    # looping through XML file using SAX style parsing part of c element tree module.
    # this allows you to rearrange or remove parts of the tree whilst parsing and takes less resources.
    # parse with event based parsing. Every time it sees the event, it will emit the event and the element it finds.
    # Any time it sees a start tag, (as a tuple) generate next item in its iteration.
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        tag_types.add(elem.tag)
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"): # iter method returns in an iteration all the subtags within the element named "tag"
                
                if 'naptan' not in tag.attrib['k']:
                    attrib_types[tag.attrib['k']] = tag.attrib['v']
                    #print tag.attrib['k']
                
                if is_street_name(tag): # if I have a tag that is specified in the way we want in is_street_name
                    audit_street_type(street_types, tag.attrib['v'])

                if is_city_name(tag): # if I have a tag that is specified in the way we want in is_city_name
                    city_types.add(tag.attrib['v'])

                if is_postcode_name(tag): # if I have a tag that is specified in the way we want in is_postcode_name
                    postcode_types.add(tag.attrib['v'])
    
    ## checking postcode, city and tag types.
    print "=======postcode_types========"
    print postcode_types
    print "=======city_types========"
    print city_types
    print "=======tag_types======= "
    print tag_types
    #print "=======attrib_types======= "
    #for x in attrib_types:
        #print x

    osm_file.close()
    return street_types


def update_name(name, mapping):
    name = name.split()
    #print name
    for entry in mapping:
        for i in range(0, len(name)):
            if entry == name[i]:
                name[i] = mapping[entry]
    name = " ".join(name)
    return name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    #for st_type, ways in st_types.iteritems():
        #for name in ways:
            #better_name = update_name(name, mapping)
            #print name, "=>", better_name


if __name__ == '__main__':
    test()