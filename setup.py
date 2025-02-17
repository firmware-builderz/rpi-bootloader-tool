#!/usr/bin/python3
import codecs
from setuptools import setup, find_packages

RPITOOL_VERSION = "0.0.1"
RPITOOL_DOWNLOAD = ('https://github.com/websploit/websploit/tarball/' + RPITOOL_VERSION)


def read_file(filename):
	"""
	Read a utf8 encoded text file and return its contents.
	"""
	with codecs.open(filename, 'r', 'utf8') as f:
		return f.read()

def read_requirements():
    with open('requirements.txt') as f: 
        return f.readlines() 


setup(
	name='rpitool',
	packages=[
		'rpitool',
		'rpitool.modules',
		'rpitool.utils'],
	package_data={
          'rpitool': [
              'utils/*',
          ],
      },

	version=RPITOOL_VERSION,
	description='RPI TOOL is a high level MITM framework',
	long_description=read_file('README.md'),
	long_description_content_type='text/markdown',
    # packages = find_packages(),
    entry_points ={ 
            'console_scripts': [ 
                'rpitool = rpitool.rpitool:loop'
            ] 
        },

	license='MIT',
	author='Fardin Allahverdinazhand',
	author_email='0x0ptim0us@gmail.com',
	url='https://github.com/websploit/websploit',
	download_url=RPITOOL_DOWNLOAD,
	keywords=['python3', 'rpitool', 'MITM'],
	classifiers=[
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Natural Language :: English',
	],

	install_requires= read_requirements(),

)