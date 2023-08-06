from setuptools import setup

setup(
    name="hwpkg",
    version="0.0.1",
    description="Honeywell demo package",
    py_modules=["hwpkg"],
    package_dir={'':'src'},
    url='https://github.com/ashokdhudla/honeywell_pkg',
    author='ashokdhudla@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],)