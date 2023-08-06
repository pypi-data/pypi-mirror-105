# 1. calltrace
record and trace the function call chain

# 2. why develop it

当我在开源项目上做二次开发时，我想知道完整的函数调用过程，可一些复杂的代码总是难以追踪，于是，我编写这个脚本，使用它来追踪函数的调用过程。

有些调用过程发生在第三方包里，你可以用filter_func 进行过滤

When I do secondary development on an open source project, I want to know the complete function calling process, but some complex code is always difficult to trace, so I write this script and use it to trace the function calling process.

Some of the calls take place in third-party packages. You can use filter_ Func filter

# 3. how to install
```shell script
pip install calltrace
```

# 4. example

```python
from calltrace import CallTrace

def func1():
    print('ok')

def func2():
    func1()

def func3():
    func2()

def func4():
    func3()

def file_filter(filename):
    if filename.find('calc') != -1:
        return True
    return False


with CallTrace(filter_func=lambda x: x.find('calc') == -1):
    func4()

# call_trace = CallTrace(filter_func=lambda x: x.find('calc') == -1)
# call_trace.start()
# func4()
# call_trace.stop()
# call_trace.output()
```