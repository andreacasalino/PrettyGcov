import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import unittest
from util.Paths import Paths, forceUnix
from PrettyGcov.Scanner import FileExtensionFilter, scan

TEST_FOLDER=forceUnix(os.path.join(Paths.dataPath(), 'foo'))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
class TestScan(unittest.TestCase):
    def filePredicate(self, fileName):
        # force unix like path
        fileName = forceUnix(fileName)
        print('===============>>>>> {}'.format(fileName))
        self.scanned.append(fileName)
        return True

    def checkScanned(self, expected):
        self.assertEqual(len(self.scanned), len(self.scanned), "Should have found {} files".format(len(expected)))
        for fileName in expected:
            self.assertTrue(fileName in self.scanned, "Should have found {}".format(fileName))

    def test_no_filter(self):
        self.scanned = []
        scan(TEST_FOLDER, self.filePredicate)
        print('--------------')
        self.checkScanned([
            '{}/fooA.foo'.format(TEST_FOLDER),
            '{}/fooB'.format(TEST_FOLDER),
            '{}/anotherA'.format(TEST_FOLDER),
            '{}/sub/subA.foo'.format(TEST_FOLDER),
            '{}/sub/subB'.format(TEST_FOLDER)
        ])

    def test_with_file_filter(self):
        self.scanned = []
        filter = FileExtensionFilter('foo')
        scan(TEST_FOLDER, self.filePredicate, fileFilter = filter.check)
        print('--------------')
        self.checkScanned([
            '{}/fooA.foo'.format(TEST_FOLDER),
            '{}/sub/subA.foo'.format(TEST_FOLDER),
        ])

    def test_with_directory_filter(self):
        self.scanned = []
        filter = FileExtensionFilter('foo')
        scan(TEST_FOLDER, self.filePredicate, directoryFilter = lambda directory : directory.find('sub') == -1 )
        print('--------------')
        self.checkScanned([
            '{}/fooA.foo'.format(TEST_FOLDER),
            '{}/fooB'.format(TEST_FOLDER),
            '{}/anotherA'.format(TEST_FOLDER),
        ])

if __name__ == '__main__':
    unittest.main()
