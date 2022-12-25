from __future__ import annotations

from PrettyGcov.GcovStat import GCovStat, getFileStat
from PrettyGcov.GcovFile import GcovFile

class CoverageTree:
    def __init__(self, path: list[str]):
        self.path_ = path

        # coverage of the entire folder associated to this node
        self.stat_ = GCovStat()

        # files in the folder represented by this node, map with:
        # <fileName, 
        # {
        #   stat: GcovStat of that specific file 
        #   report: GcovFile of that specific file 
        # }
        # >
        self.files_ = {}

        # sub-folders in the folder represented by this node, map with:
        # <subFolderName, CoverageTree associated to the subfolder>
        self.subFolders_ = {} 
    
    # return [isFile, obj];
    # if isFile=True returns:
    #   {
    #       stat: GcovStat of that specific file 
    #       report: GcovFile of that specific file 
    #   }
    # otherwise returns a CoverageTree
    def getEntry(self, path: list[str]):
        if len(self.path_) > len(path):
            raise Exception('{} is an invalid path'.format(path))
        for index in range(0, len(self.path_)):
            if path[index] != self.path_[index]:
                raise Exception('{} is an invalid path'.format(path))
        
        relativePath = path[len(self.path_):]
        cursor = self
        while True:
            if len(relativePath) == 0:
                return [False, cursor]
            next_slice = relativePath[0] 
            
            if next_slice in cursor.files_:
                if len(relativePath) != 1:
                    raise Exception('{} is an invalid path'.format(path))
                return [True, cursor.files_[next_slice]]

            if not next_slice in cursor.subFolders_:
                raise Exception('{} is an invalid path'.format(path))

            cursor = cursor.subFolders_[next_slice]
            relativePath = relativePath[1:]

    def atSubfolder(self, name: str) -> CoverageTree:
        if not name in self.subFolders_:
            child = CoverageTree(self.path_[:])
            child.path_.append(name)
            self.subFolders_[name] = child
        return self.subFolders_[name]

    def addFile(self, name: str, gcovFile: GcovFile):
        self.files_[name] = {
            'stat':getFileStat(gcovFile),
            'report':gcovFile
        }

    def updateStatRecursive_(self):
        for subfolder, child in self.subFolders_.items():
            child.updateStatRecursive_()
            self.stat_.add(child.stat_)
        for file, info in self.files_.items():
            self.stat_.add(info['stat'])

    def __repr__(self) -> str:
        class Traverser:
            def __init__(self):
                self.stringStream = ''

            def traverse(self, node, leftSpace = None):
                if leftSpace == None:
                    leftSpace = ''
                for subName, subNode in node.subFolders_.items():
                    self.stringStream += '{} {}\n'.format(leftSpace, subName)
                    self.traverse(subNode, leftSpace + ' ')
                for fileName, fileNode in node.files_.items():
                    source = fileNode['report'].source
                    self.stringStream += '{} {} source: {}\n'.format(leftSpace, fileName, source)

        result = '-----------------------------------------\n'
        traverser = Traverser()
        traverser.traverse(self) 
        result += traverser.stringStream
        result += '-----------------------------------------\n'
        return result

def firstInDict(subject):
    front_key = list(subject)[0]
    return subject[front_key]

def slicePath(fileName):
    slices = fileName.split('/')
    if slices[0] == '':
        slices = slices[1:]
    return slices

from PrettyGcov.CoverageMap import CoverageMap

def makeCoverageTree(coverage_map: CoverageMap) -> CoverageTree:
    result = None   
    for fileNameAbs, gcov_file in coverage_map.files_.items():
        slices = slicePath(fileNameAbs)
        if result == None:
            result = CoverageTree([slices[0]])            
        fileName = slices[-1]
        recipient = result
        for slice in slices[1:-1]:
            recipient = recipient.atSubfolder(slice)
        recipient.addFile(fileName, gcov_file)
    # remove common root
    root = result
    while True:
        if len(root.files_) > 0:
            break
        if len(root.subFolders_) != 1:
            break
        root = firstInDict(root.subFolders_)
    result = root
    result.updateStatRecursive_()
    return result
