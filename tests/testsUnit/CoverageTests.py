import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import unittest
from util.CppProjectTest.CMakeHandler import configureAndRunTests
from PrettyGcov.CoverageMap import CoverageMap
from PrettyGcov.CoverageTree import makeCoverageTree

class TestCoverageMap(unittest.TestCase):
    def __init__(self, *args, **kw):
        self.src_folder, self.build_folder, self.install_folder = configureAndRunTests().getPaths()
        unittest.TestCase.__init__(self, *args, **kw)

    def makeCoverageMap(self):
        coverage_map = CoverageMap(self.build_folder)
        coverage_map.addSourceDirectory(self.src_folder)
        coverage_map.generate()
        return coverage_map

    def test_flat_map(self):
        coverage_map = self.makeCoverageMap()
        print(coverage_map)

        # check files
        expectedFiles = []
        expectedFiles.append('{}{}'.format(self.src_folder, '/include/XML-Parser/Converter.h'))
        expectedFiles.append('{}{}'.format(self.src_folder, '/include/XML-Parser/Error.h'))
        expectedFiles.append('{}{}'.format(self.src_folder, '/include/XML-Parser/Parser.h'))
        expectedFiles.append('{}{}'.format(self.src_folder, '/include/XML-Parser/Tag.h'))

        expectedFiles.append('{}{}'.format(self.src_folder, '/source/Converter.cpp'))
        expectedFiles.append('{}{}'.format(self.src_folder, '/source/Error.cpp'))
        expectedFiles.append('{}{}'.format(self.src_folder, '/source/Parser.cpp'))
        expectedFiles.append('{}{}'.format(self.src_folder, '/source/Tag.cpp'))

        self.assertEqual(len(coverage_map.files_), len(expectedFiles), "invalid coverage map")
        for fileName in expectedFiles:
            self.assertTrue(fileName in coverage_map.files_, "Should have found {}".format(fileName))

    def test_tree(self):
        coverage_map = self.makeCoverageMap()
        coverage_tree = makeCoverageTree(coverage_map)
        print(coverage_tree)

        # TODO check generated tree

if __name__ == '__main__':
    unittest.main()
