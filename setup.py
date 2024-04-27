import codecs
import os
import platform
import subprocess
import sys
from contextlib import suppress
from distutils.ccompiler import new_compiler
from distutils.extension import Extension
from distutils.sysconfig import customize_compiler

from setuptools import setup, find_packages
from setuptools.command.install import install

"""
How pip install works:

1. pip creates a temporary file, in Linux it"s in /tmp, and on Windows it"s in the temp dir of the user.
2. pip downloads/extracts the package to that temp directory (whether from a tar.gz or from an online source or from a repository)
3. pip runs the following operations in order:
  - setup.py install
  - setup.py build
  - setup.py install_lib
  - setup.py build_py
  - setup.py build_ext
"""


class PreInstall(install):
    def run(self):
        try:
            # 1. Try to import mecab
            import mecab
        except:
            try:
                # 2. Try to install python-mecab-kor and import mecab again
                with suppress():
                    subprocess.call(
                        [sys.executable, "-m", "pip", "install", "python-mecab-kor"],
                        stderr=subprocess.DEVNULL,
                    )

                import mecab
            except:
                try:
                    # 3. Try to install python-mecab-ko and import mecab again
                    with suppress():
                        inst = "curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash > /dev/null 2>&1"
                        os.system(inst)
                        subprocess.call(
                            [sys.executable, "-m", "pip", "install", "python-mecab-ko"],
                            stderr=subprocess.DEVNULL,
                        )
                    import mecab
                except:
                    # 4. Cannot install mecab.
                    pass

        super().run()


def get_extra_compile_args():
    if platform.system() == "Linux":
        extra_compile_args = ["-std=c++11"]
        extra_link_args = []
    elif platform.system() == "Darwin":
        extra_compile_args = ["-std=c++11", "-stdlib=libc++"]
        extra_link_args = ["-stdlib=libc++"]
    elif platform.system() == "Windows":
        extra_compile_args = ["/utf-8"]
        extra_link_args = []
    else:
        extra_compile_args = []
        extra_link_args = []
    return extra_compile_args, extra_link_args


def cythonize():
    extra_compile_args, extra_link_args = \
        get_extra_compile_args()

    _ext_modules = [
        Extension(
            "kss_cython",
            sources=[
                "csrc/kss_cython.pyx",
                "csrc/sentence_splitter.cpp",
            ],
            language="c++",
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            include_dirs=["."],
        )
    ]

    try:
        # 1. Try to import Cython and cythonize
        from Cython.Build import cythonize
        return cythonize(_ext_modules, language_level="3")
    except:
        try:
            # 2. Try to install Cython and import Cython and cythonize again
            with suppress():
                subprocess.call(
                    [sys.executable, "-m", "pip", "install", "Cython"],
                    stderr=subprocess.DEVNULL,
                )

            from Cython.Build import cythonize
            return cythonize(_ext_modules, language_level="3")
        except:
            # 3. Cannot install Cython.
            return None


def is_compilable():
    try:
        # 1. Try to compile csrc/sentence_splitter.cpp
        extra_compile_args, extra_link_args = get_extra_compile_args()
        compiler = new_compiler()
        customize_compiler(compiler)
        compiler.compile(["csrc/sentence_splitter.cpp"], extra_postargs=extra_compile_args)
        return True
    except:
        # 2. Cannot compile csrc/sentence_splitter.cpp
        return False


def cythonize_if_possible():
    cythonized_result = cythonize()

    if cythonized_result and is_compilable():
        # 1. Cythonize and compile csrc/sentence_splitter.cpp
        return cythonized_result
    else:
        # 2. Cannot use Cython implementation
        return None


def read_file(filename, cb):
    with codecs.open(filename, "r", "utf8") as f:
        return cb(f)


version = None
with open(os.path.join("kss", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("__version__"):
            version = line.split("=")[1].strip().replace("'", "").replace('"', "")

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

install_requires = [
    "emoji==1.2.0", "pecab", "networkx", "jamo",
    "hangul-jamo", "hanja==0.13.3", "tossi", "distance",
    "unidecode", "cmudict", "koparadigm", "kollocate",
    "bs4", "numpy", "pytest", "scipy"
]

setup(
    name="kss",
    version=version,
    author="Hyunwoong Ko",
    author_email="kevin.brain@kakaobrain.com",
    url="https://github.com/hyunwoongko/kss",
    license="BSD 3-Clause \"New\" or \"Revised\" License",
    description="A Toolkit for Korean sentence segmentation",
    long_description_content_type="text/markdown",
    platforms=["any"],
    install_requires=install_requires,
    long_description=long_description,
    packages=find_packages(exclude=["bench", "assets", ".java", ".pytest_cache"]),
    python_requires=">=3",
    zip_safe=False,
    package_data={
        "cython": ["csrc/*"],
        "g2p": ["kss/_modules/g2p/assets/*"],
        "augmentation": ["kss/_modules/augmentation/assets/*"],
    },
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
    cmdclass={"install": PreInstall},
    ext_modules=cythonize_if_possible(),
)
