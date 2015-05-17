import os

from setuptools import setup, find_packages

# here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, 'README.txt')) as f:
#    README = f.read()
# with open(os.path.join(here, 'CHANGES.txt')) as f:
#    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'enum',
    ]

setup(name='HorseLife',
      version='0.0',
      description='HorseLife',
      long_description='Better description to come.',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid horses game horselife',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='HorseLife',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = interface.web:main
      [console_scripts]
      initialize_testpyramid_db = testpyramid.scripts.initializedb:main
      """,
      )
