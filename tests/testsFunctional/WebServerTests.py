import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from util.CppProjectTest.CMakeHandler import configureAndRunTests
from PrettyGcov.WebServer.WebServer import runServer

src_folder, build_folder, install_folder = configureAndRunTests().getPaths()

if __name__ == '__main__':
    runServer(port=9500, verbose=False, gcovFileFolder=build_folder, srcFolders=[src_folder])
