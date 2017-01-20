#!/usr/bin/env python


class CCSocketException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class NoneObject(CCSocketException):
    def __init__(self):
        self.message = "[!] Do not created server or client"


class Timeout(CCSocketException):
    def __init__(self, timeout):
        self.message = "[!] Connecting timeout %d" % timeout


class AlreadyCreated(CCSocketException):
    def __init__(self, flag):
        self.message = "[!] Another %s was been created" % flag


class NotServerObject(CCSocketException):
    def __init__(self, flag):
        self.message = "[!] %s not server object" % flag


class NotClientObject(CCSocketException):
    def __init__(self, flag):
        self.message = "[!] %s not client object" % flag


class NotListen(CCSocketException):
    def __init__(self):
        self.message = "[!] Server not set listen count"


class NotAttribute(CCSocketException):
    def __init__(self, attribute):
        self.message = "[!] UDP kinds has not %s" % attribute


class PortAlreadyUsed(CCSocketException):
    def __init__(self, port):
        self.message = "[!] %d port is already used" % port


class ErrorAddress(CCSocketException):
    def __init__(self, address):
        self.message = '''[!] Error address: %(address)s, format must be tuple(str, int)''' % {"address": address, "type": type(address)}
