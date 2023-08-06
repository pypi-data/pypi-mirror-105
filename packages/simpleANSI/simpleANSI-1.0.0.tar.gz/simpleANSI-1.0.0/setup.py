from setuptools import setup, find_packages

with open('README.md') as READMEFile:
    README = READMEFile.read()
    
with open('HISTORY.md') as HISTORYFile:
    HISTORY = HISTORYFile.read()
    
setup_args = {'name': 'simpleANSI',
              'version': '1.0.0',
              'description': 'A simple wrapper for ANSI escape codes',
              'long_description_content_type': 'text/markdown',
              'long_description': README + '\n\n' + HISTORY,
              'license': 'MIT',
              'packages': find_packages(),
              'author': 'AwesomeCronk',
              'author_email': 'awesomecronk@gmail.com',
              'keywords': ['ANSI'],
              'url': 'https://github.com/AwesomeCronk/simpleANSI',
              'download_url': 'https://pypi.org/project/simpleANSI'
    }

install_requires = ['ctypes']

if __name__ == '__main__':
    setup(**setup_args, install_requires = install_requires)
    