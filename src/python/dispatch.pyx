# distutils: language = c++
# distutils: sources = ../cpp/DataFetcher.cpp

from libcpp.vector cimport vector
from libcpp.string cimport string

import numpy as np
cimport numpy as np

np.import_array()

cdef extern from "../cpp/DataFetcher.h":
    cdef cppclass DataFetcher:
        DataFetcher(string)
        unsigned int entries()
        void get_entry(unsigned int)
        short * adc()
        double * pedestal()
        unsigned int adc_rows()
        unsigned int adc_cols()
        unsigned int number_particles()
        int * pdg_code()
        int * track_id()
        int * parent_id()
        double * start_momentum()
        double * trajectory_length()
        vector[string] process()
        vector[vector[double]] particle_x()
        vector[vector[double]] particle_y()
        vector[vector[double]] particle_z()
        vector[vector[double]] particle_t()

cdef class dispatch:
    cdef DataFetcher * cobj
    def __cinit__(self, string file_path):
        self.cobj = new DataFetcher(file_path)
        if self.cobj == NULL:
            raise MemoryError("Not enough memory.")
    def __dealloc__(self):
        del self.cobj
    def entries(self):
        return self.cobj.entries()
    def get_entry(self, unsigned int entry):
        self.cobj.get_entry(entry)
    def adc_rows(self):
        return self.cobj.adc_rows()
    def adc_cols(self):
        return self.cobj.adc_cols()
    def adc(self):
        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp> (self.cobj.adc_rows() * self.cobj.adc_cols())
        ndarray = np.PyArray_SimpleNewFromData(
            1,
            shape,
            np.NPY_SHORT,
            self.cobj.adc()
        )
        return ndarray
    def pedestal(self):
        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp> (self.cobj.adc_rows() + self.cobj.adc_rows())
        ndarray = np.PyArray_SimpleNewFromData(
            1,
            shape,
            np.NPY_DOUBLE,
            self.cobj.pedestal()
        )
        return ndarray
    def number_particles(self):
        return self.cobj.number_particles()
    def pdg_code(self):
        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp> self.cobj.number_particles()
        ndarray = np.PyArray_SimpleNewFromData(
            1,
            shape,
            np.NPY_INT,
            self.cobj.pdg_code()
        )
        return ndarray
    def track_id(self):
        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp> self.cobj.number_particles()
        ndarray = np.PyArray_SimpleNewFromData(
            1,
            shape,
            np.NPY_INT,
            self.cobj.track_id()
        )
        return ndarray
    def parent_id(self):
        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp> self.cobj.number_particles()
        ndarray = np.PyArray_SimpleNewFromData(
            1,
            shape,
            np.NPY_INT,
            self.cobj.parent_id()
        )
        return ndarray
    def start_momentum(self):
        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp> self.cobj.number_particles()
        ndarray = np.PyArray_SimpleNewFromData(
            1,
            shape,
            np.NPY_DOUBLE,
            self.cobj.start_momentum()
        )
        return ndarray
    def trajectory_length(self):
        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp> self.cobj.number_particles()
        ndarray = np.PyArray_SimpleNewFromData(
            1,
            shape,
            np.NPY_DOUBLE,
            self.cobj.trajectory_length()
        )
        return ndarray
    def process(self):
        return self.cobj.process()
    def particle_x(self):
        return self.cobj.particle_x()
    def particle_y(self):
        return self.cobj.particle_y()
    def particle_z(self):
        return self.cobj.particle_z()
    def particle_t(self):
        return self.cobj.particle_t()
