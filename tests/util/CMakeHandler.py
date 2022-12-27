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
    # info={
    #  'name':'name of folder in build for this prj',
    #  'srcLocation':'name of the folder inside the fetched prj storing the sources',
    #  'url':'git project to fetch',
    #  'tag':'tag representing the commit/branch to fetch',
    # }
    def __init__(self, info):
        def checkAttribute(info, name):
            if not name in info:
                raise Exception('{} not specified'.format(name))
        checkAttribute(info, 'name')
        checkAttribute(info, 'srcLocation')
        checkAttribute(info, 'url')
        checkAttribute(info, 'tag')
        self.info = info
        self.options = {}

        self.build_folder = os.path.join(Paths.testsRoot(), 'build', self.info['name'])
        self.install_folder= os.path.join(self.build_folder, 'install')
        self.src_folder = os.path.join(self.build_folder, '_src')

    def withOption(self, name, value):
        self.options[name] = value
        return self

    def generateCMakeProject_(self):
        if not os.path.exists(self.src_folder):
            os.makedirs(self.src_folder)
        options=''
        for name, value in self.options.items():
            options += 'SET({} {} CACHE BOOL "" FORCE)\n'.format(name, value)
        data=''
        with open(os.path.join(Paths.testsRoot(), 'util', 'CMakeLists.txt'), 'r') as stream:
            data = stream.read()
            data = data.replace('$OPTIONS', options)
            data = data.replace('$NAME', self.info['name'])
            data = data.replace('$URL', self.info['url'])
            data = data.replace('$TAG', self.info['tag'])
        with open(os.path.join(self.src_folder, 'CMakeLists.txt'), 'w') as stream:
            stream.write(data)

    def runCommand_(self, toRun, verbose):
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
        self.generateCMakeProject_()
        configure_cmd = ['cmake']
        configure_cmd.append(self.src_folder)
        configure_cmd.append('-B./')
        configure_cmd.append('-DCMAKE_INSTALL_PREFIX:STRING={}'.format(self.install_folder))
        if hasNinja():
            configure_cmd.append('-GNinja')
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
        tests=[]
        bin_folder = os.path.join(self.install_folder, 'bin')
        scan(bin_folder, lambda path : tests.append(path))
        for test in tests:
            print('===== Running: ', test)
            pathParent = os.path.split(test)[0]
            proc = subprocess.Popen(test, cwd=pathParent)
            proc.communicate()
            # clean up all produced files
            def cleaner(path):
                if not path in tests:
                    os.remove(path)
            scan(bin_folder, cleaner)
        print('============================= DONE =============================')

    def getFetchFolder_(self):
        def extractValue(content, name):
            start = content.find(name)
            end = content.find('\n', start)
            return content[start+len(name):end]

        with open('{}/CMakeCache.txt'.format(self.build_folder), 'r') as f:
            content = f.read()
            return  extractValue(content, 'FETCHCONTENT_BASE_DIR:PATH=')

    def getPaths(self):
        fetch_folder = self.getFetchFolder_()
        src = os.path.join(fetch_folder, '{}-src'.format(self.info['name']), self.info['srcLocation'])
        build = os.path.join(fetch_folder, '{}-build'.format(self.info['name']))
        return [src, build, self.install_folder]


def configureAndRunTests(info, options={}, showCfg=False, showBuild=False, showInstall=False, showTests=True):
    result = CMakeHandler(info)
    for name, value in options.items():
        result.withOption(name, value)
    result.configure(verbose=showCfg)
    result.build(verbose=showBuild)
    result.install(verbose=showInstall)
    result.runTests(verbose=showTests)
    return result

def configureXmlParser(showCfg=False, showBuild=False, showInstall=False, showTests=True):
    info={
        'name':'xml-parser',
        'srcLocation':'Lib',
        'url':'https://github.com/andreacasalino/XML-parser.git',
        'tag':'d3f2810bd5b1e278d0fb2e8eadd2b24ff533f11e',
    }
    opts={
        'BUILD_XML_Parser_SAMPLES':'OFF',
        'BUILD_XML_Parser_TESTS':'ON',
    }
    return configureAndRunTests(info, opts, showCfg, showBuild, showInstall, showTests)

def configureMinimalSocket(showCfg=False, showBuild=False, showInstall=False, showTests=True):
    info={
        'name':'minimal-socket',
        'srcLocation':'src',
        'url':'https://github.com/andreacasalino/Minimal-Socket.git',
        'tag':'14918a1ec78da2479225bf048a9c4154c128ff7d',
    }
    opts={
        'BUILD_MinimalCppSocket_SAMPLES':'OFF',
        'BUILD_MinimalCppSocket_TESTS':'ON',
    }
    return configureAndRunTests(info, opts, showCfg, showBuild, showInstall, showTests)

def configureEFG(showCfg=False, showBuild=False, showInstall=False, showTests=True):
    info={
        'name':'efg',
        'srcLocation':'src',
        'url':'https://github.com/andreacasalino/Easy-Factor-Graph.git',
        'tag':'0801273b002b58d272ea656bbe6ebbc2c24cc909',
    }
    opts={
        'BUILD_EFG_SAMPLES':'OFF',
        'BUILD_EFG_TESTS':'ON',
    }
    return configureAndRunTests(info, opts, showCfg, showBuild, showInstall, showTests)
