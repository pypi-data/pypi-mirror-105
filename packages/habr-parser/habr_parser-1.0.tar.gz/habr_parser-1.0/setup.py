from distutils.core import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='habr_parser',
    packages=['habr_parser'],
    version='1.0',
    license='gpl-3.0',
    description='Parser for habr.com',
    author='goonate',
    author_email='goonate@cock.li',
    url='https://gitlab.com/goonate/habr_parser',
    download_url='https://gitlab.com/goonate/habr-parser/-/archive/v1.0/habr-parser-v1.0.tar.gz',
    keywords=['habr_parser', 'habr', 'parser'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6'
)
