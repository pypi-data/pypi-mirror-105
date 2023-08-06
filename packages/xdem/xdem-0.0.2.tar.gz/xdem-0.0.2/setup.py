from os import path

from setuptools import setup
from setuptools.command.install import install
import subprocess
import sys

FULLVERSION = '0.0.2'
VERSION = FULLVERSION

class PostInstall(install):

    pkgs = "git+https://github.com/GlacioHack/GeoUtils.git"


    def run(self):
        install.run(self)

        print(subprocess.getoutput(f"{sys.executable} -m pip install --force-reinstall {self.pkgs}"))



setup(name='xdem',
      version=FULLVERSION,
      description='Set of tools to manipulate Digital Elevation Models (DEMs) ',
      url='https://github.com/GlacioHack/xdem',
      author='The GlacioHack Team',
      author_email="john@doe.com",
      license='BSD-3',
      packages=['xdem'],
      install_requires=['numpy', 'scipy', 'rasterio', 'geopandas',
          'pyproj', 'tqdm','scikit-gstat', 'scikit-image'],
      extras_require={'rioxarray': ['rioxarray'], 'richdem': ['richdem'], 'pdal': [
          'pdal'], 'opencv': ['opencv'], "pytransform3d": ["pytransform3d"]},
      scripts=[],
      cmdclass={"install": PostInstall},
      zip_safe=False)

write_version = True


def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'
"""
    if not filename:
        filename = path.join(path.dirname(__file__), 'xdem',
                             'version.py')

    a = open(filename, 'w')
    try:
        a.write(cnt % (FULLVERSION, VERSION))
    finally:
        a.close()


if write_version:
    write_version_py()
