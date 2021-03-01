from abc import ABCMeta, abstractmethod


class AbstractSet(metaclass=ABCMeta):
    @abstractmethod
    def set(self):
        raise NotImplementedError