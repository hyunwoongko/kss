import codecs
import os
import platform
import subprocess
import sys
from contextlib import suppress
from distutils.extension import Extension

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext

"""
1. pip creates a temporary file, in Linux it's in /tmp, and on Windows it's in the temp dir of the user.
2. pip downloads/extracts the package to that temp directory (whether from a tar.gz or from an online source or from a repository)
3. pip runs the following operations in order:
  - setup.py install
  - setup.py build
  - setup.py install_lib
  - setup.py build_py
    -> install mecab / Cython
  - setup.py build_ext
    -> build Cython extension if possible
"""


class PreInstall(build_ext):
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


def cythonize():
    if platform.system() == 'Linux':
        extra_compile_args = ['-std=c++11']
        extra_link_args = []
    elif platform.system() == 'Darwin':
        extra_compile_args = ['-std=c++11', '-stdlib=libc++']
        extra_link_args = ['-stdlib=libc++']
    elif platform.system() == 'Windows':
        extra_compile_args = ['/utf-8']
        extra_link_args = []
    else:
        return None

    _ext_modules = [
        Extension(
            "kss_cython",
            sources=[
                'csrc/kss_cython.pyx',
                'csrc/sentence_splitter.cpp',
            ],
            language='c++',
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            include_dirs=["."],
        )
    ]

    try:
        from Cython.Build import cythonize

        return cythonize(_ext_modules, language_level="3")

    except:
        with suppress():
            subprocess.call(
                [sys.executable, "-m", "pip", "install", "Cython"],
                stderr=subprocess.DEVNULL,
            )

            try:
                from Cython.Build import cythonize

                return cythonize(_ext_modules, language_level="3")
            except:
                return None



def read_file(filename, cb):
    with codecs.open(filename, "r", "utf8") as f:
        return cb(f)


version = None
with open(os.path.join("kss", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("__version__"):
            version = line.split("=")[1].strip().replace('"', "").replace("'", "")

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
    install_requires=["emoji==1.2.0", "regex", "pecab", "networkx"],
    long_description=long_description,
    packages=find_packages(exclude=["bench", "assets", ".java", ".pytest_cache"]),
    python_requires=">=3",
    zip_safe=False,
    package_data={"": ["csrc/*"]},
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
    cmdclass={"build_ext": PreInstall},
    ext_modules=cythonize(),
)
