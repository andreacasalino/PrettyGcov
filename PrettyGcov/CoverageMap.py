import subprocess, sys, os
from PrettyGcov.Scanner import *
from PrettyGcov.GcovFile import GcovFile, UncovarbleFile

def run_gcov(fileName: str):
    cmd = ['gcov', fileName]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        outs, errs = proc.communicate()
        if proc.returncode != 0:
            raise Exception('Something went wrong running gcov: check you have gcov properly installed on your system')

class CoverageMap:
    def __init__(self, root_dir_gcda_files: str):
        self.files_ = {}
        self.root = root_dir_gcda_files
        self.sourcePaths = []
        self.verbosity_ = False

    def verbosity(self):
        self.verbosity_ = True

    def addSourceDirectory(self, directory: str):
        abs_path = os.path.abspath(directory)
        self.sourcePaths.append(abs_path)

    def isSource_(self, fileName: str) -> bool:
        for dir in self.sourcePaths:
            if fileName.find(dir) == 0:
                return True
        return False

    def parse_(self, fileName: str):
        verb = self.verbosity_
        if verb:
            print('calling gcov on {} to generate .gocv files'.format(fileName))
        run_gcov(fileName)

        # iterate all .gcov files that were generated
        def process_gcov_file(gcovFileName):
            parsed = GcovFile(gcovFileName)
            isSource = self.isSource_(parsed.source)
            if verb and isSource:
                print('Collecting results for {}'.format(parsed.source))
            if not isSource:
                return

            if parsed.source in self.files_:
                self.files_[parsed.source].merge(parsed)
            else:
                self.files_[parsed.source] = parsed

        extension_filter = FileExtensionFilter('gcov')
        scan('./', process_gcov_file, fileFilter = extension_filter.check)
        scan('./', lambda gcovFileName : os.remove(gcovFileName), fileFilter = extension_filter.check)

    def addUncoverables_(self):
        filter = FileExtensionFilter('h')
        filter.addExtension('c')
        filter.addExtension('hpp')
        filter.addExtension('cpp')
        for dir in self.sourcePaths:
            def process(fileName):
                path = fileName.replace('\\', '/')
                if not path in self.files_:
                    parsed = UncovarbleFile(path)
                    self.files_[parsed.source] = parsed
            scan(dir, process, fileFilter = filter.check)

    def generate(self):
        print('computing coverage map ...')
        extension_filter = FileExtensionFilter('gcda')
        scan(self.root, self.parse_, fileFilter = extension_filter.check)
        self.addUncoverables_()
        print('coverage map computed')

    def __repr__(self) -> str:
        result=''
        for file, gcovFile in self.files_.items():
            result += '-----------------------------------------\n'
            result += str(gcovFile)
        return result
