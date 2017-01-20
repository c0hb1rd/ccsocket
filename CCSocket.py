import socket
import time

from CCSocketException import *

TCP_SERVER = "TCP Server"
TCP_CLIENT = "TCP Client"
UDP_SERVER = "UDP Server"
UDP_CLIENT = "UDP Client"


class CCSocket:
    def __init__(self, ip, port, timeout=None):
        self.ip = ip
        self.port = port
        self.address = (self.ip, self.port)

        self.timeout = 10 if not timeout else timeout
        self.address = (ip, port)
        self.server = None
        self.client = None
        self.count = None

        self.flags = {
            "ip": self.ip,
            "port": self.port,
            "type": None,
            "timeout": self.timeout,
        }

    def TcpServer(self):
        if not self.server and not self.flags["type"]:
            self.flags["type"] = TCP_SERVER
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.server.bind(self.address)
            except socket.error as exception:
                if exception.errno == 10048:
                    self.__throwPortAlreadyUsed()
            return self
        else:
            self.__throwCreatedRaise()

    def UdpServer(self):
        if not self.server and not self.flags["type"]:
            self.flags["type"] = UDP_SERVER
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                self.server.bind(self.address)
            except socket.error as exception:
                if exception.errno == 10048:
                    self.__throwPortAlreadyUsed()
            return self
        else:
            self.__throwCreatedRaise()

    def TcpClient(self):
        if not self.client and not self.flags["type"]:
            self.flags["type"] = TCP_CLIENT
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__timeoutWork("self.client.connect(self.address)")
            self.client.settimeout(self.timeout)
            return self
        else:
            self.__throwCreatedRaise()

    def UdpClient(self):
        if not self.client and not self.flags["type"]:
            self.flags["type"] = UDP_CLIENT
            self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client.settimeout(self.timeout)
            return self
        else:
            self.__throwCreatedRaise()

    def listen(self, count):
        self.__throwNoneRaise()
        self.__throwNotServerObject()
        self.__throwNotListenAttribute()
        self.server.listen(count)
        self.count = count
        return self

    def accept(self):
        self.__throwNoneRaise()
        self.__throwNotListen()
        self.__throwNotAcceptAttribute()
        if not self.isServerOrClient() == "Server":
            self.__throwNotServerObject()
        c, a = self.server.accept()
        return c, a

    def send(self, context, client=None, address=None):
        objectType = self.isTcpOrUdp()
        objectKind = self.isServerOrClient()
        if objectType == "TCP":
            if objectKind == "Server":
                if not isinstance(client, socket.socket):
                    self.__throwNotClientObject()
                result = self.__tcpSend(context, client)
            else:
                result = self.__tcpSend(context)
        else:
            if client:
                self.__throwNotClientAttribute()
            if objectKind == "Server":
                if not address or not len(address) == 2 or not isinstance(address, tuple) or not isinstance(address[0], str) or not isinstance(address[1], int):
                    self.__throwErrorAddress(address)
                result = self.__udpSend(context, address)
            else:
                if address:
                    if not len(address) == 2 or not isinstance(address, tuple) or not isinstance(address[0], str) or not isinstance(address[1], int):
                        self.__throwErrorAddress(address)
                result = self.__udpSend(context, address)
        return result

    def receive(self, size, client=None):
        objectType = self.isTcpOrUdp()
        objectKind = self.isServerOrClient()
        if objectType == "TCP":
            if objectKind == "Server":
                if not isinstance(client, socket.socket):
                    self.__throwNotClientObject()
                result = self.__tcpReceive(size, client)
            else:
                result = self.__tcpReceive(size)
        else:
            result = self.__udpReceive(size)
        return result

    def getType(self):
        self.__throwNoneRaise()
        return self.flags["type"]

    def isServerOrClient(self):
        self.__throwNoneRaise()
        return self.flags['type'].split(" ")[1]

    def isTcpOrUdp(self):
        self.__throwNoneRaise()
        return self.flags["type"].split(" ")[0]

    def quit(self):
        self.__throwNoneRaise()
        flag = self.isServerOrClient()
        if flag == "Server":
            self.server.close()
        elif flag == "Client":
            self.client.close()

    def __tcpSend(self, context, client=None):
        if client:
            return client.send(context)
        else:
            return self.client.send(context)

    def __udpSend(self, context, address=None):
        if self.isServerOrClient() == "Server":
            return self.server.sendto(context, address)
        else:
            if address:
                return self.client.sendto(context, address)
            else:
                return self.client.sendto(context, self.address)

    def __tcpReceive(self, size, client=None):
        if client:
            return client.recv(size)
        else:
            return self.client.recv(size)

    def __udpReceive(self, size):
        if self.isServerOrClient() == "Server":
            return self.server.recvfrom(size)
        else:
            return self.client.recvfrom(size)

    def __timeoutWork(self, work):
        start = time.time()
        while True:
            try:
                eval(work)
                break
            except:
                time.sleep(0.5)
                end = time.time()
                if end - start > self.timeout:
                    self.__throwTimeoutRaise()

    def __throwCreatedRaise(self):
        raise AlreadyCreated(self.flags["type"])

    def __throwNoneRaise(self):
        if not self.flags["type"]:
            raise NoneObject()

    def __throwTimeoutRaise(self):
        raise Timeout(self.timeout)

    def __throwNotServerObject(self):
        if not self.flags["type"].split(" ")[1] == "Server":
            raise NotServerObject(self.flags["type"])

    def __throwNotListenAttribute(self):
        if self.isTcpOrUdp() == "UDP":
            raise NotAttribute("listen function")

    def __throwNotAcceptAttribute(self):
        if self.isTcpOrUdp() == "UDP":
            raise NotAttribute("accept function")

    def __throwNotClientAttribute(self):
        if self.isTcpOrUdp() == "UDP":
            raise NotAttribute("client arguments only request target address")

    def __throwNotClientObject(self):
        if not self.flags["type"].split(" ")[1] == "Client":
            raise NotClientObject(self.flags["type"])

    def __throwNotListen(self):
        if self.flags["type"] == TCP_SERVER:
            raise NotListen()

    def __throwPortAlreadyUsed(self):
        raise PortAlreadyUsed(self.port)

    def __throwErrorAddress(self, address):
        raise ErrorAddress(address)
