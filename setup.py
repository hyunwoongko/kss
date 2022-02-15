import codecs
from setuptools import setup, find_packages

required = [
    "emoji",
    "regex",
]


def read_file(filename, cb):
    with codecs.open(filename, "r", "utf8") as f:
        return cb(f)


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kss",
    version="3.4",
    author="Hyunwoong Ko",
    author_email="kevin.ko@tunib.ai",
    url="https://github.com/hyunwoongko/kss",
    license='BSD 3-Clause "New" or "Revised" License',
    description="A Toolkit for Korean sentence segmentation",
    long_description_content_type="text/markdown",
    platforms=["any"],
    install_requires=required,
    long_description=long_description,
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3",
    zip_safe=False,
    package_data={"": ["kss/pynori/resources/*"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
