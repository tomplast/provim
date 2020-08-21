from setuptools import setup

setup(name='provim',
      version='0.1.0',
      description='PROVIM is a profile manager for VIM',
      url='',
      author='Tomas "tomplast" Gustavsson',
      author_email='tomplast@gmail.com',
      license='',
      packages=['provim'],
      entry_points = {
          'console_scripts': [
              'provim=provim.provim:main',                  
          ],              
      },
      zip_safe=False)
