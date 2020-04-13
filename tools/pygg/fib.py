#! /usr/bin/python3.7
import os, sys, importlib as il

if os.path.exists(sys.argv[1]):
    spec = il.util.spec_from_loader(
        "pygg", il.machinery.SourceFileLoader("pygg", os.path.realpath(sys.argv[1]))
    )
    pygg = il.util.module_from_spec(spec)
    spec.loader.exec_module(pygg)
    del sys.argv[1]
else:
    import pygg


@pygg.thunk_fn
def fib(gg: pygg.GG, n: int) -> pygg.Term:
    if n < 2:
        return gg.str_value(str(n))
    else:
        a = gg.thunk(fib, [n - 1])
        b = gg.thunk(fib, [n - 2])
        return gg.thunk(add_str, [a, b])


@pygg.thunk_fn
def add_str(gg: pygg.GG, a: pygg.Value, b: pygg.Value) -> pygg.Term:
    ai = int(a.as_str())
    bi = int(b.as_str())
    return gg.str_value(str(ai + bi))


pygg.main()
