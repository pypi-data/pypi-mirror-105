from distutils.core import setup
setup(
name='npytools',
version='1.1',
author='Nasir Ali',
author_email='nasiralis1731@gmail.com',
author_url='https://facebook.com/nasir.xo',
packages=['npytools'],
scripts=['bin/nbot'],
install_requires=[
'bs4',
'requests',
'sympy',
'faker',
'wikipedia',
'bing-image-downloader',
'googletrans',
'python-aiml',
'PyDictionary',
'pycricbuzz',
 ],
)
