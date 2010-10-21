import unittest
from osm_downloader import Region

class Tester(unittest.TestCase):

    def testGeneratesNum(self):
        self.assertEquals(len(list(Region((0,0,0.04,0.04)).tiles(step=0.01))),
                          16)
        self.assertEquals(len(list(Region((0,0,0.01,0.01)).tiles(step=0.01))),
                          1)
        self.assertEquals(len(list(Region((0,0,0.1,0.01)).tiles(step=0.01))),
                          10)
        self.assertEquals(len(list(Region((-180,-90,180,90)).tiles(1))),
                          360*180)
        

if __name__ == '__main__':
    unittest.main()
