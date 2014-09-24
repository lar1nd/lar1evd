#!/usr/bin/env python

import subprocess
import fileinput

from distutils.core import setup
from distutils.extension import Extension

import numpy

def root_flags(root_config='root-config'):
    root_inc = subprocess.Popen([root_config, '--incdir'],
        stdout=subprocess.PIPE).communicate()[0].strip()
    root_ldflags = subprocess.Popen([root_config, '--libs'],
        stdout=subprocess.PIPE).communicate()[0].strip().split(' ')
    return root_inc, root_ldflags

def root_release(root_config='root-config'):
    root_version = subprocess.Popen([root_config, '--version'],
        stdout=subprocess.PIPE).communicate()[0].strip().split('/')
    return root_version

def replace(file_path, search_string, replace_string):
    for line in fileinput.input(file_path, inplace=True):
        print line.replace(search_string, replace_string),

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

root_version = root_release()

if root_version[0] == '5.34' and int(root_version[1]) >= 20:
    indent = '      '
    comment = '//'
    line = (
        'branch_element_->GetInfo()->GetOffsets()[branch_element_->GetID()];',
        'branch_element_->GetInfo()->GetElementOffset(branch_element_->GetID());',
    )
    tree_element_reader = '../cpp/TreeElementReader.cpp'
    replace(tree_element_reader, indent + line[0], indent + comment + line[0])
    replace(tree_element_reader, indent + comment + line[1], indent + line[1])

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
