from __future__ import annotations

def trimEol(line):
    if line[-1] == '\n':
        return line[:-1]
    return line

def parse_kind(kind):
    if kind[-1] == '#':
        return '#'
    if kind == '-' :
        return kind
    return 'C'

def parse_line(line):
    if(line[0]!=' '):
        return None

    def findSep(line, start_pos):
        result = line.find(':', start_pos)
        if result == -1:
            raise Exception('Found invalid line when parsing gcov file:\n {}'.format(line))
        return result
    first_sep=findSep(line, 0)
    second_sep=findSep(line, first_sep+1)

    kind = parse_kind(line[0:first_sep].lstrip())
    numb = int(line[first_sep+1:second_sep].lstrip())
    content = trimEol(line[second_sep+1:])
    return {
        'kind':kind,
        'line_numb':numb,
        'line_content':content
    }

def fixPathSyntax(subject):
    # Path in Windows are by defualt with \. here we fix it to /    
    return subject.replace('\\', '/')

# for each line:
#   '#' -> not covered
#   'C' -> non covered
#   '-' -> non coverable
class GcovFileBase:
    def __init__(self):
        self.source = None
        self.lines = []

    def __repr__(self) -> str:
        result='Source: {}\n'.format(self.source)
        count=1 
        for line in self.lines:
            result+='{} {} {}\n'.format(line['kind'], count, line['line'])
            count += 1
        return result

def merge_kind(a, b):
    if a == 'C' or b == 'C':
        return 'C'
    if a == '#' or b == '#':
        return '#'
    return '-'  

class GcovFile(GcovFileBase):
    def __init__(self, filename: str):
        super().__init__()
        with open(filename, 'r') as stream:
            for line in stream.readlines():
                content = parse_line(line)

                if(content == None):
                    continue

                if content['line_numb'] == 0:
                    if content['line_content'].find('Source') == 0:
                        source_start = content['line_content'].find(':') + 1 
                        self.source = content['line_content'][source_start:]
                    continue

                index = content['line_numb'] - 1
                if index < len(self.lines):
                    if self.lines[index] == None:
                        self.lines[index] = {'kind':content['kind'], 'line':content['line_content']}
                        continue                    
                    if content['line_content'] != self.lines[index]['line']:
                        raise Exception('Incosistency in gcov file at: '.format(filename))
                    self.lines[index]['kind'] = merge_kind(self.lines[index]['kind'], content['kind'])

                else:
                    while len(self.lines) < index:
                        self.lines.append(None)
                    self.lines.append({'kind':content['kind'], 'line':content['line_content']})

        if self.source == None:
            raise Exception('Source not found in .gcov file')

        for line in self.lines:
            if line == None:
                raise Exception('Invalid gcov file at: '.format(filename))

        self.source = fixPathSyntax(self.source)

    def merge(self, anotherGcovFile: GcovFile):
        if self.source != anotherGcovFile.source:
            raise Exception('Trying to merge {} with {}'.format(self.source, anotherGcovFile.source))
        if len(self.lines) != len(anotherGcovFile.lines):
            raise Exception('Incosistency merging 2 files from {}'.format(self.source))
        for k in range(len(self.lines)):
            o_kind = anotherGcovFile.lines[k]['kind']
            this_kind = self.lines[k]['kind']
            self.lines[k]['kind'] = merge_kind(this_kind, o_kind)

class UncovarbleFile(GcovFileBase):
    def __init__(self, filename: str):
        super().__init__()
        self.source = fixPathSyntax(filename)
        self.lines = []
        with open(filename, 'r') as stream:
            for line in stream.readlines():
                self.lines.append({'kind':'-', 'line':trimEol(line)})
