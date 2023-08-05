import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "nqdb",
    version = "0.1.0",
    url = 'https://bitbucket.org/luca_de_alfaro/nqdb',
    license = 'BSD',
    author = 'Luca de Alfaro',
    author_email = 'dealfaro@alumni.stanford.edu',
    maintainer = 'Luca de Alfaro',
    maintainer_email = 'dealfaro@alumni.stanford.edu',
    description = 'Interface to Google Datastore, mimicking aspects of ndb, but allowing for different backends and caching',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = ['nqdb'],
    install_requires = [
        "functools",
        "google.cloud.datastore",
        "uuid",
        "contextlib",
        "json",
        "numbers",
        "datetime",
        "pytz",
        "zlib",
        "base64",
    ],
    include_package_data = True,
    zip_safe = False,
    platforms = 'any',
    python_requires=">=3.7",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
