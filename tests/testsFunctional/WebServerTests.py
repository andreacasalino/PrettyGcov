import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from util.CMakeHandler import configureXmlParser, configureMinimalSocket, configureEFG
from PrettyGcov.WebServer.WebServer import runServer

# prjToRun = configureXmlParser
prjToRun = configureMinimalSocket
# prjToRun = configureEFG

src_folder, build_folder, install_folder = prjToRun().getPaths()

if __name__ == '__main__':
    runServer(port=9500, verbose=False, gcovFileFolder=build_folder, srcFolders=[src_folder])
