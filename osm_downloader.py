#!/usr/bin/env python

import datetime
import math

## {{{ http://code.activestate.com/recipes/66472/ (r1)
def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    counter = 0
    while 1:
        next_ = start + counter * inc
        if inc > 0 and next_ >= end:
            break
        elif inc < 0 and next_ <= end:
            break
        counter += 1
        yield next_
## end of http://code.activestate.com/recipes/66472/ }}}

class Tile(object):
    def __init__(self, *bounds):
        self.bounds = bounds

    @property
    def url(self):
        return "http://api.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f" % self.bounds

class DownloadRegion(object):
    def __init__(self, bounds, step=0.04, overlap=0.001, name=None):
        self.bounds = bounds
        if not name:
            name = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        self.name = name
        self.step = step
        self.overlap = overlap

    def tiles(self):
        minx = self.step * math.floor( self.left / self.step )
        maxx = self.step * math.ceil( self.right / self.step )
        miny = self.step * math.floor( self.bottom / self.step )
        maxy = self.step * math.ceil( self.top / self.step )

        for x in frange(miny, maxy, self.step):
            for y in frange(minx, maxx, self.step):
                yield Tile(x - self.overlap,
                           y - self.overlap,
                           x + self.overlap + self.step,
                           y + self.overlap + self.step)
        
    @property
    def left(self): return self.bounds[0]

    @property
    def bottom(self): return self.bounds[1]

    @property
    def right(self): return self.bounds[2]

    @property
    def top(self): return self.bounds[3]


if __name__ == '__main__':
    ts = list(DownloadRegion((0,0,0.04,0.04), step=0.01, overlap=0.001).tiles())
    for t in ts:
        print t
    print len(ts)
