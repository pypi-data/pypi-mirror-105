import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'oopschool1235',      
  packages = ['oopschool'], 
  version = '0.0.5',  
  license='MIT', 
  description = 'oopschool',
  long_description=DESCRIPTION,
  author = 'Ryu',                 
  author_email = 'chanpawit1810@gmail.com',     
  url = 'https://github.com/Chanpawit/OOPschool',
  download_url = 'https://github.com/Chanpawit/OOPschool',
  keywords = ['OOP', 'School'],   
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Education',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)