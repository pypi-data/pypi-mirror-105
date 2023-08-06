#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, Extension

def main():
    setup(name="PyExit",
          version="1.0.1",
          description="Exit the program",
          author="Vadim Simakin",
          author_email="sima.vad@yandex.ru",
          ext_modules=[Extension("_pyexit", ["_pyexit.c"])],
          packages=['pyexit']
    )

if __name__ == "__main__":
    main()

