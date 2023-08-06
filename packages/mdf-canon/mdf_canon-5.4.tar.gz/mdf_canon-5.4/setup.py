from setuptools import setup, find_packages
import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='mdf_canon',
    version='5.4',
    packages=find_packages(include=['mdf_canon', 'mdf_canon.*']),
    install_requires=['tables','numpy','scipy'],
    
    description="MDF Canon: common library",
    long_description=README,
    author='Daniele Paganelli',
    author_email='dp@mythsmith.it',
    url='https://www.expertlabservice.it/en/software/measurement-development-framework',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)