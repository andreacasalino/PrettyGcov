###################################################################################
###                                  ASSETS                                     ###
###################################################################################

ElementStats_HTML="""
<div>
    <!-- file name info -->
    <div class="column" style="width: 40%;"> {ELEMENT} </div>

    <!-- coverge info -->
    <div class="column" style="width: 55%;"> 
        <div class="column" style="width: 50px; background-color:rgb({RED}, {GREEN},0);">{PRCTG_COVERED}%</div>
        <div class="column" style="width: 80%; margin-left: 10px;">
            <div class="column covered" style="width: {PRCTG_COVERED}%;">{LINES_COVERED}</div>
            <div class="column uncovered" style="width: {PRCTG_UNCOVERED}%;">{LINES_UNCOVERED}</div>
        </div>
    </div>
</div>
<br>
<br>
"""

File_HTML="""
<head>
{STYLE}
</head>
<body>

{NAVIGATION}
    <br>
    <br>

{FILE_STATS}

{LINES}
</body>
"""

FileLine_HTML="""<p class="noSpace {CLASS}">{LINE}:   {CONTENT}</p>"""

Folder_HTML="""
<head>
{STYLE}
</head>
<body>
    
{NAVIGATION}
    <br>
    <br>

{FOLDER_STATS}

    <p> Folder content: </p>

{LINES}
    
</body>
"""

Link_HTML="""<a class="cliccable" style="color: white;" href="{URL}">{DESC}</a>"""

Style_HTML="""
<style>
    body {
        background-color: black;
        color: white;
    }

    .noSpace {margin:0;padding:0;}
    .column {float: left;}
    .covered {background-color: green}
    .uncovered {background-color: red}
    
    .cliccable {
        cursor: pointer;
        opacity: 1.0;
        filter: alpha(opacity=100);
    }
    .cliccable:hover {
        cursor: pointer;
        opacity: 0.5;
        filter: alpha(opacity=50);
    }
</style>
"""

PAGES = {
    'ElementStats':ElementStats_HTML,
    'File':File_HTML,
    'FileLine':FileLine_HTML,
    'Folder':Folder_HTML,
    'Link':Link_HTML,
    'Style':Style_HTML
}

###################################################################################

def importPage(name: str) -> str:
    return PAGES[name]

def replaceWithNumb(subject: str, toFind: str, val: any) -> str:
    return subject.replace(toFind, str(val))

from PrettyGcov.GcovStat import GCovStat

def makeElementStats(elementInfo: str, coverage: GCovStat) -> str:
    result = importPage('ElementStats')
    result = result.replace('{ELEMENT}', elementInfo)
    prctg_cov = coverage.getCoveragePrctg()

    result = replaceWithNumb(result, '{PRCTG_COVERED}', round(prctg_cov * 100, 2))
    result = replaceWithNumb(result, '{PRCTG_UNCOVERED}', round((1.0 - prctg_cov) * 100, 2))
    result = replaceWithNumb(result, '{LINES_COVERED}', coverage.covered_)
    result = replaceWithNumb(result, '{LINES_UNCOVERED}', coverage.total_ - coverage.covered_)

    red_val = round(255 * (1.0 - prctg_cov), 0)
    result = replaceWithNumb(result, '{RED}', red_val)
    green_val = round(255 * prctg_cov, 0)
    result = replaceWithNumb(result, '{GREEN}', green_val)
    return result

def makeLink(url: str, desc: str) -> str:
    result = importPage('Link')
    result = result.replace('{URL}', url)
    result = result.replace('{DESC}', desc)
    return result

from PrettyGcov.CoverageTree import CoverageTree
from PrettyGcov.GcovFile import GcovFile

class PageFactory:
    def __init__(self, port: int, coverage_tree: CoverageTree):
        self.coverageTree_ = coverage_tree
        self.port_ = port

    def makePage(self, path: list[str]) -> str:
        isFile, info = self.coverageTree_.getEntry(path)
        if isFile:
            return self.makeFilePage_(info['report'] , info['stat'])
        return self.makeFolderPage_(info)

    def makeUrl_(self, path: list[str]) -> str:
        params = ''
        for slice in path:
            params += '&{}={}'.format('slice', slice)
        params = params[1:]
        return 'http://localhost:{}/element?{}'.format(self.port_, params)

    def makeFilePage_(self, gcovFile: GcovFile, gcovStat: GCovStat) -> str:
        result = importPage('File')
        result = result.replace('{STYLE}', importPage('Style'))

        result = result.replace('{NAVIGATION}', makeLink(self.makeUrl_(self.coverageTree_.path_), 'back to root'))

        stats = makeElementStats(gcovFile.source, gcovStat)
        result = result.replace('{FILE_STATS}', stats)

        lines = ''
        newLineTemplate = importPage('FileLine')
        linesCount = 1
        for line in gcovFile.lines:
            cls = ''
            if line['kind'] == 'C':
                cls = 'covered'
            elif line['kind'] == '#':
                cls = 'uncovered'
            newLine = newLineTemplate.replace('{CLASS}', cls)
            newLine = replaceWithNumb(newLine, '{LINE}', linesCount)
            newLine = replaceWithNumb(newLine, '{CONTENT}', line['line'])
            linesCount += 1
            lines += '\n'
            lines += newLine
        result = result.replace('{LINES}', lines)
        return result

    def makeFolderPage_(self, subTree: CoverageTree) -> str:
        result = importPage('Folder')
        result = result.replace('{STYLE}', importPage('Style'))

        navigation_links = makeLink(self.makeUrl_(self.coverageTree_.path_), 'back to root')
        if subTree.path_ != self.coverageTree_.path_:
            navigation_links += '<br>\n'
            navigation_links += makeLink(self.makeUrl_(subTree.path_[:-1]), 'go up')
        result = result.replace('{NAVIGATION}', navigation_links)

        stats = makeElementStats(subTree.path_[-1], subTree.stat_)
        result = result.replace('{FOLDER_STATS}', stats)

        lines = ''
        # sub folders
        for fileName, subFolderTree in subTree.subFolders_.items():
            fileStat = subFolderTree.stat_
            filePath = subFolderTree.path_
            link = makeLink(self.makeUrl_(filePath), '{}/'.format(fileName))
            lines += makeElementStats(link, fileStat)
        # files
        for fileName, info in subTree.files_.items():
            fileStat = info['stat']
            filePath = []
            for slice in subTree.path_:
                filePath.append(slice)
            filePath.append(fileName)
            link = makeLink(self.makeUrl_(filePath), fileName)
            lines += makeElementStats(link, fileStat)
        result = result.replace('{LINES}', lines)
        return result
