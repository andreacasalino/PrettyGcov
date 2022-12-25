import os

class FileExtensionFilter:
    def __init__(self, ext: str):
        self.extensions = ['.{}'.format(ext)]

    def addExtension(self, ext: str):
        self.extensions.append('.{}'.format(ext))

    def check(self, fileName: str) -> bool:
        fileName_ext = os.path.splitext(fileName)[1]
        for extension in self.extensions:
            if extension == fileName_ext:
                return True
        return  False

def scan(directory: str, filePredicate, fileFilter = lambda path : True, directoryFilter = lambda path : True):
    for fileName in os.listdir(directory):
        filePath = os.path.join(directory, fileName)
        if os.path.isfile(filePath):
            if fileFilter(filePath):
                filePredicate(filePath)
        elif directoryFilter(filePath):
            scan(filePath, filePredicate, fileFilter, directoryFilter)
