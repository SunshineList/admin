# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


def singleton(cls):
    _instance = {}

    def wrapper(*args, **kwargs):
        if not _instance.get(cls):
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return wrapper


class SingletonMeta(type):

    def __call__(self, *args, **kwargs):
        if not hasattr(self, "_instance"):
            self._instance = super(SingletonMeta, self).__call__(*args, **kwargs)
        return self._instance


def _itersubclasses(cls, _seen=None, _event_type=None):
    """
    递归获取cls的所有子类
    """
    if _seen is None:
        _seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError:  # fails only when cls is type
        subs = cls.__subclasses__(cls)
    if _event_type:
        subs = list(filter(lambda x: hasattr(x, "_event_type"), subs))
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in _itersubclasses(sub, _seen):
                yield sub


# 构造一个通用的策略模式
class CustomStrategySuper(metaclass=ABCMeta):
    @abstractmethod
    def business_strategy(*args, **kwargs):
        pass


class StrategyContext(object):
    # 注册所有策略类的子类
    strategy_dict = {
        getattr(strategy, "_event_type"): strategy
        for strategy in _itersubclasses(CustomStrategySuper, _event_type=True)
    }

    def __init__(self, event_type):
        self.event_type = event_type  # 传入一个事件类型 然后根据事件类型找到对应的策略
        self.strategy = self.strategy_dict.get(event_type)

    def execute(self, *args, **kwargs):
        assert self.strategy, "未找到事件类型对应的策略类"
        return self.strategy().business_strategy(*args, **kwargs)


if __name__ == "__main__":
    instance = StrategyContext("A").execute()
    print(instance)
