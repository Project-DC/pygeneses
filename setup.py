import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyevolution",
    version="0.1.0",
    description="PyTorch based framework for training artificial agents in bio-inspired environments",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Project-DC/pyevolve",
    author="Siddhartha Dhar Choudhury",
    author_email="sdharchou@gmail.com",
    license="GNU General Public License v3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
    ],
    packages=[package for package in find_packages()],
    package_data={'pyevolution': [
        'envs/prima_vita/images/*.png'
    ]},
    install_requires=["pygame", "numpy", "torch"],
)
