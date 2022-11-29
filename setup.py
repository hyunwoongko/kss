import codecs
import os
import subprocess
import sys
from contextlib import suppress

from setuptools import setup, find_packages
from setuptools.command.install import install

required = [
    "emoji==1.2.0",
    "regex",
    "more_itertools",
]


class InstallCommand(install):
    def run(self):
        try:
            import mecab
        except:
            with suppress():
                subprocess.call(
                    [sys.executable, "-m", "pip", "install", "python-mecab-kor"],
                    stderr=subprocess.DEVNULL,
                )

        super().run()


def read_file(filename, cb):
    with codecs.open(filename, "r", "utf8") as f:
        return cb(f)


version = None
with open(os.path.join('kss', '__init__.py'), encoding='utf-8') as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kss",
    version=version,
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
    cmdclass={"install": InstallCommand},
)
