import numpy as np
import itertools
import string
import random
from types import SimpleNamespace, FunctionType

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def __str__(self):
        ret = ""
        for k in self.keys():
            ret += "{}: {}\n".format(k, self[k])
        return ret

class TimeVar(object):
    """ Vector variable used for defining time series. """
    def __init__(self, name = '', time = 0):
        self.name = name
        self.val = np.ones(time)
    def setTime(self, time, val = 0):
        self.val = val * np.ones(time)
    def __call__(self, pos):
        return self.val[pos]
    def __getitem__(self, index):
        self.val[index]

class Varspace(SimpleNamespace):
    def __getitem__(self, name):
        return getattr(self, name)
    def __setitem__(self, name, val):
        if isinstance(val, FunctionType):
            self.__dict__.update([[name, FunctionType(
                val.__code__,
                self.__dict__,
                name=name
            )]])
        else: self.__dict__.update([[name, val]])
    def __setattr__(self, name, val):
        if isinstance(val, FunctionType):
            self.__dict__.update([[name, FunctionType(
                val.__code__,
                self.__dict__,
                name=name
            )]])
        else: self.__dict__.update([[name, val]])
        
    def addEq(self, var, eq, label = ''):
        """Add expression to run in each step
        
        Best works as lambda expressions of a single argument t.
        They will be run for each step t.
        """
        eq = FunctionType(
            eq.__code__,
            self.__dict__,
            name=var
        )
        if "eqs" in self.__dict__.keys():
            self.eqs.append([var, eq])
        else:
            self.eqs = [(var, eq)]
        if var not in self.__dict__.keys():
            self.__dict__.update([[var, TimeVar(label)]])

    def run(self, t = 0, rep = 1):
        """Run all equations for a speciffied time range
        
        Repeats steps rep times.
        """
        for c_t in t:
            for _ in range(rep - 1):
                for tup in self.eqs:
                    self.__dict__[tup[0]].val[c_t] = (tup[1])(c_t)

    def setTime(self, t = 0):
        """Sets periods for objects in Namespace"""
        [var[1].setTime(t) for var in self.__dict__.items() if type(var[1]).__name__ == 'TimeVar']

    def getRes(self):
        """Returns TimeVar objects values as dictionary"""
        return {key : val.val for key, val in self.__dict__.items() if type(val).__name__ == 'TimeVar'}