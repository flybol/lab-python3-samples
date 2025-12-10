def decoA(fn):
    print("执行装饰器decoA")

    # decoA(decoB(decoC(fn)))
    # callableA(callable2(callableC))
    def wrapperA(name: str):
        print("装饰器decoA:", name, fn.__name__)
        fn(name)  # wrapperB
        print("wrapperA 结束", fn.__name__)

    return wrapperA  # callableA


def decoB(fn):
    print("执行装饰器decoB")

    # callableB(callableC)
    def wrapperB(name: str):
        print("装饰器decoB:", name, fn.__name__)
        fn(name)  # wrapperC
        print("wrapperB 结束", fn.__name__)

    return wrapperB  # callableB


def decoC(fn):
    print("执行装饰器decoC")

    def wrapperC(name: str):
        print("装饰器decoC:", name, fn.__name__)
        fn(name)  # 调用被装饰的函数
        print("wrapperC 结束", fn.__name__)

    return wrapperC  # callableC


@decoA
@decoB
@decoC  # Python 规范里明确：先应用离函数最近的那个装饰器。
def fn(name):
    print("被装饰的函数:", name)


# fn = decoA(decoB(decoC(fn)))
print("最终fn指向：", fn.__name__)
fn("曼波~")  # 等价wrapperA("曼波~"))
