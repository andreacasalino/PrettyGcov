import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from util.CppProjectTest.CMakeHandler import configureAndRunTests

configureAndRunTests(True, True, True, True)
