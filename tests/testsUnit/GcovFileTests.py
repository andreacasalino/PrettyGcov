import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import unittest
from PrettyGcov.GcovFile import GcovFile, UncovarbleFile
from util.Paths import Paths

class TestGcovFile(unittest.TestCase):
    def test_parse(self):
        parsed = GcovFile('{}/foo.gcov_test'.format(Paths.dataPath()))
        print('from GcovFile: {}'.format(parsed.source))
        for line in parsed.lines:
            print('from GcovFile: {} : {}'.format(line['kind'], line['line']))

        self.assertEqual(parsed.source, '/home/andrea/Scrivania/GitProj/GcovReport/cpp-sample/src/logger/Formatter.h', "Invalid source parsed")
        self.assertEqual(len(parsed.lines), 7, "Invalid lines parsed")

        self.assertEqual(parsed.lines[0]['kind'], '-', "Invalid lines parsed")
        self.assertEqual(parsed.lines[0]['line'], 'first', "Invalid lines parsed")

        self.assertEqual(parsed.lines[1]['kind'], '#', "Invalid lines parsed")
        self.assertEqual(parsed.lines[1]['line'], 'second second', "Invalid lines parsed")

        self.assertEqual(parsed.lines[2]['kind'], 'C', "Invalid lines parsed")
        self.assertEqual(parsed.lines[2]['line'], 'third', "Invalid lines parsed")

        self.assertEqual(parsed.lines[3]['kind'], '#', "Invalid lines parsed")
        self.assertEqual(parsed.lines[3]['line'], 'fourth', "Invalid lines parsed")

        self.assertEqual(parsed.lines[4]['kind'], 'C', "Invalid lines parsed")
        self.assertEqual(parsed.lines[4]['line'], 'fifth', "Invalid lines parsed")

        self.assertEqual(parsed.lines[5]['kind'], '-', "Invalid lines parsed")
        self.assertEqual(parsed.lines[5]['line'], 'sixth', "Invalid lines parsed")

        self.assertEqual(parsed.lines[6]['kind'], 'C', "Invalid lines parsed")
        self.assertEqual(parsed.lines[6]['line'], 'seventh', "Invalid lines parsed")

    # TODO test merge
        
    def test_uncoverable(self):
        source = '{}/uncoverable.h'.format(Paths.dataPath())
        source = source.replace('\\', '/')
        parsed = UncovarbleFile(source)
        print('from UncovarbleFile: {}'.format(parsed.source))
        for line in parsed.lines:
            print('from UncovarbleFile: {} : {}'.format(line['kind'], line['line']))

        self.assertEqual(parsed.source, source, "Invalid source parsed")
        self.assertEqual(len(parsed.lines), 5, "Invalid lines parsed")

        self.assertEqual(parsed.lines[0]['line'], '#include <iostream>', "Invalid lines parsed")
        self.assertEqual(parsed.lines[1]['line'], 'int main() {', "Invalid lines parsed")
        self.assertEqual(parsed.lines[2]['line'], '  std::cout << "hello" << std::endl;', "Invalid lines parsed")
        self.assertEqual(parsed.lines[3]['line'], '  return 0;', "Invalid lines parsed")
        self.assertEqual(parsed.lines[4]['line'], '}', "Invalid lines parsed")

        for line in parsed.lines:
            self.assertEqual(line['kind'], '-', "Invalid lines parsed")

if __name__ == '__main__':
    unittest.main()
