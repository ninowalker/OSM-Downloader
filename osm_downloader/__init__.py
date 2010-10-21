import datetime
import math
from progressbar import ProgressBar
import urllib
import os, stat, time

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

class Region(object):
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

class Downloader(object):
    def __init__(self, dir, max_age=None):
        self.dir = dir
        self.max_age = max_age

    def download(self, region, callback=None):
        tiles = list(region.tiles())
        pbar = ProgressBar(maxval=len(tiles))
        pbar.start()
        for i,tile in enumerate(tiles):
            f = self._download(tile)
            if callback:
                callback(f)
            pbar.update(i+1)
        pbar.finish()
        print "Downloads complete"

    def _download(self, tile):
        filename = os.path.join(self.dir, "%f_%f__%f_%f.osm.xml" % tile.bounds)
        if os.path.exists(filename):
            if not self.max_age:
                return filename
            if os.stat(filename)[stat.ST_MTIME] + self.max_age > time.time():
                return filename
        d = urllib.urlopen(tile.url).read()
        with open(os.path.join(self.dir, filename),"w") as f:
            f.write(d)
        return filename

if __name__ == '__main__':
    d = Downloader("/tmp", 5)
    d.download(Region((0,0,1,1), step=0.2))