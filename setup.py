from distutils.core import setup
import luca

description, long_description = luca.__doc__.split('\n', 1)

setup(name='luca',
      version='0.1',
      description=description.strip(),
      long_description=long_description.strip(),
      author='Brandon Rhodes',
      author_email='brandon@rhodesmill.org',
      url='https://github.com/brandon-rhodes/luca',
      classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: BSD License',
        ],
      packages=['luca'],
      )
