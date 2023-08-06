import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("VERSION", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="PyLo",
    version=version,
    author="miile7",
    author_email="miile7@gmx.de",
    description=("A python program to record image series with Lorentz-TEM."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miile7/pylo-project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    python_requires='>=3.5',
)