from __future__ import annotations

def parse_slice(line, start_pos):
    terminator_pos = line.find(':', start_pos)
    result =  line[start_pos:terminator_pos]
    result = result.lstrip()
    return result, terminator_pos + 1

def parse_kind(kind):
    if kind[-1] == '#':
        return '#'
    if kind == '-' :
        return kind
    return 'C'

def trimEol(line):
    if line[-1] == '\n':
        return line[:-1]
    return line

def parse_line(line):
    kind, cursor = parse_slice(line, 0)
    line_numb, cursor = parse_slice(line, cursor)
    line_content = line[cursor:]
    return {'kind':parse_kind(kind), 'line_numb':line_numb, 'line_content':trimEol(line_content)}

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
        count=0 
        for line in self.lines:
            result+='{} {} {}\n'.format(line['kind'], count, line['line'])
            count += 1
        return result

class GcovFile(GcovFileBase):
    def __init__(self, filename: str):
        super().__init__()
        with open(filename, 'r') as stream:
            for line in stream.readlines():
                content = parse_line(line)
                if content['line_numb'] == '0':
                    if content['line_content'].find('Source') == 0:
                        source_start = content['line_content'].find(':') + 1 
                        self.source = content['line_content'][source_start:]
                    continue

                self.lines.append({'kind':content['kind'], 'line':content['line_content']})
        if self.source == None:
            raise Exception('Source not found in .gcov file')
        self.source = fixPathSyntax(self.source)

    def merge(self, anotherGcovFile: GcovFile):
        if self.source != anotherGcovFile.source:
            raise Exception('Trying to merge {} with {}'.format(self.source, anotherGcovFile.source))
        if len(self.lines) != len(anotherGcovFile.lines):
            raise Exception('Incosistency merging 2 files from {}'.format(self.source))
        for k in range(len(self.lines)):
            o_kind = anotherGcovFile.lines[k]['kind']
            if o_kind == 'C':
                self.lines[k]['kind'] = 'C'        

class UncovarbleFile(GcovFileBase):
    def __init__(self, filename: str):
        super().__init__()
        self.source = fixPathSyntax(filename)
        self.lines = []
        with open(filename, 'r') as stream:
            for line in stream.readlines():
                self.lines.append({'kind':'-', 'line':trimEol(line)})
