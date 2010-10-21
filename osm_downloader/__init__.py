import datetime
import math
from progressbar import ProgressBar
import urllib
import os, stat, time
import threading

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
        #print "http://api.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f" % self.bounds
        return "http://api.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f" % self.bounds

class Region(object):
    def __init__(self, bounds):
        self.bounds = bounds

    def tiles(self, step=0.04, overlap=0.001):
        minx = step * math.floor( self.left / step )
        maxx = step * math.ceil( self.right / step )
        miny = step * math.floor( self.bottom / step )
        maxy = step * math.ceil( self.top / step )

        for y in frange(miny, maxy, step):
            for x in frange(minx, maxx, step):
                yield Tile(x - overlap,
                           y - overlap,
                           x + overlap + step,
                           y + overlap + step)
        
    @property
    def left(self): return self.bounds[0]

    @property
    def bottom(self): return self.bounds[1]

    @property
    def right(self): return self.bounds[2]

    @property
    def top(self): return self.bounds[3]

class Downloader(object):
    def __init__(self, dir, max_age=None, prefix="osm"):
        self.dir = dir
        self.max_age = max_age
        self.prefix = prefix

    def download(self, region, step=0.04, overlap=0.001, callback=None, threaded=False):
        threads = set([])
        tiles = list(region.tiles(step=step, overlap=overlap))
        print "Downloading %f,%f to %f,%f (%d tiles)..." % (region.bottom, region.left, region.top, region.right, len(tiles))
        pbar = ProgressBar(maxval=len(tiles))
        pbar.start()
        for i,tile in enumerate(tiles):
            is_new, f = self._download(tile)
            if callback:
                if threaded:
                    print "Starting callback thread..."
                    t = threading.Thread(target=callback, args=(is_new, f))
                    t.daemon = False
                    t.start()
                    threads.add(t)
                else:
                    callback(is_new, f)
            pbar.update(i+1)
        pbar.finish()
        print "Downloads complete"
        if not len(threads):
            return
        
        pbar = ProgressBar(maxval=len(threads))
        pbar.start()
        print "Waiting for %d threads to complete" % len(threads)
        i = 0
        while (len(threads)):
            t = threads.pop()
            t.join()
            pbar.update(i)
            i += 1
        pbar.finish()

    def _download(self, tile):
        filename = os.path.join(self.dir, (self.prefix + "_%f_%f__%f_%f.osm.xml") % tile.bounds)
        if os.path.exists(filename):
            if not self.max_age:
                return False, filename
            if os.stat(filename)[stat.ST_MTIME] + self.max_age > time.time():
                return False, filename
        d = urllib.urlopen(tile.url).read()
        with open(filename, "w") as f:
            f.write(d)
        return True, filename

if __name__ == '__main__':
    d = Downloader("/tmp", 5)
    d.download(Region((0,0,1,1), step=0.2))
