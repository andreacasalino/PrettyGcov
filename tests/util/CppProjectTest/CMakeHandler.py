import subprocess

def unWrap(toRun):
    result = toRun[0]
    for slice in toRun[1:]:
        result += ' '
        result += slice
    return result

def hasNinja():
    try:
        proc = subprocess.Popen(["ninja", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        return proc.returncode == 0
    except:
        pass
    return False

import os
from util.Paths import Paths
from PrettyGcov.Scanner import scan 

class CMakeHandler:
    def __init__(self):
        self.src_folder = os.path.join(Paths.testsRoot(), 'util', 'CppProjectTest')
        self.build_folder = os.path.join(Paths.testsRoot(), 'build')
        self.install_folder= os.path.join(Paths.testsRoot(), 'build', 'install')
        
    def runCommand_(self, toRun, verbose):
        if not os.path.exists(self.build_folder):
            os.mkdir(self.build_folder)
        print('===== from {}'.format(self.build_folder))
        print('===== running: {}'.format(unWrap(toRun)))
        with subprocess.Popen(toRun, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.build_folder) as proc:   
            if verbose:
                print('===== stdout')
                for line in proc.stdout:                
                    print(line[:-1].decode())
            out, err = proc.communicate()
            err = err.decode()
            if proc.returncode != 0:
                print('===== stderr')
                print(err)
                raise Exception('Something went wrong')
        print('============================= DONE =============================')

    def configure(self, verbose=False):
        print('============================= Configuring CMake project =============================')
        configure_cmd = ['cmake']
        configure_cmd.append(self.src_folder)
        configure_cmd.append('-B./')
        configure_cmd.append('-DCMAKE_INSTALL_PREFIX:STRING={}'.format(self.install_folder))
        if hasNinja():
            configure_cmd.append('-GNinja')
        configure_cmd.append('-DBUILD_XML_Parser_SAMPLES="OFF"')
        configure_cmd.append('-DBUILD_XML_Parser_TESTS="ON"')
        configure_cmd.append('-DCMAKE_CONFIGURATION_TYPES="Release"')
        configure_cmd.append('-DCMAKE_BUILD_TYPE:STRING=Release')
        self.runCommand_(configure_cmd, verbose)

    def build(self, verbose=False):
        print('============================= Building CMake targets =============================')
        build_cmd = ['cmake', '--build', './', '--config', 'Release']
        self.runCommand_(build_cmd, verbose)

    def install(self, verbose=False):
        print('============================= Installing CMake targets =============================')
        install_cmd = ['cmake', '--install', './', '--config', 'Release']
        self.runCommand_(install_cmd, verbose)

    def runTests(self, verbose=False):
        print('============================= Running tests =============================')
        def runTest(path):
            print('===== Running tests: ', path)
            pathParent = os.path.split(path)[0]
            proc = subprocess.Popen(path, cwd=pathParent)
            proc.communicate()

        def isTest(path):
            return path.find('Test') != -1

        bin_folder = os.path.join(self.install_folder, 'bin')
        scan(bin_folder, runTest, fileFilter=isTest)
        print('============================= DONE =============================')

    def getLibSrc(self):
        to_find = 'XML-Parser-Core_SOURCE_DIR:STATIC='
        with open('{}/CMakeCache.txt'.format(self.build_folder), 'r') as f:
            content = f.read()
            start = content.find(to_find)
            end = content.find('\n', start)
            result = '{}/Lib'.format(content[start+len(to_find):end])
            return result

    def getPaths(self):
        return [self.getLibSrc(), self.build_folder, self.install_folder]


def configureAndRunTests(showCfg=False, showBuild=False, showInstall=False, showTests=True):
    result = CMakeHandler()
    result.configure(verbose=showCfg)
    result.build(verbose=showBuild)
    result.install(verbose=showInstall)
    result.runTests(verbose=showTests)
    return result
