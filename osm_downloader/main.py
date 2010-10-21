#!/usr/bin/env python 
from optparse import OptionParser
from osm_downloader import Downloader, Region
import os

def main():
    usage = """usage: python osm_downloader.py [options] (-b <left,bottom,right,top>|-c <lat,lng> -r <range in meters>"""
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--step",
                      type="float", dest="step", default=0.04,
                      help="the step size of the tile to download")
    parser.add_option("-o", "--overlap",
                      type="float", dest="overlap", default=0.001,
                      help="the area to overlap to avoid lost nodes")
    parser.add_option("-d", "--dir",
                      dest="dir", default=".",
                      help="download directory", metavar="DIR")
    parser.add_option("-a", "--max_age",
                      type="int", dest="max_age", default=60*60*24*7,
                      help="max age of the file in seconds; default 1 week")
    parser.add_option("-c", "--center",
                      dest="center",
                      help="center point")
    parser.add_option("-b", "--bounds",
                      dest="bounds",
                      help="left,bottom,right,top")
    parser.add_option("-r", "--range",
                      dest="range", default=None, type="int",
                      help="the range in meters")
    
    (opts, args) = parser.parse_args()
    
    if len(args) != 0:
        parser.print_help()
        exit(-1)
        
    d = Downloader(opts.dir, opts.max_age)

    step = opts.step
    region = None
    if opts.range and opts.center:
        lat, lng = map(float, opts.center.split(","))
        r = opts.range * (1 / 111044.736) # meters * ( 1 arc degree / x meters) = arc degrees (at the equator)
        print "Downloading within %f degrees of %f, %f" % (r, lat, lng)
        region = Region((lng-r, lat-r, lng+r, lat+r))

    elif opts.bounds:
        region = Region(map(float, opts.bounds.split(",")))
        
    if not region:
        parser.print_help()
        exit(-1)

    d.download(region, step=step)

    
if __name__=='__main__':
    main()
