
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "nqlog",
    version = "0.1.0",
    url = 'https://bitbucket.org/luca_de_alfaro/nqlog/src/master/',
    license = 'BSD',
    author = 'Luca de Alfaro',
    author_email = 'luca@dealfaro.com',
    maintainer = 'Luca de Alfaro',
    maintainer_email = 'luca@dealfaro.com',
    description = 'Interface to Google Cloud Logging that enables aggregated operation logs',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = ['nqlog'],
    install_requires = [
        "datetime",
        "logging",
        "os",
        "uuid",
        "threading",
        "traceback",
        "google.cloud.logging",
    ],
    include_package_data = True,
    zip_safe = False,
    platforms = 'any',
    python_requires=">=3.7",
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
