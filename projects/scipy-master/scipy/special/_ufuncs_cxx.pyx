# This file is automatically generated by generate_ufuncs.py.
# Do not edit manually!
include "_ufuncs_extra_code_common.pxi"

cdef extern from "_ufuncs_cxx_defs.h":
    cdef double _func_faddeeva_dawsn "faddeeva_dawsn"(double) nogil
cdef void *_export_faddeeva_dawsn = <void*>_func_faddeeva_dawsn
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double complex _func_faddeeva_dawsn_complex "faddeeva_dawsn_complex"(double complex) nogil
cdef void *_export_faddeeva_dawsn_complex = <void*>_func_faddeeva_dawsn_complex
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double complex _func_faddeeva_erf "faddeeva_erf"(double complex) nogil
cdef void *_export_faddeeva_erf = <void*>_func_faddeeva_erf
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double complex _func_faddeeva_erfc "faddeeva_erfc"(double complex) nogil
cdef void *_export_faddeeva_erfc = <void*>_func_faddeeva_erfc
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double _func_faddeeva_erfcx "faddeeva_erfcx"(double) nogil
cdef void *_export_faddeeva_erfcx = <void*>_func_faddeeva_erfcx
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double complex _func_faddeeva_erfcx_complex "faddeeva_erfcx_complex"(double complex) nogil
cdef void *_export_faddeeva_erfcx_complex = <void*>_func_faddeeva_erfcx_complex
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double _func_faddeeva_erfi "faddeeva_erfi"(double) nogil
cdef void *_export_faddeeva_erfi = <void*>_func_faddeeva_erfi
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double complex _func_faddeeva_erfi_complex "faddeeva_erfi_complex"(double complex) nogil
cdef void *_export_faddeeva_erfi_complex = <void*>_func_faddeeva_erfi_complex
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double complex _func_faddeeva_log_ndtr "faddeeva_log_ndtr"(double complex) nogil
cdef void *_export_faddeeva_log_ndtr = <void*>_func_faddeeva_log_ndtr
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double complex _func_faddeeva_ndtr "faddeeva_ndtr"(double complex) nogil
cdef void *_export_faddeeva_ndtr = <void*>_func_faddeeva_ndtr
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double complex _func_faddeeva_w "faddeeva_w"(double complex) nogil
cdef void *_export_faddeeva_w = <void*>_func_faddeeva_w
cdef extern from "_ufuncs_cxx_defs.h":
    cdef double complex _func_wrightomega "wrightomega"(double complex) nogil
cdef void *_export_wrightomega = <void*>_func_wrightomega
# distutils: language = c++