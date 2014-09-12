#!/usr/bin/env python

import subprocess

from distutils.core import setup
from distutils.extension import Extension

import numpy

def root_flags(root_config='root-config'):
    root_inc = subprocess.Popen([root_config, '--incdir'],
        stdout=subprocess.PIPE).communicate()[0].strip()
    root_ldflags = subprocess.Popen([root_config, '--libs'],
        stdout=subprocess.PIPE).communicate()[0].strip().split(' ')
    return root_inc, root_ldflags

try:
    root_inc, root_ldflags = root_flags()
except OSError:
    rootsys = os.getenv('ROOTSYS', None)
    if rootsys is None:
        raise RuntimeError(
            "root-config is not in PATH and ROOTSYS is not set. "
            "Is ROOT installed and setup properly?")
    try:
        root_config = os.path.join(rootsys, 'bin', 'root-config')
        root_inc, root_ldflags = root_flags(root_config)
    except OSError:
        raise RuntimeError(
            "ROOTSYS is {0} but running {1} failed".format(
                rootsys, root_config))

module = Extension(
    name="dispatch",
    sources=[
        "dispatch.cpp",
        "../cpp/DataFetcher.cpp",
        "../cpp/TreeElementReader.cpp",
    ],
    language='c++',
    include_dirs=[
        numpy.get_include(),
        root_inc
    ],
    extra_compile_args=[],
    extra_link_args=root_ldflags
)

setup(
    ext_modules=[
        module
    ]
)
