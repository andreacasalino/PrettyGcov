import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from util.Paths import Paths

BUILD_FOLDER = os.path.join(Paths.testsRoot(), 'build')
if not os.path.exists(BUILD_FOLDER):
    os.mkdir(BUILD_FOLDER)

from PrettyGcov.GcovStat import GCovStat, getFileStat
from PrettyGcov.GcovFile import GcovFile
from PrettyGcov.WebServer.PageFactory import makeElementStats, PageFactory

def elementStatsGen():
    coverage = GCovStat()
    coverage.covered_ = 50
    coverage.total_ = 80

    elementStatsPage = makeElementStats('/foo/foo/foo', coverage)
    with open('{}/ElementStatsSample.html'.format(BUILD_FOLDER), 'w') as f:
        f.write(elementStatsPage)
elementStatsGen()

def filePageGen():
    class FakeTree:
        def __init__(self):
            self.path_ = ['the', 'root', 'path']
    factory = PageFactory(9500, FakeTree())
    gcovFile = GcovFile('{}/foo.gcov_test'.format(Paths.dataPath()))
    gcovStat = getFileStat(gcovFile)
    filePage = factory.makeFilePage_(gcovFile, gcovStat)
    with open('{}/FileSample.html'.format(BUILD_FOLDER), 'w') as f:
        f.write(filePage)
filePageGen()

from util.CMakeHandler import configureXmlParser
from PrettyGcov.CoverageMap import CoverageMap
from PrettyGcov.CoverageTree import makeCoverageTree

def folderPageGen():
    src_folder, build_folder, install_folder = configureXmlParser().getPaths()
    coverage_map = CoverageMap(build_folder)
    coverage_map.addSourceDirectory(src_folder)
    coverage_map.generate()

    coverage_tree = makeCoverageTree(coverage_map)

    factory = PageFactory(9500, coverage_tree)
    folderPage = factory.makeFolderPage_(coverage_tree)
    with open('{}/FolderSample.html'.format(BUILD_FOLDER), 'w') as f:
        f.write(folderPage)
folderPageGen()
