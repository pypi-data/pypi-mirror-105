from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'JIT Compiler Attacker'
LONG_DESCRIPTION = 'Reverse engineering ML models to steal hidden model parameters using software cache timing attacks'

setup(
    name="jaxed",
    version=VERSION,
    author="Kaustubh Shivdikar",
    author_email="kaustubhcs07@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['jaxed', 'libxsmm', 'cache attack', 'timing attack',
              'flush reload', 'security', 'vulnerability'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ]
)
