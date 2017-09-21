import time
import numpy as np
import sys
from cq.testpkg import TestTest

from cq.app import app
from cq.utils.primitives import CQTask, CQGroup


def calc1(x):
    print("calc1")

    return np.array(x)**2


def calc2(x, y, s=1):
    print("calc2")

    x = np.array(x)
    y = np.array(y)

    time.sleep(s)

    return x*y


tt = TestTest(42)


def f1(x):
    print("LOCALS", locals())
    print("......", globals()['__builtins__'].keys())
    print(tt)
    return tt.p(x)


def p1(x):
    #print("GLOBALS", globals())
    #print("LOCALS", locals())
    print("......", globals()['__builtins__'].keys())


groups = []

x1 = np.random.randn(100)
x2 = np.random.randn(100)

#groups.append({'fct': calc1,
#               'args': (x1,)})
#groups.append({'fct': calc2,
#               'kwargs': {'x': x1,
#                          'y': x2}})
#groups.append({'fct': p1,
#               'args': (42,)})


for _ in range(10):
    x = np.random.randn(100)
    y = np.random.randn(100)
    #groups.append({'fct': calc1,
    #               'args': (x,)})
    groups.append({'fct': calc2,
                   'args': (x, y, 3)})

##groups.append({'fct': lambda _x, _y, _s: calc2(_x, _y, _s),
##               'args': (x1, x2, 3)})
##
##groups.append({'fct': f1,
##               'args': (42,)})
##groups.append({'fct': f1,
##               'args': (43,)})

cqGroup = CQGroup(groups)
cqGroup.apply_async()
