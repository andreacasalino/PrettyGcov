import os

def makeAbs(subject):
    return os.path.abspath(subject)

TESTS_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
TESTS_ROOT_PATH = makeAbs(TESTS_ROOT_PATH)
print('TESTS_ROOT_PATH: {}'.format(TESTS_ROOT_PATH))

class Paths:
    def root():
        return makeAbs(os.path.join(TESTS_ROOT_PATH, '..'))

    def testsRoot():
        return TESTS_ROOT_PATH

    def dataPath():
        return makeAbs(os.path.join(TESTS_ROOT_PATH, 'data'))

def forceUnix(fileName):
    return fileName.replace('\\', '/')
