from setuptools import setup
import os

VERSION = "0.0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="example-pkg-Prac2909",
    description="example-pkg-Prac2909 is now example_pkg_try2",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["example_pkg_try2"],
    classifiers=["Development Status :: 7 - Inactive"],
)
