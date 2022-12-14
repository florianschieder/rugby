#include <Python.h>

/////////////////////////// Rust-C binding ///////////////////////////
int rugby_sum(int lowerBound, int upperBound);

/////////////////////////// C-Python binding ///////////////////////////

static PyObject * binding_sum(PyObject *self, PyObject *args)
{
    int lowerBound, upperBound;

    if (!PyArg_ParseTuple(args, "ii", &lowerBound, &upperBound)) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to retrieve arguments");
    }

    return PyLong_FromLong(rugby_sum(lowerBound, upperBound));
}

/////////////////////////// Python module metadata ///////////////////////////

static PyMethodDef RugbyBindingMethods[] = {
    {"sum", binding_sum, METH_VARARGS,
     "Calculate the Gauss sum of a range of two numbers"},
    {NULL, NULL, 0, NULL},
};

static PyModuleDef RugbyBindingModule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "rugby_binding",
    .m_doc = "Rust/Python interop illustration",
    .m_size = -1,
    .m_methods = RugbyBindingMethods,
};

//////////////////////// Python module initialization ////////////////////////

PyMODINIT_FUNC PyInit_rugby_binding() {
  PyObject *module = PyModule_Create(&RugbyBindingModule);
  if (module == NULL) {
    return NULL;
  }

  return module;
}