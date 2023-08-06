"""
This module contains the set of AssetMove' exceptions.
"""


class BasicException(Exception):
    def __init__(self, *args, **kwargs):
        super(BasicException, self).__init__(*args, **kwargs)


class SystemUnNormal(BasicException):
    """系统不可用,维护中"""


class InsufficientBalance(BasicException):
    """账户余额不足"""
