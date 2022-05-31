#include "itermethods.cpp"

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(iterMethods, m)
{
    m.def("top_relaxation", &top_relaxation);
	m.def("top_relaxation_test", &top_relaxation_test);
	m.def("min_discrepancies_test", &min_discrepancies_test);
	m.def("min_discrepancies", &min_discrepancies);
};

