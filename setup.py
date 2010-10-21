from distutils.core import setup

setup(name = "osm_donwloader",
      version = "0.0.1",
      description = "A set of tools for downloading OSM files via the API.",
      author = "Nino Walker",
      author_email = "nino.walker@gmail.com",
      url = "http://www.github.com/ninowalker/osm-donwloader",
      packages = ['osm_downloader'],
      scripts = ['osm_download.py'],
      long_description = """A dirt simple utility for downloading OSM data.""",
      license = "MIT License."
      )
