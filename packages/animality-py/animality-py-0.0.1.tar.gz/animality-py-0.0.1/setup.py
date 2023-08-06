from setuptools import setup
setup(
  name = 'animality-py',
  packages = ['animality'],
  version = '0.0.1',
  license='MIT',
  description = 'A python API wrapper for https://animal-api.nitcord.repl.co/api',
  long_description = open('README.md', 'r', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  author = 'vierofernando',
  author_email = 'vierofernando9@gmail.com',
  url = 'https://github.com/animal-api/animality-py',
  download_url = 'https://github.com/animal-api/animality-py/archive/0.0.1.tar.gz',
  keywords = ['Animals', 'API', 'Hamburger', 'Pats', 'Headpats', 'API Wrapper'],
  install_requires=[
    'aiohttp'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
  python_requires='>=3.7'
)
