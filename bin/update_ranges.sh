#!/bin/sh


wget -O isbn_hyphenate/RangeMessage.xml http://www.isbn-international.org/agency?rmxml=1
isbn_hyphenate/isbn_xml2py.py isbn_hyphenate/RangeMessage.xml > isbn_hyphenate/isbn_lengthmaps.py
