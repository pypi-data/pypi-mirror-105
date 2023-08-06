from distutils.core import setup


setup(
    name='habr_parser',
    packages=['habr_parser'],
    version='1.5',
    license='gpl-3.0',
    description='Parser for habr.com',
    author='goonate',
    author_email='goonate@cock.li',
    url='https://gitlab.com/goonate/habr-parser',
    download_url='https://gitlab.com/goonate/habr-parser/-/archive/v1.5/habr-parser-v1.5.tar.gz',
    keywords=['habr_parser', 'habr', 'parser'],
    install_requires=[
        'BeautifulSoup4',
        'aiohttp',
        'asyncio',
        'requests',
        'lxml',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6'
)
