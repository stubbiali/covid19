# -*- coding: utf-8 -*-
import abc


from covid19.updater import Updater


ledger = {}


def registry(name):
    def wrapper(cls):
        ledger[name] = cls
        return cls
    return wrapper


class Patcher(abc.ABC):
    def __init__(self, name, update_data):
        if update_data:
            updater = Updater.factory(name)
            updater.run()

    @abc.abstractmethod
    def run(self):
        pass

    @staticmethod
    def factory(name, update_data=True, *args, **kwargs):
        if name not in ledger:
            raise RuntimeError(f"Patcher {name} does not exist.")
        return ledger[name](name, update_data, *args, **kwargs)

