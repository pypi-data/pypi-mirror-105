"""Top-level package for pydonitest."""

__author__ = """Andoni Sooklaris"""
__email__ = 'andoni.sooklaris@gmail.com'
__version__ = '0.1.1'


import logging
import threading


class ExtendedLogger(logging.Logger):
    """
    Extend the logging.Logger class.
    """

    def __init__(self, name, level=logging.NOTSET):
        self._count = 0
        self._countLock = threading.Lock()
        return super(ExtendedLogger, self).__init__(name, level)

    def var(self, varname, value, include_modules=True, include_extended_logger=True):
        """
        Extend .debug() method to log the name, value and datatype of a variable or variables.
        Optionally include modules and instances of this class. Functionally, this allows
        for iterating over `locals()` and automatically excluding modules and/or loggers
        from the logged output, instead leaving just the variables desired to be logged.

        For example, if `locals()` returns `{'a': 1, 'b': 2, 'logging': "<module 'logging' from..."}`

        The user can set `include_modules=False` to exclude the 'logging' module when iterating
        over `locals()`:

        >>> for k, v in locals().items():
        >>>     logger.var(k, v, include_modules=False)
        {timestamp} : DEBUG : __main__ : Variable 'a' {int}: 1
        {timestamp} : DEBUG : __main__ : Variable 'b' {int}: 2
        """
        dtype = value.__class__.__name__
        value = str(value)

        if dtype == 'module' and not include_modules:
            return None

        if 'ExtendedLogger' in dtype and not include_extended_logger:
            return None

        msg = f"Variable '{varname}' {{{dtype}}}: {value}"
        return super(ExtendedLogger, self).debug(msg)

    def logvars(self, var_dict):
        """
        Iterate over dictionary and call `self.var` on each variable name, variable value pair,
        excluding modules and instances of this class.
        """
        for varname, value in var_dict.items():
            self.var(varname, value, include_modules=False, include_extended_logger=False)
