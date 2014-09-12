#!/usr/bin/env bash

cython --cplus --fast-fail --line-directives dispatch.pyx
python setup.py build_ext --inplace
