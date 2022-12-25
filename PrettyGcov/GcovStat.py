from __future__ import annotations

class GCovStat:
    def __init__(self):        
        self.total_ = 0
        self.covered_ = 0

    def getCoveragePrctg(self) -> float:
        if self.total_ == 0:
            return 1.0
        return 1.0 * self.covered_ / self.total_

    def add(self, o: GCovStat):
        self.covered_ += o.covered_
        self.total_ += o.total_

from PrettyGcov.GcovFile import GcovFile

def getFileStat(gcovFile : GcovFile) -> GCovStat:
    retVal = GCovStat()
    for line in gcovFile.lines:
        if line['kind'] == 'C':
            retVal.covered_ += 1
            retVal.total_ += 1
        if line['kind'] == '#':
            retVal.total_ += 1
    return retVal
