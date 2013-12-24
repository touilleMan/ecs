import os
import sys

from setuptools import setup, find_packages

sys.path.append('.')
from ecs import metadata


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


# See here for more options:
# <http://pythonhosted.org/setuptools/setuptools.html>
setup_dict = dict(
    name=metadata.package,
    version=metadata.version,
    author=metadata.authors[0],
    author_email=metadata.emails[0],
    maintainer=metadata.authors[0],
    maintainer_email=metadata.emails[0],
    url=metadata.url,
    description=metadata.description,
    long_description=read('README.md'),
    download_url=metadata.url,
    # Find a list of classifiers here:
    # <http://pypi.python.org/pypi?%3Aaction=list_classifiers>
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    packages=find_packages(),
    install_requires=[],
    zip_safe=False,  # don't use eggs
)


def main():
    setup(**setup_dict)


if __name__ == '__main__':
    main()
