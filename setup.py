# cython: language_level=3, boundscheck=False
# 設置cython 的python 版本 否則會自動使用python 2
from setuptools import setup
from Cython.Build import cythonize

setup(
    # ext_modules=cythonize(module_list='twstock.py',exclude='twstock.py')
    ext_modules = cythonize("twstock.py")
)