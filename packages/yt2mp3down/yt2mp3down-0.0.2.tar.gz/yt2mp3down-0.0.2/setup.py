  
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='yt2mp3down',
  version='0.0.2',
  description='Download Youtube videos as mp3',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Hasinthaka Piyumal',
  author_email='hasinthakapiyumal@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='yt2mp3', 
  packages=find_packages(),
  install_requires=[''] 
)