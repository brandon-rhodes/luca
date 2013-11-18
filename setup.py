from setuptools import setup, find_packages
import luca

description, long_description = luca.__doc__.split('\n', 1)

setup(name='luca',
      version='1.0',
      description=description.strip(),
      long_description=long_description.strip(),
      author='Brandon Rhodes',
      author_email='brandon@rhodesmill.org',
      url='https://github.com/brandon-rhodes/luca',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Office/Business',
          'Topic :: Office/Business :: Financial',
          'Topic :: Office/Business :: Financial :: Accounting',
          ],
      packages=find_packages(),
      install_requires=[
        'blessings',
        'docopt',
        'fdfgen',
        'pyyaml',
        'reportlab',
        'requests',
        'pyPdf',
        ],
      entry_points={'console_scripts': [
            'luca = luca.commandline:main',
            ]}
      )
