import unittest
from osm_downloader import DownloadRegion

class Tester(unittest.TestCase):

    def testGeneratesNum(self):
        self.assertEquals(len(list(DownloadRegion((0,0,0.04,0.04), step=0.01).tiles())),
                          16)
        self.assertEquals(len(list(DownloadRegion((0,0,0.01,0.01), step=0.01).tiles())),
                          1)
        self.assertEquals(len(list(DownloadRegion((0,0,0.1,0.01), step=0.01).tiles())),
                          10)
        self.assertEquals(len(list(DownloadRegion((-180,-90,180,90), step=1).tiles())),
                          360*180)
        

if __name__ == '__main__':
    unittest.main()
