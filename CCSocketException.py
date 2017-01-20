#!/usr/bin/env python


class CCSocketException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class NoneObject(CCSocketException):
    def __init__(self):
        self.message = "Do not created server or client"


class Timeout(CCSocketException):
    def __init__(self, timeout):
        self.message = "Connecting timeout %d" % timeout


class AlreadyCreated(CCSocketException):
    def __init__(self, flag):
        self.message = "Another %s was been created" % flag