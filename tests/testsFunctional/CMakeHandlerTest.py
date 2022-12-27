import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from util.CMakeHandler import configureXmlParser

print(configureXmlParser(True, True, True, True).getPaths())
