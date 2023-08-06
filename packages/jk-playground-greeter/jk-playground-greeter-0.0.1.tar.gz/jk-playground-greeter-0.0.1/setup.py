from setuptools import setup, find_packages  # noqa: H301

NAME = "jk-playground-greeter"
VERSION = "0.0.1"

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programing Language :: Python :: 3'
]

setup(
    name=NAME,
    version=VERSION,
    description="Playground project for testing package publishing process",
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author="Josip Klaric",
    author_email="josipklaric@gmail.com",
    url="https://github.com/josipklaric/python-greeter-module",
    keywords=["playground", "module", "test"],
    python_requires=">=3.6",
    install_requires=[''],
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True
)