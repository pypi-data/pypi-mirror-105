#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *method_exit(PyObject *self, PyObject *args) {
int *code = 0;
if(!PyArg_ParseTuple(args, "|b", &code)) {
return NULL;
}
exit(code);
Py_INCREF(Py_None);
return Py_None;
}

static PyMethodDef PEMethods[] = {
    {"exit", method_exit, METH_VARARGS, "Exit the program using C exit()"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pyexitmodule = {
    PyModuleDef_HEAD_INIT,
    "_pyexit",
    "Exit the program using C exit()",
    -1,
    PEMethods
};


PyMODINIT_FUNC PyInit__pyexit(void) {
    return PyModule_Create(&pyexitmodule);
}

