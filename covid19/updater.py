# -*- coding: utf-8 -*-
import abc


ledger = {}


def registry(name):
    def wrapper(cls):
        ledger[name] = cls
        return cls
    return wrapper


class Updater(abc.ABC):
    @abc.abstractmethod
    def run(self):
        pass

    @staticmethod
    def factory(name, *args, **kwargs):
        if name not in ledger:
            raise RuntimeError(f"Updater {name} does not exist.")
        return ledger[name](*args, **kwargs)

