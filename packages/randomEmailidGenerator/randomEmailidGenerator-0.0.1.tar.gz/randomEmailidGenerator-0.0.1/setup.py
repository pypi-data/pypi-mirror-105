from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='randomEmailidGenerator',
  version='0.0.1',
  description='A very basic random email id generator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Pranay Bankar',
  author_email='pranaybankar2890@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='email generator', 
  packages=find_packages(),
  install_requires=[''] 
)