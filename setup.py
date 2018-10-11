from setuptools import setup

setup(name="checkpatch",
      version='0.1',
      description="Robust checkpatch runner",
      url='http://github.com/tnadav/checkpatch',
      author="Nadav Tenenbaum",
      author_email="tnadav@gmail.com",
      packages=['checkpatch'],
      scripts=['bin/checkdir', 'bin/checkfile'],
      include_package_data=True,
      zip_safe=False)
