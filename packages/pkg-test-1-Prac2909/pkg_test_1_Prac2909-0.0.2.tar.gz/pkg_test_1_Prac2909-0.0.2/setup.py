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
    name="pkg_test_1_Prac2909",
    description="pkg_test_1_Prac2909 is now pkg_test_2_Prac2909",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["pkg_test_2_Prac2909"],
    classifiers=["Development Status :: 7 - Inactive"],
)
