#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals
import xml.dom.minidom
import sys

def getText(startnode):
    rc = ""
    for node in startnode.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def parsePrefixLengthMap(dom):
    prefix = getText(dom.getElementsByTagName("Prefix")[0])
    lengthMap = []
    for rule in dom.getElementsByTagName("Rules")[0].getElementsByTagName("Rule"):
        rule_range = getText(rule.getElementsByTagName("Range")[0])
        length = getText(rule.getElementsByTagName("Length")[0])
        (range_min, range_max) = rule_range.strip().split('-')
        range_to_length = { 'min'    : int(range_min),
                            'max'    : int(range_max),
                            'length' : int(length)
                            }
        lengthMap.append(range_to_length)
    return (prefix, lengthMap)

if len(sys.argv) != 2:
	print("Usage:\n./isbn_xml2py.py RangeMessage.xml > isbn_lengthmaps.py", file=sys.stderr)
	sys.exit(2)

xmlfile = sys.argv[1]
dom = xml.dom.minidom.parse(xmlfile)

ISBNRangeMessage = dom.getElementsByTagName("ISBNRangeMessage")[0]

groups_length = {}
for ean in ISBNRangeMessage.getElementsByTagName("EAN.UCCPrefixes")[0].getElementsByTagName("EAN.UCC"):
    (prefix, lengthMap) = parsePrefixLengthMap(ean)
    groups_length[prefix] = lengthMap

publisher_length = {}
for group in ISBNRangeMessage.getElementsByTagName("RegistrationGroups")[0].getElementsByTagName("Group"):
    (prefix, lengthMap) = parsePrefixLengthMap(group)
    publisher_length[prefix] = lengthMap

messageSerial = getText(ISBNRangeMessage.getElementsByTagName("MessageSerialNumber")[0])
messageDate = getText(ISBNRangeMessage.getElementsByTagName("MessageDate")[0])

print('# Generated from RangeMessage.xml with isbn_xml2py.py')
print('# Available from http://www.isbn-international.org/agency?rmxml=1')
print('# MessageDate: ' + messageDate)
print('# MessageSerialNumber: ' + messageSerial)
print('groups_length = ' + repr(groups_length).replace("u'", "'"))
print('publisher_length = ' + repr(publisher_length).replace("u'", "'"))
