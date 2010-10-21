from setuptools import setup

setup(name = "osm_downloader",
      version = "0.0.1",
      install_requires = ['progressbar'],
      description = "A set of tools for downloading OSM files via the API.",
      author = "Nino Walker",
      author_email = "nino.walker@gmail.com",
      url = "http://www.github.com/ninowalker/osm-donwloader",
      packages = ['osm_downloader'],
      long_description = """A dirt simple utility for downloading OSM data.""",
      license = "MIT License.",
      entry_points = {
          'console_scripts': [
              'osm_download = osm_downloader.main:main',
          ],
        }
      )
