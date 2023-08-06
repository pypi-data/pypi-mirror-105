from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.2"
DESCRIPTION = 'Python code Encryption and Decryption use algorithms'
LONG_DESCRIPTION = 'KRISHTO'

# Setting up
setup(
    name="krishto",
    version=VERSION,
    author="K.A.ISHAN OSHADA",
    author_email="<ic31908@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['krishto.Encryption_methods','krishto.Encryption_methods().E2D_1','etc..'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
